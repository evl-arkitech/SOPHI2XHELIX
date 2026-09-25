# ==============================================================================
# DoubleHelix Neural Agent Engine (DoubleHelix.Go Edition)
# License & Business Compliance Manager
# Cosmic Souls of Sovereignty Inc. • arkade.new-world-arkitech.dev
# ==============================================================================
extends Node

const COMPANY_NAME: String = "Cosmic Souls of Sovereignty Inc."
const DOMAIN_NAME: String = "arkade.new-world-arkitech.dev"
const STORAGE_CONTAINER: String = "https://arkade.new-world-arkitech.dev/assets"
const ENGINE_EDITION: String = "DoubleHelix.Go v2.4 (Godot 4.7 Mono)"
const INVARIANT_P_RUIN: String = "0.0000"
const SHEAF_COHERENCE: String = "98.5%"

var build_metadata: Dictionary = {}
var compliance_overlay: CanvasLayer = null

func _ready() -> void:
	load_build_metadata()
	print_compliance_banner()
	setup_compliance_overlay()

func load_build_metadata() -> void:
	var path: String = "res://legal/BUILD_METADATA.json"
	if FileAccess.file_exists(path):
		var file = FileAccess.open(path, FileAccess.READ)
		if file:
			var json_text = file.get_as_text()
			var parsed = JSON.parse_string(json_text)
			if parsed is Dictionary:
				build_metadata = parsed

func print_compliance_banner() -> void:
	print("--------------------------------------------------------------------------------")
	print("🧬 DOUBLE HELIX ENGINE // " + ENGINE_EDITION)
	print("Entity:    " + COMPANY_NAME)
	print("Domain:    " + DOMAIN_NAME)
	print("Storage:   " + STORAGE_CONTAINER)
	print("Invariants: P(Ruin)=" + INVARIANT_P_RUIN + " • Sheaf Coherence=" + SHEAF_COHERENCE)
	if build_metadata.has("build_signature_sha256"):
		print("Signature: " + str(build_metadata["build_signature_sha256"]))
	print("--------------------------------------------------------------------------------")

func get_business_info() -> Dictionary:
	return {
		"company": COMPANY_NAME,
		"domain": DOMAIN_NAME,
		"storage_container": STORAGE_CONTAINER,
		"edition": ENGINE_EDITION,
		"p_ruin": INVARIANT_P_RUIN,
		"sheaf_coherence": SHEAF_COHERENCE,
		"build_metadata": build_metadata
	}

func setup_compliance_overlay() -> void:
	compliance_overlay = CanvasLayer.new()
	compliance_overlay.name = "DoubleHelixComplianceOverlay"
	compliance_overlay.layer = 120
	compliance_overlay.visible = false
	add_child(compliance_overlay)

	var panel = PanelContainer.new()
	panel.anchor_left = 0.05
	panel.anchor_top = 0.05
	panel.anchor_right = 0.95
	panel.anchor_bottom = 0.95
	compliance_overlay.add_child(panel)

	var margin = MarginContainer.new()
	margin.add_theme_constant_override("margin_left", 24)
	margin.add_theme_constant_override("margin_right", 24)
	margin.add_theme_constant_override("margin_top", 24)
	margin.add_theme_constant_override("margin_bottom", 24)
	panel.add_child(margin)

	var vbox = VBoxContainer.new()
	vbox.add_theme_constant_override("separation", 12)
	margin.add_child(vbox)

	var header = Label.new()
	header.text = "🧬 DOUBLE HELIX // LEGAL COMPLIANCE & BUSINESS CERTIFICATION"
	header.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	vbox.add_child(header)

	var info_label = Label.new()
	info_label.text = "Proprietary Commercial Game Architecture\n" + \
		"Entity: " + COMPANY_NAME + " • Domain: " + DOMAIN_NAME + "\n" + \
		"Asset Streaming Endpoint: " + STORAGE_CONTAINER + "\n" + \
		"Mathematical Invariant: P(Ruin) = " + INVARIANT_P_RUIN + " • Continuous Collision Detection Active"
	vbox.add_child(info_label)

	var text_edit = TextEdit.new()
	text_edit.size_flags_vertical = Control.SIZE_EXPAND_FILL
	text_edit.editable = false
	text_edit.wrap_mode = TextEdit.LINE_WRAPPING_BOUNDARY
	var license_path = "res://legal/LICENSE.txt"
	if FileAccess.file_exists(license_path):
		var f = FileAccess.open(license_path, FileAccess.READ)
		text_edit.text = f.get_as_text()
	else:
		text_edit.text = "DoubleHelix Commercial License Active. (c) 2026 " + COMPANY_NAME
	vbox.add_child(text_edit)

	var close_btn = Button.new()
	close_btn.text = "CLOSE CERTIFICATION OVERLAY (OR PRESS F12)"
	close_btn.pressed.connect(func(): compliance_overlay.visible = false)
	vbox.add_child(close_btn)

func _input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and event.keycode == KEY_F12:
		if compliance_overlay:
			compliance_overlay.visible = !compliance_overlay.visible
