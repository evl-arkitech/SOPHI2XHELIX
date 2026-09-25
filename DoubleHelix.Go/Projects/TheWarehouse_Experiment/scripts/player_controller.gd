extends CharacterBody3D

# First-Person Survival Horror Player Controller
# Author: The Arkitech & Sophianat

@export var walk_speed: float = 3.2
@export var sprint_speed: float = 5.5
@export var crouch_speed: float = 1.8
@export var mouse_sensitivity: float = 0.0025
@export var gravity: float = 9.8

# Camera & Head Bob
@onready var head: Node3D = $Head
@onready var camera: Camera3D = $Head/Camera3D
@onready var flashlight: SpotLight3D = $Head/Camera3D/Flashlight
@onready var interact_ray: RayCast3D = $Head/Camera3D/InteractRay

var bob_phase: float = 0.0
var bob_frequency: float = 8.0
var bob_amplitude: float = 0.05
var default_cam_y: float = 1.65

# Flashlight & Battery Management
var battery: float = 100.0
var battery_drain_rate: float = 1.2 # % per second when on
var is_flashlight_on: bool = true
var flicker_timer: float = 0.0

# 180 Look Back
var is_looking_back: bool = false
var look_back_target_yaw: float = 0.0

# Footstep cadence
var footstep_distance: float = 0.0
var next_footstep_threshold: float = 1.8

# Interact Target
var current_interactable: Node = null

func _ready() -> void:
	Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)
	if camera:
		default_cam_y = camera.position.y

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseMotion and Input.get_mouse_mode() == Input.MOUSE_MODE_CAPTURED:
		head.rotate_y(-event.relative.x * mouse_sensitivity)
		camera.rotate_x(-event.relative.y * mouse_sensitivity)
		camera.rotation.x = clamp(camera.rotation.x, deg_to_rad(-85.0), deg_to_rad(85.0))
	
	if event.is_action_pressed("toggle_light"):
		toggle_flashlight()
		
	if event.is_action_pressed("look_back"):
		perform_quick_look_back()
		
	if event.is_action_pressed("interact") and current_interactable != null:
		if current_interactable.has_method("interact"):
			current_interactable.interact(self)
			
	if event.is_action_pressed("pause"):
		if Input.get_mouse_mode() == Input.MOUSE_MODE_CAPTURED:
			Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)
		else:
			Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)

func _physics_process(delta: float) -> void:
	# Gravity
	if not is_on_floor():
		velocity.y -= gravity * delta

	# Input movement
	var input_dir = Input.get_vector("move_left", "move_right", "move_forward", "move_backward")
	var move_dir = (head.global_transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()
	
	var target_speed = walk_speed
	if Input.is_action_pressed("sprint") and input_dir.y < 0:
		target_speed = sprint_speed
	elif Input.is_action_pressed("crouch"):
		target_speed = crouch_speed
		
	if move_dir != Vector3.ZERO:
		velocity.x = move_dir.x * target_speed
		velocity.z = move_dir.z * target_speed
		
		# Head bob and footstep calculation
		bob_phase += delta * target_speed * bob_frequency
		var bob_offset = sin(bob_phase) * bob_amplitude
		camera.position.y = default_cam_y + bob_offset
		
		footstep_distance += target_speed * delta
		if footstep_distance >= next_footstep_threshold:
			footstep_distance = 0.0
			var is_in_water = global_position.y < 0.2 and GlobalGameState.current_act == GlobalGameState.StoryAct.ACT2_ROUTING_FLOOR
			SoundManager.play_footstep(is_in_water)
	else:
		velocity.x = move_toward(velocity.x, 0, walk_speed * 4.0 * delta)
		velocity.z = move_toward(velocity.z, 0, walk_speed * 4.0 * delta)
		camera.position.y = move_toward(camera.position.y, default_cam_y, delta * 2.0)
		bob_phase = 0.0

	move_and_slide()
	
	# Battery & Flashlight processing
	_process_flashlight(delta)
	
	# Raycast interaction checking
	_process_interaction()

func _process_flashlight(delta: float) -> void:
	if is_flashlight_on:
		battery = max(0.0, battery - (battery_drain_rate * delta))
		GlobalGameState.player_battery = battery
		GlobalGameState.battery_drain_total += battery_drain_rate * delta
		
		if battery <= 0.0:
			flashlight.visible = false
			is_flashlight_on = false
		elif battery < 20.0:
			# Voltage flicker when below 20%
			flicker_timer -= delta
			if flicker_timer <= 0.0:
				flicker_timer = randf_range(0.08, 0.45)
				flashlight.light_energy = randf_range(0.2, 1.4)
		else:
			flashlight.light_energy = 1.6
	else:
		flashlight.visible = false

func toggle_flashlight() -> void:
	if battery > 0.0:
		is_flashlight_on = not is_flashlight_on
		flashlight.visible = is_flashlight_on
		GlobalGameState.player_flashlight_on = is_flashlight_on

func perform_quick_look_back() -> void:
	# Instantly snap or quickly rotate yaw by 180 degrees
	head.rotate_y(PI)
	GlobalGameState.look_backs_performed += 1
	GlobalGameState.has_looked_back_at_a = true

func _process_interaction() -> void:
	if interact_ray and interact_ray.is_colliding():
		var collider = interact_ray.get_collider()
		if collider and collider.is_in_group("interactable"):
			current_interactable = collider
			return
	current_interactable = null
