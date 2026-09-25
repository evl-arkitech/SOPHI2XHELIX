# @tool
class_name TacticalAIOpponent
extends CharacterBody3D

## Real-Life Simulation Autonomous Opponent
## Operates under pure physical acoustic rules:
## - Stalks through the residence emitting physical footsteps & floorboard creaks
## - Listens to Sheaf difference records (footsteps, barricading, doors opening)
## - Physical line-of-sight vision cone through darkness and shadows
## - Uses authentic shotgun or suppressed pistol with physical muzzle flashes

@export_enum("intruder", "occupant") var role: String = "intruder"
@export var movement_speed: float = 2.4
@export var patrol_points: Array[Vector3] = []

enum AIState { PATROL, INVESTIGATE, STALK, ENGAGE, FLEE }
var current_state: AIState = AIState.PATROL

var target_position_investigate: Vector3 = Vector3.ZERO
var target_player: Node3D = null
var sheaf_engine: SOPHISheafEngine = null

# Vitals & Combat
var health: float = 100.0
var weapon_cooldown: float = 0.0
var step_timer: float = 0.0
var vision_angle_deg: float = 70.0
var vision_range: float = 18.0

# Nodes
@onready var vision_ray: RayCast3D = $VisionRay
@onready var flashlight: SpotLight3D = $Flashlight
@onready var character_mesh: MeshInstance3D = $CharacterMesh
@onready var muzzle_flash: OmniLight3D = $MuzzleFlash

func _ready() -> void:
	sheaf_engine = get_tree().root.find_child("SOPHISheafEngine", true, false) as SOPHISheafEngine
	if sheaf_engine:
		sheaf_engine.acoustic_event_emitted.connect(_on_acoustic_event_heard)
		
	# Find player
	target_player = get_tree().root.find_child("TacticalPlayer", true, false)
	
	# Setup role lighting
	if role == "intruder":
		if flashlight: flashlight.visible = false
	else:
		if flashlight:
			flashlight.visible = true
			flashlight.light_energy = 3.5

func _physics_process(delta: float) -> void:
	if Engine.is_editor_hint():
		return
		
	if weapon_cooldown > 0.0:
		weapon_cooldown -= delta
		
	if not target_player:
		target_player = get_tree().root.find_child("TacticalPlayer", true, false)
		
	_check_vision_cone()
	_execute_behavior_state(delta)

func _check_vision_cone() -> void:
	if not target_player or not vision_ray:
		return
		
	var to_player = target_player.global_position - global_position
	var dist = to_player.length()
	if dist > vision_range:
		return
		
	var forward = -transform.basis.z
	var angle_to_player = rad_to_deg(forward.angle_to(to_player.normalized()))
	
	if angle_to_player <= vision_angle_deg * 0.5:
		vision_ray.target_position = to_player
		vision_ray.force_raycast_update()
		if vision_ray.is_colliding():
			var collider = vision_ray.get_collider()
			if collider == target_player:
				current_state = AIState.ENGAGE

func _execute_behavior_state(delta: float) -> void:
	var target_dest = global_position
	var speed = movement_speed
	
	match current_state:
		AIState.PATROL:
			if patrol_points.size() > 0:
				target_dest = patrol_points[0]
			else:
				# Move toward center corridor
				target_dest = Vector3(7.0, 0.0, 4.0)
				
		AIState.INVESTIGATE:
			target_dest = target_position_investigate
			speed = movement_speed * 0.8 # sneaking toward noise
			if global_position.distance_to(target_dest) < 1.5:
				current_state = AIState.PATROL
				
		AIState.STALK:
			if target_player:
				target_dest = target_player.global_position
				speed = movement_speed * 0.6 # silent stalking
				
		AIState.ENGAGE:
			if target_player:
				target_dest = target_player.global_position
				speed = movement_speed * 1.3
				_aim_and_fire_at_player(delta)
				
	_move_towards(target_dest, speed, delta)

