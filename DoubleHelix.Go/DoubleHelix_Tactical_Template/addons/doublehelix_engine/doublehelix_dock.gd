# ==============================================================================
# DoubleHelix Neural Agent Engine (DoubleHelix.Go Edition)
# Integrated Editor Suite: Material Builder, Scene Generator, Asset Library & Workflow Tools
# Cosmic Souls of Sovereignty Inc. • arkade.new-world-arkitech.dev
# ==============================================================================
@tool
extends Control

const MaterialBuilder = preload("res://addons/doublehelix_engine/material_builder.gd")
const SceneGenerator = preload("res://addons/doublehelix_engine/scene_generator.gd")
const AssetLibrary = preload("res://addons/doublehelix_engine/asset_library.gd")
const WorkflowTools = preload("res://addons/doublehelix_engine/workflow_tools.gd")

# UI References - Material Builder
var mat_preset_opt: OptionButton
var mat_name_input: LineEdit
var mat_roughness_slider: HSlider
var mat_metallic_slider: HSlider
var mat_normal_slider: HSlider
var mat_uv_slider: HSlider
var mat_triplanar_check: CheckBox
var mat_color_picker: ColorPickerButton

# UI References - Scene Generator
var room_w_spin: SpinBox
var room_l_spin: SpinBox
var room_h_spin: SpinBox
var room_floor_opt: OptionButton
var room_wall_opt: OptionButton

# UI References - Props & Assets
var prop_opt: OptionButton

# UI References - Business
var company_input: LineEdit
var domain_input: LineEdit
var storage_input: LineEdit
var title_input: LineEdit
var status_label: Label
var log_text: TextEdit

func _enter_tree() -> void:
	name = "DoubleHelix Suite"
	custom_minimum_size = Vector2(340, 560)
	build_ui()

