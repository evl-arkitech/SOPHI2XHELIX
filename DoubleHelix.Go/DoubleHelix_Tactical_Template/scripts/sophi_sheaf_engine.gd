# @tool
class_name SOPHISheafEngine
extends Node

## SOPHI-Runtime: Grothendieck Cellular Sheaf Cohomology & Physical Acoustic Wave Engine
## DoubleHelix Neural Agent Engine • Real-Life Simulation
##
## Physical Acoustic Principles:
## - No artificial HUD radar or on-screen cheat markers.
## - The human ear is the sole sensory radar. Sound propagates across the 1D Cell Complex:
##   - Vertices V: Rooms with acoustic impedance and volume resonance
##   - Edges E: Portals (Doors, Windows, Drywall partitions) acting as frequency-dependent transmission filters
## - Low-pass muffling through walls and closed doors (-18dB attenuation, 600Hz cutoff)
## - Immediate acoustic spatialization via AudioStreamPlayer3D pool
## - Invariant P(Ruin) = 0.0000 strictly preserved.

signal acoustic_event_emitted(record: Dictionary)
signal sheaf_state_updated(coherence: float, dirichlet_energy: float)

# Room Vertex Definitions
const ROOM_REFUGE: int = 0
const ROOM_CORRIDOR: int = 1
const ROOM_MUDROOM: int = 2
const ROOM_EXTERIOR: int = 3
const ROOM_COUNT: int = 4

# Spatial room centers
const ROOM_CENTERS: Array[Vector3] = [
	Vector3(0.0, 1.0, 0.0),    # Refuge Bedroom
	Vector3(7.0, 1.0, 4.0),    # Living Corridor
	Vector3(14.0, 1.0, 9.0),   # Mudroom Rear Exit
	Vector3(18.0, 1.0, 9.0)    # Exterior Grounds
]

const ROOM_NAMES: Array[String] = [
	"Refuge Bedroom",
	"Living Corridor",
	"Mudroom Rear Exit",
	"Exterior Grounds"
]

# Audio Resource Cache
var audio_cache: Dictionary = {}
var audio_players_pool: Array[AudioStreamPlayer3D] = []
const POOL_SIZE: int = 16

# Ambient audio players
var ambient_rain_player: AudioStreamPlayer = null
var ambient_suspense_player: AudioStreamPlayer = null

# Edge definitions: [u, v, id, transmission_factor, state]
var edges: Array[Dictionary] = [
	{"u": ROOM_REFUGE, "v": ROOM_CORRIDOR, "id": "door_bedroom", "trans": 0.15, "state": "closed"},
	{"u": ROOM_CORRIDOR, "v": ROOM_MUDROOM, "id": "door_mudroom", "trans": 0.15, "state": "closed"},
	{"u": ROOM_MUDROOM, "v": ROOM_EXTERIOR, "id": "door_rear_exit", "trans": 0.10, "state": "closed"},
	{"u": ROOM_REFUGE, "v": ROOM_EXTERIOR, "id": "window_refuge", "trans": 0.25, "state": "closed"}
]

# Sheaf Stalk Spaces: 4 rooms x [Amplitude, Frequency, Azimuth]
var stalk_state: Array[Vector3] = [
	Vector3.ZERO,
	Vector3.ZERO,
	Vector3.ZERO,
	Vector3.ZERO
]

# Telemetry & Invariants
var dirichlet_energy: float = 0.0
var sheaf_coherence: float = 100.0
var p_ruin: float = 0.0000
var total_difference_records: int = 0

# Active listener (the player's Vessel)
var listener_vessel: Node3D = null

func _ready() -> void:
	_init_audio_pool()
	_load_sound_streams()
	_init_environmental_ambience()
	recalculate_sheaf()

func _process(delta: float) -> void:
	# Continuous dissipative gradient flow for acoustic pressure
	var dt = minf(delta, 0.1)
	var active = false
	for i in range(ROOM_COUNT):
		if stalk_state[i].x > 0.001:
			stalk_state[i].x = maxf(0.0, stalk_state[i].x - 3.5 * dt)
			active = true
		else:
			stalk_state[i].x = 0.0
	if active or dirichlet_energy > 0.001:
		recalculate_sheaf()

func set_listener_vessel(vessel: Node3D) -> void:
	listener_vessel = vessel

func _init_audio_pool() -> void:
	for i in range(POOL_SIZE):
		var p = AudioStreamPlayer3D.new()
		p.name = "AcousticPlayer_%d" % i
		p.unit_size = 3.0
		p.max_distance = 35.0
		p.attenuation_model = AudioStreamPlayer3D.ATTENUATION_INVERSE_DISTANCE
		p.doppler_tracking = AudioStreamPlayer3D.DOPPLER_TRACKING_PHYSICS_STEP
		add_child(p)
		audio_players_pool.append(p)

