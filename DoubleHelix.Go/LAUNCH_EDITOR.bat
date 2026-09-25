@echo off
title DoubleHelix Engine - Custom Godot 4.7 Mono Editor
echo ==============================================================================
echo 🧬 DOUBLE HELIX ENGINE // Godot 4.7 Mono Custom Editor Suite
echo Entity:    Cosmic Souls of Sovereignty Inc. • New-World-Arkitech.DEV
echo Domain:    arkade.new-world-arkitech.dev
echo Storage:   https://arkade.new-world-arkitech.dev/assets
echo ==============================================================================

set SCRIPT_DIR=%~dp0
set GODOT_EXE="%SCRIPT_DIR%Godot_v4.7.2-stable_mono_win64\Godot_v4.7.2-stable_mono_win64.exe"
set PROJECT_DIR="%SCRIPT_DIR%DoubleHelix_Tactical_Template"

start "" %GODOT_EXE% --editor --path %PROJECT_DIR%
