###  Explorable Traversal Trajectories

An agent navigates specific subgraphs along defined operational trajectories to accomplish primary cognitive workflows.

#### Trajectory A: Real-Time Working Memory and Gated Input Ingestion

* **Functional Scope:** Ingesting live token streams, arbitrating working memory retention, and minimizing metabolic/computational footprint.

* **Active Route:**
  
  1. Incoming tokens arrive at `N01_SCRATCH`.
  
  2. Representations project along `E01` to `N02_GATE`.
  
  3. If `N02_GATE` evaluates the input as task-relevant, it disinhibits the thalamocortical loop via `E02`, locking the state into active attention.
  
  4. Non-critical tokens transition along `E03` to `N03_SILENT`, where they remain accessible as transient fast weights without consuming primary attention capacity.
  
  5. The sequence state evaluates against expected tokens at `N09_SURPRISE` via `E04`.

#### Trajectory B: Surprise-Gated Episodic Encoding

* **Functional Scope:** Transforming unexpected, high-salience experiences into orthogonal engrams and relational graph topology.

* **Active Route:**
  
  1. When surprise exceeds baseline thresholds, `N09_SURPRISE` modulates `N08_TITANS` via `E05`, updating test-time parameters using the surprise gradient:
     $$S_t = -\nabla_M \ell(M_{t-1}; x_t)$$
  
  2. Concurrently, `N01_SCRATCH` routes the token context along `E06` to `N04_SEPARATE`.
  
  3. `N04_SEPARATE` projects high-dimensional sparse representations along `E07` to establish an attractor basin in `N05_ATTRACT`.
  
  4. Concurrently, relational entities project along `E08` to `N07_GRAPH`, instantiating new vertices and semantic edges in the episodic knowledge graph.

#### Trajectory C: Associative Pattern Completion and Multi-Hop Retrieval

* **Functional Scope:** Reconstructing full historical episodes from ambiguous, incomplete sensory cues and traversing disjoint semantic documents.

* **Active Route:**
  
  1. A partial cue enters `N01_SCRATCH` and routes to `N04_SEPARATE` and `N07_GRAPH`.
  
  2. The cue acts as an initial state $\xi^{(0)}$ in `N05_ATTRACT`, propagating along `E09` via CCCP energy minimization:
     $$\xi^{(1)} = X \, \text{softmax}\left(\beta \, X^T \xi^{(0)}\right)$$
  
  3. Relational components trigger Personalized PageRank on `N07_GRAPH`, diffusing probability mass along `E10` across multi-hop entity pathways:
     $$p^{(t+1)} = (1 - \alpha) \, p_0 + \alpha \, A \, D^{-1} p^{(t)}$$
  
  4. Retrieved candidates converge on `N06_COMPARE` for cross-attention verification.
  
  5. Verified representations route through `E11` to hydrate `N01_SCRATCH` with retrieved context.

#### Trajectory D: Offline Tripartite Consolidation (Sleep Replay)

* **Functional Scope:** Transferring volatile episodic buffers into stable parametric weights without catastrophic interference.

* **Active Route:**
  
  1. Low system utilization activates `N11_TRIPLE`.
  
  2. `N11_TRIPLE` samples completed memory vectors from `N05_ATTRACT` via `E12` and relational walks from `N07_GRAPH` via `E13`, generating synthetic replay batches $\mathcal{D}_{\text{replay}}$.
  
  3. Batches route along `E14` into `N10_PARAM` using student-teacher distillation:
     $$\mathcal{L}_{\text{consolidation}}(\theta) = (1 - \gamma)\mathcal{L}_{\text{task}} + \gamma \mathcal{D}_{\text{KL}}(p_\theta \,\Vert{}\, p_{\text{frozen}}) + \sum_k \frac{\lambda}{2} \Omega_k (\theta_k - \theta_{\text{frozen}, k})^2$$
  
  4. `N12_REGULAR` enforces weight-preservation bounds via `E15`, penalizing modifications to synapses with high importance values $\Omega_k$.
  
  5. Consolidated items in `N05_ATTRACT` are cleared, while unique episodic anchor traces remain indexed in `N07_GRAPH`.

#### Trajectory E: Error-Induced Destabilization and Targeted Reconsolidation

* **Functional Scope:** Selectively modifying consolidated facts within base weights without full model retraining.

* **Active Route:**
  
  1. A high-confidence mismatch occurs between recalled facts and live verification, triggering `N09_SURPRISE`.
  
  2. `N09_SURPRISE` activates `N13_DESTAB` along `E16`, initiating proteasome-style destabilization that unlocks target layer parameters.
  
  3. `N13_DESTAB` engages `N14_SURGERY` via `E17`, computing subject entity keys $k_*$ and target factual values $v_*$.
  
  4. `N14_SURGERY` executes a rank-one matrix update along `E18` directly into `N10_PARAM`:
     $$\Delta W = \frac{(v_* - W_{\text{out}} k_*)(C^{-1} k_*)^T}{k_*^T C^{-1} k_*}$$
  
  5. The target fact is restabilized, leaving surrounding semantic knowledge unaltered
