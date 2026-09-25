# @tool
class_name TacticalPlayer
extends CharacterBody3D

## Real-Life Simulation: The Vessel (Modern First & Third Person Tactical Controller)
## Pure Diegetic Simulation:
## - ZERO on-screen overlays, ZERO radars, ZERO artificial HUD text/bars.
## - You possess only your Vessel, your mind, your ears, and proximate physical tools.
## - Surface-aware acoustic footsteps: carpet, hardwood, squeaky joists, tile, gravel.
## - Physiological feedback: audible breathing, heartbeat panic, impact gasps, physical camera recoil.
## - Physical weapon aiming down sights (ADS) with no artificial crosshairs.
## - Volumetric halogen flashlight / tactical phosphor NVG.
## - Seamless First-Person and Over-The-Shoulder Third-Person toggle [V].

signal vessel_injured(new_health: float)
signal weapon_discharged(weapon_type: String)

@export_enum("occupant", "intruder") var role: String = "occupant"
@export_enum("first_person", "third_person") var starting_perspective: String = "first_person"

# Movement Parameters
@export var walk_speed: float = 3.2
@export var sprint_speed: float = 5.8
@export var crouch_speed: float = 1.6
@export var acceleration: float = 10.0
@export var friction: float = 12.0
@export var mouse_sensitivity: float = 0.0022

# Vitals (Internal Biological State)
var health: float = 100.0
var stamina: float = 100.0
var is_crouching: bool = false
var is_sprinting: bool = false
var is_aiming_down_sights: bool = false
var is_first_person: bool = true
var is_flashlight_on: bool = false
var is_nvg_on: bool = false

# Weapon State (Physical Tactical Tools)
var weapon_type: String = "shotgun"
var shells_chambered: int = 6
var shells_reserve: int = 18
var fire_cooldown: float = 0.0
var weapon_damage: float = 85.0

# Node References
@onready var neck: Node3D = $Neck
@onready var fp_camera: Camera3D = $Neck/FirstPersonCamera
@onready var tp_spring_arm: SpringArm3D = $Neck/SpringArm3D
@onready var tp_camera: Camera3D = $Neck/SpringArm3D/ThirdPersonCamera
@onready var flashlight: SpotLight3D = $Neck/FirstPersonCamera/Flashlight
@onready var flashlight_bounce: OmniLight3D = $Neck/FirstPersonCamera/FlashlightBounce
@onready var nvg_illuminator: OmniLight3D = $Neck/NVGIlluminator
@onready var interaction_ray: RayCast3D = $Neck/FirstPersonCamera/InteractionRay
@onready var floor_ray: RayCast3D = $FloorRay
@onready var weapon_rig: Node3D = $Neck/FirstPersonCamera/WeaponRig
@onready var tactical_shotgun: Node3D = get_node_or_null("Neck/FirstPersonCamera/WeaponRig/TacticalShotgun")
@onready var muzzle_flash: OmniLight3D = $Neck/FirstPersonCamera/WeaponRig/MuzzleFlash
@onready var character_mesh: MeshInstance3D = $CharacterMesh


# Biological Audio Feedback Players (Attached to the Vessel)
@onready var breath_player: AudioStreamPlayer = $VesselSensors/BreathAudio
@onready var heart_player: AudioStreamPlayer = $VesselSensors/HeartAudio
@onready var body_audio: AudioStreamPlayer3D = $VesselSensors/BodyImpactAudio

# Internal Transform Memory
var camera_pitch: float = 0.0
var head_bob_phase: float = 0.0
var original_cam_y: float = 0.0
var hip_weapon_pos: Vector3 = Vector3(0.20, -0.18, -0.38)
var ads_weapon_pos: Vector3 = Vector3(0.0, -0.046, -0.30)
var footstep_distance_travelled: float = 0.0
var sheaf_engine: SOPHISheafEngine = null

# Night vision post-process screen tint (Ocular Adaptation)
@onready var nvg_lens: ColorRect = $OcularVignette/NVGLens
@onready var shock_vignette: TextureRect = $OcularVignette/ShockVignette

func setup_role(new_role: String) -> void:
	_configure_vessel_for_role(new_role)

func _ready() -> void:

	if not Engine.is_editor_hint():
		Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
		
	sheaf_engine = get_tree().root.find_child("SOPHISheafEngine", true, false) as SOPHISheafEngine
	if sheaf_engine:
		sheaf_engine.set_listener_vessel(self)
		
	if fp_camera:
		original_cam_y = fp_camera.position.y
		
	is_first_person = (starting_perspective == "first_person")
	_configure_vessel_for_role(role)
	_update_perspective_rig()
	
	if muzzle_flash:
		muzzle_flash.visible = false
	if shock_vignette:
		shock_vignette.modulate.a = 0.0
		
	tactical_shotgun = find_child("TacticalShotgun", true, false)

