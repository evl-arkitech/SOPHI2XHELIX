# ==============================================================================
# DoubleHelix Neural Agent Engine (DoubleHelix.Go Edition)
# Asset Library & Modular 3D Kit Generator for Godot 4.7
# Cosmic Souls of Sovereignty Inc. • arkade.new-world-arkitech.dev
# ==============================================================================
@tool
class_name DoubleHelixAssetLibrary
extends RefCounted

const MaterialBuilder = preload("res://addons/doublehelix_engine/material_builder.gd")

## Catalog of remote Arkade storage assets
const ARKADE_ASSETS_CATALOG: Dictionary = {
	"pbr_textures": [
		{"id": "walnut_wood", "label": "Walnut Wood PBR 2K", "category": "Textures", "url": "textures/pbr/wood/walnut_diffuse_2k.jpg"},
		{"id": "tile", "label": "Ceramic Tile PBR 2K", "category": "Textures", "url": "textures/pbr/tiles/tile_diffuse_2k.jpg"},
		{"id": "drywall_plaster", "label": "Drywall Plaster PBR 2K", "category": "Textures", "url": "textures/pbr/drywall/plaster_diffuse_2k.jpg"},
		{"id": "exterior_brick", "label": "Exterior Brick PBR 2K", "category": "Textures", "url": "textures/pbr/brick/brick_diffuse_2k.jpg"},
		{"id": "granite_countertop", "label": "Granite Slab PBR 2K", "category": "Textures", "url": "textures/pbr/kitchen/granite_diffuse_2k.jpg"},
		{"id": "brushed_steel", "label": "Brushed Steel Normal", "category": "Textures", "url": "textures/pbr/metal/steel_brushed_normal.jpg"},
		{"id": "rain_glass", "label": "Rain Droplets Glass", "category": "Textures", "url": "textures/pbr/glass/glass_rain_normal.jpg"}
	],
	"blueprints": [
		{"id": "blueprint_colonial", "label": "Colonial House Architectural Layout", "category": "Blueprints", "url": "art/blueprint_level1_colonial.jpg"},
		{"id": "blueprint_tenement", "label": "Urban Tenement Floorplan", "category": "Blueprints", "url": "blueprints/tactical_house_blueprint.png"}
	],
	"clothing_models": [
		{"id": "denim_dark_d", "label": "Intruder Denim Dark Albedo", "category": "Clothing", "url": "clothing/unreal_pbr/T_Denim_Dark_D.png"},
		{"id": "denim_dark_n", "label": "Intruder Denim Dark Normal", "category": "Clothing", "url": "clothing/unreal_pbr/T_Denim_Dark_N.png"}
	]
}

## Procedurally builds modular 3D props with PBR materials and physics colliders
static func generate_modular_prop(prop_type: String) -> Node3D:
	match prop_type:
		"tactical_crate":
			return build_tactical_crate()
		"security_door":
			return build_security_door()
		"tactical_desk":
			return build_tactical_desk()
		"gun_cabinet":
			return build_gun_cabinet()
		"concrete_barrier":
			return build_concrete_barrier()
		"security_camera":
			return build_security_camera()
		_:
			return build_tactical_crate()

## Builds a 1m x 1m x 1m wooden/metal tactical cover crate
static func build_tactical_crate() -> StaticBody3D:
	var body = StaticBody3D.new()
	body.name = "TacticalCrate"

	var mesh_inst = MeshInstance3D.new()
	var box = BoxMesh.new()
	box.size = Vector3(1.0, 1.0, 1.0)
	mesh_inst.mesh = box
	mesh_inst.material_override = MaterialBuilder.build_preset("walnut_wood")
	body.add_child(mesh_inst)

	var col = CollisionShape3D.new()
	var c_box = BoxShape3D.new()
	c_box.size = Vector3(1.0, 1.0, 1.0)
	col.shape = c_box
	body.add_child(col)

	return body

## Builds a heavy steel security door with frame
static func build_security_door() -> Node3D:
	var door_root = Node3D.new()
	door_root.name = "SecurityDoorAssembly"

	# Outer Frame
	var frame_body = StaticBody3D.new()
	frame_body.name = "DoorFrame"
	door_root.add_child(frame_body)

	# Left Post
	var left_post = MeshInstance3D.new()
	var post_box = BoxMesh.new()
	post_box.size = Vector3(0.12, 2.2, 0.15)
	left_post.mesh = post_box
	left_post.position = Vector3(-0.55, 1.1, 0)
	left_post.material_override = MaterialBuilder.build_preset("brushed_steel")
	frame_body.add_child(left_post)

	# Right Post
	var right_post = MeshInstance3D.new()
	right_post.mesh = post_box
	right_post.position = Vector3(0.55, 1.1, 0)
	right_post.material_override = MaterialBuilder.build_preset("brushed_steel")
	frame_body.add_child(right_post)

	# Door Leaf
	var leaf_body = StaticBody3D.new()
	leaf_body.name = "DoorLeaf"
	leaf_body.position = Vector3(0, 1.05, 0)
	door_root.add_child(leaf_body)

	var leaf_mesh = MeshInstance3D.new()
	var leaf_box = BoxMesh.new()
	leaf_box.size = Vector3(0.96, 2.1, 0.06)
	leaf_mesh.mesh = leaf_box
	leaf_mesh.material_override = MaterialBuilder.build_preset("brushed_steel")
	leaf_body.add_child(leaf_mesh)

	var leaf_col = CollisionShape3D.new()
	var lc_box = BoxShape3D.new()
	lc_box.size = Vector3(0.96, 2.1, 0.06)
	leaf_col.shape = lc_box
	leaf_body.add_child(leaf_col)

	return door_root

