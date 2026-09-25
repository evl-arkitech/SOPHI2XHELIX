# ==============================================================================
# DoubleHelix Neural Agent Engine (DoubleHelix.Go Edition)
# Procedural 3D Scene & Tactical Level Generator for Godot 4.7
# Cosmic Souls of Sovereignty Inc. • arkade.new-world-arkitech.dev
# ==============================================================================
@tool
class_name DoubleHelixSceneGenerator
extends RefCounted

const MaterialBuilder = preload("res://addons/doublehelix_engine/material_builder.gd")

## Builds a complete 3-room tactical residence (City Echoes layout)
static func generate_tactical_residence(output_path: String = "scenes/tactical_residence.tscn") -> Dictionary:
	var root = Node3D.new()
	root.name = "TacticalResidence"

	# Build Room 1: Refuge Bedroom (10m x 8m)
	var bedroom = build_room_node(
		"RefugeBedroom",
		Vector3(0, 0, 0),
		Vector3(10.0, 3.2, 8.0),
		"walnut_wood",
		"drywall_plaster",
		true, # has door to corridor
		Vector3(0, 0, 4.0),
		true, # has window
		Vector3(-5.0, 1.2, 0)
	)
	root.add_child(bedroom)
	bedroom.owner = root

	# Build Room 2: Living Corridor (16m x 10m)
	var corridor = build_room_node(
		"LivingCorridor",
		Vector3(0, 0, 9.0),
		Vector3(16.0, 3.2, 10.0),
		"polished_tile",
		"drywall_plaster",
		true, # door to mudroom
		Vector3(8.0, 0, 0),
		false,
		Vector3.ZERO
	)
	root.add_child(corridor)
	corridor.owner = root

	# Build Room 3: Mudroom & Rear Exit (8m x 6m)
	var mudroom = build_room_node(
		"MudroomRearExit",
		Vector3(12.0, 0, 9.0),
		Vector3(8.0, 3.2, 6.0),
		"granite_countertop",
		"exterior_brick",
		true, # exterior back door
		Vector3(4.0, 0, 0),
		true, # exterior window
		Vector3(0, 1.2, -3.0)
	)
	root.add_child(mudroom)
	mudroom.owner = root

	# Spawn Points
	var occupant_spawn = Marker3D.new()
	occupant_spawn.name = "OccupantDefenderSpawn"
	occupant_spawn.position = Vector3(0, 0.2, 0)
	root.add_child(occupant_spawn)
	occupant_spawn.owner = root

	var intruder_spawn = Marker3D.new()
	intruder_spawn.name = "IntruderInfiltratorSpawn"
	intruder_spawn.position = Vector3(18.0, 0.2, 9.0) # Outside rear mudroom exit
	root.add_child(intruder_spawn)
	intruder_spawn.owner = root

	# Exterior Lighting (Carriage Sconce for Intruder Visibility)
	var ext_light = OmniLight3D.new()
	ext_light.name = "MudroomExteriorSconce"
	ext_light.position = Vector3(16.5, 2.2, 9.0)
	ext_light.light_color = Color(1.0, 0.88, 0.72)
	ext_light.light_energy = 2.4
	ext_light.omni_range = 14.0
	ext_light.shadow_enabled = true
	root.add_child(ext_light)
	ext_light.owner = root

	# Corridor Corner CCTV Camera
	var cctv = Camera3D.new()
	cctv.name = "SurveillanceCCTV_Cam1"
	cctv.position = Vector3(-7.2, 3.0, 4.8)
	cctv.rotation_degrees = Vector3(-25.0, -45.0, 0.0)
	root.add_child(cctv)
	cctv.owner = root

	# Recursively assign owner to all descendant nodes so PackedScene includes them
	set_owner_recursive(root, root)

	# Save PackedScene
	var scene = PackedScene.new()
	var pack_res = scene.pack(root)
	if pack_res != OK:
		root.free()
		return {"error": "Failed to pack scene", "code": pack_res}

	var res_path = "res://" + output_path.trim_prefix("res://")
	var global_dir = ProjectSettings.globalize_path(res_path.get_base_dir())
	DirAccess.make_dir_recursive_absolute(global_dir)

	var save_res = ResourceSaver.save(scene, res_path)
	root.free()

	if save_res != OK:
		return {"error": "Failed to save scene", "code": save_res}

	return {
		"success": true,
		"scene_path": res_path,
		"rooms": 3,
		"occupant_spawn": "Vector3(0, 0.2, 0)",
		"intruder_spawn": "Vector3(18, 0.2, 9)",
		"cctv_camera": true
	}