func _configure_vessel_for_role(vessel_role: String) -> void:
	role = vessel_role
	if role == "occupant":
		weapon_type = "shotgun"
		shells_chambered = 6
		shells_reserve = 18
		weapon_damage = 90.0
		is_flashlight_on = true
		is_nvg_on = false
		if flashlight:
			flashlight.visible = true
			flashlight.light_color = Color(1.0, 0.94, 0.84)
			flashlight.light_energy = 5.2
			flashlight.spot_range = 28.0
			flashlight.spot_angle = 56.0
		if flashlight_bounce:
			flashlight_bounce.visible = true
		if nvg_lens:
			nvg_lens.visible = false
		if nvg_illuminator:
			nvg_illuminator.visible = false
	else:
		# Infiltrator / Intruder
		weapon_type = "pistol"
		shells_chambered = 15
		shells_reserve = 30
		weapon_damage = 42.0
		is_flashlight_on = false
		is_nvg_on = true
		if flashlight:
			flashlight.visible = false
		if flashlight_bounce:
			flashlight_bounce.visible = false
		if nvg_lens:
			nvg_lens.visible = true
		if nvg_illuminator:
			nvg_illuminator.visible = true


func _unhandled_input(event: InputEvent) -> void:
	if Engine.is_editor_hint():
		return
		
	if event is InputEventMouseMotion and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
		# Vessel Head Turning (Yaw & Pitch)
		rotate_y(-event.relative.x * mouse_sensitivity)
		camera_pitch = clampf(camera_pitch - event.relative.y * mouse_sensitivity, deg_to_rad(-86.0), deg_to_rad(86.0))
		if neck:
			neck.rotation.x = camera_pitch
			
	if event is InputEventKey and event.pressed:
		# Toggle First / Third Person Vessel Perspective [V]
		if event.keycode == KEY_V:
			is_first_person = not is_first_person
			_update_perspective_rig()
			
		# Physical Flashlight / NVG Toggle [F]
		elif event.keycode == KEY_F:
			_toggle_illumination_device()
			
		# Environmental Physical Manipulation [E] (Door knobs, latch, locks)
		elif event.keycode == KEY_E:
			_manipulate_proximity_object()
			
		# Barricade Door with Reinforced Timber [B] (Occupant)
		elif event.keycode == KEY_B:
			_apply_door_barricade()
			
		# Reload Weapon Shells [R]
		elif event.keycode == KEY_R:
			_reload_shells()
			
		# Esc toggles mouse lock
		elif event.keycode == KEY_ESCAPE:
			if Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
				Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
			else:
				Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

func _physics_process(delta: float) -> void:
	if Engine.is_editor_hint():
		return
		
	if fire_cooldown > 0.0:
		fire_cooldown -= delta
		
	# Holding [E] allows continuous lockpicking of locked doors
	if Input.is_key_pressed(KEY_E) and interaction_ray and interaction_ray.is_colliding():
		var door_target = interaction_ray.get_collider()
		if door_target is TacticalDoor and door_target.is_locked:
			door_target.pick_lock_step(delta)
		
	_process_locomotion(delta)
	_process_weapon_and_aim(delta)
	_process_biological_telemetry(delta)

## Locomotion with physical surface detection & acoustic acoustic emission
func _process_locomotion(delta: float) -> void:
	# Void fall-through safety recovery
	if global_position.y < -10.0:
		if role == "intruder":
			global_position = Vector3(18.0, 0.2, 9.0)
		else:
			global_position = Vector3(0.0, 0.2, 0.0)
		velocity = Vector3.ZERO
		return

	if not is_on_floor():
		velocity.y -= 9.8 * delta
	else:
		velocity.y = 0.0
		
	var input_vec: Vector2 = Vector2.ZERO
	if Input.is_key_pressed(KEY_W): input_vec.y -= 1
	if Input.is_key_pressed(KEY_S): input_vec.y += 1
	if Input.is_key_pressed(KEY_A): input_vec.x -= 1
	if Input.is_key_pressed(KEY_D): input_vec.x += 1
	input_vec = input_vec.normalized()
	
	is_crouching = Input.is_key_pressed(KEY_C) or Input.is_key_pressed(KEY_CTRL)
	is_sprinting = Input.is_key_pressed(KEY_SHIFT) and not is_crouching and input_vec.y < 0
	
	var target_speed = walk_speed
	if is_crouching:
		target_speed = crouch_speed
	elif is_sprinting:
		target_speed = sprint_speed
		
	var move_dir = (transform.basis * Vector3(input_vec.x, 0, input_vec.y)).normalized()
	
	if move_dir.length_squared() > 0.01:
		velocity.x = lerpf(velocity.x, move_dir.x * target_speed, acceleration * delta)
		velocity.z = lerpf(velocity.z, move_dir.z * target_speed, acceleration * delta)
		
		# Organic head bobbing in First Person
		if is_first_person and is_on_floor():
			head_bob_phase += delta * (8.5 * (target_speed / walk_speed))
			if fp_camera:
				fp_camera.position.y = original_cam_y + sin(head_bob_phase) * 0.035
				
		# Surface-dependent footstep acoustic tracking
		var horizontal_displacement = Vector2(velocity.x, velocity.z).length() * delta
		footstep_distance_travelled += horizontal_displacement
		var stride = 1.9 if not is_sprinting else 1.45
		if is_crouching: stride = 1.6
		
		if footstep_distance_travelled >= stride and is_on_floor():
			footstep_distance_travelled = 0.0
			_emit_surface_footstep()
	else:
		velocity.x = lerpf(velocity.x, 0.0, friction * delta)
		velocity.z = lerpf(velocity.z, 0.0, friction * delta)
		if is_first_person and fp_camera:
			fp_camera.position.y = lerpf(fp_camera.position.y, original_cam_y, 8.0 * delta)
			
	move_and_slide()

