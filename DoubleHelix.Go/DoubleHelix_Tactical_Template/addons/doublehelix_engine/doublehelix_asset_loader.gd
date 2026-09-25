# ==============================================================================
# DoubleHelix Neural Agent Engine (DoubleHelix.Go Edition)
# Universal Remote & Local Asset Loader for Godot 4.7
# Cosmic Souls of Sovereignty Inc. • arkade.new-world-arkitech.dev
# ==============================================================================
extends Node

signal asset_download_completed(path: String, success: bool)

const DEFAULT_STORAGE_CONTAINER: String = "https://arkade.new-world-arkitech.dev/assets"
const CACHE_DIR: String = "user://asset_cache/"

var storage_container_url: String = DEFAULT_STORAGE_CONTAINER
var manifest: Dictionary = {}
var memory_texture_cache: Dictionary = {}

func _ready() -> void:
	# Ensure user cache directory exists
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(CACHE_DIR))
	load_manifest()

func load_manifest() -> void:
	var manifest_path = "res://assets/doublehelix_asset_manifest.json"
	if FileAccess.file_exists(manifest_path):
		var file = FileAccess.open(manifest_path, FileAccess.READ)
		if file:
			var parsed = JSON.parse_string(file.get_as_text())
			if parsed is Dictionary:
				manifest = parsed
				if manifest.has("storage_container_url"):
					storage_container_url = manifest["storage_container_url"]

	# Check project settings override
	if ProjectSettings.has_setting("doublehelix/business/storage_container"):
		storage_container_url = str(ProjectSettings.get_setting("doublehelix/business/storage_container"))

func resolve_asset_url(rel_path: String) -> String:
	if rel_path.begins_with("http://") or rel_path.begins_with("https://"):
		return rel_path
	var clean = rel_path.trim_prefix("res://").trim_prefix("/")
	if clean.begins_with("assets/"):
		clean = clean.substr(7)
	return storage_container_url.rstrip("/") + "/" + clean

func get_cache_file_path(rel_path: String) -> String:
	var safe_name = rel_path.replace("/", "_").replace("\\", "_").replace(":", "_")
	return CACHE_DIR + safe_name

## Synchronous texture loader with multi-tier resolution:
## Tier 1: Memory Cache
## Tier 2: Local res://assets/ path
## Tier 3: Disk cache in user://asset_cache/
## Tier 4: Fallback procedural checker texture
func load_texture(rel_path: String) -> Texture2D:
	if memory_texture_cache.has(rel_path):
		return memory_texture_cache[rel_path]

	# 1. Check local res://
	var res_candidates = [
		rel_path,
		"res://" + rel_path.trim_prefix("res://"),
		"res://assets/" + rel_path.trim_prefix("res://").trim_prefix("assets/")
	]
	for cand in res_candidates:
		if ResourceLoader.exists(cand):
			var tex = load(cand)
			if tex is Texture2D:
				memory_texture_cache[rel_path] = tex
				return tex

	# 2. Check disk cache
	var cache_file = get_cache_file_path(rel_path)
	if FileAccess.file_exists(cache_file):
		var img = Image.new()
		var err = img.load(cache_file)
		if err == OK:
			var tex = ImageTexture.create_from_image(img)
			memory_texture_cache[rel_path] = tex
			return tex

	# 3. Procedural Fallback
	var fallback = generate_fallback_texture()
	memory_texture_cache[rel_path] = fallback
	return fallback

## Builds a standard PBR material with Diffuse, Normal, Roughness, and Metallic
func create_pbr_material(
	diffuse_rel_path: String,
	normal_rel_path: String = "",
	roughness_rel_path: String = "",
	metallic: float = 0.0,
	uv_scale: Vector3 = Vector3(1.0, 1.0, 1.0)
) -> StandardMaterial3D:
	var mat = StandardMaterial3D.new()
	mat.albedo_texture = load_texture(diffuse_rel_path)

	if normal_rel_path != "":
		mat.normal_enabled = true
		mat.normal_texture = load_texture(normal_rel_path)

	if roughness_rel_path != "":
		mat.roughness_texture = load_texture(roughness_rel_path)

	mat.metallic = metallic
	mat.uv1_scale = uv_scale
	return mat

## Creates material from registered PBR preset in manifest
func create_material_from_preset(preset_name: String) -> StandardMaterial3D:
	if manifest.has("pbr_materials") and manifest["pbr_materials"].has(preset_name):
		var pbr = manifest["pbr_materials"][preset_name]
		var albedo = pbr.get("albedo", "")
		var normal = pbr.get("normal", "")
		var roughness = pbr.get("roughness", "")
		var metallic = float(pbr.get("metallic", 0.0))
		var uv = Vector3(1.0, 1.0, 1.0)
		if pbr.has("uv_scale") and pbr["uv_scale"].size() >= 2:
			uv = Vector3(pbr["uv_scale"][0], pbr["uv_scale"][1], 1.0)
		return create_pbr_material(albedo, normal, roughness, metallic, uv)

	# Default fallback material
	var fallback_mat = StandardMaterial3D.new()
	fallback_mat.albedo_color = Color(0.2, 0.25, 0.3)
	return fallback_mat

## Asynchronously downloads an asset from arkade.new-world-arkitech.dev into user cache
func download_asset_async(rel_path: String) -> void:
	var remote_url = resolve_asset_url(rel_path)
	var cache_dest = get_cache_file_path(rel_path)

	var http = HTTPRequest.new()
	add_child(http)
	http.request_completed.connect(func(result, response_code, headers, body):
		if response_code == 200:
			var f = FileAccess.open(cache_dest, FileAccess.WRITE)
			if f:
				f.store_buffer(body)
			asset_download_completed.emit(rel_path, true)
		else:
			asset_download_completed.emit(rel_path, false)
		http.queue_free()
	)
	http.request(remote_url)

## Generates a procedural 64x64 grid pattern for missing textures
func generate_fallback_texture() -> ImageTexture:
	var img = Image.create(64, 64, false, Image.FORMAT_RGBA8)
	for y in range(64):
		for x in range(64):
			var is_even = ((x / 8) + (y / 8)) % 2 == 0
			var col = Color(0.2, 0.22, 0.28) if is_even else Color(0.12, 0.14, 0.18)
			img.set_pixel(x, y, col)
	return ImageTexture.create_from_image(img)
