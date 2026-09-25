extends StaticBody3D

# Dais Choice Station Trigger
# Author: The Arkitech & Sophianat

@export var choice_type: GlobalGameState.EndingChoice = GlobalGameState.EndingChoice.SUCCESSION
@export var prompt_text: String = "[E] Make Terminal Choice"

func interact(player: Node) -> void:
	var dais = get_parent()
	if dais and dais.has_method("execute_terminal_choice"):
		dais.execute_terminal_choice(choice_type)
