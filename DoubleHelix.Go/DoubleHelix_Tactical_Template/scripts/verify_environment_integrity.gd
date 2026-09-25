extends SceneTree

func _init() -> void:
	print("[VERIFY] Starting Double Helix Environment Architecture Integrity Audit...")
	
	# 1. Test suburban_dollhouse_residence.tscn
	var dollhouse_scene = load("res://scenes/suburban_dollhouse_residence.tscn")
	if not dollhouse_scene:
		printerr("[FAIL] Could not load res://scenes/suburban_dollhouse_residence.tscn")
		quit(1)
		return
	var dollhouse_instance = dollhouse_scene.instantiate()
	root.add_child(dollhouse_instance)
	print("[PASS] Suburban Dollhouse Scene instantiated successfully.")
	
	# Verify Hero Prop: Grand Piano in Dollhouse
	var piano = dollhouse_instance.find_child("GrandPiano", true, false)
	if piano:
		print("[PASS] Grand Piano Hero Prop detected in Suburban Dollhouse.")
	else:
		printerr("[FAIL] Grand Piano not found in Suburban Dollhouse!")
		quit(1)
		return
		
	# Verify Sofa Suite in Dollhouse
	var sofa = dollhouse_instance.find_child("LivingRoomSuite", true, false)
	if sofa:
		print("[PASS] Craftsman Living Room Sofa Suite detected in Suburban Dollhouse.")
	else:
		printerr("[FAIL] Living Room Suite not found in Suburban Dollhouse!")
		quit(1)
		return
		
	# Verify Staircase in Dollhouse
	var stairs = dollhouse_instance.find_child("CraftsmanStaircase", true, false)
	if stairs:
		print("[PASS] Craftsman Two-Tone Staircase detected in Suburban Dollhouse.")
	else:
		printerr("[FAIL] Craftsman Staircase not found in Suburban Dollhouse!")
		quit(1)
		return

	dollhouse_instance.queue_free()

	# 2. Test city_echoes_sophi.tscn (Tactical Simulation)
	var game_scene = load("res://scenes/city_echoes_sophi.tscn")
	if not game_scene:
		printerr("[FAIL] Could not load res://scenes/city_echoes_sophi.tscn")
		quit(1)
		return
	var game_instance = game_scene.instantiate()
	root.add_child(game_instance)
	print("[PASS] City Echoes Tactical Simulation Scene instantiated successfully.")
	
	# Check Tactical Residence
	var res = game_instance.find_child("TacticalResidence", true, false)
	if not res:
		printerr("[FAIL] TacticalResidence node missing in City Echoes!")
		quit(1)
		return
	print("[PASS] Tactical Residence node verified.")
	
	# Verify Grand Piano in Tactical Residence
	var tac_piano = res.find_child("GrandPiano", true, false)
	if tac_piano:
		print("[PASS] Grand Piano verified in Tactical Residence.")
	else:
		printerr("[FAIL] Grand Piano missing in Tactical Residence!")
		quit(1)
		return
		
	# Verify Spawns
	var occ_spawn = res.find_child("OccupantDefenderSpawn", true, false)
	var int_spawn = res.find_child("IntruderInfiltratorSpawn", true, false)
	if occ_spawn and int_spawn:
		print("[PASS] Spawn points verified: Occupant at ", occ_spawn.position, ", Intruder at ", int_spawn.position)
	else:
		printerr("[FAIL] Spawn points missing!")
		quit(1)
		return

	game_instance.queue_free()
	
	print("===============================================================================")
	print("[ALL CHECKS PASSED] Environment modeling complete & mathematically compliant!")
	print("===============================================================================")
	quit(0)
