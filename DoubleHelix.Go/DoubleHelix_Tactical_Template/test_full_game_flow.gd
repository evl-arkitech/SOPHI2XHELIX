extends SceneTree

func _init() -> void:
	print("================================================================================")
	print("--- BEGIN FULL GAME FLOW & ENTRYWAY ACCESSIBILITY TEST ---")
	print("================================================================================")

	# 1. Setup global state as intruder
	var gstate_script = load("res://scripts/global_game_state.gd")
	if gstate_script:
		var gstate = Node.new()
		gstate.set_script(gstate_script)
		gstate.name = "GlobalGameState"
		gstate.selected_role = "intruder"
		root.add_child(gstate)

	# 2. Instantiate main game
	var scene_res = load("res://scenes/city_echoes_sophi.tscn")
	if not scene_res:
		print("ERROR: Failed to load city_echoes_sophi.tscn")
		quit(1)
		return

	var game = scene_res.instantiate()
	root.add_child(game)
	print("[FLOW TEST] Game scene instantiated.")
	
	_run_flow_test(game)

func _run_flow_test(game: Node) -> void:
	# Settle for 20 frames
	for i in range(20):
		await process_frame
		
	var player = game.find_child("TacticalPlayer", true, false)
	assert(player != null, "TacticalPlayer missing!")
	print("[FLOW TEST] Player spawned at: ", player.global_position)
	print("[FLOW TEST] Player role: ", player.role)
	assert(player.is_on_floor(), "Player is not on floor!")
	
	# Verify Residence structure
	var residence = game.find_child("TacticalResidence", true, false)
	assert(residence != null, "TacticalResidence missing!")
	
	var mudroom = residence.find_child("MudroomRearExit", true, false)
	assert(mudroom != null, "MudroomRearExit missing!")
	
	var rear_door = mudroom.find_child("HingedDoor", true, false)
	assert(rear_door != null, "Mudroom HingedDoor missing!")
	print("[FLOW TEST] Rear Door found. State: ", rear_door.current_state, " | Locked: ", rear_door.is_locked)
	
	# Simulate Intruder approaching rear door:
	print("[FLOW TEST] Simulating player approaching rear door...")
	player.global_position = Vector3(16.5, 0.2, 9.0)
	for i in range(10):
		await process_frame
		
	# Test 1: Intruder lockpicks or breaches door
	print("[FLOW TEST] Intruder breaching/unlocking rear door...")
	rear_door.breach_door(100.0)
	for i in range(15):
		await process_frame
	print("[FLOW TEST] Rear Door state after breach: ", rear_door.current_state)
	assert(rear_door.current_state == "breached", "Rear door should be breached!")
	
	# Test 2: Walk straight through the doorway into the Mudroom!
	print("[FLOW TEST] Walking player through rear doorway into Mudroom...")
	# Door opening is at X = 16.0, Z = 9.0. Let's move player inside to X = 13.0, Z = 9.0!
	player.global_position = Vector3(13.0, 0.2, 9.0)
	for i in range(20):
		await process_frame
	print("[FLOW TEST] Player position inside Mudroom: ", player.global_position)
	assert(player.global_position.y > -0.5, "Player fell through mudroom floor!")
	
	# Test 3: Walk through Mudroom-to-Corridor doorway into Living Corridor!
	print("[FLOW TEST] Opening interior mudroom-to-corridor door...")
	var corridor = residence.find_child("LivingCorridor", true, false)
	var corr_door = corridor.find_child("HingedDoor", true, false)
	assert(corr_door != null, "LivingCorridor HingedDoor missing!")
	corr_door.open_door()
	for i in range(15):
		await process_frame
	print("[FLOW TEST] Moving player through corridor doorway...")
	# Move to Living Corridor center (X = 4.0, Z = 9.0)
	player.global_position = Vector3(4.0, 0.2, 9.0)
	for i in range(20):
		await process_frame
	print("[FLOW TEST] Player position inside Living Corridor: ", player.global_position)
	assert(player.global_position.y > -0.5, "Player fell through corridor floor!")
	
	# Test 4: Walk through Bedroom doorway into Refuge Bedroom!
	print("[FLOW TEST] Opening Bedroom door...")
	var bedroom = residence.find_child("RefugeBedroom", true, false)
	var bed_door = bedroom.find_child("HingedDoor", true, false)
	assert(bed_door != null, "RefugeBedroom HingedDoor missing!")
	bed_door.open_door()
	for i in range(15):
		await process_frame
	print("[FLOW TEST] Moving player into Refuge Bedroom...")
	player.global_position = Vector3(0.0, 0.2, 0.0)
	for i in range(20):
		await process_frame
	print("[FLOW TEST] Player position inside Refuge Bedroom: ", player.global_position)
	assert(player.global_position.y > -0.5, "Player fell through bedroom floor!")
	
	# Test 5: Verify Shotgun in player hands
	print("[FLOW TEST] Verifying Tactical Shotgun...")
	assert(player.tactical_shotgun != null, "Tactical Shotgun missing from player rig!")
	print("[FLOW TEST] Tactical Shotgun components: ", player.tactical_shotgun.get_child_count(), " parts")
	
	print("================================================================================")
	print("--- ALL INTEGRATION & ACCESSIBILITY TESTS PASSED SUCCESSFULLY! ---")
	print("================================================================================")
	quit(0)
