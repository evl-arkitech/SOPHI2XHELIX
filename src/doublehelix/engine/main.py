"""Main entrypoint for the headless game engine executable.

Invoked directly or by Container 3's game_runner.py simulation worker.
Outputs profiling metrics between __METRICS_START__ and __METRICS_END__ delimiters.
"""

import argparse
import json
import sys
from doublehelix.engine.kernel import DeterministicKernel


def main():
    parser = argparse.ArgumentParser(description="DoubleHelix Headless Deterministic Game Engine")
    parser.add_argument("--headless-ticks", type=int, default=1000, help="Number of ticks to simulate")
    parser.add_argument("--simulated-bots", type=int, default=5, help="Number of virtual actors fuzzing inputs")
    parser.add_argument("--profile-telemetry", action="store_true", help="Output telemetry metrics JSON")
    parser.add_argument("--world-width", type=float, default=640.0)
    parser.add_argument("--world-height", type=float, default=360.0)

    args = parser.parse_args()

    kernel = DeterministicKernel(
        max_entities=100,
        bot_count=args.simulated_bots,
        world_width=args.world_width,
        world_height=args.world_height
    )

    metrics = kernel.run_simulation(total_ticks=args.headless_ticks)

    if args.profile_telemetry:
        print(f"ALLOC_IN_UPDATE: {metrics['allocations_in_loop']}")
        print("__METRICS_START__")
        print(json.dumps(metrics))
        print("__METRICS_END__")
    else:
        print(f"Simulation completed: {metrics['ticks_executed']} ticks, avg {metrics['avg_frame_time_ms']}ms/frame")

    sys.exit(metrics.get("exit_code", 0))


if __name__ == "__main__":
    main()
