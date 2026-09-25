/**
 * Cloudflare Durable Object: HelixStateSynchronizer
 * 
 * Provides globally coordinated, consistent, low-latency state synchronization
 * between Strand Alpha (Synthesis) and Strand Beta (Verification) with real-time WebSockets.
 */

import { HelixState, ParityGateResult } from "../types";

export class HelixStateSynchronizer {
  private state: DurableObjectState;
  private currentHelixState: HelixState;
  private sockets: Set<WebSocket>;

  constructor(state: DurableObjectState) {
    this.state = state;
    this.sockets = new Set();
    this.currentHelixState = {
      tier: "LEVEL_1_KERNEL",
      codebase: {},
      avg_frame_time_ms: 0.0,
      allocations_in_loop: 0,
      headless_bot_crashes: 0,
      visual_anomalies: 0,
      spatial_invariants_valid: true,
      current_cycle: 0,
      max_cycles_per_tier: 5,
      last_updated: new Date().toISOString()
    };

    // Load persisted state from Durable Object storage
    this.state.blockConcurrencyWhile(async () => {
      const stored = await this.state.storage.get<HelixState>("helix_state");
      if (stored) {
        this.currentHelixState = stored;
      }
    });
  }

  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);

    // 1. WebSocket upgrade for real-time telemetry streaming
    if (request.headers.get("Upgrade") === "websocket") {
      const pair = new WebSocketPair();
      const [client, server] = Object.values(pair);

      server.accept();
      this.sockets.add(server);

      // Send initial state upon connection
      server.send(JSON.stringify({ type: "INITIAL_STATE", state: this.currentHelixState }));

      server.addEventListener("close", () => {
        this.sockets.delete(server);
      });

      return new Response(null, { status: 101, webSocket: client });
    }

    // 2. HTTP State endpoints
    if (url.pathname.endsWith("/state") && request.method === "GET") {
      return new Response(JSON.stringify(this.currentHelixState), {
        headers: { "Content-Type": "application/json" }
      });
    }

    if (url.pathname.endsWith("/update") && request.method === "POST") {
      const patch: any = await request.json();
      const frame = patch.frame_data_url || "";
      delete patch.frame_data_url;
      this.currentHelixState = {
        ...this.currentHelixState,
        ...patch,
        last_updated: new Date().toISOString()
      };
      await this.state.storage.put("helix_state", this.currentHelixState);
      this.broadcast({ type: "STATE_UPDATED", state: this.currentHelixState, frame });

      return new Response(JSON.stringify({ success: true, state: this.currentHelixState }), {
        headers: { "Content-Type": "application/json" }
      });
    }

    if (url.pathname.endsWith("/frame") && request.method === "POST") {
      const body: any = await request.json();
      this.broadcast({ type: "FRAME_STREAM", frame: body.frame_data_url || body.frame, telemetry: body.telemetry });
      return new Response(JSON.stringify({ broadcasted: true }), {
        headers: { "Content-Type": "application/json" }
      });
    }

    if (url.pathname.endsWith("/rung-passed") && request.method === "POST") {
      const result: ParityGateResult = await request.json();
      this.broadcast({ type: "RUNG_EVALUATED", result });
      return new Response(JSON.stringify({ broadcasted: true }), {
        headers: { "Content-Type": "application/json" }
      });
    }

    return new Response("Not found", { status: 404 });
  }

  private broadcast(message: any) {
    const data = JSON.stringify(message);
    for (const ws of this.sockets) {
      try {
        ws.send(data);
      } catch (err) {
        this.sockets.delete(ws);
      }
    }
  }
}