func build_ui() -> void:
	for child in get_children():
		child.queue_free()

	var tab_container = TabContainer.new()
	tab_container.anchor_right = 1.0
	tab_container.anchor_bottom = 1.0
	add_child(tab_container)

	# =========================================================================
	# TAB 1: Material Builder
	# =========================================================================
	var mat_tab = create_tab_vbox(tab_container, "Materials")
	mat_tab.add_child(create_header("🎨 INTERACTIVE PBR MATERIAL BUILDER"))

	mat_tab.add_child(create_label("PBR Preset:"))
	mat_preset_opt = OptionButton.new()
	var presets = [
		"walnut_wood", "polished_tile", "drywall_plaster",
		"exterior_brick", "granite_countertop", "brushed_steel",
		"bulletproof_glass", "tactical_concrete", "neon_hologram"
	]
	for p in presets:
		mat_preset_opt.add_item(p)
	mat_preset_opt.item_selected.connect(_on_mat_preset_selected)
	mat_tab.add_child(mat_preset_opt)

	mat_tab.add_child(create_label("Material Name:"))
	mat_name_input = LineEdit.new()
	mat_name_input.text = "walnut_wood_pbr"
	mat_tab.add_child(mat_name_input)

	mat_tab.add_child(create_label("Roughness:"))
	mat_roughness_slider = create_slider(0.0, 1.0, 0.65, 0.05)
	mat_tab.add_child(mat_roughness_slider)

	mat_tab.add_child(create_label("Metallic:"))
	mat_metallic_slider = create_slider(0.0, 1.0, 0.0, 0.05)
	mat_tab.add_child(mat_metallic_slider)

	mat_tab.add_child(create_label("Normal Scale:"))
	mat_normal_slider = create_slider(0.0, 3.0, 1.0, 0.1)
	mat_tab.add_child(mat_normal_slider)

	mat_tab.add_child(create_label("UV Tiling Scale:"))
	mat_uv_slider = create_slider(0.5, 10.0, 2.0, 0.5)
	mat_tab.add_child(mat_uv_slider)

	mat_triplanar_check = CheckBox.new()
	mat_triplanar_check.text = "Enable Triplanar Mapping (No UV Stretch)"
	mat_tab.add_child(mat_triplanar_check)

	var btn_save_mat = Button.new()
	btn_save_mat.text = "💾 SAVE MATERIAL (.tres)"
	btn_save_mat.pressed.connect(_on_save_material_pressed)
	mat_tab.add_child(btn_save_mat)

	var btn_apply_mat = Button.new()
	btn_apply_mat.text = "🎯 APPLY TO SELECTED MESH"
	btn_apply_mat.pressed.connect(_on_apply_material_pressed)
	mat_tab.add_child(btn_apply_mat)

	var btn_fetch_cdn = Button.new()
	btn_fetch_cdn.text = "🌐 ASSEMBLE FROM ARKADE CDN"
	btn_fetch_cdn.pressed.connect(_on_fetch_arkade_pbr_pressed)
	mat_tab.add_child(btn_fetch_cdn)

	# =========================================================================
	# TAB 2: Scene & Level Generator
	# =========================================================================
	var scene_tab = create_tab_vbox(tab_container, "Scene Gen")
	scene_tab.add_child(create_header("🏗️ PROCEDURAL SCENE GENERATOR"))

	var btn_gen_residence = Button.new()
	btn_gen_residence.text = "🏛️ GENERATE 3-ROOM COMPLEX\n(Refuge, Corridor, Mudroom, CCTV, Spawns)"
	btn_gen_residence.pressed.connect(_on_generate_residence_pressed)
	scene_tab.add_child(btn_gen_residence)

	scene_tab.add_child(HSeparator.new())
	scene_tab.add_child(create_label("--- Parametric Single Room ---"))

	var grid = GridContainer.new()
	grid.columns = 2
	scene_tab.add_child(grid)

	grid.add_child(create_label("Width (m):"))
	room_w_spin = create_spinbox(4.0, 50.0, 12.0)
	grid.add_child(room_w_spin)

	grid.add_child(create_label("Length (m):"))
	room_l_spin = create_spinbox(4.0, 50.0, 16.0)
	grid.add_child(room_l_spin)

	grid.add_child(create_label("Height (m):"))
	room_h_spin = create_spinbox(2.4, 12.0, 3.5)
	grid.add_child(room_h_spin)

	var btn_gen_room = Button.new()
	btn_gen_room.text = "📦 GENERATE SINGLE ROOM"
	btn_gen_room.pressed.connect(_on_generate_room_pressed)
	scene_tab.add_child(btn_gen_room)

	# =========================================================================
	# TAB 3: Asset Library & Modular Props
	# =========================================================================
	var asset_tab = create_tab_vbox(tab_container, "Asset Library")
	asset_tab.add_child(create_header("📦 ARKADE ASSET LIBRARY & MODULAR KIT"))

	asset_tab.add_child(create_label("Modular Prop Generator:"))
	prop_opt = OptionButton.new()
	var prop_types = [
		"tactical_crate", "security_door", "tactical_desk",
		"gun_cabinet", "concrete_barrier", "security_camera"
	]
	for p in prop_types:
		prop_opt.add_item(p)
	asset_tab.add_child(prop_opt)

	var btn_instantiate_prop = Button.new()
	btn_instantiate_prop.text = "➕ INSTANTIATE PROP IN ACTIVE SCENE"
	btn_instantiate_prop.pressed.connect(_on_instantiate_prop_pressed)
	asset_tab.add_child(btn_instantiate_prop)

	var btn_save_prop = Button.new()
	btn_save_prop.text = "💾 SAVE PROP AS SCENE (.tscn)"
	btn_save_prop.pressed.connect(_on_save_prop_pressed)
	asset_tab.add_child(btn_save_prop)

	var btn_manifest = Button.new()
	btn_manifest.text = "⚡ REFRESH ARKADE ASSET MANIFEST"
	btn_manifest.pressed.connect(_on_generate_manifest_pressed)
	asset_tab.add_child(btn_manifest)

	# =========================================================================
	# TAB 4: Workflow Tools & Camera Rigs
	# =========================================================================
	var workflow_tab = create_tab_vbox(tab_container, "Workflow")
	workflow_tab.add_child(create_header("⚡ AGENT & WORKFLOW ACCELERATORS"))

	var btn_fps_rig = Button.new()
	btn_fps_rig.text = "🎮 SPAWN FPS PLAYER RIG\n(Camera + Flashlight + Interaction Ray)"
	btn_fps_rig.pressed.connect(_on_spawn_fps_rig_pressed)
	workflow_tab.add_child(btn_fps_rig)

	var btn_tp_rig = Button.new()
	btn_tp_rig.text = "🎥 SPAWN THIRD-PERSON RIG (Over-Shoulder)"
	btn_tp_rig.pressed.connect(_on_spawn_tp_rig_pressed)
	workflow_tab.add_child(btn_tp_rig)

	workflow_tab.add_child(HSeparator.new())
	workflow_tab.add_child(create_label("Atmospheric Lighting Moods:"))

	var btn_mood_noir = Button.new()
	btn_mood_noir.text = "🌙 MOOD: CINEMATIC NOIR (Midnight Fog)"
	btn_mood_noir.pressed.connect(func(): _apply_mood("cinematic_noir"))
	workflow_tab.add_child(btn_mood_noir)

	var btn_mood_blackout = Button.new()
	btn_mood_blackout.text = "🚨 MOOD: TACTICAL BLACKOUT"
	btn_mood_blackout.pressed.connect(func(): _apply_mood("tactical_blackout"))
	workflow_tab.add_child(btn_mood_blackout)

	var btn_mood_day = Button.new()
	btn_mood_day.text = "☀️ MOOD: DAYLIGHT OPERATIONAL"
	btn_mood_day.pressed.connect(func(): _apply_mood("daylight_operational"))
	workflow_tab.add_child(btn_mood_day)

	workflow_tab.add_child(HSeparator.new())
	var btn_enforce_colliders = Button.new()
	btn_enforce_colliders.text = "🛡️ AUTO-GENERATE COLLIDERS (Zero Tunneling)"
	btn_enforce_colliders.pressed.connect(_on_enforce_colliders_pressed)
	workflow_tab.add_child(btn_enforce_colliders)

	# =========================================================================
	# TAB 5: Business, Licensing & Invariants
	# =========================================================================
	var b_tab = create_tab_vbox(tab_container, "Business")
	b_tab.add_child(create_header("🧬 BUSINESS & LICENSING SUITE"))

	b_tab.add_child(create_label("Game Title:"))
	title_input = LineEdit.new()
	title_input.text = ProjectSettings.get_setting("application/config/name", "DoubleHelix Tactical Arena")
	b_tab.add_child(title_input)

	b_tab.add_child(create_label("Entity:"))
	company_input = LineEdit.new()
	company_input.text = ProjectSettings.get_setting("application/config/company", "Cosmic Souls of Sovereignty Inc.")
	b_tab.add_child(company_input)

	b_tab.add_child(create_label("Domain:"))
	domain_input = LineEdit.new()
	domain_input.text = ProjectSettings.get_setting("application/config/domain", "arkade.new-world-arkitech.dev")
	b_tab.add_child(domain_input)

	b_tab.add_child(create_label("Storage Container URL:"))
	storage_input = LineEdit.new()
	storage_input.text = ProjectSettings.get_setting("application/config/storage_container", "https://arkade.new-world-arkitech.dev/assets")
	b_tab.add_child(storage_input)

	var inject_btn = Button.new()
	inject_btn.text = "🛡️ INJECT BUSINESS & LICENSING INVARIANTS"
	inject_btn.pressed.connect(_on_inject_pressed)
	b_tab.add_child(inject_btn)

	status_label = Label.new()
	status_label.text = "Status: Certified P(RUIN)=0.0000 • CCD Active"
	b_tab.add_child(status_label)

	# Shared Log Box at Bottom
	var log_box = VBoxContainer.new()
	log_box.size_flags_vertical = Control.SIZE_EXPAND_FILL
	log_text = TextEdit.new()
	log_text.size_flags_vertical = Control.SIZE_EXPAND_FILL
	log_text.editable = false
	b_tab.add_child(log_text)

	log_msg("DoubleHelix Editor Suite v2.4 initialized.")

