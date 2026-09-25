extends Node

# Global Game State Singleton for The Warehouse: The Pale Frequency
# Author: The Arkitech & Sophianat

enum StoryAct {
	ACT1_COLD_CONCRETE,
	ACT2_ROUTING_FLOOR,
	ACT3_BROADCAST_HUB,
	EPILOGUE
}

enum EndingChoice {
	NONE,
	SUCCESSION, # Choice A: Take up the microphone / bone-saw mantle
	SEVERANCE   # Choice B: Throw the transformer overload lever
}

var current_act: StoryAct = StoryAct.ACT1_COLD_CONCRETE
var chosen_ending: EndingChoice = EndingChoice.NONE

# Story Milestones
var has_woken_up: bool = false
var has_passed_mannequin_a: bool = false
var has_looked_back_at_a: bool = false
var substation_power_restored: bool = false
var security_gate_unlocked: bool = false
var hydraulic_valves_turned: int = 0
const TOTAL_HYDRAULIC_VALVES: int = 3
var airlock_wheel_progress: float = 0.0
var airlock_completed: bool = false

# Player Telemetry & Psychological Profile
var time_elapsed: float = 0.0
var stalker_encounters: int = 0
var battery_drain_total: float = 0.0
var look_backs_performed: int = 0
var fear_coefficient: float = 0.0 # 0.0 to 1.0 based on heart rate / close encounters
var player_flashlight_on: bool = true
var player_battery: float = 100.0

signal act_changed(new_act: StoryAct)
signal objective_updated(objective_text: String)
signal pa_broadcast_received(speaker_name: String, text: String, duration: float)
signal game_ended(ending: EndingChoice)

func _process(delta: float) -> void:
	if current_act != StoryAct.EPILOGUE:
		time_elapsed += delta

func set_act(new_act: StoryAct) -> void:
	current_act = new_act
	emit_signal("act_changed", new_act)

func turn_hydraulic_valve() -> int:
	hydraulic_valves_turned += 1
	if hydraulic_valves_turned >= TOTAL_HYDRAULIC_VALVES:
		emit_signal("objective_updated", "All 3 Hydraulic Bypass Valves engaged. Proceed to Staging Airlock Wheel.")
	else:
		emit_signal("objective_updated", "Hydraulic Valves turned: %d/%d" % [hydraulic_valves_turned, TOTAL_HYDRAULIC_VALVES])
	return hydraulic_valves_turned

func trigger_ending(choice: EndingChoice) -> void:
	chosen_ending = choice
	current_act = StoryAct.EPILOGUE
	emit_signal("game_ended", choice)
	get_tree().change_scene_to_file("res://scenes/epilogue_screen.tscn")

func reset_state() -> void:
	current_act = StoryAct.ACT1_COLD_CONCRETE
	chosen_ending = EndingChoice.NONE
	has_woken_up = false
	has_passed_mannequin_a = false
	has_looked_back_at_a = false
	substation_power_restored = false
	security_gate_unlocked = false
	hydraulic_valves_turned = 0
	airlock_wheel_progress = 0.0
	airlock_completed = false
	time_elapsed = 0.0
	stalker_encounters = 0
	battery_drain_total = 0.0
	look_backs_performed = 0
	fear_coefficient = 0.0
	player_flashlight_on = true
	player_battery = 100.0
