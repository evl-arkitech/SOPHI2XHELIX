"""Container 3: Headless Game Runtime modules."""

from doublehelix.runtime.game_runner import app, run_simulation, start_runtime_server, SimRequest
from doublehelix.runtime.telemetry import parse_telemetry_output
from doublehelix.runtime.elasticity import (
    WindkesselConfig,
    ElasticRuntimeWindkessel,
    NirodhaResetConfig,
    ActiveInferenceNirodhaEngine,
    GammaPhaseSynchronizer,
    CausalLaplacianConsensus,
)
from doublehelix.runtime.decision_core import (
    ActionCandidate,
    TriageMetrics,
    EpistemicRolloutResult,
    SomaticAttentionalTriage,
    RecognitionPrimedGenerator,
    EpistemicDecouplingSandbox,
    SensemakingResetWatchdog,
    OutlierEngineeredDecisionCore,
)
from doublehelix.runtime.sheaf_sophi import (
    DifferenceRecord,
    SubliminalHypothesis,
    PoincareDifferentialIncubator,
    GrothendieckCellularSheaf,
    TeslaMonoidalOptic,
    LinearSessionChannel,
    LinearSessionEndpoint,
)

__all__ = [
    "app",
    "run_simulation",
    "start_runtime_server",
    "SimRequest",
    "parse_telemetry_output",
    "WindkesselConfig",
    "ElasticRuntimeWindkessel",
    "NirodhaResetConfig",
    "ActiveInferenceNirodhaEngine",
    "GammaPhaseSynchronizer",
    "CausalLaplacianConsensus",
    "ActionCandidate",
    "TriageMetrics",
    "EpistemicRolloutResult",
    "SomaticAttentionalTriage",
    "RecognitionPrimedGenerator",
    "EpistemicDecouplingSandbox",
    "SensemakingResetWatchdog",
    "OutlierEngineeredDecisionCore",
    "DifferenceRecord",
    "SubliminalHypothesis",
    "PoincareDifferentialIncubator",
    "GrothendieckCellularSheaf",
    "TeslaMonoidalOptic",
    "LinearSessionChannel",
    "LinearSessionEndpoint",
]