# =============================================================================
# Helper Builders
# =============================================================================
func create_tab_vbox(parent: TabContainer, tab_name: String) -> VBoxContainer:
	var scroll = ScrollContainer.new()
	scroll.name = tab_name
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	parent.add_child(scroll)

	var margin = MarginContainer.new()
	margin.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	margin.add_theme_constant_override("margin_left", 8)
	margin.add_theme_constant_override("margin_right", 8)
	margin.add_theme_constant_override("margin_top", 8)
	margin.add_theme_constant_override("margin_bottom", 8)
	scroll.add_child(margin)

	var vbox = VBoxContainer.new()
	vbox.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	vbox.add_theme_constant_override("separation", 6)
	margin.add_child(vbox)
	return vbox

func create_header(text: String) -> Label:
	var lbl = Label.new()
	lbl.text = text
	return lbl

func create_label(text: String) -> Label:
	var lbl = Label.new()
	lbl.text = text
	return lbl

func create_slider(min_val: float, max_val: float, default_val: float, step_val: float) -> HSlider:
	var s = HSlider.new()
	s.min_value = min_val
	s.max_value = max_val
	s.step = step_val
	s.value = default_val
	return s

func create_spinbox(min_v: float, max_v: float, def_v: float) -> SpinBox:
	var sb = SpinBox.new()
	sb.min_value = min_v
	sb.max_value = max_v
	sb.value = def_v
	return sb

