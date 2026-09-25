extends SceneTree

var frame_count: int = 0
var stage: int = 0
var active_scene_node: Node = null
var artifact_dir: String = "C:/Users/evlga/.gemini/antigravity-cli/brain/cea400a4-d001-4c98-8a59-03c56e952067"

func _init() -> void:
	print("[PROOF-CAPTURE] Starting enhanced in-engine gameplay frame capture...")
	var timer = Timer.new()
	timer.wait_time = 0.05
	timer.autostart = true
	timer.timeout.connect(_on_tick)
	root.add_child(timer)
	
	_load_menu()

func _load_menu() -> void:
	print("[PROOF-CAPTURE] Loading Main Menu...")
	var scn = load("res://scenes/main_menu.tscn").instantiate()
	root.add_child(scn)
	active_scene_node = scn
	stage = 1
	frame_count = 0

func _on_tick() -> void:
	frame_count += 1
	
	if stage == 1 and frame_count >= 8:
		# 1. Main Menu
		_capture("proof_main_menu.png")
		if active_scene_node: active_scene_node.queue_free()
		stage = 2
		frame_count = 0
		_load_occupant(false) # Flashlight OFF
		
	elif stage == 2 and frame_count >= 12:
		# 2. Occupant in Bedroom with Flashlight OFF (Natural Moonlight Silhouettes)
		_capture("proof_occupant_dark_silhouette.png")
		stage = 3
		frame_count = 0
		_turn_on_flashlight()
		
	elif stage == 3 and frame_count >= 8:
		# 3. Occupant with Flashlight ON (Volumetric Beam + Ambient Bounce)
		_capture("proof_occupant_flashlight_beam.png")
		if active_scene_node: active_scene_node.queue_free()
		stage = 4
		frame_count = 0
		_load_intruder()
		
	elif stage == 4 and frame_count >= 14:
		# 4. Intruder Exterior View (Porch Light, Rain, and Mudroom Approach)
		_capture("proof_intruder_exterior_approach.png")
		if active_scene_node: active_scene_node.queue_free()
		stage = 5
		frame_count = 0
		_load_cctv_focus()
		
	elif stage == 5 and frame_count >= 12:
		# 5. CCTV Surveillance Terminal
		_capture("proof_cctv_security_feed.png")
		if active_scene_node: active_scene_node.queue_free()
		stage = 6
		frame_count = 0
		_load_occupant_corridor()

	elif stage == 6 and frame_count >= 12:
		# 6. Looking through open doorway into corridor
		_capture("proof_occupant_doorway_corridor.png")
		print("[PROOF-CAPTURE] ALL ENHANCED IN-ENGINE GAMEPLAY SCREENSHOTS CAPTURED!")
		quit(0)

func _load_occupant_corridor() -> void:
	print("[PROOF-CAPTURE] Loading Occupant doorway & corridor view...")
	var state = root.get_node_or_null("GlobalGameState")
	if state: state.selected_role = "occupant"
	var scn = load("res://scenes/city_echoes_sophi.tscn").instantiate()
	root.add_child(scn)
	active_scene_node = scn

	# Open the bedroom door so we can see down the corridor
	var bed = active_scene_node.find_child("RefugeBedroom", true, false)
	if bed:
		var d = bed.find_child("HingedDoor", true, false)
		if d and d.has_method("open_door"):
			d.open_door()

	var player = active_scene_node.find_child("TacticalPlayer", true, false)
	if player:
		player.global_position = Vector3(0.0, 0.2, 1.5)
		player.rotation_degrees.y = 180.0
		player.is_flashlight_on = false
		if player.flashlight: player.flashlight.visible = false
		if player.flashlight_bounce: player.flashlight_bounce.visible = false

func _load_occupant(flashlight_enabled: bool) -> void:
	print("[PROOF-CAPTURE] Loading Occupant scenario (Flashlight=", flashlight_enabled, ")...")
	var state = root.get_node_or_null("GlobalGameState")
	if state: state.selected_role = "occupant"
	var scn = load("res://scenes/city_echoes_sophi.tscn").instantiate()
	root.add_child(scn)
	active_scene_node = scn
	
	var player = active_scene_node.find_child("TacticalPlayer", true, false)
	if player:
		# Stand near bedroom doorway looking across the bedroom at the bed, nightstand, and window
		player.global_position = Vector3(1.2, 0.2, 1.8)
		player.rotation_degrees.y = -50.0
		player.is_flashlight_on = flashlight_enabled
		if player.flashlight: player.flashlight.visible = flashlight_enabled
		if player.flashlight_bounce: player.flashlight_bounce.visible = flashlight_enabled

func _turn_on_flashlight() -> void:
	if active_scene_node:
		var player = active_scene_node.find_child("TacticalPlayer", true, false)
		if player:
			player.is_flashlight_on = true
			if player.flashlight: player.flashlight.visible = true
			if player.flashlight_bounce: player.flashlight_bounce.visible = true

func _load_intruder() -> void:
	print("[PROOF-CAPTURE] Loading Intruder exterior scenario...")
	var state = root.get_node_or_null("GlobalGameState")
	if state: state.selected_role = "intruder"
	var scn = load("res://scenes/city_echoes_sophi.tscn").instantiate()
	root.add_child(scn)
	active_scene_node = scn
	
	var player = active_scene_node.find_child("TacticalPlayer", true, false)
	if player:
		# Position intruder on the backyard lawn looking at the illuminated back porch and door
		player.global_position = Vector3(23.0, 0.4, 9.0)
		player.rotation_degrees.y = 90.0 # Face the house (-X)
		player.is_nvg_on = true
		if player.nvg_lens: player.nvg_lens.visible = true
		if player.nvg_illuminator: player.nvg_illuminator.visible = true

func _load_cctv_focus() -> void:
	print("[PROOF-CAPTURE] Focusing CCTV in-world monitor...")
	var state = root.get_node_or_null("GlobalGameState")
	if state: state.selected_role = "occupant"
	var scn = load("res://scenes/city_echoes_sophi.tscn").instantiate()
	root.add_child(scn)
	active_scene_node = scn
	
	var cam = Camera3D.new()
	cam.position = Vector3(6.5, 1.15, 5.8)
	cam.rotation_degrees = Vector3(-12, 0, 0)
	active_scene_node.add_child(cam)
	cam.current = true

func _capture(filename: String) -> void:
	var img = root.get_texture().get_image()
	if img and not img.is_empty():
		var out_path = artifact_dir + "/" + filename
		img.save_png(out_path)
		print("[PROOF-CAPTURE] Saved screenshot: ", out_path, " (", img.get_width(), "x", img.get_height(), ")")
	else:
		print("[PROOF-CAPTURE] Warning: viewport texture empty for ", filename)
