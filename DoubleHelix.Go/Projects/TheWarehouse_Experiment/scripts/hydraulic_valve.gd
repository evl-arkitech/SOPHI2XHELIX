extends StaticBody3D

# Hydraulic Bypass Valve (Act 2 Puzzle Component)
# Author: The Arkitech & Sophianat

@export var valve_index: int = 1
var is_turned: bool = false

@onready var wheel_mesh: Node3D = $WheelMesh

func _ready() -> void:
	add_to_group("interactable")

func interact(player: Node) -> void:
	if is_turned:
		return
	is_turned = true
	
	# Animate wheel turn
	if wheel_mesh:
		var tween = create_tween()
		tween.tween_property(wheel_mesh, "rotation_degrees:z", wheel_mesh.rotation_degrees.z + 720.0, 1.2)
		
	SoundManager.play_scrape_cue()
	var turned_count = GlobalGameState.turn_hydraulic_valve()
	
	# Play steam hiss / pressure drop
	SoundManager.play_sub_bass_drop()