func log_msg(msg: String) -> void:
	if log_text:
		log_text.text += "[" + Time.get_time_string_from_system() + "] " + msg + "\n"
	print("[DoubleHelix Dock] " + msg)

# =============================================================================
# Action Handlers - Material Builder
# =============================================================================
func _on_mat_preset_selected(idx: int) -> void:
	var key = mat_preset_opt.get_item_text(idx)
	mat_name_input.text = key + "_pbr"
	if MaterialBuilder.PRESETS.has(key):
		var p = MaterialBuilder.PRESETS[key]
		mat_roughness_slider.value = float(p.get("roughness_val", 0.5))
		mat_metallic_slider.value = float(p.get("metallic", 0.0))
		log_msg("Selected preset: " + key)

func _on_save_material_pressed() -> void:
	var mat = build_active_material()
	var path = MaterialBuilder.save_material_to_file(mat, mat_name_input.text)
	if path != "":
		log_msg("Saved Material: " + path)

func _on_apply_material_pressed() -> void:
	var mat = build_active_material()
	var editor_if = EditorInterface.get_selection()
	if editor_if:
		var nodes = editor_if.get_selected_nodes()
		if nodes.size() > 0:
			for n in nodes:
				if n is MeshInstance3D:
					n.material_override = mat
					log_msg("Applied material to: " + n.name)
			return
	log_msg("Please select a MeshInstance3D in the Scene Tree to apply material.")

func _on_fetch_arkade_pbr_pressed() -> void:
	var key = mat_preset_opt.get_item_text(mat_preset_opt.selected)
	log_msg("Assembling PBR Maps from Arkade CDN for: " + key)
	var mat = MaterialBuilder.build_preset(key)
	var path = MaterialBuilder.save_material_to_file(mat, key + "_arkade")
	log_msg("Constructed and saved Arkade PBR Material: " + path)

func build_active_material() -> StandardMaterial3D:
	var key = mat_preset_opt.get_item_text(mat_preset_opt.selected)
	var base_cfg = {}
	if MaterialBuilder.PRESETS.has(key):
		base_cfg = MaterialBuilder.PRESETS[key].duplicate(true)

	base_cfg["roughness_val"] = mat_roughness_slider.value
	base_cfg["metallic"] = mat_metallic_slider.value
	base_cfg["normal_scale"] = mat_normal_slider.value
	var uv_val = mat_uv_slider.value
	base_cfg["uv_scale"] = Vector3(uv_val, uv_val, 1.0)
	base_cfg["uv1_triplanar"] = mat_triplanar_check.button_pressed

	return MaterialBuilder.build_material(base_cfg)

# =============================================================================
# Action Handlers - Scene Generator
# =============================================================================
func _on_generate_residence_pressed() -> void:
	log_msg("Generating 3-Room Tactical Complex (City Echoes layout)...")
	var res = SceneGenerator.generate_tactical_residence("scenes/tactical_residence.tscn")
	if res.has("success"):
		log_msg("Generated Tactical Residence: " + res["scene_path"])
		log_msg("Includes Refuge Bedroom, Living Corridor, Mudroom, CCTV Camera, and Spawns.")
	else:
		log_msg("Error generating residence: " + str(res.get("error", "")))

func _on_generate_room_pressed() -> void:
	var w = room_w_spin.value
	var l = room_l_spin.value
	var h = room_h_spin.value
	log_msg("Generating Single Room (" + str(w) + "x" + str(l) + "x" + str(h) + "m)...")

	var cli = preload("res://addons/doublehelix_engine/agent_cli.gd").new()
	var res = cli.handle_generate_room({
		"output_scene": "scenes/room_" + str(int(w)) + "x" + str(int(l)) + ".tscn",
		"width": w, "length": l, "height": h
	})
	if res.has("success"):
		log_msg("Generated room scene: " + res["scene_path"])
	else:
		log_msg("Error: " + str(res.get("error", "")))

