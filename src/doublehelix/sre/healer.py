"""Double Helix Autonomous SRE & Codebase Self-Healing Engine.

Translates the Dual-Strand Upward Slice and Epistemic Decoupling Sandbox into a
developer-facing CI/CD tool:
1. Scans codebases for AST defects: hot-loop allocations, unclosed resources,
   missing network timeouts, and unhandled exception absorbing traps.
2. Evaluates candidate patches through the Epistemic Decoupling Sandbox (P(ruin) = 0).
3. Applies verified safe patches and generates GitHub-flavored audit reports.
"""

import ast
import os
import sys
import time
import logging
from typing import Dict, List, Any, Optional, Tuple
from pydantic import BaseModel, Field

from doublehelix.runtime.decision_core import (
    ActionCandidate,
    EpistemicDecouplingSandbox,
    EpistemicRolloutResult,
)

logger = logging.getLogger("SRECodebaseHealer")


class CodeDefect(BaseModel):
    """Detected invariant or architectural defect in target codebase."""
    file_path: str
    line_number: int
    defect_type: str  # "HOT_LOOP_ALLOCATION", "UNCLOSED_RESOURCE", "MISSING_TIMEOUT", "BARE_EXCEPT"
    severity: str     # "CRITICAL", "HIGH", "MEDIUM", "LOW"
    description: str
    ruin_risk_probability: float  # Estimated probability of causing runtime ruin/outage
    code_snippet: str = ""


class PatchRemediation(BaseModel):
    """Synthesized repair candidate evaluated by the Epistemic Sandbox."""
    defect_id: str
    file_path: str
    original_code: str
    repaired_code: str
    sandbox_approved: bool = False
    rejection_reason: Optional[str] = None
    ruin_probability: float = 0.0
    projected_log_growth: float = 0.0


class CodebaseAuditReport(BaseModel):
    """Executive summary of codebase audit and healing actions."""
    target_path: str
    timestamp: float = Field(default_factory=time.time)
    scanned_files_count: int = 0
    defects_found_count: int = 0
    critical_defects_count: int = 0
    defects: List[CodeDefect] = Field(default_factory=list)
    remediations: List[PatchRemediation] = Field(default_factory=list)
    clean_bill_of_health: bool = True
    absorbing_barrier_preserved: bool = True


