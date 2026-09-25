extends SceneTree

func _init() -> void:
	print("[GAME-VERIFY] Checking City Echoes SOPHI edition scenes...")
	
	# 1. Verify Main Menu Scene
	var menu_scene = load("res://scenes/main_menu.tscn")
	if not menu_scene:
		print("[ERROR] Failed to load main_menu.tscn")
		quit(1)
		return
	var menu = menu_scene.instantiate()
	print("[GAME-VERIFY] Main Menu Scene loaded successfully: ", menu.name)
	menu.free()
	
	# 2. Verify Master Tactical Level Scene
	var game_scene = load("res://scenes/city_echoes_sophi.tscn")
	if not game_scene:
		print("[ERROR] Failed to load city_echoes_sophi.tscn")
		quit(1)
		return
	var game = game_scene.instantiate()
	print("[GAME-VERIFY] City Echoes SOPHI Master Scene loaded successfully: ", game.name)
	
	# 3. Check SOPHI Sheaf Engine presence
	var sheaf = game.get_node_or_null("SOPHISheafEngine")
	assert(sheaf != null, "SOPHISheafEngine must be child of CityEchoesGame")
	print("[GAME-VERIFY] SOPHISheafEngine node found in game hierarchy")
	
	# 4. Check Residence and CCTV
	var res = game.get_node_or_null("TacticalResidence")
	assert(res != null, "TacticalResidence must be child of CityEchoesGame")
	var cctv = game.get_node_or_null("CCTVMonitorTerminal")
	assert(cctv != null, "CCTVMonitorTerminal must be child of CityEchoesGame")
	print("[GAME-VERIFY] Physical CCTV Monitor terminal verified at: ", cctv.position)
	
	# 5. Verify Player scene
	var player_scene = load("res://scenes/tactical_player.tscn")
	assert(player_scene != null, "TacticalPlayer scene must exist")
	var player = player_scene.instantiate()
	print("[GAME-VERIFY] TacticalPlayer (The Vessel) instantiated with role: ", player.role)
	player.free()
	
	# 6. Verify AI Opponent scene
	var ai_scene = load("res://scenes/tactical_ai_opponent.tscn")
	assert(ai_scene != null, "TacticalAIOpponent scene must exist")
	var ai = ai_scene.instantiate()
	print("[GAME-VERIFY] TacticalAIOpponent instantiated with role: ", ai.role)
	ai.free()
	
	game.free()
	print("[GAME-VERIFY] ALL CITY ECHOES SOPHI GAME COMPONENTS VERIFIED CLEANLY!")
	quit(0)
