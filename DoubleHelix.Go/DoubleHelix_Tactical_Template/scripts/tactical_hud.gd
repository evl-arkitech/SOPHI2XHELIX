# @tool
class_name TacticalHUD
extends Control

## Tactical HUD with SOPHI Acoustic Sheaf Radar & Biometric Telemetry
## Renders circular acoustic Sheaf radar, noise meter, vital status, and P(Ruin)=0.0000 invariants.

@onready var radar_panel: Control = $RadarContainer/RadarDisplay
@onready var health_bar: ProgressBar = $VitalsContainer/HealthBar
@onready var battery_bar: ProgressBar = $VitalsContainer/BatteryBar
@onready var noise_meter: ProgressBar = $VitalsContainer/NoiseMeter
@onready var role_badge: Label = $TopHeader/RoleBadge
@onready var weapon_label: Label = $BottomRight/WeaponLabel
@onready var ammo_label: Label = $BottomRight/AmmoLabel
@onready var interaction_prompt: Label = $CenterContainer/InteractionPrompt
@onready var crosshair: Control = $CenterContainer/Crosshair
@onready var sheaf_coherence_label: Label = $TopHeader/SheafCoherenceLabel
@onready var dirichlet_label: Label = $TopHeader/DirichletLabel
@onready var threat_warning_label: Label = $RadarContainer/ThreatWarning
@onready var nvg_overlay: ColorRect = $NVGOverlay

var player_role: String = "occupant"
var current_health: float = 100.0
var max_health: float = 100.0
var battery_pct: float = 100.0
var current_noise: float = 0.0
var sheaf_coherence: float = 100.0
var dirichlet_energy: float = 0.0
var threat_vector: Vector2 = Vector2.ZERO
var threat_amplitude: float = 0.0
var threat_room: String = "All Clear"
var is_nvg_active: bool = false

# Acoustic ripple animations for radar
var active_ripples: Array[Dictionary] = []

func _ready() -> void:
	if radar_panel:
		radar_panel.draw.connect(_on_radar_draw)
	if nvg_overlay:
		nvg_overlay.visible = false

func _process(delta: float) -> void:
	# Decay noise meter smoothly
	current_noise = lerpf(current_noise, 0.0, 4.0 * delta)
	if noise_meter:
		noise_meter.value = current_noise
		
	# Update active radar ripples
	var i = active_ripples.size() - 1
	while i >= 0:
		active_ripples[i]["radius"] += 45.0 * delta
		active_ripples[i]["alpha"] -= 0.8 * delta
		if active_ripples[i]["alpha"] <= 0.0:
			active_ripples.remove_at(i)
		i -= 1
		
	if radar_panel:
		radar_panel.queue_redraw()

func set_role(role: String) -> void:
	player_role = role
	if role_badge:
		if role == "occupant":
			role_badge.text = "🛡️ DEFENDER (OCCUPANT) • REFUGE RESIDENCE"
			role_badge.modulate = Color(0.2, 0.9, 1.0)
		else:
			role_badge.text = "⚡ INFILTRATOR (INTRUDER) • EXTERIOR BREACH"
			role_badge.modulate = Color(1.0, 0.3, 0.2)

func update_vitals(health: float, battery: float, noise: float) -> void:
	current_health = health
	battery_pct = battery
	current_noise = maxf(current_noise, noise)
	
	if health_bar:
		health_bar.value = health
	if battery_bar:
		battery_bar.value = battery

func update_weapon_info(weapon_name: String, current_ammo: int, max_ammo: int) -> void:
	if weapon_label:
		weapon_label.text = weapon_name
	if ammo_label:
		ammo_label.text = "%d / %d" % [current_ammo, max_ammo]

