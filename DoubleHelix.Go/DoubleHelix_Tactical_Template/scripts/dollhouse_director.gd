# @tool
class_name DollhouseDirector
extends Node3D

## Suburban Residential "Dollhouse" Director // Double Helix Engine
## Controls dual-camera perspectives (Isometric Dollhouse vs First-Person Vessel),
## floor-level visibility culling (Level 0 vs Level 1), and dynamic cross-section cutaway.

@export var level_0_path: NodePath = NodePath("Level_0_Ground")
@export var level_1_path: NodePath = NodePath("Level_1_Upper")
@export var dollhouse_cam_path: NodePath = NodePath("DollhouseCamera")

@onready var level_0: Node3D = get_node_or_null(level_0_path)
@onready var level_1: Node3D = get_node_or_null(level_1_path)
@onready var dollhouse_cam: Camera3D = get_node_or_null(dollhouse_cam_path)

var is_dollhouse_view: bool = true
var current_floor_mode: int = 0 # 0: Level 0, 1: Level 1, 2: Both
var is_cutaway_active: bool = true

func _ready() -> void:
	_update_floor_visibility()
	_update_camera_mode()

func _unhandled_input(event: InputEvent) -> void:
	if Engine.is_editor_hint():
		return
		
	if event is InputEventKey and event.pressed:
		# [T] Toggle Dollhouse Top-Down vs First-Person Tactical View
		if event.keycode == KEY_T:
			is_dollhouse_view = not is_dollhouse_view
			_update_camera_mode()
			
		# [1] View Ground Floor (Level 0)
		elif event.keycode == KEY_1:
			current_floor_mode = 0
			_update_floor_visibility()
			
		# [2] View Upper Floor (Level 1)
		elif event.keycode == KEY_2:
			current_floor_mode = 1
			_update_floor_visibility()
			
		# [3] View Both Floors (Stacked Manifold)
		elif event.keycode == KEY_3:
			current_floor_mode = 2
			_update_floor_visibility()
			
		# [C] Toggle Cross-Section Wall Cutaway (1.1m vs 2.7m)
		elif event.keycode == KEY_C:
			is_cutaway_active = not is_cutaway_active
			_update_cutaway_scale()

func _update_camera_mode() -> void:
	if dollhouse_cam:
		dollhouse_cam.current = is_dollhouse_view
	var player = find_child("TacticalPlayer", true, false)
	if player:
		if is_dollhouse_view:
			Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
		else:
			Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

func _update_floor_visibility() -> void:
	if level_0:
		level_0.visible = (current_floor_mode == 0 or current_floor_mode == 2)
	if level_1:
		level_1.visible = (current_floor_mode == 1 or current_floor_mode == 2)

func _update_cutaway_scale() -> void:
	var target_scale_y = 0.407 if is_cutaway_active else 1.0 # 1.1m / 2.7m = 0.407
	if level_0:
		_scale_walls(level_0, target_scale_y)
	if level_1:
		_scale_walls(level_1, target_scale_y)

func _scale_walls(parent: Node, scale_y: float) -> void:
	for c in parent.get_children():
		if "Wall" in c.name:
			c.scale.y = scale_y
			# Adjust position so base remains on floor
			c.position.y = (2.7 * scale_y) / 2.0
		elif c.get_child_count() > 0:
			_scale_walls(c, scale_y)
