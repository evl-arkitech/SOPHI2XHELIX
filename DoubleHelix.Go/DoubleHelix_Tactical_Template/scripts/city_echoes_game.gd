# @tool
class_name CityEchoesGame
extends Node3D

## Master Game Coordinator for City Echoes: SOPHI Edition
## Pure Diegetic Real-Life Simulation • Grothendieck Cellular Sheaf Acoustic Physics
## Dual-Role Execution: Defender (Occupant) vs Infiltrator (Intruder)

@export var player_scene: PackedScene = preload("res://scenes/tactical_player.tscn")
@export var ai_scene: PackedScene = preload("res://scenes/tactical_ai_opponent.tscn")

var sheaf_engine: SOPHISheafEngine = null
var active_player: TacticalPlayer = null
var active_ai: TacticalAIOpponent = null

@onready var residence: Node3D = $TacticalResidence
@onready var cctv_monitor: Node3D = $CCTVMonitorTerminal

func _ready() -> void:
	# Ensure Sheaf engine is active
	sheaf_engine = $SOPHISheafEngine
	
	# Determine selected role from global state
	var selected_role = "occupant"
	var state_node = get_node_or_null("/root/GlobalGameState")
	if state_node and "selected_role" in state_node:
		selected_role = state_node.selected_role
		
	_setup_tactical_scenario(selected_role)
	_wire_interactive_doors()

func _setup_tactical_scenario(player_role: String) -> void:
	var occupant_spawn = Vector3(0.0, 0.2, 0.0)
	var intruder_spawn = Vector3(18.0, 0.2, 9.0)
	
	var occ_marker = residence.find_child("OccupantDefenderSpawn", true, false)
	if occ_marker:
		occupant_spawn = occ_marker.global_position
		
	var int_marker = residence.find_child("IntruderInfiltratorSpawn", true, false)
	if int_marker:
		intruder_spawn = int_marker.global_position
		
	# Instantiate Player
	if player_scene:
		active_player = player_scene.instantiate() as TacticalPlayer
		add_child(active_player)
		
		if player_role == "occupant":
			active_player.global_position = occupant_spawn
			active_player.setup_role("occupant")
		else:
			active_player.global_position = intruder_spawn
			active_player.setup_role("intruder")
			
	# Instantiate Autonomous Opponent
	if ai_scene:
		active_ai = ai_scene.instantiate() as TacticalAIOpponent
		add_child(active_ai)
		
		if player_role == "occupant":
			# AI plays the Intruder infiltrating the rear mudroom
			active_ai.global_position = intruder_spawn
			active_ai.role = "intruder"
			active_ai.patrol_points = [
				Vector3(14.0, 0.2, 9.0), # Mudroom door
				Vector3(7.0, 0.2, 4.0),  # Corridor
				Vector3(0.0, 0.2, 0.0)   # Refuge Bedroom
			]
		else:
			# AI plays the Occupant guarding the bedroom
			active_ai.global_position = occupant_spawn
			active_ai.role = "occupant"
			active_ai.patrol_points = [
				Vector3(0.0, 0.2, 0.0),  # Bedroom
				Vector3(4.0, 0.2, 2.0),  # Bedroom threshold
				Vector3(7.0, 0.2, 4.0)   # Corridor patrol
			]

func _wire_interactive_doors() -> void:
	if not residence:
		return
		
	# Wire bedroom door
	var bed_door = residence.find_child("RefugeBedroom", true, false)
	if bed_door:
		var d = bed_door.find_child("HingedDoor", true, false)
		if d and not d.has_method("interact"):
			d.set_script(preload("res://scripts/tactical_door.gd"))
			d.edge_id = "door_bedroom"
			
	# Wire corridor door
	var corr = residence.find_child("LivingCorridor", true, false)
	if corr:
		var d = corr.find_child("HingedDoor", true, false)
		if d and not d.has_method("interact"):
			d.set_script(preload("res://scripts/tactical_door.gd"))
			d.edge_id = "door_mudroom"
			
	# Wire mudroom rear exit door
	var mud = residence.find_child("MudroomRearExit", true, false)
	if mud:
		var d = mud.find_child("HingedDoor", true, false)
		if d and not d.has_method("interact"):
			d.set_script(preload("res://scripts/tactical_door.gd"))
			d.edge_id = "door_rear_exit"
			d.is_locked = true # Intruder must pick lock or kick
