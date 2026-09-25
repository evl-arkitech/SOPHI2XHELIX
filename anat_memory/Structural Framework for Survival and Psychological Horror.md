# Structural Framework for Survival and Psychological Horror

AI coding assistants frequently fail at video game development because they default to generic, isolated scripts—such as a basic player controller or a simple raycast jump scare—without understanding the authoritative system architecture, state transitions, and data flow contracts that bind a game together. Survival and psychological horror titles are among the most architecturally demanding genres because fear relies on friction, predictability under the hood, precise tension pacing, and strict resource limitations.

The technical specifications, state machines, algorithmic loops, and architectural contracts below are designed to be referenced directly or pasted into an AI assistant to implement a production-ready survival horror framework across modern native engines (Unreal, Unity, Godot) and high-performance Web runtimes (WebGPU, Web Workers, OPFS).

---

## The Horror Gameplay Execution Flow: Systems Breakdown

Survival horror replaces the traditional power fantasy with systemic vulnerability. The macro execution flow must be architected around tension build-up, panic escalation, and safe recovery.

```
[Cold Boot / Compliance Splash]
       │
       ▼
[Title Gate ("Press Any Button")] (Audio Context Unlocked / Input Bound)
       │
       ▼
[Main Menu Hierarchy]
       │
       ▼
[Prologue / Safe Introduction] (Establishes baseline lighting & sound)
       │
       ▼
┌───────────────────────────────────────────────────────────┐
│ Core Meso Pacing Loop                                     │
│                                                           │
│  [Exploration / Scavenging] (Tension Accumulation)        │
│          │                                                │
│          ▼                                                │
│  [Suspense / Sound Anomalies]                             │
│          │                                                │
│          ▼                                                │
│  [Stalker / Combat Encounter] (Panic Peak / Resource Cost)│
│          │                                                │
│          ▼                                                │
│  [Sanctuary / Safe Room] (Tension Release / Save Point)   │
└───────────────────────────────────────────────────────────┘
       │
       ▼
[Point of No Return / Climax Boss]
       │
       ▼
[Denouement / Ending Sequence]
       │
       ▼
[Post-Game Atomic Serialization] (NG+ / Completion Unlocks)
```

### 1. The Horror Micro-Loop (Second-to-Second Mechanical Friction)
In an action game, the micro-loop emphasizes responsiveness, low input latency, and snappy feedback. In horror, the micro-loop is engineered with deliberate friction:
* **Locomotion Mechanics:** Avatar movement includes simulated weight (acceleration and deceleration curves rather than instantaneous directional snapping). Running drains a stamina meter; complete exhaustion enforces a temporary movement penalty, visual camera shake, and heavy, audible breathing that alerts nearby entities.
* **Dynamic Flashlight & Battery Drain:** A continuous, battery-dependent light source with a localized spotlight cone. The battery drain follows a non-linear decay function:
  $$I_{\text{light}}(t) = I_{\text{max}} \cdot \left(\frac{B(t)}{B_{\text{max}}}\right)^\gamma$$
  where $B(t)$ is current battery charge and $\gamma \ge 1.5$. As battery levels fall below $20\%$, the light initiates random voltage flickering via Perlin noise modulating intensity and flicker frequency, forcing the player to manage battery replacements under stress.
* **Aiming Wobble & Reticle Bloom:** Weapon aiming is stabilized only when standing completely still. Movement or high heart-rate values apply procedural sway to the camera and expand the shot spread, making panic firing resource-inefficient.

### 2. The Horror Meso-Loop (Minute-to-Minute Tension and Release)
The meso-loop balances environmental exploration, puzzle solving, inventory triage, and evasive survival:
* **The Tension Curve:** The gameplay loops between four distinct environmental states:
  * **Exploration:** Low acoustic volume, resource gathering, ambient world storytelling.
  * **Anticipation:** Environmental cues (flickering fluorescent lights, distant pipe bangs, creature vocalizations, spatialized footsteps).
  * **Confrontation / Evasion:** Active encounter with a hostile entity. Resources must be expended (ammunition, light flares) or evasive action taken (hiding in closets, crawling under tables, breaking line of sight).
  * **Sanctuary:** Entering a dedicated Safe Room. Hostile AI cannot cross the threshold; dynamic music shifts to a calming melodic progression; and the player accesses the storage chest and save terminal.

