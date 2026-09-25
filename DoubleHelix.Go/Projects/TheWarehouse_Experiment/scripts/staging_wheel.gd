extends StaticBody3D

# Staging Airlock Wheel Puzzle
# Requires turning heavy steel wheel while holding [E].
# Author: The Arkitech & Sophianat

@export var turn_duration: float = 4.0
var current_turn_time: float = 0.0
var is_turning: bool = false
var is_completed: bool = false

@onready var wheel_mesh: Node3D = $WheelMesh
@onready var door_mesh: Node3D = $AirlockDoor

func _ready() -> void:
	add_to_group("interactable")

func interact(player: Node) -> void:
	if is_completed:
		return
		
	if GlobalGameState.hydraulic_valves_turned < GlobalGameState.TOTAL_HYDRAULIC_VALVES:
		GlobalGameState.emit_signal("objective_updated", "Airlock hydraulic pressure locked! Turn all 3 bypass valves first (%d/3)." % GlobalGameState.hydraulic_valves_turned)
		SoundManager.play_scrape_cue()
		return
		
	is_turning = true

func _process(delta: float) -> void:
	if is_completed:
		return
		
	if is_turning:
		if Input.is_action_pressed("interact"):
			current_turn_time += delta
			var progress = clamp(current_turn_time / turn_duration, 0.0, 1.0)
			GlobalGameState.airlock_wheel_progress = progress * 100.0
			GlobalGameState.emit_signal("objective_updated", "Opening Airlock: %d%% (Watch your back!)" % int(progress * 100.0))
			
			if wheel_mesh:
				wheel_mesh.rotate_z(delta * 4.0)
				
			if progress >= 1.0:
				_complete_airlock()
		else:
			is_turning = false
			GlobalGameState.emit_signal("objective_updated", "Hold [E] to turn airlock wheel.")

func _complete_airlock() -> void:
	is_completed = true
	is_turning = false
	GlobalGameState.airlock_completed = true
	
	SoundManager.play_sub_bass_drop()
	SoundManager.play_pa_chime()
	
	if door_mesh:
		var tween = create_tween()
		tween.tween_property(door_mesh, "position:y", door_mesh.position.y + 4.0, 2.0)
		
	var director = get_tree().get_first_node_in_group("mission_director")
	if director and director.has_method("on_airlock_completed"):
		director.on_airlock_completed()
