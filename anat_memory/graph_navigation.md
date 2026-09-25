### Traversal Interface and Graph Navigation Operations

To explore and manipulate the memory graph programmatically, an autonomous agent executes seven operational graph primitives:

* `OBSERVE(node_id)`: Inspects the current state, activation norms, and local connectivity of a vertex without changing its values.

* `HOP(source_node, edge_id)`: Traverses an explicit directed edge, transferring intermediate activation tensors to downstream targets.

* `GATING_CHECK(node_id, threshold)`: Evaluates whether basal ganglia routing (`N02_GATE`) or surprise scoring (`N09_SURPRISE`) permits onward signal propagation.

* `DIFFUSE(graph_node, query_entities, steps)`: Executes Personalized PageRank over `N07_GRAPH`, returning stationary node probabilities for contextual enrichment.

* `SETTLE_ENERGY(hopfield_node, input_state)`: Runs CCCP updates on `N05_ATTRACT` until convergence:
  $$\Vert{}\xi^{(t+1)} - \xi^{(t)}\Vert{} < \Delta \xi_{\text{tol}}$$

* `DESTABILIZE(param_node, target_layer, key)`: Cleaves synaptic constraints in `N10_PARAM`, preparing feedforward parameters for rank-one modification.

* `ENOUGH()`: Terminating signal executed when retrieved evidence satisfies the downstream task, ending search to preserve compute.
