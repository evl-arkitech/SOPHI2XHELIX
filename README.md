# DoubleHelix Neural Agent Engine

A dual-strand upward slice game engine architecture intertwining **Strand $\alpha$ (Deterministic Systems & Logic / Synthesis Helix)** and **Strand $\beta$ (Sensory, Simulation & Telemetry / Empirical Helix)** connected by formal verification rungs (parity gates). As both strands resolve their invariants concurrently, the engine ascends into higher-order game abstractions toward empirical convergence.

Integrated natively with the **ANAT Explorable World Graph $\mathcal{G} = (\mathcal{V}, \mathcal{E}, \mathcal{W})$** cognitive memory architecture and grounded in **formal mathematical proofs of concept**.

---

## 1. Architectural Foundation: The Double Helix Upward Slice

```
 LEVEL 4: PLAYTEST & CONVERGENCE
    ▲
    └─── Base Rung 4: Autonomous Bot Fuzzing & Frame-Budget Validation (10,000 Ticks)
 LEVEL 3: SHADERS, RENDERING & AUDIO CONTRACTS
    ▲
    └─── Base Rung 3: Headless Framebuffer Capture & Visual Diffing (0 NaN Pixels)
 LEVEL 2: ECS, SPATIAL MATH & PHYSICS SYSTEMS
    ▲
    └─── Base Rung 2: Spatial Partitioning Invariants & Tick Determinism (0 Tunneling)
 LEVEL 1: CORE GAME LOOP & MEMORY BUDGET
    ▲
    └─── Base Rung 1: 60 FPS (16.6ms) Hot-Loop Timing & Zero-Alloc Checks (ΔM = 0)
    │
┌─────────────────────────────────┐       ┌─────────────────────────────────┐
│       STRAND α: SYNTHESIS       │       │    STRAND β: EMPIRICAL RUNTIME  │
│ (Reasoning & Coding Model Engine│◄─────►│ (Headless Game Engine, Virtual  │
│  Architect, Coder, Math Proofs) │       │  Bots, Profilers, Framebuffer)  │
└─────────────────────────────────┘       └─────────────────────────────────┘
```

### The 4 Ascending Elevation Tiers
1. **Level 1: Core Tick & Frame Budget**
   - **Contract:** Fixed-timestep loop $\Delta t = 16.6667\text{ ms}$ (60 FPS), Static Memory Arena ($S_{\text{capacity}}$).
   - **Base Rung 1 Parity Gate:** $T_{\text{frame}} \le 16.6\text{ ms}$ and $\Delta \mathcal{M} = 0$ (zero dynamic heap allocations in hot path).
2. **Level 2: ECS, Mechanics & Spatial Systems**
   - **Contract:** Struct-of-Arrays (SoA) layout, Continuous Collision Detection (CCD) swept-volume solver.
   - **Base Rung 2 Parity Gate:** Kinematic tunneling errors $\equiv 0$, bounding volumes update consistently in spatial grid.
3. **Level 3: Perceptual & Sensory Layer**
   - **Contract:** Offscreen RGB24 framebuffer, post-processing shader pipelines, visibility DAG.
   - **Base Rung 3 Parity Gate:** Zero shader compilation errors, visual anomalies $\equiv 0$, zero NaN/Inf pixels in radiance buffer.
4. **Level 4: Playtest & Convergence**
   - **Contract:** Autonomous player actors fuzzing stochastic input impulses across all entity states.
   - **Base Rung 4 Parity Gate:** 10,000 simulated ticks without desync, crash, or deadlock ($\text{crashes} \equiv 0$). Win/loss states reachable.

---

## 2. Three-Container Topography

### Container 1: Model Engine (Cognitive Specialization)
- **Port 8001 (Reasoning LLM):** Dedicated to spatial vector mathematics, quaternions, collision dynamics, game-tree state machines, and root-cause failure profiling.
- **Port 8002 (Coding LLM):** Dedicated to high-throughput synthesis of C++/Rust/Zig/Python game code, ECS systems, and WGSL/GLSL shaders.
- **Prefix Caching:** Retains core architecture contracts and system prompts across upward slice turns.