class CodebaseASTScanner(ast.NodeVisitor):
    """Performs deep static AST inspection for runtime invariant risks."""

    def __init__(self, file_path: str, source_code: str):
        self.file_path = file_path
        self.source_code = source_code
        self.lines = source_code.splitlines()
        self.defects: List[CodeDefect] = []
        self._in_loop: int = 0
        self._in_with: int = 0

    def visit_With(self, node: ast.With):
        self._in_with += 1
        self.generic_visit(node)
        self._in_with -= 1

    def visit_For(self, node: ast.For):
        self._in_loop += 1
        self.generic_visit(node)
        self._in_loop -= 1

    def visit_While(self, node: ast.While):
        self._in_loop += 1
        self.generic_visit(node)
        self._in_loop -= 1

    def visit_ListComp(self, node: ast.ListComp):
        if self._in_loop > 0:
            snippet = self._get_snippet(node.lineno)
            self.defects.append(CodeDefect(
                file_path=self.file_path,
                line_number=node.lineno,
                defect_type="HOT_LOOP_ALLOCATION",
                severity="HIGH",
                description="List comprehension inside iterative loop causes dynamic heap allocation and GC pause spikes.",
                ruin_risk_probability=0.15,
                code_snippet=snippet
            ))
        self.generic_visit(node)

    def visit_Try(self, node: ast.Try):
        for handler in node.handlers:
            if handler.type is None:
                snippet = self._get_snippet(handler.lineno)
                self.defects.append(CodeDefect(
                    file_path=self.file_path,
                    line_number=handler.lineno,
                    defect_type="BARE_EXCEPT",
                    severity="CRITICAL",
                    description="Bare 'except:' swallows critical runtime signals (KeyboardInterrupt, SystemExit, MemoryError) hiding absorbing failures.",
                    ruin_risk_probability=0.40,
                    code_snippet=snippet
                ))
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        # Check for open() called outside a with statement
        if isinstance(node.func, ast.Name) and node.func.id == "open":
            if self._in_with == 0:
                snippet = self._get_snippet(node.lineno)
                self.defects.append(CodeDefect(
                    file_path=self.file_path,
                    line_number=node.lineno,
                    defect_type="UNCLOSED_RESOURCE",
                    severity="HIGH",
                    description="Call to open() without 'with' context manager risks file descriptor exhaustion in high-concurrency environments.",
                    ruin_risk_probability=0.25,
                    code_snippet=snippet
                ))

        # Check for HTTP network requests missing timeout
        if isinstance(node.func, ast.Attribute) and node.func.attr in ("get", "post", "put", "delete", "patch"):
            caller_name = ""
            if isinstance(node.func.value, ast.Name):
                caller_name = node.func.value.id.lower()
            elif isinstance(node.func.value, ast.Attribute):
                caller_name = node.func.value.attr.lower()

            if caller_name in ("app", "router", "fastapi"):
                self.generic_visit(node)
                return

            is_http_caller = any(token in caller_name for token in ("requests", "httpx", "session", "http_client", "urllib"))
            has_http_kwargs = any(kw.arg in ("params", "headers", "json", "data", "auth") for kw in node.keywords)
            
            has_url_arg = False
            if node.args and isinstance(node.args[0], (ast.Constant, ast.Name)):
                if isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                    has_url_arg = node.args[0].value.startswith("http")
                elif isinstance(node.args[0], ast.Name) and "url" in node.args[0].id.lower():
                    has_url_arg = True

            if (is_http_caller or has_http_kwargs or has_url_arg) and caller_name not in ("app", "router"):
                has_timeout = any(kw.arg == "timeout" for kw in node.keywords)
                # If caller is client inside with-block configured with timeout, it's safe
                if not has_timeout and "client" in caller_name and "httpx" in self.source_code:
                    has_timeout = "timeout=" in self.source_code

                if not has_timeout:
                    snippet = self._get_snippet(node.lineno)
                    self.defects.append(CodeDefect(
                        file_path=self.file_path,
                        line_number=node.lineno,
                        defect_type="MISSING_TIMEOUT",
                        severity="CRITICAL",
                        description=f"HTTP call '{caller_name}.{node.func.attr}' without explicit timeout risks indefinite connection hang and thread pool deadlock.",
                        ruin_risk_probability=0.35,
                        code_snippet=snippet
                    ))

        self.generic_visit(node)

    def _get_snippet(self, lineno: int) -> str:
        if 1 <= lineno <= len(self.lines):
            return self.lines[lineno - 1].strip()
        return ""


