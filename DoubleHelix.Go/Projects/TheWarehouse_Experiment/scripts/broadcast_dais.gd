extends Node3D

# Broadcast Dais & Terminal Choice Coordinator (Act 3)
# Author: The Arkitech & Sophianat

@export var station1_path: NodePath # Succession
@export var station2_path: NodePath # Severance

var is_choice_made: bool = false

func _ready() -> void:
	var s1 = get_node_or_null(station1_path)
	if s1:
		s1.add_to_group("interactable")
		if not s1.has_method("interact"):
			s1.set_script(load("res://scripts/dais_station_choice.gd"))
			s1.choice_type = GlobalGameState.EndingChoice.SUCCESSION
			
	var s2 = get_node_or_null(station2_path)
	if s2:
		s2.add_to_group("interactable")
		if not s2.has_method("interact"):
			s2.set_script(load("res://scripts/dais_station_choice.gd"))
			s2.choice_type = GlobalGameState.EndingChoice.SEVERANCE

func execute_terminal_choice(choice: GlobalGameState.EndingChoice) -> void:
	if is_choice_made:
		return
	is_choice_made = true
	
	SoundManager.play_sub_bass_drop()
	
	if choice == GlobalGameState.EndingChoice.SUCCESSION:
		GlobalGameState.emit_signal("objective_updated", "SUCCESSION ACCEPTED: You grasp the microphone. The Frequency lives.")
	else:
		GlobalGameState.emit_signal("objective_updated", "SEVERANCE EXECUTED: Transformers overload. The Frequency is shattered.")
		
	await get_tree().create_timer(3.0).timeout
	GlobalGameState.trigger_ending(choice)
