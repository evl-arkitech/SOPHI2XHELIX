extends Control

# Start Screen & Main Menu
# Author: The Arkitech & Sophianat

@onready var start_btn: Button = $VBoxContainer/StartButton
@onready var audio_btn: Button = $VBoxContainer/AudioTestButton
@onready var quit_btn: Button = $VBoxContainer/QuitButton
var video_player: VideoStreamPlayer = null

func _ready() -> void:
	Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)
	start_btn.pressed.connect(_on_start_pressed)
	audio_btn.pressed.connect(_on_audio_test_pressed)
	quit_btn.pressed.connect(_on_quit_pressed)
	video_player = get_node_or_null("VideoStreamPlayer")
	
	if video_player:
		# If video file exists, play looped
		video_player.play()
		
	SoundManager.start_ambient_hum()

func _on_start_pressed() -> void:
	GlobalGameState.reset_state()
	SoundManager.play_sub_bass_drop()
	get_tree().change_scene_to_file("res://scenes/warehouse_world.tscn")

func _on_audio_test_pressed() -> void:
	SoundManager.play_pa_chime()
	SoundManager.play_scrape_cue()

func _on_quit_pressed() -> void:
	get_tree().quit()
