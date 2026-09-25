# DoubleHelix Dedicated Cloudflare Edge Server

A dedicated, globally distributed Cloudflare Edge Server for the **DoubleHelix Neural Agent Engine**, providing sub-millisecond edge API routing, real-time WebSocket state synchronization, and Cloudflare Workers AI integration.

---

## Capabilities

1. **Global Edge State Synchronization (Durable Objects)**
   - `HelixStateSynchronizer` maintains the authoritative global state of the ascending upward slice.
   - Low-latency WebSockets (`/ws`) broadcast state transitions, Base Rung parity results, and empirical telemetry vectors to all connected dashboards, IDEs, and local runtimes.

2. **Cloudflare Workers AI Inference**
   - Direct execution on Cloudflare's serverless edge GPUs:
     - **Reasoning:** `@cf/meta/llama-3.1-8b-instruct` (spatial math proofs, zero-alloc layout contracts, root-cause diagnostics).
     - **Coding:** `@cf/qwen/qwen2.5-coder-7b-instruct` (high-throughput game code & shader synthesis).
   - Standard OpenAI-compatible `/v1/chat/completions` API endpoint at the edge.

3. **ANAT Explorable World Graph Edge Engine**
   - Sub-millisecond routing across all 17 vertices and 25 directed edges of the ANAT cognitive memory architecture.
   - Instant edge trajectory execution:
     - `POST /api/anat/traverse` with Trajectories `A` (Working Memory), `B` (Surprise), `C` (Hopfield CCCP), `D` (Sleep Consolidation), `E` (ROME Surgery).

4. **Edge Parity Gate Evaluation & Mathematical Proofs**
   - `POST /api/parity/evaluate` validates telemetry vectors against the 4 Base Rung contracts with analytical proof generation directly on the edge.

5. **Real-Time Edge Visualizer Dashboard**
   - Interactive HTML5 / Canvas / WebGL dashboard served directly from edge locations (`GET /`) displaying animated 3D double helix strands, live telemetry meters, and ANAT graph status.

---

## API Reference

| Method | Path | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Real-Time Helix Ascension & ANAT Dashboard |
| `GET` | `/ws` | WebSocket endpoint for live telemetry streaming |
| `GET` | `/api/helix/state` | Returns the current global `HelixState` |
| `POST` | `/api/helix/update` | Updates state properties & broadcasts via WebSockets |
| `POST` | `/api/parity/evaluate` | Evaluates a Base Rung parity gate with mathematical proofs |
| `GET` | `/api/anat/graph` | Returns the 17 nodes and 25 edges of the ANAT World Graph |
| `POST` | `/api/anat/traverse` | Executes an ANAT cognitive trajectory at the edge |
| `POST` | `/v1/chat/completions` | OpenAI-compatible endpoint powered by Workers AI |
| `GET` | `/health` | Edge server health check & Cloudflare PoP location (`colo`) |

---

## Deployment & Local Development

### 1. Local Development
```bash
cd cloudflare-edge
npm install
npm run dev
```

### 2. Deploy to Cloudflare
```bash
npx wrangler deploy
```

### 3. Connect Local DoubleHelix Engine to Edge Server
Set the environment variable in your local Python Double Helix engine:
```bash
$env:REASONING_LLM_URL="https://doublehelix-edge-server.<your-subdomain>.workers.dev/v1"
$env:CODING_LLM_URL="https://doublehelix-edge-server.<your-subdomain>.workers.dev/v1"
```