### 3. The Horror Macro-Loop (Hours-Long Campaign Progression)
* **Spatial Lock-and-Key Architecture:** The game environment (e.g., an abandoned hospital, gothic mansion, or derelict research facility) operates as an interconnected, non-linear hub. Progression is blocked by mechanical or biological locks: physical keys, electronic keycards, missing valve handles, power circuit breakers, or chemical puzzle compounds.
* **Resource Depletion Economy:** The global economy acts as a finite resource sink. The total amount of ammunition, healing supplies, and save consumables in the world is strictly budgeted. The game tracks player accuracy and remaining supplies, preventing resource stockpiling through limited carrying capacity.
* **The Point of No Return:** Prior to the climactic sequence, navigation back to earlier hub sectors is permanently cut off (e.g., an elevator shaft collapses or fire doors lock down). The engine purges earlier hub sectors and ambient assets from memory, allocating full system resources to high-fidelity boss arenas and dynamic cinematic sequences.

---

## The Two-Tier AI Architecture (Stalker System)

A primary reason AI assistants fail to generate convincing horror enemies is that they write simple finite state machines that immediately run `MoveTo(Player.Position)`. This breaks immersion: the creature either behaves like a homing missile or gets stuck on wall geometry.

High-end horror titles like *Alien: Isolation* solve this by dividing the artificial intelligence into two distinct tiers: a **Macro Director** and a **Micro Agent**.

```
               ┌────────────────────────────────────────┐
               │        Macro AI (The Director)         │
               │ - Has global awareness (player coords) │
               │ - Evaluates Menace/Intensity: I_player │
               │ - Assigns dynamic search areas (Jobs)  │
               │ - Recalls Stalker to backstage on peak │
               └───────────────────┬────────────────────┘
                                   │
                     Dispatches Job (Target Sector)
                                   │
                                   ▼
               ┌────────────────────────────────────────┐
               │      Micro AI (The Stalker Agent)      │
               │ - Sensorially blind to player coords   │
               │ - Sensory Inputs: FOV, Sound Listeners │
               │ - State Machine: Patrol/Search/Hunt    │
               │ - Executes standard local pathfinding  │
               └────────────────────────────────────────┘
```

### Tier 1: The Director (Macro AI)
The Director acts as an invisible matchmaker between player tension and monster presence. It holds global awareness of all entity positions, health values, and room IDs, but it never gives the monster the player's direct coordinates.

The Director tracks a continuous Menace / Intensity Gauge ($I_{\text{player}} \in [0, 100]$):
$$I_{\text{player}}(t) = w_p \cdot P_{\text{prox}} + w_v \cdot V_{\text{los}} + w_a \cdot A_{\text{noise}} + w_h \cdot (1.0 - H_{\text{current}})$$
Where:
* $P_{\text{prox}}$ is proximity intensity (inversely proportional to spatial distance between player and monster).
* $V_{\text{los}}$ is 1.0 if the monster maintains visual line of sight with the player, otherwise 0.0.
* $A_{\text{noise}}$ is the player's acoustic signature (running, shooting, slamming doors).
* $H_{\text{current}}$ is the player's current health percentage.
* $w_p, w_v, w_a, w_h$ are calibrated weight coefficients.

The Director operates on a continuous feedback loop:
1. **Build Tension:** When $I_{\text{player}} < 40$, the Director issues a "Job" to the Micro AI, instructing it to sweep the sector or corridor adjacent to the player's general vicinity.
2. **Sustain Encounter:** When $40 \le I_{\text{player}} \le 85$, the monster hunts naturally within that zone using its own senses.
3. **Relieve Over-Saturation (Backstage Transition):** If $I_{\text{player}} \ge 90$ for longer than a sustained threshold (e.g., 20 seconds of continuous pursuit without death), the Director intervenes to prevent player fatigue. It issues a withdrawal command, forcing the monster to enter a ceiling vent, ventilation shaft, or secondary pathing layer. The monster is held "backstage" until $I_{\text{player}}$ bleeds below 30, resetting the cycle.

### Tier 2: The Stalker Agent (Micro AI)
The Stalker entity runs inside the physical game simulation and possesses zero privileged knowledge. It must locate the player using discrete perception systems:
* **Visual Perception:** Three nested field-of-view (FOV) cones:
  * **Near Peripheral Cone:** $160^\circ$ angle, 3-meter radius. Detects fast movement instantly.
  * **Direct Sight Cone:** $60^\circ$ angle, 15-meter radius. Detects crouching or standing avatars. Requires continuous line-of-sight raycasts to avatar sockets (head, spine, pelvis).
  * **Flashlight Detection Raycast:** If the player's flashlight is switched on, any intersection between the player's light frustum and the creature's collision bounds immediately alters the creature's state to Alerted.
