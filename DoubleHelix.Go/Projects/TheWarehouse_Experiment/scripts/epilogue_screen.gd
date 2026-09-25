extends Control

# Epilogue & Psychological Assessment Dossier
# Author: The Arkitech & Sophianat

@onready var title_label: Label = $VBoxContainer/TitleLabel
@onready var outcome_label: Label = $VBoxContainer/OutcomeLabel
@onready var metrics_label: Label = $VBoxContainer/MetricsLabel
@onready var restart_btn: Button = $VBoxContainer/RestartButton
@onready var quit_btn: Button = $VBoxContainer/QuitButton

func _ready() -> void:
	Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)
	restart_btn.pressed.connect(_on_restart_pressed)
	quit_btn.pressed.connect(_on_quit_pressed)
	
	_render_dossier()

func _render_dossier() -> void:
	if GlobalGameState.chosen_ending == GlobalGameState.EndingChoice.SUCCESSION:
		title_label.text = "TERMINAL OUTCOME: THE SUCCESSION"
		outcome_label.text = "You accepted the broadcaster microphone.\nThe Pale Frequency hums anew through your vocal cords.\nThe mannequins bow in silent reverence.\nYou are the keeper of the loop."
	else:
		title_label.text = "TERMINAL OUTCOME: THE SEVERANCE"
		outcome_label.text = "You threw the transformer overload lever.\nArc flashes incinerate the bone-meal resin skeletons.\nThe overhead horns crackle, pop, and fall silent.\nThe warehouse collapses into quiet, peaceful dark."
		
	var minutes = int(GlobalGameState.time_elapsed / 60.0)
	var seconds = int(fmod(GlobalGameState.time_elapsed, 60.0))
	
	metrics_label.text = """
	[PSYCHOLOGICAL PROFILE & TELEMETRY AUDIT]
	--------------------------------------------------
	Time in Facility: %02d:%02d
	Stalker Contact Encounters: %d
	180-Degree Look Backs: %d
	Flashlight Battery Expended: %.1f%%
	Calculated Fear Index: %.2f / 1.00
	DoubleHelix Parity Gate: PASSED (Zero-Alloc Invariant)
	--------------------------------------------------
	""" % [
		minutes, seconds,
		GlobalGameState.stalker_encounters,
		GlobalGameState.look_backs_performed,
		GlobalGameState.battery_drain_total,
		GlobalGameState.fear_coefficient
	]

func _on_restart_pressed() -> void:
	GlobalGameState.reset_state()
	get_tree().change_scene_to_file("res://scenes/main_menu.tscn")

func _on_quit_pressed() -> void:
	get_tree().quit()
