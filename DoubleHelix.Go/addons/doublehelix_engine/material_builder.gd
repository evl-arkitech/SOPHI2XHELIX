# ==============================================================================
# DoubleHelix Neural Agent Engine (DoubleHelix.Go Edition)
# Interactive PBR Material Builder & Preset Assembler for Godot 4.7
# Cosmic Souls of Sovereignty Inc. • arkade.new-world-arkitech.dev
# ==============================================================================
@tool
class_name DoubleHelixMaterialBuilder
extends RefCounted

const STORAGE_CONTAINER_DEFAULT: String = "https://arkade.new-world-arkitech.dev/assets"

## Standard PBR preset library with remote Arkade & local paths
const PRESETS: Dictionary = {
	"walnut_wood": {
		"name": "Walnut Hardwood Floor",
		"albedo": "textures/pbr/wood/walnut_diffuse_2k.jpg",
		"normal": "textures/pbr/wood/walnut_normal_2k.jpg",
		"roughness": "textures/pbr/wood/walnut_roughness_2k.jpg",
		"metallic": 0.0,
		"roughness_val": 0.65,
		"uv_scale": Vector3(2.0, 2.0, 1.0)
	},
	"polished_tile": {
		"name": "Polished Ceramic Tile",
		"albedo": "textures/pbr/tiles/tile_diffuse_2k.jpg",
		"normal": "textures/pbr/tiles/tile_normal_2k.jpg",
		"roughness": "textures/pbr/tiles/tile_roughness_2k.jpg",
		"metallic": 0.05,
		"roughness_val": 0.25,
		"uv_scale": Vector3(3.0, 3.0, 1.0)
	},
	"drywall_plaster": {
		"name": "Interior Drywall Plaster",
		"albedo": "textures/pbr/drywall/plaster_diffuse_2k.jpg",
		"normal": "textures/pbr/drywall/plaster_normal_2k.jpg",
		"roughness": "textures/pbr/drywall/plaster_roughness_2k.jpg",
		"metallic": 0.0,
		"roughness_val": 0.9,
		"uv_scale": Vector3(1.0, 1.0, 1.0)
	},
	"exterior_brick": {
		"name": "Weathered Urban Brick",
		"albedo": "textures/pbr/brick/brick_diffuse_2k.jpg",
		"normal": "textures/pbr/brick/brick_normal_2k.jpg",
		"roughness": "textures/pbr/brick/brick_roughness_2k.jpg",
		"metallic": 0.0,
		"roughness_val": 0.85,
		"uv_scale": Vector3(3.0, 3.0, 1.0)
	},
	"granite_countertop": {
		"name": "Kitchen Granite Slab",
		"albedo": "textures/pbr/kitchen/granite_diffuse_2k.jpg",
		"normal": "textures/pbr/kitchen/granite_normal_2k.jpg",
		"roughness": "textures/pbr/kitchen/granite_roughness_2k.jpg",
		"metallic": 0.1,
		"roughness_val": 0.35,
		"uv_scale": Vector3(1.5, 1.5, 1.0)
	},
	"brushed_steel": {
		"name": "Industrial Brushed Steel",
		"albedo": "textures/pbr/metal/steel_brushed_normal.jpg",
		"normal": "textures/pbr/metal/steel_brushed_normal.jpg",
		"roughness": "textures/pbr/drywall/plaster_roughness_2k.jpg",
		"metallic": 0.85,
		"roughness_val": 0.3,
		"uv_scale": Vector3(2.0, 2.0, 1.0)
	},
	"bulletproof_glass": {
		"name": "Reinforced Tactical Glass",
		"albedo": "",
		"normal": "textures/pbr/glass/glass_rain_normal.jpg",
		"metallic": 0.1,
		"roughness_val": 0.08,
		"transparency": BaseMaterial3D.TRANSPARENCY_ALPHA,
		"albedo_color": Color(0.85, 0.92, 0.98, 0.25),
		"refraction_enabled": true,
		"refraction_scale": 0.04
	},
	"tactical_concrete": {
		"name": "Tactical Bunker Concrete",
		"albedo": "textures/pbr/carpet/carpet_diffuse_2k.jpg", # fallback textured albedo
		"normal": "textures/pbr/drywall/plaster_normal_2k.jpg",
		"roughness": "textures/pbr/drywall/plaster_roughness_2k.jpg",
		"metallic": 0.0,
		"roughness_val": 0.95,
		"albedo_color": Color(0.45, 0.47, 0.5),
		"uv_scale": Vector3(4.0, 4.0, 1.0)
	},
	"neon_hologram": {
		"name": "Cyberpunk Neon Hologram",
		"albedo": "",
		"albedo_color": Color(0.1, 0.85, 0.95, 0.7),
		"emission_enabled": true,
		"emission": Color(0.1, 0.85, 0.95),
		"emission_energy_multiplier": 2.5,
		"transparency": BaseMaterial3D.TRANSPARENCY_ALPHA,
		"cull_mode": BaseMaterial3D.CULL_DISABLED
	}
}

