# ==============================================================================
# DoubleHelix Neural Agent Engine (DoubleHelix.Go Edition)
# Workflow Accelerator, Camera Rigs & Lighting Moods for Godot 4.7
# Cosmic Souls of Sovereignty Inc. • arkade.new-world-arkitech.dev
# ==============================================================================
@tool
class_name DoubleHelixWorkflowTools
extends RefCounted

## Instantiates a complete First-Person Tactical Character Controller
static func setup_fps_player_rig(parent: Node, spawn_pos: Vector3 = Vector3(0, 0.2, 0)) -> CharacterBody3D:
	var player = CharacterBody3D.new()
	player.name = "DoubleHelixFPSPlayer"
	player.position = spawn_pos
	parent.add_child(player)
	player.owner = parent

	# 1. Capsule Collision Shape
	var col = CollisionShape3D.new()
	col.name = "PlayerCollision"
	var cap = CapsuleShape3D.new()
	cap.radius = 0.4
	cap.height = 1.8
	col.shape = cap
	col.position = Vector3(0, 0.9, 0)
	player.add_child(col)
	col.owner = parent

	# 2. Head & Camera Pivot
	var head = Node3D.new()
	head.name = "HeadPivot"
	head.position = Vector3(0, 1.65, 0)
	player.add_child(head)
	head.owner = parent

	var cam = Camera3D.new()
	cam.name = "Camera3D"
	cam.current = true
	head.add_child(cam)
	cam.owner = parent

	# 3. Tactical Flashlight
	var flashlight = SpotLight3D.new()
	flashlight.name = "TacticalFlashlight"
	flashlight.position = Vector3(0.2, -0.15, -0.2)
	flashlight.light_energy = 2.4
	flashlight.spot_range = 28.0
	flashlight.spot_angle = 32.0
	flashlight.spot_attenuation = 1.2
	flashlight.shadow_enabled = true
	head.add_child(flashlight)
	flashlight.owner = parent

	# 4. Interaction RayCast
	var ray = RayCast3D.new()
	ray.name = "InteractionRay"
	ray.target_position = Vector3(0, 0, -2.5)
	ray.enabled = true
	head.add_child(ray)
	ray.owner = parent

	print("[DoubleHelix Workflow] Instantiated FPS Tactical Player Rig at: " + str(spawn_pos))
	return player

## Instantiates a Third-Person Over-The-Shoulder Camera Rig
static func setup_third_person_rig(parent: Node, spawn_pos: Vector3 = Vector3(0, 0.2, 0)) -> CharacterBody3D:
	var player = CharacterBody3D.new()
	player.name = "DoubleHelixThirdPersonPlayer"
	player.position = spawn_pos
	parent.add_child(player)
	player.owner = parent

	var col = CollisionShape3D.new()
	col.name = "PlayerCollision"
	var cap = CapsuleShape3D.new()
	cap.radius = 0.4
	cap.height = 1.8
	col.shape = cap
	col.position = Vector3(0, 0.9, 0)
	player.add_child(col)
	col.owner = parent

	# SpringArm Pivot
	var arm = SpringArm3D.new()
	arm.name = "SpringArm3D"
	arm.position = Vector3(0.45, 1.6, 0) # Over-the-shoulder offset
	arm.spring_length = 2.4
	arm.margin = 0.2
	player.add_child(arm)
	arm.owner = parent

	var cam = Camera3D.new()
	cam.name = "Camera3D"
	cam.current = true
	arm.add_child(cam)
	cam.owner = parent

	print("[DoubleHelix Workflow] Instantiated Third-Person Tactical Rig at: " + str(spawn_pos))
	return player

## Applies atmospheric lighting mood presets to the active scene
static func apply_lighting_mood(scene_root: Node, mood_name: String) -> void:
	# Find or create WorldEnvironment
	var env_node = scene_root.find_child("WorldEnvironment", true, false)
	if not env_node:
		env_node = WorldEnvironment.new()
		env_node.name = "WorldEnvironment"
		scene_root.add_child(env_node)
		env_node.owner = scene_root

	var env = Environment.new()
	match mood_name:
		"cinematic_noir":
			env.background_mode = Environment.BG_COLOR
			env.background_color = Color(0.015, 0.02, 0.035)
			env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
			env.ambient_light_color = Color(0.04, 0.06, 0.12)
			env.ambient_light_energy = 0.35
			env.glow_enabled = true
			env.glow_bloom = 0.15
			env.volumetric_fog_enabled = true
			env.volumetric_fog_density = 0.025
			env.volumetric_fog_albedo = Color(0.1, 0.14, 0.22)
		"tactical_blackout":
			env.background_mode = Environment.BG_COLOR
			env.background_color = Color(0.005, 0.006, 0.01)
			env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
			env.ambient_light_color = Color(0.01, 0.015, 0.02)
			env.ambient_light_energy = 0.1
			env.glow_enabled = true
			env.volumetric_fog_enabled = true
			env.volumetric_fog_density = 0.04
		"daylight_operational":
			env.background_mode = Environment.BG_COLOR
			env.background_color = Color(0.55, 0.72, 0.95)
			env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
			env.ambient_light_color = Color(0.7, 0.8, 0.9)
			env.ambient_light_energy = 1.0
			env.glow_enabled = false
			env.volumetric_fog_enabled = false

	env_node.environment = env
	print("[DoubleHelix Workflow] Applied Lighting Mood: " + mood_name)

## Ensures all MeshInstance3D nodes in scene have physics colliders (zero tunneling)
static func ensure_collision_on_meshes(scene_root: Node) -> int:
	var added = 0
	var queue = [scene_root]

	while queue.size() > 0:
		var node = queue.pop_front()
		if node is MeshInstance3D and node.mesh:
			# Check if already has CollisionObject3D ancestor
			var parent = node.get_parent()
			var has_collider = false
			while parent and parent != scene_root.get_parent():
				if parent is CollisionObject3D:
					has_collider = true
					break
				parent = parent.get_parent()

			if not has_collider:
				var aabb = node.mesh.get_aabb()
				var body = StaticBody3D.new()
				body.name = node.name + "AutoCollider"
				body.position = node.position
				node.get_parent().add_child(body)
				body.owner = scene_root

				var col = CollisionShape3D.new()
				col.name = "Shape"
				var b_shape = BoxShape3D.new()
				b_shape.size = aabb.size
				col.shape = b_shape
				col.position = aabb.get_center()
				body.add_child(col)
				col.owner = scene_root
				added += 1

		for c in node.get_children():
			queue.push_back(c)

	print("[DoubleHelix Workflow] Auto-generated " + str(added) + " collision shapes.")
	return added