* **Acoustic Perception:** A noise-listening interface hooked into the navigation mesh. When an action occurs (e.g., running creates a 10-meter noise radius; firing a handgun creates an 80-meter noise radius), a spherical sound event is broadcast. The monster's AI controller evaluates path distance to the sound origin. If within hearing range, it abandons its current patrol route and generates a path to investigate the disturbance.

---

## Horror Pushdown Automaton (PDA) State Machine

To handle real-time inventory management, item inspection, safe rooms, and sudden interruptions (e.g., controller disconnects, hardware rest mode), the game lifecycle must run on a Pushdown Automaton (PDA) stack rather than a flat finite state machine.

| Stack Configuration (Top $\to$ Bottom) | Trigger Event | Operation | Next Stack State | Time Scale ($\Delta t$) | Subsystem Behavior & Audio State |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `[BootState]` | `BOOT_COMPLETE` | Replace | `[TitleGateState]` | $\Delta t = 1.0$ | Platform logos cleared. User input bound; audio context initialized on first click. |
| `[TitleGateState]` | `START_PRESSED` | Replace | `[MainMenuState]` | $\Delta t = 1.0$ | Primary controller assigned to Player 0; save storage mounted. |
| `[MainMenuState]` | `GAME_START` | Replace | `[ExplorationState]` | $\Delta t = 1.0$ | World geometry streamed; player avatar spawned; Director initialized. |
| `[ExplorationState]` | `OPEN_INVENTORY` (Diegetic) | Push | `[DiegeticInventoryState, ExplorationState]` | $\Delta t = 1.0$ (Real-Time) | Simulation continues running. Monster can still attack. HUD renders holographic backpack. |
| `[DiegeticInventoryState, ExplorationState]` | `INSPECT_ITEM` | Push | `[ItemInspectState, DiegeticInventoryState, ExplorationState]` | $\Delta t = 0.0$ (Paused) | Simulation frozen. 3D item isolated in viewport for examination/clue discovery. |
| `[ItemInspectState, ...]` | `BACK_PRESSED` | Pop | `[DiegeticInventoryState, ExplorationState]` | $\Delta t = 1.0$ (Unfreeze) | Simulation unfreezes; focus returns to real-time inventory grid. |
| `[DiegeticInventoryState, ExplorationState]` | `CLOSE_INVENTORY` | Pop | `[ExplorationState]` | $\Delta t = 1.0$ | Inventory UI detached; full locomotion and camera control restored. |
| `[ExplorationState]` | `ENTER_SAFE_ZONE` | Replace | `[SafeRoomState]` | $\Delta t = 1.0$ | Navmesh boundary locks out monster; music shifts to safe room horizontal sequence. |
| `[ExplorationState]` | `JUMPSCARE_TRIGGER` | Push | `[CinematicGrabState, ExplorationState]` | $\Delta t = 1.0$ | Player control locked; camera interpolated toward attacker; audio stinger fires. |
| `[AnyState]` | `PAD_DISCONNECT` | Push | `[HardwareAlertState, AnyState]` | $\Delta t = 0.0$ (Forced) | TRC/XR compliance alert; audio buses muted; input polling waits for controller re-link. |

---

## Psychological Sanity & Dynamic Audio Architecture

Fear in video games is primarily driven by audio-visual distortion rather than raw polygon rendering. The game engine must coordinate an integrated Sanity Pipeline that alters rendering shaders and audio DSP buses in lockstep.

### 1. The Sanity Decay Function
Sanity ($S \in [0.0, 1.0]$, where $1.0$ is completely lucid and $0.0$ is full psychological breakdown) continuously evaluates based on exposure to environmental stressors:

$$S(t + \Delta t) = \text{clamp}\left( S(t) + \left( -\lambda_d \cdot (1 - L_v) - \lambda_m \cdot M_{\text{prox}} - \lambda_c \cdot C_{\text{los}} + \lambda_r \cdot R_{\text{safe}} \right) \Delta t, \, 0.0, \, 1.0 \right)$$

Where:
* $L_v \in [0, 1]$ is ambient light exposure at player eye coordinates (0.0 = pitch black, 1.0 = direct light).
* $M_{\text{prox}} \in [0, 1]$ is proximity to an unkilled entity.
* $C_{\text{los}} \in \{0, 1\}$ is direct visual contact (gazing at a monster).
* $R_{\text{safe}} \in [0, 1]$ is sanctuary recovery (being inside a safe room or standing under a streetlamp).
* $\lambda_d, \lambda_m, \lambda_c, \lambda_r$ are decay/recovery rate constants.

