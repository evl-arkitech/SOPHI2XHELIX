"""DoubleHelix Hermes Integration Package.

Fuses Nous Research Hermes 3 Sovereign Neural Cortex with the
Double Helix Dual-Strand Upward Slice Engine and the 17-Node
ANAT Explorable World Graph memory architecture.
"""

from doublehelix.hermes.client import HermesClient
from doublehelix.hermes.bridge import HybridLLMBridge
from doublehelix.hermes.tools import DOUBLE_HELIX_HERMES_TOOLS, DoubleHelixHermesDispatcher
from doublehelix.hermes.singularity import ANATHermesSingularity

__all__ = [
    "HermesClient",
    "HybridLLMBridge",
    "DOUBLE_HELIX_HERMES_TOOLS",
    "DoubleHelixHermesDispatcher",
    "ANATHermesSingularity",
]
