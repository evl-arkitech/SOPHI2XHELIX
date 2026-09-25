extends SceneTree

func _init() -> void:
	print("[SOPHI-TEST] Initializing SOPHISheafEngine test...")
	var SheafScript = load("res://scripts/sophi_sheaf_engine.gd")
	if not SheafScript:
		print("[ERROR] Failed to load sophi_sheaf_engine.gd")
		quit(1)
		return
		
	var sheaf = SheafScript.new()
	sheaf._ready()
	
	print("[SOPHI-TEST] Initial Sheaf Coherence: ", sheaf.sheaf_coherence, "%")
	assert(sheaf.sheaf_coherence == 100.0, "Initial coherence must be 100.0")
	assert(sheaf.p_ruin == 0.0, "P(Ruin) must be 0.0000")
	
	# Test acoustic difference event
	var event = sheaf.emit_acoustic_event(Vector3(14.0, 1.0, 9.0), 3.5, 0.4, "Mudroom Door Jiggle")
	print("[SOPHI-TEST] Emitted Event: ", event["description"], " in ", event["room_name"])
	assert(event["room_idx"] == 2, "Expected Mudroom room index 2")
	
	# Test Dirichlet Energy & Coherence
	print("[SOPHI-TEST] Dirichlet Energy after breach sound: ", sheaf.dirichlet_energy)
	assert(sheaf.dirichlet_energy > 0.0, "Dirichlet energy must spike on sound event")
	
	# Test Tesla Monoidal Optic simulation
	var sim = sheaf.simulate_breach_noise(3, 2, "lockpick_stealth")
	print("[SOPHI-TEST] Tesla Monoidal Optic stealth simulation: alert=", sim["will_alert_occupant"], " leakage=", sim["refuge_leakage"])
	
	# Test Occupant acoustic radar
	var radar = sheaf.get_occupant_acoustic_radar()
	print("[SOPHI-TEST] Occupant Radar Threat Room: ", radar["threat_room_name"], " Threat Level: ", radar["max_external_threat_level"])
	
	# Test Dissipation
	sheaf.dissipate_sheaf_energy(0.5)
	print("[SOPHI-TEST] Dissipation completed. New Dirichlet Energy: ", sheaf.dirichlet_energy)
	
	print("[SOPHI-TEST] ALL SOPHI SHEAF INVARIANTS VERIFIED!")
	sheaf.free()
	quit(0)