## Constructs a complete StandardMaterial3D from a configuration dictionary
static func build_material(cfg: Dictionary) -> StandardMaterial3D:
	var mat = StandardMaterial3D.new()

	# 1. Albedo Color & Texture
	if cfg.has("albedo_color"):
		mat.albedo_color = cfg["albedo_color"]
	else:
		mat.albedo_color = Color.WHITE

	var albedo_path = cfg.get("albedo", "")
	if albedo_path != "":
		mat.albedo_texture = resolve_texture(albedo_path)

	# 2. Normal Map
	var normal_path = cfg.get("normal", "")
	if normal_path != "":
		mat.normal_enabled = true
		mat.normal_texture = resolve_texture(normal_path)
		mat.normal_scale = float(cfg.get("normal_scale", 1.0))

	# 3. Roughness
	var rough_path = cfg.get("roughness", "")
	if rough_path != "":
		mat.roughness_texture = resolve_texture(rough_path)
	mat.roughness = float(cfg.get("roughness_val", 0.5))

	# 4. Metallic
	var metal_path = cfg.get("metallic_texture", "")
	if metal_path != "":
		mat.metallic_texture = resolve_texture(metal_path)
	mat.metallic = float(cfg.get("metallic", 0.0))

	# 5. Ambient Occlusion
	var ao_path = cfg.get("ao_texture", "")
	if ao_path != "":
		mat.ao_enabled = true
		mat.ao_texture = resolve_texture(ao_path)

	# 6. Emission
	if cfg.get("emission_enabled", false):
		mat.emission_enabled = true
		mat.emission = cfg.get("emission", Color.WHITE)
		mat.emission_energy_multiplier = float(cfg.get("emission_energy_multiplier", 1.0))

	# 7. Transparency & Refraction
	if cfg.has("transparency"):
		mat.transparency = cfg["transparency"]
	if cfg.get("refraction_enabled", false):
		mat.refraction_enabled = true
		mat.refraction_scale = float(cfg.get("refraction_scale", 0.05))

	# 8. UV Scale & Triplanar
	if cfg.has("uv_scale"):
		mat.uv1_scale = cfg["uv_scale"]
	if cfg.get("uv1_triplanar", false):
		mat.uv1_triplanar = true

	if cfg.has("cull_mode"):
		mat.cull_mode = cfg["cull_mode"]

	return mat

## Builds material from registered preset identifier
static func build_preset(preset_key: String) -> StandardMaterial3D:
	if PRESETS.has(preset_key):
		return build_material(PRESETS[preset_key])
	return StandardMaterial3D.new()

## Saves material resource to disk at res://materials/<name>.tres
static func save_material_to_file(mat: StandardMaterial3D, material_name: String) -> String:
	var clean_name = material_name.to_snake_case().validate_filename()
	var dir_path = "res://materials"
	var global_dir = ProjectSettings.globalize_path(dir_path)
	DirAccess.make_dir_recursive_absolute(global_dir)

	var file_path = dir_path + "/" + clean_name + ".tres"
	var err = ResourceSaver.save(mat, file_path)
	if err == OK:
		print("[DoubleHelix MaterialBuilder] Saved material: " + file_path)
		return file_path
	else:
		print("[DoubleHelix MaterialBuilder] Failed to save material: " + str(err))
		return ""

## Resolves local or cached texture resource
static func resolve_texture(path: String) -> Texture2D:
	if path == "":
		return null

	var candidates = [
		path,
		"res://" + path.trim_prefix("res://"),
		"res://assets/" + path.trim_prefix("res://").trim_prefix("assets/"),
		"user://asset_cache/" + path.replace("/", "_").replace("\\", "_")
	]

	for cand in candidates:
		if ResourceLoader.exists(cand):
			var res = load(cand)
			if res is Texture2D:
				return res

	# Check disk cache file directly
	var cache_file = "user://asset_cache/" + path.replace("/", "_").replace("\\", "_")
	if FileAccess.file_exists(cache_file):
		var img = Image.new()
		if img.load(cache_file) == OK:
			return ImageTexture.create_from_image(img)

	return null
