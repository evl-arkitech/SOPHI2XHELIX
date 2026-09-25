extends CharacterBody3D

# SightlineMannequin: Quantum Observer Stalker AI
# Freezes when in camera frustum and illuminated; stalks relentlessly when sightline is broken.
# Author: The Arkitech & Sophianat

@export var stalk_speed: float = 4.8
@export var stop_distance: float = 1.3
@export var is_mannequin_a: bool = false

@onready var mesh_instance: Node3D = $VisualMesh
@onready var head_bone: Node3D = $VisualMesh/HeadNode
@onready var stalk_audio: AudioStreamPlayer3D = $StalkAudio

var player: Node3D = null
var is_currently_observed: bool = false
var was_observed_last_frame: bool = false
var has_relocated_act1: bool = false

func _ready() -> void:
	add_to_group("stalkers")
	# Look for player node in tree
	await get_tree().process_frame
	player = get_tree().get_first_node_in_group("player")

func _physics_process(delta: float) -> void:
	if player == null:
		player = get_tree().get_first_node_in_group("player")
		if player == null:
			return

	is_currently_observed = check_player_observation()

	# If newly observed this frame, snap head into an unsettling tilt
	if is_currently_observed and not was_observed_last_frame:
		_on_observed_snap()
	
	was_observed_last_frame = is_currently_observed

	if is_currently_observed:
		# Frozen in place by active observation
		velocity = Vector3.ZERO
		move_and_slide()
		return

	# Act 1 special event: Relocate Mannequin A directly behind player when looked away
	if is_mannequin_a and GlobalGameState.has_passed_mannequin_a and not has_relocated_act1:
		_execute_act1_relocation()
		return

	# UNOBSERVED: Stalk toward player position
	var to_player = player.global_position - global_position
	var dist = to_player.length()

	# Rotate toward player
	var look_target = player.global_position
	look_target.y = global_position.y
	look_at(look_target, Vector3.UP)

	if dist > stop_distance:
		var dir = to_player.normalized()
		velocity.x = dir.x * stalk_speed
		velocity.z = dir.z * stalk_speed
		
		# Play scraping sound occasionally when moving
		if stalk_audio and not stalk_audio.playing and randf() < 0.05:
			stalk_audio.pitch_scale = randf_range(0.85, 1.15)
			stalk_audio.play()
	else:
		velocity.x = 0
		velocity.z = 0
		GlobalGameState.stalker_encounters += 1
		GlobalGameState.fear_coefficient = min(1.0, GlobalGameState.fear_coefficient + 0.15 * delta)

	move_and_slide()

func check_player_observation() -> bool:
	if player == null:
		return false
		
	var cam: Camera3D = player.get_node_or_null("Head/Camera3D")
	if cam == null:
		return false

	# 1. Frustum Check
	var my_head_pos = global_position + Vector3(0, 1.6, 0)
	if not cam.is_position_in_frustum(my_head_pos):
		return false

	# 2. Angle / Dot Product Check
	var cam_forward = -cam.global_transform.basis.z.normalized()
	var dir_to_me = (my_head_pos - cam.global_position).normalized()
	var dot = cam_forward.dot(dir_to_me)
	if dot < 0.45: # Outside ~63 degree visual cone
		return false

	# 3. Raycast Occlusion Check (Ensure no walls or obstacles block vision)
	var space_state = get_world_3d().direct_space_state
	var query = PhysicsRayQueryParameters3D.create(cam.global_position, my_head_pos)
	query.exclude = [player.get_rid(), self.get_rid()]
	var result = space_state.intersect_ray(query)
	
	if result:
		# If ray hit an obstacle that is not part of this mannequin, sight is occluded
		return false

	# 4. Illumination Check: Is player's flashlight on or are we close enough to be in peripheral silhouette?
	var dist = (global_position - player.global_position).length()
	if GlobalGameState.player_flashlight_on:
		return true
	elif dist < 3.0:
		# Silhouette is visible within close range even in dark
		return true

	return false

func _on_observed_snap() -> void:
	if head_bone:
		head_bone.rotation_degrees = Vector3(
			randf_range(-15.0, 35.0),
			randf_range(-45.0, 45.0),
			randf_range(-30.0, 30.0)
		)

func _execute_act1_relocation() -> void:
	has_relocated_act1 = true
	GlobalGameState.has_looked_back_at_a = true
	
	# Place 1.0m directly behind the player's current gaze direction
	var cam = player.get_node_or_null("Head/Camera3D")
	if cam:
		var behind = cam.global_transform.basis.z.normalized()
		global_position = player.global_position + (behind * 1.2)
		global_position.y = 0.0 # Snap to floor
		look_at(player.global_position, Vector3.UP)
		if head_bone:
			head_bone.rotation_degrees = Vector3(45.0, 0.0, 25.0)
			
	SoundManager.play_sub_bass_drop()
	SoundManager.play_scrape_cue()
