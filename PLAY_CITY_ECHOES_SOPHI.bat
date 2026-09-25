@echo off
title City Echoes: SOPHI Real-Life Simulation // Double Helix Engine
echo ===============================================================================
echo   CITY ECHOES: SOPHI EDITION
echo   Real-Life Tactical Simulation (Defender vs Infiltrator)
echo   Cosmic Souls of Sovereignty Inc. - arkade.new-world-arkitech.dev
echo ===============================================================================
echo.
echo [Controls]
echo   WASD           - Move / Locomotion (Surface-aware footsteps)
echo   Shift          - Sprint (Heavy, loud footsteps)
echo   C / Ctrl       - Crouch / Sneak (Silent footsteps, minimises floor creaks)
echo   Right Click    - Aim Down Sights (Eye level physical barrel alignment)
echo   Left Click     - Discharge Weapon (12-Gauge Shotgun / Suppressed 9mm)
echo   R              - Feed Shells / Reload
echo   E              - Turn Door Knob / Lockpick
echo   B              - Barricade Door with Reinforced Timber (Occupant)
echo   F              - Toggle Volumetric Flashlight / Night Vision Goggles
echo   V              - Seamlessly Toggle 1st Person and 3rd Person View
echo   F12            - Legal Compliance Certification & Invariant Audit
echo   Esc            - Capture / Free Mouse Cursor
echo.
echo [Simulation Note]
echo   No on-screen HUD, no cheat radars, no floating bars.
echo   Rely entirely on your biological Vessel, your ears, and proximate tools.
echo.
echo Launching Godot 4.7 Mono Simulation Engine...

start "" "DoubleHelix.Go\Godot_v4.7.2-stable_mono_win64\Godot_v4.7.2-stable_mono_win64.exe" --path "DoubleHelix.Go\DoubleHelix_Tactical_Template"
exit
