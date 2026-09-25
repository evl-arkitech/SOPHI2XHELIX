"""Unit and integration tests for Double Helix Autonomous Codebase SRE & Self-Healing."""

import os
import tempfile
import pytest
from doublehelix.sre.healer import (
    CodebaseASTScanner,
    AutonomousCodebaseHealer,
    CodeDefect,
    PatchRemediation,
)


def test_codebase_ast_scanner_defects():
    sample_flawed_code = """
import requests

def bad_worker():
    # 1. Hot loop allocation
    for i in range(10):
        items = [x * 2 for x in range(100)]
    
    # 2. Bare except
    try:
        val = 1 / 0
    except:
        pass

    # 3. Unclosed file descriptor
    f = open("leak.txt", "r")

    # 4. Network call missing timeout
    res = requests.get("https://api.example.com/data")
"""

    scanner = CodebaseASTScanner("sample_flawed.py", sample_flawed_code)
    import ast
    tree = ast.parse(sample_flawed_code)
    scanner.visit(tree)

    defect_types = [d.defect_type for d in scanner.defects]
    assert "HOT_LOOP_ALLOCATION" in defect_types
    assert "BARE_EXCEPT" in defect_types
    assert "UNCLOSED_RESOURCE" in defect_types
    assert "MISSING_TIMEOUT" in defect_types


def test_autonomous_codebase_healer_workflow():
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "flawed_module.py")
        code = """
def risky_function():
    try:
        1 / 0
    except:
        pass
"""
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(code)

        healer = AutonomousCodebaseHealer(target_dir=tmpdir)
        audit_report = healer.scan_codebase()

        assert audit_report.scanned_files_count == 1
        assert audit_report.defects_found_count == 1
        assert audit_report.critical_defects_count == 1
        assert audit_report.absorbing_barrier_preserved is False

        # Run healing with Epistemic Sandbox
        healed_report = healer.heal_codebase(audit_report, apply_patches=True)
        assert len(healed_report.remediations) == 1
        remediation = healed_report.remediations[0]
        assert remediation.sandbox_approved is True
        assert "except Exception as e:" in remediation.repaired_code

        # Verify file on disk was patched safely
        with open(test_file, "r", encoding="utf-8") as f:
            patched_code = f.read()
        assert "except Exception as e:" in patched_code
        assert "except:" not in patched_code

        # Generate markdown report
        md = healer.generate_markdown_report(healed_report)
        assert "Double Helix SRE Audit Report" in md
        assert "Epistemic Sandbox Healing Actions" in md
