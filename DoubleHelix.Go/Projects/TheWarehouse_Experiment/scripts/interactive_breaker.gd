extends StaticBody3D

# Interactive Sub-Station B Breaker Switch
# Author: The Arkitech & Sophianat

@export var prompt_text: String = "[E] Throw Main Breaker Switch"
var is_activated: bool = false

func interact(player: Node) -> void:
	if is_activated:
		return
	is_activated = true
	prompt_text = "Sub-Station B (ONLINE)"
	
	# Play electrical spark/hum SFX
	SoundManager.play_sub_bass_drop()
	
	# Notify mission director
	var director = get_tree().get_first_node_in_group("mission_director")
	if director and director.has_method("on_substation_breaker_activated"):
		director.on_substation_breaker_activated()
		
	# Switch indicator light from red to green
	var light = get_node_or_null("OmniLight3D")
	if light:
		light.light_color = Color(0.1, 0.9, 0.2)