## Builds a tactical operational desk
static func build_tactical_desk() -> StaticBody3D:
	var desk = StaticBody3D.new()
	desk.name = "TacticalDesk"

	# Tabletop
	var top = MeshInstance3D.new()
	var top_box = BoxMesh.new()
	top_box.size = Vector3(1.8, 0.08, 0.9)
	top.mesh = top_box
	top.position = Vector3(0, 0.75, 0)
	top.material_override = MaterialBuilder.build_preset("granite_countertop")
	desk.add_child(top)

	# Legs
	var leg_box = BoxMesh.new()
	leg_box.size = Vector3(0.08, 0.72, 0.08)
	var leg_mat = MaterialBuilder.build_preset("brushed_steel")
	for x in [-0.8, 0.8]:
		for z in [-0.38, 0.38]:
			var leg = MeshInstance3D.new()
			leg.mesh = leg_box
			leg.position = Vector3(x, 0.36, z)
			leg.material_override = leg_mat
			desk.add_child(leg)

	# Collision
	var col = CollisionShape3D.new()
	var c_box = BoxShape3D.new()
	c_box.size = Vector3(1.8, 0.76, 0.9)
	col.shape = c_box
	col.position = Vector3(0, 0.38, 0)
	desk.add_child(col)

	return desk

## Builds a reinforced gun / security cabinet
static func build_gun_cabinet() -> StaticBody3D:
	var cabinet = StaticBody3D.new()
	cabinet.name = "GunCabinet"

	var mesh = MeshInstance3D.new()
	var box = BoxMesh.new()
	box.size = Vector3(0.8, 1.8, 0.5)
	mesh.mesh = box
	mesh.position = Vector3(0, 0.9, 0)
	mesh.material_override = MaterialBuilder.build_preset("brushed_steel")
	cabinet.add_child(mesh)

	var col = CollisionShape3D.new()
	var c_box = BoxShape3D.new()
	c_box.size = Vector3(0.8, 1.8, 0.5)
	col.shape = c_box
	col.position = Vector3(0, 0.9, 0)
	cabinet.add_child(col)

	return cabinet

## Builds a concrete jersey road / tactical barricade
static func build_concrete_barrier() -> StaticBody3D:
	var barrier = StaticBody3D.new()
	barrier.name = "ConcreteBarricade"

	var mesh = MeshInstance3D.new()
	var box = BoxMesh.new()
	box.size = Vector3(2.5, 1.1, 0.6)
	mesh.mesh = box
	mesh.position = Vector3(0, 0.55, 0)
	mesh.material_override = MaterialBuilder.build_preset("tactical_concrete")
	barrier.add_child(mesh)

	var col = CollisionShape3D.new()
	var c_box = BoxShape3D.new()
	c_box.size = Vector3(2.5, 1.1, 0.6)
	col.shape = c_box
	col.position = Vector3(0, 0.55, 0)
	barrier.add_child(col)

	return barrier

## Builds a corner mounted surveillance security camera
static func build_security_camera() -> Node3D:
	var cam_mount = Node3D.new()
	cam_mount.name = "SurveillanceSecurityCameraMount"

	# Bracket
	var bracket = MeshInstance3D.new()
	var b_box = BoxMesh.new()
	b_box.size = Vector3(0.1, 0.1, 0.25)
	bracket.mesh = b_box
	bracket.material_override = MaterialBuilder.build_preset("brushed_steel")
	cam_mount.add_child(bracket)

	# Camera Body
	var body = MeshInstance3D.new()
	var c_box = BoxMesh.new()
	c_box.size = Vector3(0.18, 0.14, 0.35)
	body.mesh = c_box
	body.position = Vector3(0, -0.08, 0.18)
	body.rotation_degrees = Vector3(-20.0, 0, 0)
	body.material_override = MaterialBuilder.build_preset("brushed_steel")
	cam_mount.add_child(body)

	# Red LED indicator
	var led = OmniLight3D.new()
	led.name = "RecIndicatorLED"
	led.position = Vector3(0, -0.06, 0.36)
	led.light_color = Color(1.0, 0.15, 0.15)
	led.light_energy = 0.8
	led.omni_range = 1.5
	cam_mount.add_child(led)

	return cam_mount

## Saves any generated prop to res://props/<prop_name>.tscn
static func save_prop_to_scene(prop_node: Node, prop_name: String) -> String:
	var scene = PackedScene.new()
	var pack_res = scene.pack(prop_node)
	if pack_res != OK:
		return ""

	var dir_path = "res://props"
	var global_dir = ProjectSettings.globalize_path(dir_path)
	DirAccess.make_dir_recursive_absolute(global_dir)

	var file_path = dir_path + "/" + prop_name.to_snake_case().validate_filename() + ".tscn"
	var save_res = ResourceSaver.save(scene, file_path)
	if save_res == OK:
		print("[DoubleHelix AssetLibrary] Saved prop scene: " + file_path)
		return file_path
	return ""