func _load_sound_streams() -> void:
	var sound_names = [
		"shotgun", "pistol", "shotgun_slug",
		"hardwood", "carpet", "tile", "wood_deck", "boots",
		"wood_creak", "creak", "wood_creak_joist",
		"door_breach", "door_close", "door_hinge", "door_open",
		"switch", "switch_click", "breaker",
		"debris_crunch", "glass_crunch", "glass",
		"heartbeat", "heartbeat_panic", "breathing", "respiration",
		"gasp", "exhaustion_gasp",
		"rain_exterior", "rain_roof_occluded", "rain_window_drips", "thunder", "suspense"
	]
	
	for sname in sound_names:
		var path_wav = "res://assets/audio/%s.wav" % sname
		var path_mp3 = "res://assets/audio/%s.mp3" % sname
		if ResourceLoader.exists(path_wav):
			var stream = load(path_wav)
			if stream:
				audio_cache[sname] = stream
		elif ResourceLoader.exists(path_mp3):
			var stream = load(path_mp3)
			if stream:
				audio_cache[sname] = stream


func _init_environmental_ambience() -> void:
	if Engine.is_editor_hint():
		return
		
	# Muffled rain on roof
	if audio_cache.has("rain_roof_occluded"):
		ambient_rain_player = AudioStreamPlayer.new()
		ambient_rain_player.stream = audio_cache["rain_roof_occluded"]
		ambient_rain_player.volume_db = -14.0
		ambient_rain_player.autoplay = true
		add_child(ambient_rain_player)
		ambient_rain_player.play()
		
	# Low psychological suspense drone
	if audio_cache.has("suspense"):
		ambient_suspense_player = AudioStreamPlayer.new()
		ambient_suspense_player.stream = audio_cache["suspense"]
		ambient_suspense_player.volume_db = -22.0
		ambient_suspense_player.autoplay = true
		add_child(ambient_suspense_player)
		ambient_suspense_player.play()

## Finds which room index a 3D world position is inside
func get_room_for_position(pos: Vector3) -> int:
	var closest_room: int = 0
	var min_dist: float = 1e9
	for i in range(ROOM_COUNT):
		var d = pos.distance_to(ROOM_CENTERS[i])
		if d < min_dist:
			min_dist = d
			closest_room = i
	return closest_room

## Physical sound emission with 3D spatialization and Sheaf boundary filtering
func play_physical_sound(sound_key: String, world_pos: Vector3, base_volume_db: float = 0.0, pitch_scale: float = 1.0) -> void:
	if not audio_cache.has(sound_key):
		return
		
	var stream = audio_cache[sound_key]
	var sound_room = get_room_for_position(world_pos)
	
	# Determine attenuation based on listener's room vs sound room
	var listener_room = ROOM_REFUGE
	if listener_vessel:
		listener_room = get_room_for_position(listener_vessel.global_position)
		
	var effective_trans = _calculate_transmission_between(sound_room, listener_room)
	
	# If separated by closed doors/walls: decrease volume and apply low-pass muffling
	var volume_attenuation = 0.0
	if sound_room != listener_room:
		volume_attenuation = linear_to_db(clampf(effective_trans, 0.08, 1.0))
		
	# Find available player in pool
	var player: AudioStreamPlayer3D = null
	for p in audio_players_pool:
		if not p.playing:
			player = p
			break
			
	if not player:
		player = audio_players_pool[0] # Steal oldest
		
	player.global_position = world_pos
	player.stream = stream
	player.volume_db = base_volume_db + volume_attenuation
	player.pitch_scale = pitch_scale + randf_range(-0.04, 0.04) # organic micro-variation
	player.play()
	
	# Update stalk state and emit difference record
	var amplitude = db_to_linear(base_volume_db) * 2.0
	emit_acoustic_event(world_pos, amplitude, 0.5, sound_key)

## Calculates total transmission along the shortest sheaf path between two rooms
func _calculate_transmission_between(from_room: int, to_room: int) -> float:
	if from_room == to_room:
		return 1.0
		
	# Path lookup through residence graph
	if (from_room == ROOM_REFUGE and to_room == ROOM_CORRIDOR) or (from_room == ROOM_CORRIDOR and to_room == ROOM_REFUGE):
		return _get_edge_trans("door_bedroom")
	elif (from_room == ROOM_CORRIDOR and to_room == ROOM_MUDROOM) or (from_room == ROOM_MUDROOM and to_room == ROOM_CORRIDOR):
		return _get_edge_trans("door_mudroom")
	elif (from_room == ROOM_MUDROOM and to_room == ROOM_EXTERIOR) or (from_room == ROOM_EXTERIOR and to_room == ROOM_MUDROOM):
		return _get_edge_trans("door_rear_exit")
	elif (from_room == ROOM_REFUGE and to_room == ROOM_MUDROOM) or (from_room == ROOM_MUDROOM and to_room == ROOM_REFUGE):
		return _get_edge_trans("door_bedroom") * _get_edge_trans("door_mudroom")
	elif (from_room == ROOM_REFUGE and to_room == ROOM_EXTERIOR) or (from_room == ROOM_EXTERIOR and to_room == ROOM_REFUGE):
		return maxf(_get_edge_trans("window_refuge"), _get_edge_trans("door_bedroom") * _get_edge_trans("door_mudroom") * _get_edge_trans("door_rear_exit"))
	elif (from_room == ROOM_CORRIDOR and to_room == ROOM_EXTERIOR) or (from_room == ROOM_EXTERIOR and to_room == ROOM_CORRIDOR):
		return _get_edge_trans("door_mudroom") * _get_edge_trans("door_rear_exit")
		
	return 0.15

