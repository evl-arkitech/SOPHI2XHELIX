# @tool
class_name TacticalCCTVMonitor
extends Node3D

## In-World Physical Security Monitor (Diegetic CCTV)
## Renders a live 3D SubViewport camera feed directly onto an in-game CRT/LCD screen mesh.
## Zero HUD overlays: the player must physically stand before the monitor in the hallway.

@export var camera_path: NodePath
@export var update_fps: float = 30.0

@onready var sub_viewport: SubViewport = $SubViewport
@onready var screen_mesh: MeshInstance3D = $ScreenMesh

var target_camera: Camera3D = null
var screen_material: StandardMaterial3D = null

func _ready() -> void:
	if not sub_viewport:
		return
		
	# Find target camera in world
	if not camera_path.is_empty():
		target_camera = get_node_or_null(camera_path) as Camera3D
	else:
		target_camera = get_tree().root.find_child("SurveillanceCCTV_Cam1", true, false) as Camera3D
		
	if target_camera:
		# Reparent or duplicate camera view to SubViewport
		var cam_clone = Camera3D.new()
		cam_clone.global_transform = target_camera.global_transform
		cam_clone.fov = target_camera.fov
		sub_viewport.add_child(cam_clone)
		cam_clone.current = true
		
	# Setup screen material to display viewport texture
	if screen_mesh:
		var tex = sub_viewport.get_texture()
		screen_material = StandardMaterial3D.new()
		screen_material.albedo_texture = tex
		screen_material.emission_enabled = true
		screen_material.emission_texture = tex
		screen_material.emission_energy_multiplier = 0.85
		screen_mesh.material_override = screen_material
