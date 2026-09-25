# ==============================================================================
# DoubleHelix Neural Agent Engine (DoubleHelix.Go Edition)
# Main Godot Editor Plugin Entry Point
# Cosmic Souls of Sovereignty Inc. • arkade.new-world-arkitech.dev
# ==============================================================================
@tool
extends EditorPlugin

var dock_instance: Control
var export_plugin: EditorExportPlugin

func _enter_tree() -> void:
	print("[DoubleHelix.Go] Initializing DoubleHelix Custom Editor Suite v2.4...")

	# 1. Register Custom Editor Dock with Material Builder, Scene Gen & Workflow
	dock_instance = preload("res://addons/doublehelix_engine/doublehelix_dock.tscn").instantiate()
	add_control_to_dock(DOCK_SLOT_RIGHT_UL, dock_instance)

	# 2. Register Export Plugin for Automated Business/Licensing Injection
	export_plugin = preload("res://addons/doublehelix_engine/doublehelix_export_plugin.gd").new()
	add_export_plugin(export_plugin)

	# 3. Register Tool Menu Commands
	add_tool_menu_item("DoubleHelix: Inject Business Invariants", Callable(self, "_on_menu_inject_licensing"))
	add_tool_menu_item("DoubleHelix: Generate 3-Room Tactical Complex", Callable(self, "_on_menu_gen_complex"))
	add_tool_menu_item("DoubleHelix: Spawn FPS Player Rig", Callable(self, "_on_menu_spawn_fps"))
	add_tool_menu_item("DoubleHelix: Apply Cinematic Noir Lighting", Callable(self, "_on_menu_apply_noir"))
	add_tool_menu_item("DoubleHelix: Auto-Generate Mesh Colliders", Callable(self, "_on_menu_auto_colliders"))
	add_tool_menu_item("DoubleHelix: Refresh Arkade Asset Manifest", Callable(self, "_on_menu_sync_assets"))

	# 4. Register Autoload Singletons for Runtime Game
	add_autoload_singleton("DoubleHelixLoader", "res://addons/doublehelix_engine/doublehelix_asset_loader.gd")
	add_autoload_singleton("DoubleHelixLicense", "res://addons/doublehelix_engine/license_manager.gd")

	print("[DoubleHelix.Go] Double Helix Suite Active: Material Builder, Scene Gen & Agent Deck Ready!")

func _exit_tree() -> void:
	print("[DoubleHelix.Go] Cleaning up DoubleHelix Custom Editor Suite...")
	if dock_instance:
		remove_control_from_docks(dock_instance)
		dock_instance.queue_free()

	if export_plugin:
		remove_export_plugin(export_plugin)

	remove_tool_menu_item("DoubleHelix: Inject Business Invariants")
	remove_tool_menu_item("DoubleHelix: Generate 3-Room Tactical Complex")
	remove_tool_menu_item("DoubleHelix: Spawn FPS Player Rig")
	remove_tool_menu_item("DoubleHelix: Apply Cinematic Noir Lighting")
	remove_tool_menu_item("DoubleHelix: Auto-Generate Mesh Colliders")
	remove_tool_menu_item("DoubleHelix: Refresh Arkade Asset Manifest")

	remove_autoload_singleton("DoubleHelixLoader")
	remove_autoload_singleton("DoubleHelixLicense")

func _on_menu_inject_licensing() -> void:
	if dock_instance and dock_instance.has_method("_on_inject_pressed"):
		dock_instance._on_inject_pressed()

func _on_menu_gen_complex() -> void:
	if dock_instance and dock_instance.has_method("_on_generate_residence_pressed"):
		dock_instance._on_generate_residence_pressed()

func _on_menu_spawn_fps() -> void:
	if dock_instance and dock_instance.has_method("_on_spawn_fps_rig_pressed"):
		dock_instance._on_spawn_fps_rig_pressed()

func _on_menu_apply_noir() -> void:
	if dock_instance and dock_instance.has_method("_apply_mood"):
		dock_instance._apply_mood("cinematic_noir")

func _on_menu_auto_colliders() -> void:
	if dock_instance and dock_instance.has_method("_on_enforce_colliders_pressed"):
		dock_instance._on_enforce_colliders_pressed()

func _on_menu_sync_assets() -> void:
	if dock_instance and dock_instance.has_method("_on_generate_manifest_pressed"):
		dock_instance._on_generate_manifest_pressed()
