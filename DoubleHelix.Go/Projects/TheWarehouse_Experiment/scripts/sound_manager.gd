extends Node

# SoundManager Singleton: Procedural & Ambient Audio Engine
# Employs AudioStreamGenerator for pure procedural synthesis of sub-bass drops,
# fluorescent ballast humming, transformer hums, and radio noise bursts.

var ambient_player: AudioStreamPlayer
var tension_player: AudioStreamPlayer
var sfx_player: AudioStreamPlayer
var pa_player: AudioStreamPlayer

var is_sub_bass_playing: bool = false

func _ready() -> void:
	ambient_player = AudioStreamPlayer.new()
	ambient_player.bus = "Master"
	add_child(ambient_player)
	
	tension_player = AudioStreamPlayer.new()
	tension_player.bus = "Master"
	add_child(tension_player)
	
	sfx_player = AudioStreamPlayer.new()
	sfx_player.bus = "Master"
	add_child(sfx_player)
	
	pa_player = AudioStreamPlayer.new()
	pa_player.bus = "Master"
	add_child(pa_player)
	
	start_ambient_hum()

func start_ambient_hum() -> void:
	# Continuous 60Hz mains transformer hum with gentle random wobble
	var generator = AudioStreamGenerator.new()
	generator.mix_rate = 22050
	generator.buffer_length = 0.5
	ambient_player.stream = generator
	ambient_player.volume_db = -18.0
	ambient_player.play()
	_fill_generator_loop(ambient_player.get_stream_playback(), 60.0, 0.15)

func _fill_generator_loop(playback: AudioStreamGeneratorPlayback, freq: float, amp: float) -> void:
	if playback == null:
		return
	var frames = playback.get_frames_available()
	var phase = 0.0
	var phase_inc = (freq * TAU) / 22050.0
	for i in range(frames):
		var sample = sin(phase) * amp
		# Add faint odd harmonic (180Hz) characteristic of fluorescent ballasts
		sample += sin(phase * 3.0) * (amp * 0.25)
		playback.push_frame(Vector2(sample, sample))
		phase = fmod(phase + phase_inc, TAU)

func play_sub_bass_drop() -> void:
	# Infrasonic panic trigger: sweeps from 80Hz down to 25Hz over 2.5 seconds
	var gen = AudioStreamGenerator.new()
	gen.mix_rate = 44100
	gen.buffer_length = 3.0
	sfx_player.stream = gen
	sfx_player.volume_db = -3.0
	sfx_player.play()
	
	var playback = sfx_player.get_stream_playback()
	if playback:
		var total_frames = int(44100 * 2.5)
		var phase = 0.0
		for i in range(total_frames):
			var t = float(i) / float(total_frames)
			var current_freq = lerp(85.0, 24.0, t)
			var current_amp = lerp(0.8, 0.0, t * t)
			var phase_inc = (current_freq * TAU) / 44100.0
			var sample = sin(phase) * current_amp
			playback.push_frame(Vector2(sample, sample))
			phase = fmod(phase + phase_inc, TAU)

func play_scrape_cue() -> void:
	# Synthetic fingernails scraping corrugated cardboard/metal
	var gen = AudioStreamGenerator.new()
	gen.mix_rate = 22050
	gen.buffer_length = 1.0
	sfx_player.stream = gen
	sfx_player.volume_db = -8.0
	sfx_player.play()
	
	var playback = sfx_player.get_stream_playback()
	if playback:
		var frames = int(22050 * 0.8)
		for i in range(frames):
			var noise = (randf() * 2.0 - 1.0) * 0.35
			playback.push_frame(Vector2(noise, noise))

func play_footstep(in_water: bool = false) -> void:
	# Subtle percussive click/thump
	var gen = AudioStreamGenerator.new()
	gen.mix_rate = 22050
	gen.buffer_length = 0.2
	sfx_player.stream = gen
	sfx_player.volume_db = -16.0 if not in_water else -10.0
	sfx_player.play()
	
	var playback = sfx_player.get_stream_playback()
	if playback:
		var frames = int(22050 * 0.12)
		var phase = 0.0
		var freq = 120.0 if not in_water else 280.0
		var phase_inc = (freq * TAU) / 22050.0
		for i in range(frames):
			var decay = 1.0 - (float(i) / float(frames))
			var sample = sin(phase) * decay * 0.4
			if in_water:
				sample += (randf() * 2.0 - 1.0) * decay * 0.3 # splash noise
			playback.push_frame(Vector2(sample, sample))
			phase = fmod(phase + phase_inc, TAU)

func play_pa_chime() -> void:
	# Two-tone paging chime (E5 -> C5)
	var gen = AudioStreamGenerator.new()
	gen.mix_rate = 44100
	gen.buffer_length = 1.0
	pa_player.stream = gen
	pa_player.volume_db = -6.0
	pa_player.play()
	
	var playback = pa_player.get_stream_playback()
	if playback:
		var half_frames = int(44100 * 0.35)
		var phase = 0.0
		# Tone 1: 659.25 Hz (E5)
		var phase_inc1 = (659.25 * TAU) / 44100.0
		for i in range(half_frames):
			var decay = 1.0 - (float(i) / float(half_frames)) * 0.5
			var s = sin(phase) * decay * 0.5
			playback.push_frame(Vector2(s, s))
			phase = fmod(phase + phase_inc1, TAU)
		# Tone 2: 523.25 Hz (C5)
		phase = 0.0
		var phase_inc2 = (523.25 * TAU) / 44100.0
		for i in range(half_frames):
			var decay = 1.0 - (float(i) / float(half_frames))
			var s = sin(phase) * decay * 0.6
			playback.push_frame(Vector2(s, s))
			phase = fmod(phase + phase_inc2, TAU)
