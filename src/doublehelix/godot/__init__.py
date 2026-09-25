"""DoubleHelix.Go: Godot Engine Integration, Custom Editor Suite & AI Gaming Agent Framework.

Provides programmatic Godot editor control, automated business and licensing injection,
domain asset loader configuration for arkade.new-world-arkitech.dev, and headless agent automation.
"""

from doublehelix.godot.manager import GodotEngineManager
from doublehelix.godot.licensing import GodotLicenseInjector
from doublehelix.godot.agent_client import GodotAgentClient
from doublehelix.godot.asset_loader import GodotAssetConfig
from doublehelix.godot.scaffold import GodotProjectScaffold

__all__ = [
    "GodotEngineManager",
    "GodotLicenseInjector",
    "GodotAgentClient",
    "GodotAssetConfig",
    "GodotProjectScaffold",
]
