extends CanvasLayer

# Diegetic HUD for The Warehouse: The Pale Frequency
# Author: The Arkitech & Sophianat

@onready var objective_label: Label = $ObjectivePanel/ObjectiveLabel
@onready var pa_panel: Panel = $PAPanel
@onready var pa_speaker: Label = $PAPanel/SpeakerLabel
@onready var pa_text: Label = $PAPanel/MessageLabel
@onready var prompt_label: Label = $CenterContainer/PromptLabel
@onready var battery_bar: ProgressBar = $StatusPanel/BatteryBar
@onready var act_label: Label = $StatusPanel/ActLabel
@onready var reticle: ColorRect = $CenterContainer/Reticle

var pa_timer: float = 0.0

func _ready() -> void:
	GlobalGameState.connect("objective_updated", Callable(self, "_on_objective_updated"))
	GlobalGameState.connect("pa_broadcast_received", Callable(self, "_on_pa_broadcast"))
	GlobalGameState.connect("act_changed", Callable(self, "_on_act_changed"))
	
	if pa_panel:
		pa_panel.visible = false

func _process(delta: float) -> void:
	# Update Battery
	if battery_bar:
		battery_bar.value = GlobalGameState.player_battery
		
	# Update PA timer
	if pa_timer > 0.0:
		pa_timer -= delta
		if pa_timer <= 0.0 and pa_panel:
			pa_panel.visible = false
			
	# Update interaction prompt from player raycast
	var player = get_tree().get_first_node_in_group("player")
	if player and player.get("current_interactable") != null:
		var target = player.current_interactable
		if target.get("prompt_text") != null:
			prompt_label.text = target.prompt_text
		else:
			prompt_label.text = "[E] Interact"
		prompt_label.visible = true
	else:
		prompt_label.visible = false

func _on_objective_updated(text: String) -> void:
	if objective_label:
		objective_label.text = text

func _on_pa_broadcast(speaker: String, text: String, duration: float) -> void:
	if pa_panel:
		pa_speaker.text = speaker.to_upper()
		pa_text.text = text
		pa_panel.visible = true
		pa_timer = duration

func _on_act_changed(act: GlobalGameState.StoryAct) -> void:
	if act_label:
		match act:
			GlobalGameState.StoryAct.ACT1_COLD_CONCRETE:
				act_label.text = "ACT I: THE COLD CONCRETE"
			GlobalGameState.StoryAct.ACT2_ROUTING_FLOOR:
				act_label.text = "ACT II: THE ROUTING FLOOR"
			GlobalGameState.StoryAct.ACT3_BROADCAST_HUB:
				act_label.text = "ACT III: CENTRAL BROADCAST HUB"
			GlobalGameState.StoryAct.EPILOGUE:
				act_label.text = "EPILOGUE: FREQUENCY CONCLUDED"