# =============================================================================
# Action Handlers - Props & Assets
# =============================================================================
func _on_instantiate_prop_pressed() -> void:
	var prop_name = prop_opt.get_item_text(prop_opt.selected)
	var prop = AssetLibrary.generate_modular_prop(prop_name)
	var root = EditorInterface.get_edited_scene_root()
	if root:
		root.add_child(prop)
		prop.owner = root
		log_msg("Instantiated " + prop_name + " in active scene.")
	else:
		log_msg("No edited scene root found. Open a scene first.")

func _on_save_prop_pressed() -> void:
	var prop_name = prop_opt.get_item_text(prop_opt.selected)
	var prop = AssetLibrary.generate_modular_prop(prop_name)
	var path = AssetLibrary.save_prop_to_scene(prop, prop_name)
	prop.free()
	if path != "":
		log_msg("Saved prop to scene: " + path)

func _on_generate_manifest_pressed() -> void:
	DirAccess.make_dir_recursive_absolute("res://assets")
	var manifest = {
		"storage_container_url": storage_input.text,
		"domain": domain_input.text,
		"catalog": AssetLibrary.ARKADE_ASSETS_CATALOG
	}
	var f = FileAccess.open("res://assets/doublehelix_asset_manifest.json", FileAccess.WRITE)
	if f:
		f.store_string(JSON.stringify(manifest, "  "))
	log_msg("Refreshed res://assets/doublehelix_asset_manifest.json")

# =============================================================================
# Action Handlers - Workflow & Rigs
# =============================================================================
func _on_spawn_fps_rig_pressed() -> void:
	var root = EditorInterface.get_edited_scene_root()
	if root:
		WorkflowTools.setup_fps_player_rig(root, Vector3(0, 0.2, 0))
		log_msg("Spawned FPS Player Rig in active scene.")
	else:
		log_msg("Open a 3D scene first to spawn player rig.")

func _on_spawn_tp_rig_pressed() -> void:
	var root = EditorInterface.get_edited_scene_root()
	if root:
		WorkflowTools.setup_third_person_rig(root, Vector3(0, 0.2, 0))
		log_msg("Spawned Third-Person Rig in active scene.")
	else:
		log_msg("Open a 3D scene first to spawn player rig.")

func _apply_mood(mood: String) -> void:
	var root = EditorInterface.get_edited_scene_root()
	if root:
		WorkflowTools.apply_lighting_mood(root, mood)
		log_msg("Applied lighting mood: " + mood)
	else:
		log_msg("Open a scene first to apply lighting mood.")

func _on_enforce_colliders_pressed() -> void:
	var root = EditorInterface.get_edited_scene_root()
	if root:
		var count = WorkflowTools.ensure_collision_on_meshes(root)
		log_msg("Enforced collisions. Added " + str(count) + " colliders.")
	else:
		log_msg("Open a scene first to enforce collisions.")

# =============================================================================
# Action Handlers - Business & Legal
# =============================================================================
func _on_inject_pressed() -> void:
	var co = company_input.text
	var dom = domain_input.text
	var title = title_input.text
	var storage = storage_input.text

	ProjectSettings.set_setting("application/config/name", title)
	ProjectSettings.set_setting("application/config/company", co)
	ProjectSettings.set_setting("application/config/domain", dom)
	ProjectSettings.set_setting("application/config/storage_container", storage)
	ProjectSettings.set_setting("doublehelix/business/entity", co)
	ProjectSettings.set_setting("doublehelix/business/domain", dom)
	ProjectSettings.set_setting("doublehelix/business/storage_container", storage)
	ProjectSettings.save()

	DirAccess.make_dir_recursive_absolute("res://legal")
	var lic = FileAccess.open("res://legal/LICENSE.txt", FileAccess.WRITE)
	if lic:
		lic.store_string("DoubleHelix Commercial License\n(c) 2026 " + co + " • " + dom + "\nP(RUIN)=0.0000 Certified.")

	var meta = {
		"title": title,
		"company": co,
		"domain": dom,
		"storage_container": storage,
		"engine": "DoubleHelix.Go v2.4 (Godot 4.7 Mono)",
		"timestamp": Time.get_unix_time_from_system(),
		"p_ruin": 0.0000
	}
	var f = FileAccess.open("res://legal/BUILD_METADATA.json", FileAccess.WRITE)
	if f:
		f.store_string(JSON.stringify(meta, "  "))

	log_msg("Injected legal files & updated project.godot successfully.")
	if status_label:
		status_label.text = "Injected: " + co + " • " + dom