func update_sheaf_telemetry(coherence: float, dirichlet: float, p_ruin: float = 0.0000) -> void:
	sheaf_coherence = coherence
	dirichlet_energy = dirichlet
	if sheaf_coherence_label:
		sheaf_coherence_label.text = "SOPHI COHERENCE: %.1f%% | P(Ruin): %.4f" % [coherence, p_ruin]
	if dirichlet_label:
		dirichlet_label.text = "E_F DIRICHLET: %.4f J" % dirichlet

func update_acoustic_threat(room_name: String, amp: float, local_threat_2d: Vector2) -> void:
	threat_room = room_name
	threat_amplitude = amp
	threat_vector = local_threat_2d
	
	if threat_warning_label:
		if amp > 0.15:
			threat_warning_label.text = "ACOUSTIC SPIKE: %s (%.1f dB)" % [room_name.to_upper(), amp * 10.0]
			threat_warning_label.modulate = Color(1.0, 0.2, 0.1, 1.0)
		else:
			threat_warning_label.text = "ACOUSTIC RADAR: SCANNING..."
			threat_warning_label.modulate = Color(0.4, 0.8, 1.0, 0.7)

func add_radar_pulse(relative_angle: float, dist_normalized: float, amp: float) -> void:
	active_ripples.append({
		"angle": relative_angle,
		"dist": clampf(dist_normalized, 0.1, 0.9),
		"radius": 4.0,
		"alpha": minf(1.0, amp * 0.4 + 0.3),
		"amp": amp
	})

func set_prompt(text: String) -> void:
	if interaction_prompt:
		interaction_prompt.text = text
		interaction_prompt.visible = (text != "")

func toggle_nvg(active: bool) -> void:
	is_nvg_active = active
	if nvg_overlay:
		nvg_overlay.visible = active

func _on_radar_draw() -> void:
	if not radar_panel:
		return
		
	var center = radar_panel.size * 0.5
	var max_r = minf(center.x, center.y) - 6.0
	
	# Background circle
	radar_panel.draw_circle(center, max_r, Color(0.04, 0.08, 0.12, 0.85))
	
	# Concentric Sheaf distance rings
	for factor in [0.25, 0.5, 0.75, 1.0]:
		var r = max_r * factor
		var ring_color = Color(0.15, 0.45, 0.65, 0.35) if factor < 1.0 else Color(0.3, 0.75, 1.0, 0.8)
		radar_panel.draw_arc(center, r, 0, TAU, 32, ring_color, 1.2)
		
	# Crosshairs on radar
	radar_panel.draw_line(Vector2(center.x - max_r, center.y), Vector2(center.x + max_r, center.y), Color(0.2, 0.5, 0.7, 0.3), 1.0)
	radar_panel.draw_line(Vector2(center.x, center.y - max_r), Vector2(center.x, center.y + max_r), Color(0.2, 0.5, 0.7, 0.3), 1.0)
	
	# Center player blip
	var blip_color = Color(0.2, 0.9, 1.0) if player_role == "occupant" else Color(1.0, 0.3, 0.2)
	radar_panel.draw_circle(center, 3.5, blip_color)
	
	# Draw active acoustic ripples
	for rip in active_ripples:
		var target_pos = center + Vector2(cos(rip["angle"]), sin(rip["angle"])) * (rip["dist"] * max_r)
		var rip_col = Color(1.0, 0.25, 0.15, rip["alpha"])
		radar_panel.draw_arc(target_pos, rip["radius"], 0, TAU, 16, rip_col, 2.0)
		radar_panel.draw_circle(target_pos, 2.5, rip_col)
		
	# Draw directional threat vector arrow if active
	if threat_amplitude > 0.2 and threat_vector.length_squared() > 0.01:
		var dir = threat_vector.normalized()
		var arrow_len = minf(max_r * 0.85, max_r * (threat_amplitude / 5.0))
		var tip = center + dir * arrow_len
		var arrow_col = Color(1.0, 0.15, 0.1, 0.9)
		radar_panel.draw_line(center, tip, arrow_col, 2.2)
		radar_panel.draw_circle(tip, 4.0, arrow_col)