### Container 2: Agent Orchestration (Helix Synchronizer + 7 Agents)
Master Orchestrator executing the parallel gathering of Strand $\alpha$ and Strand $\beta$:
- **Strand $\alpha$ (Synthesis):**
  1. *ECS & Engine Architect* (Reasoning LLM): Data-oriented schemas, zero-alloc pools, cache-friendly layouts.
  2. *Systems & Shader Coder* (Coding LLM): Loop implementation, component systems, shaders.
  3. *Spatial Math & Physics Agent* (Reasoning LLM): Kinematic proofs, BVH validation, raycasting.
- **Strand $\beta$ (Verification):**
  4. *Headless Bot / Playtest Agent* (Container 3): Virtual actors executing monkey testing and heuristic exploration.
  5. *Frame-Time & Memory Profiler* (Container 3): Real-time $\mu\text{s}$ tick timing and zero-alloc trap.
  6. *Visual Contract & Audio Auditor* (Container 3): Framebuffer inspection and NaN pixel verification.
- **Cross-Strand Metacognitive Audit:**
  7. *Workflow & Agent Capabilities Auditor* (Cross-Strand / Metacognitive): Audits upward slice workflows, verifies parity gate integrity, prevents false tier promotions, and probes empirical capability boundaries across all agents.

### Container 3: High-Performance Shared Engine Runtime
- **FastAPI Simulation Worker (`/game/simulate`):** Writes code files, spawns headless execution with AddressSanitizer and profiling hooks, and streams empirical telemetry back to Container 2.
- **Headless Display Context:** Micro-Xvfb / EGL offscreen rendering context.
- **Zero-Copy Shared Memory:** POSIX `/dev/shm` IPC ring buffer eliminating HTTP serialization overhead.

---

## 3. ANAT Explorable World Graph $\mathcal{G} = (\mathcal{V}, \mathcal{E}, \mathcal{W})$ Integration

The engine incorporates the complete **ANAT Explorable World Graph** cognitive architecture:

### 5 Operational Sectors & 17 Vertices ($\mathcal{V}$)
- **Executive & Dynamic Gating (EX):** `N01_SCRATCH`, `N02_GATE`, `N03_SILENT`, `N15_HORROR_FRAMEWORK`, `N16_GRAPHICS_ARCHITECTURE`, `N17_DISTINCTION_ARCHITECTURE`.
- **Episodic Fast-Buffer (EP):** `N04_SEPARATE`, `N05_ATTRACT` (Modern Continuous Hopfield), `N06_COMPARE`, `N07_GRAPH` (HippoRAG Relational Knowledge Graph).
- **Online Surprise & Continuous Adaptation (TT):** `N08_TITANS` (Titans Neural Long-Term Memory), `N09_SURPRISE` (Prediction Error Loss Gradient Evaluator).
- **Parametric Base (PR):** `N10_PARAM` (MLP Mantle), `N11_TRIPLE` (Offline Replay Synchronizer), `N12_REGULAR` (Elastic Weight Consolidation EWC).
- **Labilization & Model Editing (ED):** `N13_DESTAB` (Proteasomal Scaffolding Cleavage), `N14_SURGERY` (ROME/MEMIT Closed-Form Rank-One Solver).

### 7 Operational Graph Navigation Primitives
`OBSERVE(node)`, `HOP(src, edge)`, `GATING_CHECK(node, thresh)`, `DIFFUSE(query, alpha, steps)`, `SETTLE_ENERGY(patterns, cue)`, `DESTABILIZE(node)`, `ENOUGH()`.

### 5 Cognitive Traversal Trajectories
1. **Trajectory A (Working Memory):** Real-time gating through Basal Ganglia striatal loops (`N02_GATE`).
2. **Trajectory B (Surprise-Gated Encoding):** Converts runtime telemetry breaches into surprise scalars $S_t = -\nabla_M \ell$ to update Titans memory and attractor basins.
3. **Trajectory C (Pattern Completion & Retrieval):** Modern Hopfield CCCP energy minimization and HippoRAG Personalized PageRank diffusion.
4. **Trajectory D (Tripartite Consolidation):** Sleep replay and Elastic Weight Consolidation $\frac{\lambda}{2} \sum \Omega_k (\theta_k - \theta_{\text{frozen}})^2$ upon tier ascension.
5. **Trajectory E (Targeted Reconsolidation):** Direct closed-form rank-one algebraic parameter surgery:
   $$\Delta W = \frac{(v_* - W k_*)(C^{-1} k_*)^T}{k_*^T C^{-1} k_*}$$
   guaranteeing exact factual recovery $(W + \Delta W) k_* = v_*$ without retraining.