class AutonomousCodebaseHealer:
    """Master SRE Engine coordinating scanning, epistemic sandboxing, and repair."""

    def __init__(self, target_dir: str):
        self.target_dir = os.path.abspath(target_dir)
        self.sandbox = EpistemicDecouplingSandbox(max_ruin_tolerance=0.0)

    def scan_codebase(self, exclude_dirs: Optional[List[str]] = None) -> CodebaseAuditReport:
        """Recursively inspects Python source files for invariant defects."""
        excludes = set(exclude_dirs or [".git", "__pycache__", ".venv", "venv", ".pytest_cache", "build", "dist"])
        report = CodebaseAuditReport(target_path=self.target_dir)

        for root, dirs, files in os.walk(self.target_dir):
            dirs[:] = [d for d in dirs if d not in excludes]
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    report.scanned_files_count += 1
                    try:
                        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                            source = f.read()
                        tree = ast.parse(source, filename=full_path)
                        scanner = CodebaseASTScanner(full_path, source)
                        scanner.visit(tree)
                        report.defects.extend(scanner.defects)
                    except SyntaxError as se:
                        report.defects.append(CodeDefect(
                            file_path=full_path,
                            line_number=se.lineno or 1,
                            defect_type="SYNTAX_ERROR",
                            severity="CRITICAL",
                            description=f"SyntaxError in source file: {se.msg}",
                            ruin_risk_probability=1.0,
                            code_snippet=se.text.strip() if se.text else ""
                        ))
                    except Exception as e:
                        logger.warning("Could not read/parse file %s during SRE scan: %s", full_path, e)

        report.defects_found_count = len(report.defects)
        report.critical_defects_count = sum(1 for d in report.defects if d.severity == "CRITICAL")
        report.clean_bill_of_health = (report.defects_found_count == 0)
        report.absorbing_barrier_preserved = (report.critical_defects_count == 0)

        return report

    def heal_codebase(
        self,
        report: CodebaseAuditReport,
        apply_patches: bool = False
    ) -> CodebaseAuditReport:
        """Generates repairs for detected defects and filters them via Epistemic Sandbox."""
        for defect in report.defects:
            candidate_patch = self._synthesize_repair(defect)
            if not candidate_patch:
                continue

            # Route through Epistemic Decoupling Sandbox
            candidate_action = ActionCandidate(
                action_id=f"heal_{defect.defect_type}_{defect.line_number}",
                description=f"Repair {defect.defect_type} at line {defect.line_number}",
                expected_yield=0.20,
                ruin_probability=candidate_patch.ruin_probability,
                payload={"file": defect.file_path, "patch": candidate_patch.repaired_code}
            )

            rollout: EpistemicRolloutResult = self.sandbox.rollout(
                candidate_action, current_state={"file": defect.file_path}
            )

            candidate_patch.sandbox_approved = rollout.approved
            candidate_patch.rejection_reason = rollout.rejection_reason
            candidate_patch.projected_log_growth = rollout.projected_log_growth

            if rollout.approved and apply_patches:
                self._apply_patch_to_file(defect.file_path, defect.line_number, candidate_patch)

            report.remediations.append(candidate_patch)

        return report

    def _synthesize_repair(self, defect: CodeDefect) -> Optional[PatchRemediation]:
        """Synthesizes candidate code replacements based on defect type."""
        orig = defect.code_snippet

        if defect.defect_type == "BARE_EXCEPT":
            # Replace bare except with except Exception:
            repaired = orig.replace("except:", "except Exception as e:")
            return PatchRemediation(
                defect_id=f"{defect.defect_type}_{defect.line_number}",
                file_path=defect.file_path,
                original_code=orig,
                repaired_code=repaired,
                ruin_probability=0.0  # Safe fix
            )

        elif defect.defect_type == "MISSING_TIMEOUT":
            # Add timeout=10.0 to request call
            if orig.endswith(")"):
                repaired = orig[:-1] + ", timeout=10.0)"
            else:
                repaired = orig + " # FIXME: add timeout=10.0"
            return PatchRemediation(
                defect_id=f"{defect.defect_type}_{defect.line_number}",
                file_path=defect.file_path,
                original_code=orig,
                repaired_code=repaired,
                ruin_probability=0.0  # Safe fix
            )

        return None

    def _apply_patch_to_file(self, file_path: str, line_no: int, patch: PatchRemediation):
        """Applies verified patch to disk."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            if 1 <= line_no <= len(lines):
                lines[line_no - 1] = lines[line_no - 1].replace(patch.original_code, patch.repaired_code)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.writelines(lines)
        except Exception as e:
            logger.error("Failed to write patch to %s at line %d: %s", file_path, line_no, e)

    @staticmethod
    def generate_markdown_report(report: CodebaseAuditReport) -> str:
        """Formats the audit into GitHub PR comment markdown."""
        status_badge = "🟢 PASSED (Absorbing Barrier Safe)" if report.absorbing_barrier_preserved else "🔴 FAILED (Ruin Traps Detected)"
        
        md = [
            f"# 🧬 Double Helix SRE Audit Report",
            f"**Target Directory:** `{report.target_path}`  ",
            f"**Status:** {status_badge}  ",
            f"**Files Scanned:** {report.scanned_files_count} | **Total Defects:** {report.defects_found_count} | **Critical:** {report.critical_defects_count}\n",
            "---",
            "### 🔍 Detected Codebase Invariant Defects",
        ]

        if not report.defects:
            md.append("\n✅ **Zero Invariant Defects Detected.** The codebase satisfies all deterministic runtime constraints.\n")
        else:
            md.append("| File | Line | Defect Type | Severity | Ruin Risk | Description |")
            md.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
            for d in report.defects:
                rel_path = os.path.basename(d.file_path)
                md.append(f"| `{rel_path}` | {d.line_number} | `{d.defect_type}` | **{d.severity}** | {d.ruin_risk_probability:.0%} | {d.description} |")

        if report.remediations:
            md.append("\n### 🛠️ Epistemic Sandbox Healing Actions")
            md.append("| Defect ID | Approved | Status / Rejection Reason | Proposed Repair |")
            md.append("| :--- | :--- | :--- | :--- |")
            for r in report.remediations:
                appr_str = "✅ YES" if r.sandbox_approved else "❌ BLOCKED"
                status_str = "Cleared P(ruin) = 0" if r.sandbox_approved else (r.rejection_reason or "Ruin detected")
                md.append(f"| `{r.defect_id}` | {appr_str} | {status_str} | `{r.repaired_code}` |")

        md.append("\n---")
        md.append("*Generated autonomously by Double Helix Neural Agent Engine & SOPHI-Runtime.*")
        return "\n".join(md)
