extends Node

# Mission Director: Master Narrative and Act Progression Coordinator
# Manages objectives, trigger zones, PA broadcasts, and transitions.
# Author: The Arkitech & Sophianat

@export var player_path: NodePath
@export var security_gate_path: NodePath
@export var mannequin_a_path: NodePath

var player: Node3D = null
var security_gate: Node3D = null
var mannequin_a: Node3D = null

var intro_timer: float = 0.0
var act1_initialized: bool = false
var corner_passed: bool = false

func _ready() -> void:
	await get_tree().process_frame
	if player_path:
		player = get_node_or_null(player_path)
	if security_gate_path:
		security_gate = get_node_or_null(security_gate_path)
	if mannequin_a_path:
		mannequin_a = get_node_or_null(mannequin_a_path)
		
	start_act1_sequence()

func start_act1_sequence() -> void:
	GlobalGameState.set_act(GlobalGameState.StoryAct.ACT1_COLD_CONCRETE)
	GlobalGameState.emit_signal("objective_updated", "Wake up on the cold concrete. Follow the yellow transit line down Aisle 4.")
	
	# Initial PA system broadcast after 4 seconds
	await get_tree().create_timer(4.5).timeout
	trigger_pa_broadcast(
		"The Broadcaster",
		"Breathe in, darling. That's stale Freon and ozone you taste. Follow the yellow line. Sub-Station B needs your hands.",
		7.5
	)

func _process(delta: float) -> void:
	if player == null:
		player = get_tree().get_first_node_in_group("player")
		if player == null:
			return

	var p_pos = player.global_position

	# Act 1 Trigger: Player passes Aisle 4 corner (Z > 12.0)
	if GlobalGameState.current_act == GlobalGameState.StoryAct.ACT1_COLD_CONCRETE:
		if not corner_passed and p_pos.z > 12.0:
			corner_passed = true
			GlobalGameState.has_passed_mannequin_a = true
			GlobalGameState.emit_signal("objective_updated", "Look back toward the aisle origin. Something has shifted.")
			
			await get_tree().create_timer(2.5).timeout
			trigger_pa_broadcast(
				"The Broadcaster",
				"Ah, ah. Don't stare, darling. It's impolite to gawk at the help. Keep moving. Left at the forklift, then punch 0-4-1-9 into the gate.",
				8.5
			)

	# Act 2 Transition Check: If security gate unlocked and player passes into routing floor
	if GlobalGameState.current_act == GlobalGameState.StoryAct.ACT1_COLD_CONCRETE and GlobalGameState.security_gate_unlocked:
		if p_pos.z > 22.0:
			GlobalGameState.set_act(GlobalGameState.StoryAct.ACT2_ROUTING_FLOOR)
			GlobalGameState.emit_signal("objective_updated", "Routing Floor entered. Locate and turn 3 Hydraulic Bypass Valves (0/3). Keep watch behind you.")
			trigger_pa_broadcast(
				"The Broadcaster",
				"Do you know what they're made of? The core isn't plaster. It's bone meal and resin. Pressed together under two thousand pounds of steam. They hold memories better that way.",
				8.5
			)

	# Act 3 Transition Check: If airlock opened and player reaches broadcast hub
	if GlobalGameState.current_act == GlobalGameState.StoryAct.ACT2_ROUTING_FLOOR and GlobalGameState.airlock_completed:
		if p_pos.z > 50.0:
			GlobalGameState.set_act(GlobalGameState.StoryAct.ACT3_BROADCAST_HUB)
			GlobalGameState.emit_signal("objective_updated", "Central Broadcast Hub reached. Approach the Dais. Make the Terminal Choice.")
			trigger_pa_broadcast(
				"The Broadcaster",
				"Here we are at last. The Frequency needs a keeper. Station 1: The Bone-Saw to accept the succession. Or Station 2: The Overload Lever to sever the signal forever.",
				9.5
			)

func trigger_pa_broadcast(speaker: String, text: String, duration: float) -> void:
	SoundManager.play_pa_chime()
	GlobalGameState.emit_signal("pa_broadcast_received", speaker, text, duration)

func on_substation_breaker_activated() -> void:
	GlobalGameState.substation_power_restored = true
	GlobalGameState.emit_signal("objective_updated", "Sub-Station B power restored. Keypad energized. Enter code 0-4-1-9 at Security Gate.")
	trigger_pa_broadcast(
		"The Broadcaster",
		"Power online, sweetheart. Left at the forklift, then punch 0-4-1-9 into the gate.",
		6.5
	)

func on_gate_unlocked() -> void:
	GlobalGameState.security_gate_unlocked = true
	GlobalGameState.emit_signal("objective_updated", "Security Transit Gate rolling open. Proceed into the Routing Floor.")
	if security_gate:
		# Animate gate opening upward
		var tween = create_tween()
		tween.tween_property(security_gate, "position:y", security_gate.position.y + 4.5, 2.5)

func on_airlock_completed() -> void:
	GlobalGameState.airlock_completed = true
	GlobalGameState.emit_signal("objective_updated", "Airlock seal broken. Proceed down the central tunnel to the Broadcast Hub.")
