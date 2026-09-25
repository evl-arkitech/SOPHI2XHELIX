@echo off
title DoubleHelix Engine - Autonomous Gaming Agent CLI
echo ==============================================================================
echo 🧬 DOUBLE HELIX ENGINE // Autonomous Gaming Agent CLI
echo ==============================================================================

set SCRIPT_DIR=%~dp0
set GODOT_CONSOLE="%SCRIPT_DIR%Godot_v4.7.2-stable_mono_win64\Godot_v4.7.2-stable_mono_win64_console.exe"
set PROJECT_DIR="%SCRIPT_DIR%DoubleHelix_Tactical_Template"

if "%1"=="" (
    echo Usage: RUN_AGENT_CLI.bat [command] [optional_json_payload]
    echo Commands:
    echo   status            Inspect engine, project, and invariants
    echo   inject_licensing  Inject business and licensing invariants
    echo   generate_room     Procedurally generate 3D tactical room
    echo   validate_scene    Validate scene node invariants
    echo.
    echo Running default status check:
    %GODOT_CONSOLE% --headless --path %PROJECT_DIR% --script "res://addons/doublehelix_engine/agent_cli.gd" -- status
) else (
    %GODOT_CONSOLE% --headless --path %PROJECT_DIR% --script "res://addons/doublehelix_engine/agent_cli.gd" -- %*
)
