@echo off
title The Warehouse: The Pale Frequency // Double Helix Engine (Godot 4.7)
echo ===============================================================================
echo   THE WAREHOUSE: THE PALE FREQUENCY
echo   Psychological Survival Horror & Quantum Observer Stalker Simulation
echo   Engineered by The Arkitech & Sophianat
echo   Powered by Double Helix Engine // Godot 4.7 Mono
echo ===============================================================================
echo.
echo [Controls]
echo   WASD           - Move / Locomotion (Concrete and Water footsteps)
echo   Shift          - Sprint (Heavy, loud footsteps)
echo   C / Ctrl       - Crouch (Silent sneak)
echo   F              - Toggle Flashlight (Battery consumption & voltage flicker)
echo   Q              - Quick 180-Degree Look Back (Keep eye on Stalkers!)
echo   E              - Interact (Throw Breakers, Enter Codes, Turn Valves, Airlock Wheel)
echo   Esc            - Capture / Free Mouse Cursor
echo.
echo [Story Acts]
echo   Act I   - The Cold Concrete (Follow Yellow Transit Line, Encounter Mannequin A)
echo   Act II  - The Routing Floor (3 Hydraulic Bypass Valves, Staging Airlock)
echo   Act III - Central Broadcast Hub (The Dais, Terminal Choice: Succession vs Severance)
echo.
echo Launching Godot 4.7 Mono Simulation Engine...

start "" "DoubleHelix.Go\Godot_v4.7.2-stable_mono_win64\Godot_v4.7.2-stable_mono_win64.exe" --path "DoubleHelix.Go\Projects\TheWarehouse_Experiment"
exit
