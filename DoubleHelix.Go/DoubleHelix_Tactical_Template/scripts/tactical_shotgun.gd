# @tool
class_name TacticalShotgun
extends Node3D

## Tactical 12-Gauge Combat Shotgun // Double Helix Rig
## Real-Life Diegetic Simulation: Multi-component steel receiver, ventilated rib barrel,
## parallel magazine tube, articulated pump fore-end slide, walnut stock with rubber recoil pad,
## and realistic brass/red 12-gauge shell chambering & cycling.

signal pump_completed()

@export var pump_slide_path: NodePath = NodePath("PumpSlide")
@export var muzzle_marker_path: NodePath = NodePath("MuzzleMarker")
@export var ejection_marker_path: NodePath = NodePath("EjectionPortMarker")
@export var chamber_shell_path: NodePath = NodePath("ChamberShell")

@onready var pump_slide: Node3D = get_node_or_null(pump_slide_path)
@onready var muzzle_marker: Marker3D = get_node_or_null(muzzle_marker_path)
@onready var ejection_marker: Marker3D = get_node_or_null(ejection_marker_path)
@onready var chamber_shell: Node3D = get_node_or_null(chamber_shell_path)

var is_cycling: bool = false
var default_pump_z: float = -0.28

func _ready() -> void:
	if pump_slide:
		default_pump_z = pump_slide.position.z

## Cycles the pump action back and forth with realistic mechanical timing
func cycle_pump() -> void:
	if is_cycling or not pump_slide:
		return
	is_cycling = true
	
	var tween = create_tween().set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_OUT)
	# Slide back 6.5 cm
	tween.tween_property(pump_slide, "position:z", default_pump_z + 0.065, 0.09)
	# Momentary mechanical pause at rear extension
	tween.tween_interval(0.04)
	# Slide forward back into battery
	tween.tween_property(pump_slide, "position:z", default_pump_z, 0.08)
	tween.finished.connect(func():
		is_cycling = false
		pump_completed.emit()
	)

func get_muzzle_global_position() -> Vector3:
	if muzzle_marker:
		return muzzle_marker.global_position
	return global_position + -global_transform.basis.z * 0.65
