# @tool
extends Control

## Cinematic Start Screen for City Echoes (SOPHI Edition)
## Unobtrusive, filmic design featuring living art, ambient rain, and direct role launch.

@onready var background_art: TextureRect = $BackgroundArt
@onready var occupant_btn: Button = $UILayout/ButtonContainer/OccupantButton
@onready var intruder_btn: Button = $UILayout/ButtonContainer/IntruderButton
@onready var quit_btn: Button = $UILayout/ButtonContainer/QuitButton
@onready var storage_status: Label = $UILayout/StorageStatus
@onready var audio_ambience: AudioStreamPlayer = $MenuAudio

var zoom_dir: float = 1.0

func _ready() -> void:
	if occupant_btn:
		occupant_btn.pressed.connect(func(): _launch_game("occupant"))
	if intruder_btn:
		intruder_btn.pressed.connect(func(): _launch_game("intruder"))
	if quit_btn:
		quit_btn.pressed.connect(func(): get_tree().quit())
		
	if storage_status:
		var container = "https://arkade.new-world-arkitech.dev/assets"
		var loader = get_node_or_null("/root/DoubleHelixLoader")
		if loader and loader.storage_container_url:
			container = loader.storage_container_url
		storage_status.text = "⚡ ARKADE PIPELINE: " + container + " [ACTIVE]"
		
	# Play rain ambience
	if ResourceLoader.exists("res://assets/audio/rain_roof_occluded.wav"):
		var stream = load("res://assets/audio/rain_roof_occluded.wav")
		if stream and audio_ambience:
			audio_ambience.stream = stream
			audio_ambience.volume_db = -12.0
			audio_ambience.play()

func _process(delta: float) -> void:
	# Subtle living Ken-Burns cinematic drift on key art
	if background_art:
		background_art.scale += Vector2(0.003, 0.003) * zoom_dir * delta
		if background_art.scale.x > 1.08:
			zoom_dir = -1.0
		elif background_art.scale.x < 1.0:
			zoom_dir = 1.0

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed:
		if event.keycode == KEY_1:
			_launch_game("occupant")
		elif event.keycode == KEY_2:
			_launch_game("intruder")
		elif event.keycode == KEY_ESCAPE:
			get_tree().quit()

func _launch_game(role: String) -> void:
	var state = get_node_or_null("/root/GlobalGameState")
	if state and "selected_role" in state:
		state.selected_role = role
	get_tree().change_scene_to_file("res://scenes/city_echoes_sophi.tscn")