func _move_towards(dest: Vector3, speed: float, delta: float) -> void:
	var dir = (dest - global_position)
	dir.y = 0.0
	
	if dir.length() > 0.4:
		var move_vec = dir.normalized()
		velocity.x = move_vec.x * speed
		velocity.z = move_vec.z * speed
		# Smooth yaw rotation toward movement
		var target_yaw = atan2(-move_vec.x, -move_vec.z)
		rotation.y = lerp_angle(rotation.y, target_yaw, 6.0 * delta)
		
		# Acoustic footsteps
		step_timer += delta * (speed / 2.0)
		if step_timer >= 1.0:
			step_timer = 0.0
			_emit_ai_footstep()
	else:
		velocity.x = 0.0
		velocity.z = 0.0
		
	if not is_on_floor():
		velocity.y -= 9.8 * delta
	else:
		velocity.y = 0.0
		
	move_and_slide()

func _emit_ai_footstep() -> void:
	if not sheaf_engine:
		return
	var room = sheaf_engine.get_room_for_position(global_position)
	var sound_key = "hardwood"
	if room == SOPHISheafEngine.ROOM_REFUGE:
		sound_key = "carpet"
	elif room == SOPHISheafEngine.ROOM_CORRIDOR:
		sound_key = "wood_creak_joist" if randf() < 0.3 else "hardwood"
	elif room == SOPHISheafEngine.ROOM_MUDROOM:
		sound_key = "tile"
	else:
		sound_key = "wood_deck"
		
	sheaf_engine.play_physical_sound(sound_key, global_position + Vector3(0, 0.1, 0), -8.0)

func _aim_and_fire_at_player(delta: float) -> void:
	if not target_player:
		return
	var dir_to_player = (target_player.global_position - global_position).normalized()
	var target_yaw = atan2(-dir_to_player.x, -dir_to_player.z)
	rotation.y = lerp_angle(rotation.y, target_yaw, 10.0 * delta)
	
	if weapon_cooldown <= 0.0:
		weapon_cooldown = 1.2 if role == "occupant" else 0.45
		# Discharge weapon
		if muzzle_flash:
			muzzle_flash.visible = true
			get_tree().create_timer(0.06).timeout.connect(func(): muzzle_flash.visible = false)
			
		if sheaf_engine:
			var sname = "shotgun" if role == "occupant" else "pistol"
			sheaf_engine.play_physical_sound(sname, global_position + Vector3(0, 1.4, 0), 10.0)
			
		# Ballistics
		var space_state = get_world_3d().direct_space_state
		var start_p = global_position + Vector3(0, 1.5, 0)
		var end_p = start_p + dir_to_player * 40.0
		var query = PhysicsRayQueryParameters3D.create(start_p, end_p)
		query.exclude = [self]
		var hit = space_state.intersect_ray(query)
		if hit and hit["collider"] == target_player:
			if target_player.has_method("take_damage"):
				target_player.take_damage(35.0 if role == "intruder" else 75.0, hit["position"])

func _on_acoustic_event_heard(record: Dictionary) -> void:
	# Don't investigate own sounds
	if record["source_pos"].distance_to(global_position) < 0.8:
		return
		
	# If event is loud enough (e.g. running footstep, door latch, breach, gunshot)
	if record["amplitude"] > 0.4 and current_state != AIState.ENGAGE:
		target_position_investigate = record["source_pos"]
		current_state = AIState.INVESTIGATE

func take_damage(amount: float, hit_pos: Vector3 = Vector3.ZERO) -> void:
	health -= amount
	if sheaf_engine:
		sheaf_engine.play_physical_sound("gasp", global_position + Vector3(0, 1.4, 0), 2.0)
	if health <= 0.0:
		# Physical elimination
		print("[TACTICAL-SIM] Opponent neutralized: ", role)
		queue_free()
	else:
		current_state = AIState.ENGAGE
