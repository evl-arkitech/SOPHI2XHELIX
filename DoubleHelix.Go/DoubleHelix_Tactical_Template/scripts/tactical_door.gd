# @tool
class_name TacticalDoor
extends StaticBody3D

## Tactical Interactive Door // Double Helix Tactical Rig
## Features:
## - True Hinge Pivot rotation (swings out of doorway clearance)
## - Diegetic audio feedback: knob rattle, latch click, wood creak, heavy breach fracture
## - Dual-role interactions: Occupant unlock/barricade, Intruder lockpick/kick/shotgun breach
## - Sheaf restriction topology sync (updates acoustic obstruction in SOPHISheafEngine)

signal door_opened()
signal door_closed()
signal door_breached()
signal door_barricaded()
signal door_unlocked()

@export var edge_id: String = "door_bedroom"
@export var is_locked: bool = false
@export var is_barricaded: bool = false
@export var door_health: float = 80.0 # Breachable with one point-blank 12-gauge blast
@export var open_angle_deg: float = 95.0
@export var open_speed: float = 5.0

var current_state: String = "closed"
var target_rotation_y: float = 0.0
var initial_rotation_y: float = 0.0
var sheaf_engine: SOPHISheafEngine = null

var lockpick_progress: float = 0.0
var is_being_picked: bool = false

@onready var collision_shape: CollisionShape3D = get_node_or_null("DoorCollision")
@onready var mesh_instance: MeshInstance3D = get_node_or_null("DoorMesh")

func _find_child_nodes() -> void:
	if not collision_shape:
		collision_shape = find_child("DoorCollision", true, false) as CollisionShape3D
		if not collision_shape:
			for c in get_children():
				if c is CollisionShape3D:
					collision_shape = c
					break
	if not mesh_instance:
		mesh_instance = find_child("DoorMesh", true, false) as MeshInstance3D
		if not mesh_instance:
			for c in get_children():
				if c is MeshInstance3D:
					mesh_instance = c
					break

func _ready() -> void:
	_find_child_nodes()
	initial_rotation_y = rotation.y
	target_rotation_y = initial_rotation_y
	sheaf_engine = get_tree().root.find_child("SOPHISheafEngine", true, false) as SOPHISheafEngine
	_sync_sheaf_state()

func _process(delta: float) -> void:
	if abs(rotation.y - target_rotation_y) > 0.001:
		rotation.y = lerpf(rotation.y, target_rotation_y, open_speed * delta)

func interact(interactor_role: String = "occupant") -> Dictionary:
	if current_state == "breached":
		return {"success": true, "message": "Doorway is splintered and breached."}
		
	if is_barricaded:
		if interactor_role == "occupant":
			is_barricaded = false
			_emit_door_sound(0.8, 0.3, "Barricade Removed")
			_sync_sheaf_state()
			return {"success": true, "message": "Barricade dismantled."}
		else:
			_emit_door_sound(1.5, 0.4, "Intruder rattled heavy timber barricade")
			return {"success": false, "message": "Heavy timber barricade locked from inside!"}
			
	if is_locked:
		if interactor_role == "intruder":
			# Intruder rattles locked knob
			_emit_door_sound(0.85, 0.7, "Locked Knob Rattle")
			return {"success": false, "message": "Locked. Hold [E] to pick lock, or shoot lock with shotgun."}
		else:
			# Occupant has key
			is_locked = false
			_emit_door_sound(0.5, 0.8, "Key Unlocked")
			door_unlocked.emit()
			
	if current_state == "closed":
		open_door()
		return {"success": true, "message": "Door opened."}
	elif current_state == "open":
		close_door()
		return {"success": true, "message": "Door closed."}
		
	return {"success": false, "message": "Door busy."}

func open_door() -> void:
	current_state = "open"
	target_rotation_y = initial_rotation_y + deg_to_rad(open_angle_deg)
	_emit_door_sound(0.65, 0.2, "Door Creaked Open")
	_sync_sheaf_state()
	door_opened.emit()

func close_door() -> void:
	current_state = "closed"
	target_rotation_y = initial_rotation_y
	_emit_door_sound(0.75, 0.4, "Door Latched Shut")
	_sync_sheaf_state()
	door_closed.emit()

func pick_lock_step(delta: float) -> bool:
	if not is_locked:
		return true
	lockpick_progress += delta * 1.5
	if lockpick_progress >= 1.0:
		is_locked = false
		lockpick_progress = 0.0
		_emit_door_sound(0.8, 0.9, "Tumbler Clicked Free")
		door_unlocked.emit()
		open_door()
		return true
	return false

func breach_door(force: float = 85.0) -> bool:
	door_health -= force
	_emit_door_sound(5.5, 0.85, "Violent Shotgun Lock Breach")
	
	if door_health <= 0.0 or force >= 75.0:
		current_state = "breached"
		target_rotation_y = initial_rotation_y + deg_to_rad(115.0)
		is_barricaded = false
		is_locked = false
		# Disable collider so splintered door never snags player walking through
		if collision_shape:
			collision_shape.set_deferred("disabled", true)
		_emit_door_sound(8.0, 0.95, "Door Wood Shattered Off Hinges")
		_sync_sheaf_state()
		door_breached.emit()
		return true
	else:
		_sync_sheaf_state()
		return false

func barricade_door() -> bool:
	if current_state != "closed":
		close_door()
	is_barricaded = true
	current_state = "barricaded"
	_emit_door_sound(2.0, 0.5, "Heavy Barricade Hammered")
	_sync_sheaf_state()
	door_barricaded.emit()
	return true

func _emit_door_sound(amplitude: float, freq: float, desc: String) -> void:
	if not sheaf_engine and is_inside_tree() and get_tree():
		sheaf_engine = get_tree().root.find_child("SOPHISheafEngine", true, false) as SOPHISheafEngine
	if sheaf_engine:
		var sound_key = "door_open"
		if "shut" in desc.to_lower() or "latched" in desc.to_lower():
			sound_key = "door_close"
		elif "breach" in desc.to_lower() or "shattered" in desc.to_lower():
			sound_key = "door_breach"
		elif "barricade" in desc.to_lower():
			sound_key = "wood_deck"
		elif "rattle" in desc.to_lower() or "lock" in desc.to_lower() or "key" in desc.to_lower() or "tumbler" in desc.to_lower():
			sound_key = "switch_click"
			
		sheaf_engine.play_physical_sound(sound_key, global_position + Vector3(0, 1.0, 0), linear_to_db(clampf(amplitude, 0.1, 8.0)))

func _sync_sheaf_state() -> void:
	if not sheaf_engine and is_inside_tree() and get_tree():
		sheaf_engine = get_tree().root.find_child("SOPHISheafEngine", true, false) as SOPHISheafEngine
	if sheaf_engine:
		sheaf_engine.set_edge_door_state(edge_id, current_state)