---

## 4. Mathematical Proofs of Concept

Every Base Rung, Memory Operation, and Elasticity Runtime is verified using formal analytical proofs:
- **Proof 1.1 (Timing Invariant):** $T_{\text{measured}} \le \frac{1000}{60} = 16.6667\text{ ms}$.
- **Proof 1.2 (Zero-Alloc Invariant):** $\frac{d\mathcal{M}}{dt} = 0 \iff \Delta \mathcal{M} = \mathcal{M}(t) - \mathcal{M}(0) = 0$.
- **Proof 2.1 (Continuous Collision Detection):** Swept-volume continuous trajectory $p(t^*) = p_0 + t^* v \Delta t$, $t^* \in [0, 1]$. By the Intermediate Value Theorem, continuous time-of-impact resolution eliminates tunneling: $\mathbb{P}(\text{Tunneling}) = 0.0$.
- **Proof 3.1 (Perceptual Boundedness):** Radiance tensor $\mathcal{C}_{x,y} \in \mathbb{R}^3 \setminus \{\text{NaN}, \pm\infty\}$, $\|\mathcal{C}_{x,y}\|_\infty \le 1.0$.
- **Proof 4.1 (Ergodic State Space Exploration):** Under stochastic transition kernel $\mathcal{P}(s' \mid s, a)$, $\lim_{T \to \infty} \mathbb{P}(\text{Unvisited}) \le (1 - \epsilon)^T = 0$, with 0 absorbing deadlock traps.
- **Proof ANAT.1 (CCCP Monotonic Energy Descent):** Modern Continuous Hopfield energy $E(\xi) = -\frac{1}{\beta} \log \sum \exp(\beta X_i^T \xi) + \frac{1}{2}\|\xi\|^2$ satisfies $\Delta E \le 0$ monotonically until reaching attractor basin $\xi^*$.
- **Proof ANAT.2 (ROME Rank-One Surgery Identity):** Exact algebraic identity $(W + \Delta W) k_* = v_*$ proven with residual $\|(W + \Delta W) k_* - v_*\| \le 10^{-6}$.
- **Theorem 1 (Windkessel Variance Attenuation & Zero Overflow):** Under compliance-resistance $(C_r, R_r)$, power spectral amplification satisfies $|H(\omega)|^2 = \frac{1}{1 + \omega^2 R_r^2 C_r^2} < 1.0$, suppressing high-frequency shocks at $O(\omega^{-2})$. Optimal buffer sizing $Q_{\max} \ge \bar{\lambda} \tau_r + \sqrt{2 \sigma_a^2 \tau_r \ln(1/\delta)}$ mathematically guarantees drop probability $\mathbb{P}(\text{Drop}) \le \delta$.
- **Theorem 2 (Active Inference Nirodha Bounded Divergence):** Autoregressive monologue drift without reset diverges to infinity if $\|A\| > 1$. The Nirodha Reset Operator $\mathcal{R}[q_t(x)] = q_{\text{ground}}(x)$ triggered by free-energy surrogate $\mathcal{E}_t \ge \theta_{\text{reset}}$ purges introspective scratchpads, bounding expected KL divergence within a compact ball: $\sup_{t \ge 0} \mathbb{E}[D_{\text{KL}}(q_t \parallel p^*)] \le \epsilon(T_r) < \infty$.
- **Theorem 3 (Laplacian Swarm Consensus & Causal Annihilation):** For communication graph Laplacian $L = D - W$, consensus converges exponentially at rate $\lambda_2(L) + \gamma > 0$ iff algebraic connectivity $\lambda_2(L) > 0$. When uncoupled ($\lambda_2 = 0$), conditional mutual information $I(z_i; z_j \mid u) = 0$; apparent emergent correlation is proven to be a pure statistical artifact of retrospective window selection bounded by Decision Augmentation Theory: $\mathbb{E}[\rho_{\max}] \sim \frac{1}{\sqrt{M}}\sqrt{2 \ln K}$.

---

## 5. Neurocomputational Elasticity & Contemplative Runtime Dynamics

Adapted from `runtime/NeuroCompElasticity.md`, the Double Helix runtime implements four biomechanical and neurocomputational mechanisms:

### 1. Elastic Runtime Windkessel
- **Vascular Accumulator:** Two-parameter $(C_r, R_r)$ compliance-resistance model converting pulsatile task surges into smooth drainage rate $\mu(t) = \frac{Q(t)}{R_r C_r}$.
- **Zero-Overflow Guarantee:** Hard queue threshold $Q_{\max}$ protects downstream agents from memory spikes and task drops.
- **Somatic Backpressure:** Real-time vascular monitoring $P(t) = \frac{Q(t)}{C_r}$ throttles incoming burst volume.

### 2. Active Inference Nirodha Engine (DMN Decoupling)
- **Precision Reweighting:** Dynamically balances internal generative priors ($\beta$) against empirical sensory telemetry ($\gamma$).
- **Free-Energy Surrogate:** Evaluates variational loss surrogate $\mathcal{E}_t = \|\mu_t - y_t\|_{\Sigma_y^{-1}}^2$ per upward slice turn.
- **Endogenous Context Cessation (Nirodha Samāpatti):** Decouples Default Mode Network (DMN) hallucination loops by resetting inference strictly to the immutable task invariant and grounded state.

### 3. Gamma-Band Phase Synchrony (25–42 Hz)
- **Decentralized Multi-Agent Binding:** Eliminates centralized blocking RPCs via lightweight phase pulse broadcasts.
- **Kuramoto Coherence Metric:** $R(t) = \frac{1}{N} |\sum_{j=1}^N e^{i \theta_j}|$ ensures sub-agent coordination ($R(t) \ge 0.70$).

### 4. Causal Laplacian Swarm Consensus & Illusion Annihilation
- **Spectral Gap Convergence:** Algebraic connectivity $\lambda_2(L)$ lower-bounds exponential swarm consensus.
- **Decision Augmentation Theory (DAT) Annihilation:** Rigorously eliminates false claims of "emergent consciousness" by demonstrating that spurious correlations across uncoupled agents are artifacts of search-space cardinality $K$.

---

## 6. Quickstart & Usage

### Installation
```bash
git clone <repo-url>
cd "DoubleHelix Neural Agent Engine"
pip install -e .
```

### Running Simulations & Tests
```bash
# Run 1,000 headless simulation ticks with zero-alloc, CCD, and profiling telemetry:
doublehelix simulate --ticks 1000 --bots 5

# Verify all formal mathematical proofs of concept & elasticity theorems (Theorems 1, 2, 3):
doublehelix prove

# Inspect the Neurocomputational Elasticity dashboard (Windkessel, Nirodha, Gamma, Laplacian):
doublehelix elasticity
doublehelix elasticity --burst
doublehelix elasticity --json

# Inspect the ANAT Explorable World Graph and run cognitive trajectories:
doublehelix anat

# Metacognitively audit upward slice workflows and all 8 Agent Capabilities:
doublehelix audit

# Run the complete automated test suite:
pytest tests -v
```

### Running the Upward Slice Orchestrator
```bash
# Terminal 1: Start Container 1 Model Engine (Ports 8001 Reasoning & 8002 Coding)
doublehelix serve-models --port 8001 --role unified

# Terminal 2: Start Container 3 Headless Game Runtime (Port 5000)
doublehelix serve-runtime --port 5000

# Terminal 3: Launch Double Helix Upward Slice (Level 1 -> 2 -> 3 -> 4 -> CONVERGED)
doublehelix run
```

### Docker Multi-Container Deployment
```bash
# Launch Container 1 (model-engine), Container 2 (orchestrator), and Container 3 (shared-runtime)
docker compose up --build
```