## Physical floor surface interrogation
func _emit_surface_footstep() -> void:
	if not sheaf_engine:
		return
		
	var sound_key = "hardwood"
	var current_room = sheaf_engine.get_room_for_position(global_position)
	
	if current_room == SOPHISheafEngine.ROOM_REFUGE:
		# Bedroom has thick wool carpet
		sound_key = "carpet"
	elif current_room == SOPHISheafEngine.ROOM_CORRIDOR:
		# Hardwood floor with occasional squeaky floorboards
		if randf() < 0.28:
			sound_key = "wood_creak_joist" if randf() < 0.5 else "wood_creak"
		else:
			sound_key = "hardwood"
	elif current_room == SOPHISheafEngine.ROOM_MUDROOM:
		# Ceramic tiles
		sound_key = "tile"
	else:
		# Exterior deck / gravel
		sound_key = "wood_deck"
		
	var vol_db = -6.0
	if is_crouching:
		vol_db = -18.0 # soft stealth footsteps
	elif is_sprinting:
		vol_db = 2.0  # heavy thumping footsteps
		
	sheaf_engine.play_physical_sound(sound_key, global_position + Vector3(0, 0.1, 0), vol_db)

## Weapon aiming down sights & discharge
func _process_weapon_and_aim(delta: float) -> void:
	# Right mouse button to physically align sights at eye level
	is_aiming_down_sights = Input.is_mouse_button_pressed(MOUSE_BUTTON_RIGHT)
	if weapon_rig:
		var target_pos = ads_weapon_pos if is_aiming_down_sights else hip_weapon_pos
		weapon_rig.position = weapon_rig.position.lerp(target_pos, 14.0 * delta)
		
	# Left mouse button to squeeze the trigger
	if Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and fire_cooldown <= 0.0:
		if shells_chambered > 0:
			_discharge_weapon()
		else:
			_dry_fire_click()

func _discharge_weapon() -> void:
	shells_chambered -= 1
	fire_cooldown = 0.9 if weapon_type == "shotgun" else 0.25
	
	# Muzzle flash light
	if muzzle_flash:
		muzzle_flash.visible = true
		get_tree().create_timer(0.06).timeout.connect(func(): muzzle_flash.visible = false)
		
	# Articulated pump action cycling
	if tactical_shotgun and weapon_type == "shotgun":
		tactical_shotgun.cycle_pump()
		
	# Camera recoil kick
	camera_pitch = clampf(camera_pitch + deg_to_rad(2.2 if weapon_type == "shotgun" else 0.8), deg_to_rad(-86.0), deg_to_rad(86.0))
	if neck:
		neck.rotation.x = camera_pitch
		
	# Physical acoustic wave propagation across residence
	if sheaf_engine:
		var sound_name = "shotgun" if weapon_type == "shotgun" else "pistol"
		sheaf_engine.play_physical_sound(sound_name, global_position + Vector3(0, 1.4, 0), 12.0)
		
	weapon_discharged.emit(weapon_type)
	_perform_ballistic_raycast()

func _dry_fire_click() -> void:
	fire_cooldown = 0.4
	if sheaf_engine:
		sheaf_engine.play_physical_sound("switch_click", global_position + Vector3(0, 1.4, 0), -4.0, 1.4)

