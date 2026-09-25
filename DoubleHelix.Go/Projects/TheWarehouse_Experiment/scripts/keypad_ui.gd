extends StaticBody3D

# Keypad Controller for Security Transit Gate
# Target Code: 0-4-1-9
# Author: The Arkitech & Sophianat

@export var required_code: String = "0419"
var entered_code: String = ""
var is_unlocked: bool = false

@onready var status_light: OmniLight3D = $StatusLight

func _ready() -> void:
	add_to_group("interactable")

func interact(player: Node) -> void:
	if is_unlocked:
		return
		
	if not GlobalGameState.substation_power_restored:
		GlobalGameState.emit_signal("objective_updated", "Keypad is unpowered. Restore Sub-Station B breakers first!")
		SoundManager.play_scrape_cue()
		return
		
	# Automatically punch in code 0-4-1-9 when player interacts after power restoration
	unlock_gate()

func unlock_gate() -> void:
	if is_unlocked:
		return
	is_unlocked = true
	if status_light:
		status_light.light_color = Color(0.1, 1.0, 0.2) # Green
		
	SoundManager.play_pa_chime()
	
	var director = get_tree().get_first_node_in_group("mission_director")
	if director and director.has_method("on_gate_unlocked"):
		director.on_gate_unlocked()