## Builds an individual room with floor, ceiling, 4 walls, and optional door/window cutouts
static func build_room_node(
	room_name: String,
	origin: Vector3,
	dimensions: Vector3,
	floor_mat_name: String,
	wall_mat_name: String,
	has_door: bool,
	door_offset: Vector3,
	has_window: bool,
	window_offset: Vector3
) -> Node3D:
	var room = Node3D.new()
	room.name = room_name
	room.position = origin

	var w = dimensions.x
	var h = dimensions.y
	var l = dimensions.z

	var floor_mat = MaterialBuilder.build_preset(floor_mat_name)
	var wall_mat = MaterialBuilder.build_preset(wall_mat_name)

	# 1. Floor
	create_box_collider_mesh(room, "Floor", Vector3(0, 0, 0), Vector3(w, 0.2, l), floor_mat)

	# 2. Ceiling
	create_box_collider_mesh(room, "Ceiling", Vector3(0, h, 0), Vector3(w, 0.2, l), wall_mat)

	# 3. Walls
	create_box_collider_mesh(room, "WallNorth", Vector3(0, h/2.0, -l/2.0), Vector3(w, h, 0.2), wall_mat)
	create_box_collider_mesh(room, "WallSouth", Vector3(0, h/2.0, l/2.0), Vector3(w, h, 0.2), wall_mat)
	create_box_collider_mesh(room, "WallWest", Vector3(-w/2.0, h/2.0, 0), Vector3(0.2, h, l), wall_mat)
	create_box_collider_mesh(room, "WallEast", Vector3(w/2.0, h/2.0, 0), Vector3(0.2, h, l), wall_mat)

	# 4. Interior Ceiling Downlight
	var light = OmniLight3D.new()
	light.name = "CeilingLight"
	light.position = Vector3(0, h - 0.3, 0)
	light.light_energy = 1.6
	light.omni_range = max(w, l) * 0.9
	light.shadow_enabled = true
	room.add_child(light)

	# 5. Interactive Door if specified
	if has_door:
		var door_body = StaticBody3D.new()
		door_body.name = "HingedDoor"
		door_body.position = door_offset + Vector3(0, 1.1, 0)
		var d_mesh = MeshInstance3D.new()
		var d_box = BoxMesh.new()
		d_box.size = Vector3(0.9, 2.1, 0.08)
		d_mesh.mesh = d_box
		d_mesh.material_override = MaterialBuilder.build_preset("walnut_wood")
		door_body.add_child(d_mesh)

		var d_col = CollisionShape3D.new()
		var dc_box = BoxShape3D.new()
		dc_box.size = Vector3(0.9, 2.1, 0.08)
		d_col.shape = dc_box
		door_body.add_child(d_col)
		room.add_child(door_body)

	# 6. Window with bulletproof glass if specified
	if has_window:
		var win = MeshInstance3D.new()
		win.name = "ExteriorWindowGlass"
		win.position = window_offset
		var win_mesh = BoxMesh.new()
		win_mesh.size = Vector3(1.6, 1.2, 0.1)
		win.mesh = win_mesh
		win.material_override = MaterialBuilder.build_preset("bulletproof_glass")
		room.add_child(win)

	return room

## Utility to create static body + mesh instance + collision shape
static func create_box_collider_mesh(
	parent: Node,
	part_name: String,
	pos: Vector3,
	size: Vector3,
	mat: Material
) -> StaticBody3D:
	var body = StaticBody3D.new()
	body.name = part_name + "StaticBody"
	body.position = pos
	parent.add_child(body)

	var mesh_inst = MeshInstance3D.new()
	mesh_inst.name = part_name + "Mesh"
	var b_mesh = BoxMesh.new()
	b_mesh.size = size
	mesh_inst.mesh = b_mesh
	if mat:
		mesh_inst.material_override = mat
	body.add_child(mesh_inst)

	var col = CollisionShape3D.new()
	col.name = part_name + "Collision"
	var c_box = BoxShape3D.new()
	c_box.size = size
	col.shape = c_box
	body.add_child(col)

	return body

static func set_owner_recursive(node: Node, new_owner: Node) -> void:
	for child in node.get_children():
		child.owner = new_owner
		set_owner_recursive(child, new_owner)