func _reload_shells() -> void:
	if shells_reserve <= 0 or shells_chambered >= (6 if weapon_type == "shotgun" else 15):
		return
	var needed = (6 if weapon_type == "shotgun" else 15) - shells_chambered
	var loaded = mini(needed, shells_reserve)
	shells_chambered += loaded
	shells_reserve -= loaded
	fire_cooldown = 1.2
	if sheaf_engine:
		sheaf_engine.play_physical_sound("switch", global_position + Vector3(0, 1.2, 0), -2.0)

func _perform_ballistic_raycast() -> void:
	var active_cam = fp_camera if is_first_person else tp_camera
	if not active_cam:
		return
		
	var space_state = get_world_3d().direct_space_state
	var screen_center = get_viewport().get_visible_rect().size * 0.5
	var ray_origin = active_cam.project_ray_origin(screen_center)
	var ray_dir = active_cam.project_ray_normal(screen_center)
	var ray_target = ray_origin + ray_dir * 60.0
	
	var query = PhysicsRayQueryParameters3D.create(ray_origin, ray_target)
	query.exclude = [self]
	var hit = space_state.intersect_ray(query)
	
	if hit:
		var collider = hit["collider"]
		if collider is TacticalDoor:
			collider.breach_door(weapon_damage)
		elif collider.has_method("take_damage"):
			collider.take_damage(weapon_damage, hit["position"])

## Biological vital state (No UI meters - experienced through ear and eye)
func _process_biological_telemetry(delta: float) -> void:
	# Recover/deplete biological stamina
	if is_sprinting:
		stamina = maxf(0.0, stamina - 22.0 * delta)
	else:
		stamina = minf(100.0, stamina + 15.0 * delta)
		
	# Respiration audio feedback
	if breath_player:
		if stamina < 30.0 or health < 50.0:
			if not breath_player.playing:
				breath_player.play()
			breath_player.volume_db = lerpf(breath_player.volume_db, 0.0, 3.0 * delta)
		else:
			breath_player.volume_db = lerpf(breath_player.volume_db, -35.0, 2.0 * delta)
			if breath_player.volume_db <= -30.0 and breath_player.playing:
				breath_player.stop()
				
	# Heartbeat thumping feedback during danger
	if heart_player:
		if health < 45.0 or (sheaf_engine and sheaf_engine.dirichlet_energy > 0.4):
			if not heart_player.playing:
				heart_player.play()
			heart_player.volume_db = lerpf(heart_player.volume_db, -2.0, 4.0 * delta)
		else:
			heart_player.volume_db = lerpf(heart_player.volume_db, -40.0, 2.0 * delta)
			if heart_player.volume_db <= -35.0 and heart_player.playing:
				heart_player.stop()
				
	# Shock vignette fading
	if shock_vignette and shock_vignette.modulate.a > 0.0:
		shock_vignette.modulate.a = maxf(0.0, shock_vignette.modulate.a - 0.4 * delta)

func take_damage(amount: float, hit_pos: Vector3 = Vector3.ZERO) -> void:
	health = maxf(0.0, health - amount)
	vessel_injured.emit(health)
	
	# Physiological gasp & shock flinch
	if sheaf_engine:
		sheaf_engine.play_physical_sound("gasp", global_position + Vector3(0, 1.6, 0), 4.0)
	if shock_vignette:
		shock_vignette.modulate.a = 0.75

func _toggle_illumination_device() -> void:
	if sheaf_engine:
		sheaf_engine.play_physical_sound("switch_click", global_position + Vector3(0, 1.4, 0), -6.0)
		
	if role == "occupant":
		is_flashlight_on = not is_flashlight_on
		if flashlight:
			flashlight.visible = is_flashlight_on
		if flashlight_bounce:
			flashlight_bounce.visible = is_flashlight_on
	else:
		is_nvg_on = not is_nvg_on
		if nvg_lens:
			nvg_lens.visible = is_nvg_on
		if nvg_illuminator:
			nvg_illuminator.visible = is_nvg_on


func _manipulate_proximity_object() -> void:
	if not interaction_ray or not interaction_ray.is_colliding():
		return
	var collider = interaction_ray.get_collider()
	if collider is TacticalDoor:
		collider.interact(role)

func _apply_door_barricade() -> void:
	if role != "occupant" or not interaction_ray or not interaction_ray.is_colliding():
		return
	var collider = interaction_ray.get_collider()
	if collider is TacticalDoor:
		collider.barricade_door()

func _update_perspective_rig() -> void:
	if is_first_person:
		if fp_camera: fp_camera.current = true
		if tp_camera: tp_camera.current = false
		if character_mesh: character_mesh.visible = false
		if weapon_rig: weapon_rig.visible = true
	else:
		if fp_camera: fp_camera.current = false
		if tp_camera: tp_camera.current = true
		if character_mesh: character_mesh.visible = true
		if weapon_rig: weapon_rig.visible = false