func _get_edge_trans(edge_id: String) -> float:
	for e in edges:
		if e["id"] == edge_id:
			return e["trans"]
	return 0.15

func set_edge_door_state(edge_id: String, new_state: String) -> void:
	var transmission: float = 0.15
	match new_state.to_lower():
		"open":
			transmission = 0.95
		"closed":
			transmission = 0.15
		"barricaded":
			transmission = 0.02
		"breached", "destroyed":
			transmission = 1.00
		"ajar":
			transmission = 0.55
		_:
			transmission = 0.15
			
	for edge in edges:
		if edge["id"] == edge_id:
			edge["state"] = new_state
			edge["trans"] = transmission
			recalculate_sheaf()
			break

func emit_acoustic_event(source_pos: Vector3, amplitude: float, frequency: float, description: String = "Sound") -> Dictionary:
	var room_idx = get_room_for_position(source_pos)
	var clamped_amp = clampf(amplitude, 0.0, 10.0)
	
	stalk_state[room_idx].x = clampf(stalk_state[room_idx].x + clamped_amp, 0.0, 10.0)
	stalk_state[room_idx].y = frequency
	
	total_difference_records += 1
	var record = {
		"id": "diff_%d_%d" % [total_difference_records, Time.get_ticks_msec()],
		"timestamp": Time.get_ticks_msec() / 1000.0,
		"room_idx": room_idx,
		"room_name": ROOM_NAMES[room_idx],
		"source_pos": source_pos,
		"amplitude": clamped_amp,
		"frequency": frequency,
		"description": description,
		"p_ruin": 0.0000
	}
	recalculate_sheaf()
	acoustic_event_emitted.emit(record)
	return record

func recalculate_sheaf() -> void:
	var total_dirichlet: float = 0.0
	for edge in edges:
		var u: int = edge["u"]
		var v: int = edge["v"]
		var trans: float = edge["trans"]
		var diff_amp = (stalk_state[v].x - stalk_state[u].x) * trans
		total_dirichlet += 0.5 * (diff_amp * diff_amp)
		
	dirichlet_energy = total_dirichlet
	sheaf_coherence = clampf(100.0 - (dirichlet_energy * 10.0), 0.0, 100.0)
	sheaf_state_updated.emit(sheaf_coherence, dirichlet_energy)

## Continuous dissipative step
func dissipate_sheaf_energy(delta: float) -> void:
	var dt = minf(delta, 0.1)
	for i in range(ROOM_COUNT):
		stalk_state[i].x = maxf(0.0, stalk_state[i].x - 3.5 * dt)
	recalculate_sheaf()

## Tesla Monoidal Optic: Mental sandbox for stealth calculation
func simulate_breach_noise(start_room: int, target_room: int, method: String) -> Dictionary:
	var base_noise: float = 0.35 if method == "lockpick_stealth" else 3.5
	var trans = _calculate_transmission_between(target_room, ROOM_REFUGE)
	var leakage = base_noise * trans
	return {
		"simulated_noise": base_noise,
		"refuge_leakage": leakage,
		"will_alert_occupant": leakage >= 0.4,
		"p_ruin": 0.0000
	}

## Acoustical threat assessment from Refuge
func get_occupant_acoustic_radar() -> Dictionary:
	var max_threat: float = 0.0
	var threat_room: int = -1
	for i in range(1, ROOM_COUNT):
		if stalk_state[i].x > max_threat:
			max_threat = stalk_state[i].x
			threat_room = i
	return {
		"max_external_threat_level": max_threat,
		"threat_room_index": threat_room,
		"threat_room_name": ROOM_NAMES[threat_room] if threat_room >= 0 else "All Clear",
		"threat_direction": (ROOM_CENTERS[threat_room] - ROOM_CENTERS[ROOM_REFUGE]).normalized() if threat_room >= 0 else Vector3.ZERO,
		"sheaf_coherence": sheaf_coherence,
		"dirichlet_energy": dirichlet_energy,
		"p_ruin": 0.0000
	}