### 2. Shader & Post-Processing Coupling
As $S$ decreases below $0.6$, the engine modulates post-processing materials dynamically:
* **Chromatic Aberration:** Displaces Red/Blue UV channels proportionally to $(1.0 - S)^2$.
* **Barrel Distortion / FOV Warping:** Progressively bulges the center of the projection matrix, simulating claustrophobic tunnel vision.
* **Vignette & Grain:** Amplifies dynamic film grain and contracts edge vignette radius, darkening the peripheral view.

### 3. Dynamic Audio: Stems and Hallucinations
The audio engine (Wwise, FMOD, or Web Audio API) executes a hybrid **Vertical Layering** and **Horizontal Resequencing** architecture:
* **Vertical Layering (Intensity Scaling):** The ambient musical score runs three continuous, tempo-synchronized stems:
  * **Stem 1 (Sub-bass drone / Room Tone):** Always unmuted ($1.0$ volume).
  * **Stem 2 (Atonal strings / Waterphone scrapes):** Volume modulated by $1.0 - S$ (increases as sanity drops).
  * **Stem 3 (Rhythmic Industrial Percussion):** Unmuted only when Stalker Micro AI enters pursuit mode.
* **Horizontal Resequencing (Zone Shifts):** Transitioning into a Safe Room schedules an immediate beat-matched transition out of the exploration loop and executes an orchestral crossfade into the Safe Room theme.
* **Auditory Hallucinations (Acoustic Deception):** When $S < 0.3$, an audio scheduler randomly instantiates phantom sound events in the 3D soundscape:
  * False footsteps positioned $5\,\text{m}$ behind the player's camera vector.
  * Whispering voices panned hard left and hard right using Head-Related Transfer Functions (HRTF).
  * Door-handle rattles assigned to nearby non-functional doors.
* **Accessibility Compliance (XAG 103):** Every auditory hallucination must be flagged in the subtitle/indicator system with distinct coloration or italicization (e.g., *[Distant Footsteps?]*), ensuring hearing-impaired players receive equivalent psychological tension without functional confusion.

---

## Storage Durability: Limited-Resource Atomic Save Protocol

Survival horror games often utilize physical in-game items (e.g., Ink Ribbons, fuel cassettes) to limit save frequency. If power fails or the tab closes during serialization, corrupting the save file breaks platform compliance and destroys player progress.

The serialization architecture must follow an Atomic Save Pattern with an immutable schema:

```
[Save Trigger Fired at Terminal]
                │
                ▼
[Validate Inventory: Consumable Save Item >= 1]
                │
                ├── No ──> [Play "Terminal Empty" Sound / Abort]
                │
               Yes
                │
                ▼
[Decrement Save Consumable Count]
                │
                ▼
[Serialize Game State Buffer (Player, Inventory, World Flags, AI)]
                │
                ▼
[Compute SHA-256 Checksum & Append Header]
                │
                ▼
[Write Payload to Temporary File ("save_slot_01.tmp")]
                │
                ▼
[Execute OS flush() and fsync() on File Descriptor]
                │
                ▼
[Atomic POSIX rename("save_slot_01.tmp" -> "save_slot_01.sav")]
                │
                ▼
[Execute fsync() on Parent Directory Descriptor]
                │
                ▼
[Update UI: Save Successful Notification]
```

---

## Technical Implementation Blueprint for AI Code Generation

1. **Pushdown Automaton State Machine Contract:** Implement `IGameState` interface with `OnEnter()`, `OnExit()`, `OnPause()`, `OnResume()`, `Update(float delta_time)`, and `Render()`. Provide `PushState`, `PopState`, and `ChangeState`.
2. **Director-to-Agent Event Contract:**
   - `DirectorContext`: `{ current_menace, player_last_known_pos, player_current_room_id, time_in_high_stress }`
   - `StalkerJob`: `{ INVESTIGATE_ZONE, PATROL_SECTOR, WITHDRAW_TO_VENTS }`
   - Director ticks every $1.0$ second; evaluates Menace using proximity, line-of-sight status, and player health.
   - If Menace exceeds $85$ for $> 15.0$ continuous seconds, Director issues `WITHDRAW_TO_VENTS`.
   - StalkerController does NOT read `Player.Position` directly; it navigates only to coordinates provided by `StalkerJob` or positions logged by its own visual raycasts and acoustic listener components.
3. **Atomic Save Routine:** Accept `SavePayload` struct, calculate SHA-256 or CRC-32 hash, write to `<slot_name>.tmp`, verify integrity, and atomically rename to `<slot_name>.sav`.
