# **Architecture of Video Game Systems: From Classical Console Execution Pipelines to Modern Native and Web Runtime Standards**

## **The Classical Console Game Execution Architecture: Start Screen to Ending Credits**

The execution architecture of traditional console software reflects a strict synthesis of hardware constraints, platform compliance mandates, and dramatic pacing models. From the initial cold boot of physical media to the post-credits serialization routine, a console title executes as a deterministic, multi-layered state machine designed to manage volatile memory, guarantee data durability, and maintain continuous player immersion.

### **Boot Ingestion, Platform Compliance, and the Main Menu Hierarchy**

The software lifecycle initiates well before the rendering of interactive graphics. Upon power delivery, the console hardware completes a power-on self-test (POST) governed by the platform operating system and security processor. This stage verifies optical disc or solid-state cartridge signatures, authenticates platform encryption keys, checks partition integrity, and maps the binary into system memory.

Control then passes to the application entry point, where the game engine allocates low-level heap memory, configures worker threads, binds hardware-specific graphics application programming interfaces (APIs), and loads shared dynamic libraries.

Immediately following engine allocation, the application enters the Splash and Branding Stack. This pipeline displays platform holder trademarks, publisher and developer identifiers, middleware technology licenses (including physics engines, video playback libraries, and audio middleware), and required legal notices1. Platform holders strictly govern this phase through compliance frameworks such as Sony Technical Requirements Checklists (TRC), Microsoft Xbox Requirements (XR, formerly TCR), and Nintendo Lotcheck2.

Platform specifications dictate exact safe-zone margins, aspect ratio scaling, typographic styling, and minimum and maximum display durations for corporate splash screens1. Middleware notices ensure contractual adherence to licensed third-party code. While historic implementations hard-coded splash timings, modern implementations stream background assets asynchronously during video playback, requiring fallback skip logic once pre-caching finishes.

Following splash presentation, the engine transitions to the Title Gate, historically designated as the "Press Start" or "Press Any Button" screen. Far from serving an aesthetic function, this screen is an architectural mechanism designed to satisfy console certification rules2:

* *Interactive State Compliance:* Platform certification mandates that an application must achieve interactive responsiveness within a strict time budget from execution launch, often within twenty to thirty seconds2. Because world streaming environments, dynamic lightmaps, and large sound banks cannot reliably deserialize within this narrow window, developers deploy a lightweight Title Gate containing minimal geometric and texture overhead to satisfy the certification timer2.  
* *Hardware Peripheral Enumeration and Binding:* Console platforms support multiple concurrent input devices across wireless radio-frequency and USB channels. The application must identify which physical device the user is holding before presenting profile-dependent UI2. The Title Gate acts as an input filter: the first peripheral to fire an action interrupt (Button\_A, Button\_Cross, or Start) registers its hardware identifier with the engine's local player registry, assigning that peripheral index to Local Player Zero and suppressing input from unassigned controllers2.  
* *User Profile Resolution and Storage Container Mounting:* Modern and late-era classical consoles disallow arbitrary storage operations prior to profile selection2. The Title Gate initiates an operating system handshake that confirms user credentials, verifies cloud entitlement tokens, mounts sandboxed file directories, and initializes local save-data containers2.  
* *Attract Mode Watchdog:* Originating in coin-operated arcade hardware, traditional console software runs an idle timer on the Title Gate. If no input interrupts occur within a calibrated threshold (typically sixty to ninety seconds), the engine transitions into an Attract Loop—playing pre-rendered demonstration reels or executing deterministic gameplay replays. This prevents visual phosphor burn-in on cathode-ray tube (CRT) and early plasma displays while offering self-resetting demonstration material for retail kiosks2.

Once controller assignment and storage allocation resolve, the engine advances to the Main Menu Hierarchy. This UI tree handles the initialization of high-level runtime configurations. The menu presents standard operational branches: New Game, Continue, Load Game, Options, and Extras. Selecting Continue initiates an asynchronous read of the most recently validated save container metadata.

Selecting Load Game enumerates all valid disk slots, verifying header cyclic redundancy checks (CRC32) or cryptographic hashes to isolate corrupted payloads before presentation. The Options stack exposes graphics, audio, gameplay, and accessibility subsystems, writing user-selected mutations to an active profile buffer.

&nbsp;

| Boot Pipeline Phase | Execution Timing | Core Platform / Technical Objective | Failure Condition / Risk Mitigation |
| :---- | :---- | :---- | :---- |
| Hardware Boot & POST | ![][image1] | Handshake hardware buses, verify cryptographic disc/cartridge signatures, map memory segments. | System freeze or read fault; handled via platform-level OS recovery routines. |
| Engine Runtime Initialization | ![][image2] | Pre-allocate fixed memory pools, configure thread worker affinity, create graphics rendering contexts. | Out-of-memory (OOM) crash; mitigated by pre-allocating static runtime memory pools. |
| Splash & Legal Stack | ![][image3] | Present corporate identities, platform branding, middleware licenses, and copyright documentation1. | Certification rejection if display times or logo dimensions violate TRC/XR rules1. |
| Title Gate ("Press Start") | Interactivity ![][image4] | Satisfy interactivity deadlines, assign hardware gamepad to Player Index 0, mount profile storage2. | Input polling stall; mitigated by operating in a user-agnostic, low-overhead loop7. |
| Attract Loop Handler | Idle ![][image5] | Stream promotional reels or run deterministic engine replays to prevent phosphor burn-in2. | Memory leaks across repeated playback; mitigated by recycling deterministic scene pools. |
| Main Menu Stack | User-driven | Parse save slot metadata, verify checksums, present game entry points and accessibility settings. | Corrupted save access; mitigated by validating file headers prior to rendering slot slots. |

### **Narrative Exposition, Camera Blending, and Onboarding Mechanics**

Selecting New Game initiates the transition from menu UI to interactive gameplay space. This transition is mediated by an expositional cinematic pipeline. Classical architectures deployed either pre-rendered Full Motion Video (FMV) streamed from optical discs or real-time cinematic sequences executed directly within the rendering engine using scripted skeletal animations and cinematic cameras.

The narrative architecture of console games often relies on dramatic exposition, introducing an inciting incident either *in media res* or via world-framing prologues. The critical engineering boundary occurs during the transition from the opening cinematic to interactive control. Classical engines frequently relied on hard visual cuts or intermediate loading screens to clear movie playback memory buffers before initializing player entities. Modern pipelines prioritize continuous camera blending: the non-interactive camera track smoothly interpolates its position, orientation, and field of view into the spatial gameplay camera component (such as a third-person spring arm or first-person rig), passing control to the player without an asset reload or visual cut.

Once the camera lands behind the character, the software routes the player through an onboarding sequence. Rather than presenting instructions via text overlays, the design relies on progressive mechanical gating:

The player begins in an isolated geometry space—such as an enclosed chamber or narrow corridor—that isolates movement and camera rotation vectors. Physical barriers prevent advancement until the player inputs specific movement actions.

Contextual button prompts appear within the Heads-Up Display (HUD) or as diegetic elements floating in 3D space, showing controller iconography mapped directly to the primary input peripheral identified at the Title Gate5. The input subsystem listens for corresponding action dispatches (IA\_Jump, IA\_Interact), unlocking navigation triggers only when the mechanical condition resolves.

Initial combat and hazard sequences employ safe failure mechanics. Enemy artificial intelligence (AI) subroutines run simplified decision trees with wide reaction delays, suppressed attack tokens, and reduced damage modifiers. This provides a low-penalty environment for players to master offensive, evasive, and defensive timing before high-stakes encounters.

HUD components are integrated progressively rather than appearing simultaneously at initial boot. Health bars, stamina meters, ammunition readouts, and navigational minimaps initialize and fade into view only as their associated mechanics are introduced, minimizing initial cognitive load.

### **Core Gameplay Loops, Progression Gating, and Narrative Milestones**

Following onboarding, the game stabilizes into its core operational structure, which functions as a system of nested loops:

![][image6]

The micro-loop governs second-to-second mechanical responses: polling inputs, advancing character state machines, evaluating skeletal animation blend trees, resolving collision volumes, executing physics simulations, and triggering visual effects and audio responses. In action titles, this loop includes weapon swings, hitbox and hurtbox intersections, hit-stop pauses, and screen-shake calculations.

The meso-loop operates on a minute-to-minute cadence, driving encounter clearing, spatial traversal, environmental puzzle resolution, and resource scavenging. This loop manages mechanical pacing by balancing tension (such as combat encounters) with recovery (such as navigation corridors, narrative dialogue, and inventory maintenance).

The macro-loop spans hours of play, directing narrative chapter advancement, skill tree progression, character stat scaling, gear acquisition, and broad world-state modifications.

Progression pacing through this loop relies on spatial and mechanical gating, as seen in the lock-and-key designs of the *Metroidvania* and *The Legend of Zelda* lineages. Navigational pathways are restricted by explicit environmental barriers (such as heavy obstacles, high ledges, locked gates, or hazardous elements) that require specific tools or character upgrades found in subsequent levels. Acquiring an ability grants systemic access to previously unreachable sectors, incentivizing backtracking while maintaining structured narrative pacing across the world.

Boss encounters serve as pacing anchors and narrative milestones, testing the mechanical skills introduced across the preceding zone. Boss architecture relies on deterministic multi-phase state machines:

* *Phase One (Pattern Establishment):* The boss demonstrates standard attack sequences with visible telegraphing wind-up frames, predictable hit zones, and generous recovery windows.  
* *Phase Two (Escalation and Arena Modulation):* Reaching a calibrated health threshold (typically sixty-six percent) triggers an invulnerable transition state. The boss plays an animation, alters the physical arena (breaking pillars or flooding areas), and adds secondary attack vectors, projectile spreads, or tight counter-attack windows.  
* *Phase Three (Enrage and Climax):* At the final threshold (typically thirty-three percent), the boss enters a heightened state characterized by compressed recovery animations, expanding area-of-effect hazards, and narrow vulnerability windows, demanding mastery of the game's core micro-loop.

Underpinning these gameplay encounters is dynamic audio processing managed by middleware such as Audiokinetic Wwise or FMOD. Traditional game audio deploys two primary techniques to adapt music to active gameplay states9:

Vertical Layering (or Stem Mixing) involves arranging a musical track into multiple synchronized stems (such as ambient pads, bass lines, strings, and percussion) that loop simultaneously at the same tempo and bar length9. The audio engine modulates real-time gain across these stems based on gameplay intensity parameters. While exploring, only ambient and light string tracks are unmuted; when entering combat, the engine fades in percussion and brass stems to heighten tension9.

Horizontal Resequencing divides musical compositions into discrete, modular segments configured with synchronized entry, exit, and transition points9. When a player crosses a narrative trigger or transitions between zones, the engine schedules an exit out of the current segment at the next downbeat or bar boundary, crossfading into a new segment and often triggering an orchestral stinger to mask the transition9.

### **Climactic Resolution, Epilogue Sequences, and Post-Game Persistence**

The final narrative movement transitions the player through the climax and into post-game persistence. As the narrative approaches its apex, the level design introduces an explicit Point of No Return—a physical threshold, sealed blast door, or story prompt warning that previous zones will become temporarily or permanently inaccessible.

Reaching this boundary allows the engine to unload secondary world sectors, unneeded ambient audio banks, and inactive NPC AI allocations from system memory. This frees system RAM and GPU resources to render the final boss arena at peak graphical fidelity.

Following the defeat of the final boss, the game executes its resolution pipeline:

* *Denouement Cinematics:* High-fidelity in-engine or pre-rendered cutscenes complete dramatic character arcs and resolve primary conflicts, transitioning into the ending sequences.  
* *Credits Presentation:* Credits roll either as a scrolling 2D UI stack over cinematic footage or as an interactive credits sequence that lets players control character movements or play miniature encounters during the text display.  
* *Post-Credits Narrative Epilogue:* A brief cinematic scene that resolves secondary character threads or introduces plot points for future installments.  
* *Post-Game Serialization:* The engine serializes the completed game state to persistent storage. It sets an immutable story completion flag, tallies lifetime statistics (including playtime, collection percentages, and death counts), and unlocks bonus modes.  
* *New Game Plus (NG+) and Extras Initialization:* The player returns to a modified Main Menu. The Title Gate and Main Menu UI dynamically reflect the completed state through alternative background art, updated menu music, or completion badges. The New Game Plus subsystem allows players to restart the narrative campaign while retaining character progression, stats, and equipment, scaling up enemy damage and health pools to sustain mechanical challenge.

## **Macro-Architecture Flow: Boot Ingestion to Post-Game Credits**

The structural flowchart below details the sequential progression, system checks, subsystem executions, and error mitigations that guide an application from cold hardware boot to post-game persistence.

&nbsp;

| Structural Phase | Input / System Trigger | Primary Subsystem | Subsystem Action and Logic | Next State Transition |
| :---- | :---- | :---- | :---- | :---- |
| **01\. Hardware POST** | System Power On / Kernel Boot | Platform BIOS / OS | Authenticate cryptographic keys, verify disc/cartridge signatures, map memory spaces. | EngineInit |
| **02\. Engine Allocation** | Binary Entry Point Fired | Game Runtime Core | Allocate fixed heap pools, assign thread affinity, bind native graphics/audio contexts. | SplashSequence |
| **03\. Splash Presentation** | Runtime Init Succeeded | Video Engine / TRC Pipeline | Display platform logos, publisher/developer identity, and third-party middleware licenses1. | TitleGate |
| **04\. Title Gate** | Assets Pre-cached to Memory | Input Subsystem / Auth | Render Title Gate; enforce TRC 30-second interactivity deadline; run Attract Mode watchdog timer2. | ProfileMount |
| **05\. Attract Mode Handler** | Idle Timer ![][image7] Without Input | Video Streamer / Replay Engine | Interrupt Title Gate; loop promotional demo footage or deterministic gameplay replays2. | TitleGate |
| **06\. Device & Profile Mount** | Hardware Action Interrupt Fired | Input Registry / Storage Manager | Assign active controller ID to Player Index 0; mount user storage sandbox; verify profile cloud entitlements2. | MainMenu |
| **07\. Main Menu Presentation** | Storage Handshake Confirmed | UI Hierarchy Manager | Check save slots via CRC32 checks; present New Game, Continue, Options, Extras. | User Selection |
| **08\. Game Launch / Prologue** | New Game Selected by User | Scene Loader / Camera Manager | Load prologue map; run opening cinematic; interpolate camera track smoothly into gameplay rig. | OnboardingZone |
| **09\. Onboarding & Tutorial** | Player Receives Avatar Control | Tutorial Director / Dynamic HUD | Isolate movement mechanics; intercept button presses via contextual glyphs; reveal HUD elements progressively. | CoreMacroLoop |
| **10\. Macro Gameplay Loop** | Onboarding Boundary Exited | Core World Director | Run nested micro/meso loops; resolve combat/traversal; apply vertical and horizontal dynamic music9. | ProgressionGate |
| **11\. Progression Lock & Key** | Environmental Obstacle Reached | Level Flow Manager | Evaluate character tool/ability inventory; grant passage or route player to unlock requirements. | BossEncounter |
| **12\. Milestone Boss Arena** | Encounter Volume Triggered | Boss State Machine / Audio Core | Seal arena geometry; run three-phase boss AI; modulate dynamic combat stems across phases9. | PointOfNoReturn |
| **13\. Point of No Return** | Climax Gate Crossed by Avatar | Memory Manager / Level Streamer | Lock world navigation; unload open-world background sectors; allocate peak memory to final boss arena. | ClimacticEncounter |
| **14\. Final Encounter** | Climax Cinematic Ends | Boss FSM / Combat Subsystem | Run high-intensity encounter mechanics; evaluate win/loss conditions; trigger death animations. | DenouementCinematic |
| **15\. Epilogue & Credits** | Final Boss HP Evaluated to Zero | Sequencer / Video Subsystem | Play narrative denouement cutscenes; roll interactive or scrolling credits; present post-credits stinger. | PostGameSerialization |
| **16\. Post-Game Persistence** | Credits Sequence Finished | Storage Subsystem (Atomic POSIX) | Write completion flag; flush volatile caches; execute atomic rename on save container13. | PostGameTitleMenu |
| **17\. Dynamic Menu Loop** | Save Container Committed | UI / Progression Manager | Reload Main Menu with modified title art, updated theme music, and unlocked New Game Plus mode. | User Loop |

## **Game State Architecture: Formalisms and Engine Frameworks**

To coordinate state transitions across boot sequences, UI hierarchies, gameplay loops, cutscenes, and pause overlays without race conditions, game systems rely on formal state machine architectures.

### **Finite State Machines versus Stack-Based Pushdown Automata**

A standard Finite State Machine (FSM) is formally defined as a 5-tuple:

![][image8]

where ![][image9] is a finite set of discrete states, ![][image10] is the input alphabet (events or triggers), ![][image11] is the state transition function, ![][image12] is the initial state, and ![][image13] is the set of final states.

While adequate for isolated entity behaviors (such as a basic enemy patrol-investigate-attack loop), a flat FSM encounters severe architectural limits when managing global game flow. The primary limitation of a flat FSM is its lack of historical context: transitioning from state ![][image14] to state ![][image15] fully overwrites the active state15.

When an interruption occurs—such as a player pausing the game, an operating system overlay appearing, or a controller disconnecting—a flat FSM cannot inherently track which state was interrupted15. To return to the correct previous context, developers would need to introduce complex conditional flags, causing a combinatorial explosion of transition paths.

To resolve this limitation, game system architects deploy a Pushdown Automaton (PDA), which augments an FSM with an unbounded Last-In-First-Out (LIFO) stack15. Formally, a pushdown automaton is defined as a 7-tuple:

![][image16]

where:

* ![][image9] represents a finite set of states17.  
* ![][image10] represents the input alphabet (events, interrupts)17.  
* ![][image17] represents the finite stack alphabet (game state descriptors)17.  
* ![][image18] is the transition relation18.  
* ![][image12] is the initial start state17.  
* ![][image19] is the initial stack bottom symbol17.  
* ![][image13] is the set of accepting final states17.

In a game architecture governed by a Pushdown Automaton, application states are pushed to and popped from an active execution stack15. When a player presses the pause button during active play, the GameplayState is not purged from memory. Instead, the engine pushes PauseMenuState to the top of the stack15. The runtime halts tick loops for underlying game actors, freezes physics updates, and redirects input polling directly to PauseMenuState21.

If the player navigates into AudioSettingsState, this new interface is pushed onto the stack above PauseMenuState16. Pressing the back button executes a pop operation, destroying AudioSettingsState and returning focus to PauseMenuState16. Resuming the game pops PauseMenuState, returning GameplayState to the top of the stack. This restores world ticking and player control instantly, without requiring the engine to reload assets, reconstruct level geometry, or re-parse player status arrays15.

### **Architectural Patterns in Modern Engines: The Unreal Engine Gameplay Framework**

The separation of long-lived system management from transient level logic is clearly illustrated by the Unreal Engine Gameplay Framework21. This framework establishes clear architectural boundaries between persistent data stores, server-authoritative rules, and local input processing21.

The UGameInstance represents the top-level application lifecycle, initializing when the process launches and persisting until the binary shuts down21. Unlike level actors, the game instance is not purged during map transitions (LoadMap), making it the primary system for managing network session drivers, user profile credentials, and cached save data21.

When a map file loads, the engine instantiates an active world space (UWorld), which initializes an AGameModeBase (or its multiplayer derivative AGameMode)21. The GameMode functions as the server-authoritative rule set21. It validates win and loss conditions, manages pawn spawn logic, controls game timeouts, and decides whether the simulation can pause21. In multiplayer environments, the GameMode exists solely on the authoritative server to prevent client-side memory tampering; connected clients hold null pointers to this class21.

To communicate match data to connected machines, the GameMode instantiates an AGameStateBase21. The GameState is replicated to every connected client, acting as a global scoreboard that tracks match timers, team scores, and high-level state flags (such as waiting to start, in progress, or post-match)21.

Player interactions are routed through the APlayerController, which bridges human inputs and in-game avatars21. A PlayerController exists on the local client for the human user and on the authoritative server for each connected participant21. It receives raw hardware events from keyboards, mice, or gamepads, processes them through input contexts, and sends command vectors to its possessed APawn or ACharacter21.

The PlayerController also manages player-facing viewports, camera rigs, and client-side UI canvases22. Individual player variables—such as current health, score, and cosmetic profiles—are attached to an APlayerState actor, which replicates across all clients to populate leaderboards and UI HUDs without requiring direct access to the underlying pawn21.

## **Native Platform Certification and Modern Technical Compliance**

Developing for dedicated gaming consoles (PlayStation 5, Xbox Series X|S, Nintendo Switch) requires compliance with platform certification suites: Sony TRC, Microsoft XR, and Nintendo Lotcheck4. Certification is a formal platform gate; failures reset submission queues, create launch delays, and incur significant engineering rework costs5.

### **Platform Certification Handshakes and Boundary Conditions**

Compliance failures most commonly stem from platform boundary conditions rather than standard gameplay bugs4. The architecture must handle real-time interruptions, input changes, and power transitions gracefully:

Modern consoles rely on rapid hardware suspension systems, such as Xbox Quick Resume or PlayStation Rest Mode5. Games must handle rapid power state changes without memory corruption, thread locks, or audio hitches4. When the operating system issues a suspend notification, the engine must pause active simulation timers, halt streaming file threads, mute audio buses, and release volatile graphics contexts.

Upon receiving a resume notification, hardware handshakes must verify user account integrity, re-synchronize time offsets to account for clock drift, and restore asset pipelines without dropping active session states4.

If a controller battery runs out or loses its wireless connection, platform certification requires the game to immediately pause the simulation and display an operating-system-compliant message informing the player4. The game must prevent ongoing damage to the player's avatar during the disconnect and continue polling hardware buses until an assigned controller reconnects4.

If an active user profile signs out or switches accounts via the operating system overlay, the engine must handle the transition securely2. Active network sessions must be terminated, pending save operations resolved, player-specific memory caches cleared, and the application returned cleanly to the Title Gate to establish a new user context2.

Loss of local Wi-Fi or Ethernet connectivity must never cause an application to crash4. Network layers must decouple offline gameplay states from online dependencies, providing non-blocking retry loops and localized UI notifications that let players continue offline if a connection drops4.

### **Storage Durability and the Atomic Save Protocol**

Save data corruption represents a critical platform certification failure4. If power is lost or the console is unplugged during a disk write, an incomplete file can render the save container permanently unreadable14.

To guarantee storage durability, console engines avoid overwriting valid save files directly27. Instead, systems implement the **Atomic Save Pattern**, utilizing low-level POSIX file operations14:

The runtime serializes the active game state into an uncompressed or binary-packed memory buffer (such as FlatBuffers or packed structs), calculating an appended cryptographic signature (such as SHA-256 or CRC32) alongside schema version tags.

The engine creates a uniquely named temporary file on the storage drive (such as save\_slot\_01.tmp).

The payload is written to this temporary file. Once writing completes, the engine calls flush() to clear application-level write buffers to the operating system kernel, followed by an explicit fsync() invocation13. The fsync() call forces the storage hardware controller to flush volatile disk caches and commit the data to physical non-volatile flash memory13.

The engine then executes an atomic rename call, replacing the active target file with the temporary file (for example, rename("save\_slot\_01.tmp", "save\_slot\_01.dat"))14. In POSIX-compliant filesystems, renaming an existing target within the same file system changes inode pointers atomically14.

If a sudden power loss occurs before or during this directory update, the file system pointer retains the original, uncorrupted save\_slot\_01.dat file14. Finally, the engine calls fsync() on the containing directory handle to force file system journal metadata updates to disk, guaranteeing persistence across sudden hardware failures14.

### **Accessibility Architecture (Xbox Accessibility Guidelines \- XAG)**

Modern game architecture mandates inclusive software design from the ground up, as formalized by frameworks like the Xbox Accessibility Guidelines (XAG)28. Integrating accessibility features early prevents costly structural rework late in production29.

Under XAG 103, critical game information must never be delivered through a single sensory channel28. Audio warnings of incoming off-screen attacks must be paired with visible screen indicators, directional markers, and haptic feedback pulses28. Dialogue and critical sound cues must be supported by customizable subtitles that include adjustable text sizes, speaker identification labels, and high-contrast letterboxing33.

Under XAG 107, all digital and analog inputs must be fully remappable33. The input subsystem must support adjustable analog deadzones, sensitivity curves, and stick-swapping configurations33. Systems must provide toggles for actions that traditionally require prolonged holds (such as converting a hold-to-aim to a toggle-aim) and offer alternatives to rapid button mashing (Quick Time Events), allowing players to replace mashed inputs with single button holds33.

Under XAG 114, interfaces must support non-destructive text scaling, screen magnifier integration, and high visual contrast (minimum 4.5:1 for critical text, 3:1 for graphical UI elements)33. UI menus must provide clear focus indicators and remain fully navigable via screen readers, integrating contextual text-to-speech narrations33.

## **Modern Web Game Runtime Architecture**

Deploying games to modern web runtimes introduces unique technical constraints. Unlike console games operating on bare-metal hardware with fixed memory allocations, web games run in sandboxed browser environments governed by asynchronous event loops, automated garbage collection, and dynamic security policies.

### **Graphics Pipelines and Multi-Threaded Execution**

Historically, browser-based games relied on WebGL, an imperative JavaScript mapping over the legacy OpenGL ES specification. WebGL incurs CPU overhead because the browser must validate state changes on the main thread for every draw call.

Modern web architecture is shifting toward WebGPU, a low-level graphics and compute API that aligns with modern native graphics backends like Vulkan, DirectX 12, and Metal. WebGPU minimizes CPU driver validation overhead through pre-compiled pipeline states and direct resource binding groups, while granting engines direct access to general-purpose GPU compute shaders. This allows browsers to offload particle physics, skeletal mesh skinning, and occlusion culling directly to the graphics hardware.

The primary bottleneck in web development is the browser's single-threaded UI loop, where Document Object Model (DOM) evaluations, CSS style calculations, garbage collection sweeps, and user input events compete for execution time. Heavy simulation workloads on the main thread cause dropped frames and unresponsive inputs.

To maintain consistent framerates, modern web engines decouple rendering from the DOM thread using an OffscreenCanvas running within a dedicated Web Worker36:

> 1. The main thread queries the canvas element and invokes canvas.transferControlToOffscreen(), transferring surface control to a background Web Worker37.  
> 2. The worker initializes a WebGPU or WebGL context directly over the transferred canvas, running its render loop independently from DOM layout updates38.  
> 3. The main thread captures browser input events (keydown, keyup, pointerdown) and writes packed input states directly into a SharedArrayBuffer using atomic memory operations (Atomics), avoiding the performance overhead of serialized postMessage calls42.  
> 4. The background worker reads input states directly from shared memory, advances the simulation, and issues GPU draw commands38. This architecture ensures that even if the DOM layout stalls or the main thread encounters heavy garbage collection, the game's simulation and rendering loops remain unblocked39.

### **The Deterministic Fixed Timestep and "Spiral of Death" Mitigation**

A frequent pitfall in web game loops is coupling physical simulation updates directly to the browser's display refresh rate via requestAnimationFrame43. High-refresh screens (120Hz, 144Hz, 240Hz) cause unconstrained simulations to run too fast, while frame drops cause physics tunneling, where fast-moving objects clip through solid geometry43.

To ensure stable, deterministic physics across all hardware, modern engines deploy a **Fixed Timestep with Accumulator Loop**44. The simulation advances in discrete, uniform steps (e.g., ![][image20]), while real-world frame delta times are accumulated:

![][image21]

![][image22]

While ![][image23], the engine executes a discrete physical tick:

![][image24]

![][image25]

If a single physics integration step is computationally expensive, or if the browser encounters a massive frame stutter (such as a garbage collection pause or tab backgrounding), ![][image26] can spike dramatically (e.g., to ![][image27])43. The accumulator then demands multiple successive simulation steps to catch up43.

However, running multiple physics ticks takes longer than the real-time frame budget, causing the subsequent frame to register an even larger ![][image26]43. This triggers a positive feedback loop known as the **Spiral of Death**, which freezes the application thread43.

To mitigate this, engines enforce an explicit frame-time ceiling, capping real-world delta times before adding them to the accumulator44:

![][image28]

Setting ![][image29] to a threshold such as ![][image30] ensures that even during massive frame drops, the accumulator only executes a bounded number of catch-up ticks, allowing the simulation to recover gracefully.

The interpolation factor ![][image31] measures the remaining fraction of time between physics frames. The rendering engine uses ![][image32] to linearly blend character transforms between their previous and current physical states (![][image33]), ensuring smooth visuals without introducing non-deterministic physics jitter.

### **Web Storage Architectures: OPFS vs. Legacy Storage**

Web storage has evolved significantly beyond the legacy, synchronous localStorage API, which is restricted to a blocking 5MB storage limit and causes major frame drops during disk access46. Modern web games rely on a tiered storage architecture:

&nbsp;

| Storage Technology | Data Formats | Thread Availability | Maximum Storage Capacity | Performance Characteristics | Primary Engine Use Case |
| :---- | :---- | :---- | :---- | :---- | :---- |
| localStorage | Strings only | Main Thread only | ![][image34] | Synchronous, blocking; interrupts rendering pipeline. | User preferences, volume settings, audio mute flags46. |
| IndexedDB | Structured JS Objects, Blobs | Main & Worker Threads | Up to dynamic origin quota (![][image35] disk)48 | Asynchronous; transactional overhead on high-frequency writes. | Downloaded asset caching, inventory metadata47. |
| **Origin Private File System (OPFS)** | Raw Binary (ArrayBuffer, Blobs) | Dedicated Workers (SyncAccessHandle)49 | Up to dynamic origin quota (![][image36], browser-managed)46 | **Synchronous zero-overhead in-place writes via dedicated worker**49. | Large game save states, level chunk caching, SQLite Wasm databases46. |

The **Origin Private File System (OPFS)** provides a sandboxed, virtual filesystem dedicated exclusively to the application's origin46. The user cannot browse or modify these files directly46. Inside a dedicated Web Worker, OPFS grants access to FileSystemSyncAccessHandle, which provides direct, synchronous, in-place binary read and write operations on disk files49.

Because FileSystemSyncAccessHandle bypasses the asynchronous Promise-based overhead of typical browser APIs, it matches the performance of native C++ file operations49. This makes it the preferred storage architecture for compiled WebAssembly engines and embedded SQLite databases running in the browser47.

To protect save data from automated browser storage eviction during low-disk-space events, engines request explicit storage persistence permissions via the browser's storage manager API (navigator.storage.persist())48.

### **Responsive Surface Sizing and Unified Input Abstraction**

Browser runtimes operate across diverse device viewports, ranging from high-density 4K desktop monitors to mobile displays. A web game engine must reconcile display pixel densities with rendering canvas resolution.

If an engine assigns a canvas element a layout size of ![][image37], but ignores window.devicePixelRatio, high-density displays (such as Apple Retina screens with a scale factor of 2.0 or 3.0) will upscale the canvas blurrily through bilinear filtering. Conversely, setting the canvas's internal pixel dimensions to the full native resolution on high-DPI displays can cause massive fill-rate performance bottlenecks on integrated GPUs.

Modern engines clamp device pixel ratios to a maximum factor (typically 1.5 or 2.0), balancing sharp visual presentation against predictable GPU fill rates across varying display hardware.

Input handling in web runtimes requires an abstraction layer that unifies multiple input paradigms:

* *Mouse and Keyboard Capture:* Modern games capture mouse movement for 3D camera controls using the Pointer Lock API (canvas.requestPointerLock()). This hides the operating system cursor and delivers unbounded, raw relative movement values (movementX, movementY).  
* *Touch Subsystems:* Mobile interfaces dynamically generate virtual on-screen joysticks by capturing pointer events. By tracking event.pointerId, the engine isolates multi-touch inputs, mapping left-hand touches to movement vectors and right-hand touches to camera rotations.  
* *The Standard Gamepad API:* Gamepads connected via Bluetooth or USB cannot dispatch interrupt events to JavaScript. Instead, the Gamepad API relies on a polling model. The engine queries connected devices at the beginning of each simulation tick, normalizing vendor-specific stick drift by applying software deadzones:

![][image38]

Finally, web runtimes must track browser tab lifecycle events. When a user switches tabs, minimizes the window, or locks their mobile device, the browser dispatches the visibilitychange event. Modern web engines listen for document.visibilityState \=== "hidden" to automatically push the pause state to the pushdown automaton, pause Web Audio contexts, and suppress game simulation updates to avoid running out of memory while running in the background.

## **Cross-Platform Technical Comparison and State Transition Specification**

To provide clear operational specifications across development environments, the tables below outline the Pushdown Automaton state transitions for interruption recovery, followed by a comparative analysis of classical consoles, modern native consoles, and modern web runtimes.

### **Pushdown Automaton State Transition Matrix**

The table below details how runtime interruptions are managed via stack manipulations, preserving execution context across pause states, configuration menus, and platform hardware alerts.

&nbsp;

| Initial Stack Top (Stop​) | Interruption Event (σ) | Stack Operation | Target Stack State (Top → Bottom) | Subsystem Response and Behavior |
| :---- | :---- | :---- | :---- | :---- |
| BootState | BOOT\_COMPLETE | Stack Replace | \[TitleGateState\] | Low-level engine assets mapped; awaiting controller assignment and storage mounting2. |
| TitleGateState | CONTROLLER\_START\_PRESSED | Stack Replace | \[MainMenuState\] | Gamepad assigned to Player 0; profile storage sandbox mounted2. |
| MainMenuState | NEW\_GAME\_SELECTED | Stack Replace | \[NarrativeCinematicState\] | Level geometry streamed; non-interactive cinematic sequencer active. |
| NarrativeCinematicState | CINEMATIC\_FINISH / SKIP | Stack Replace | \[GameplayState\] | Camera interpolates to player rig; gameplay micro-loops and HUD initialized. |
| GameplayState | PLAYER\_PAUSE\_BUTTON | Stack Push | \[PauseMenuState, GameplayState\] | Physics ticks halted; actor updates frozen; input routed to pause menu UI16. |
| PauseMenuState | SELECT\_SETTINGS | Stack Push | \[AudioVideoSettingsState, PauseMenuState, GameplayState\] | Pause menu suspended; settings configuration interface rendered16. |
| AudioVideoSettingsState | SETTINGS\_BACK\_PRESSED | Stack Pop | \[PauseMenuState, GameplayState\] | Settings serialized to disk; focus returned to pause menu16. |
| PauseMenuState | RESUME\_GAME | Stack Pop | \[GameplayState\] | Pause menu UI destroyed; world physics and simulation loops resume16. |
| GameplayState | HARDWARE\_PAD\_DISCONNECT | Stack Push | \[ModalControllerAlertState, GameplayState\] | TRC mandate triggered; simulation auto-paused; system dialog rendered4. |
| ModalControllerAlertState | CONTROLLER\_RECONNECTED | Stack Pop | \[GameplayState\] | Gamepad index re-established; modal dialog dismissed; simulation resumes4. |
| GameplayState | FINAL\_BOSS\_DEFEATED | Stack Replace | \[EndingCreditsState\] | World unloaded; credits pipeline and background scenes initialized. |
| EndingCreditsState | CREDITS\_COMPLETE | Stack Replace | \[ContextualPostGameMenuState\] | Save data finalized with completion flags; NG+ parameters unlocked. |

### **Technical Architecture Comparison**

The table below contrasts classical consoles, modern native platforms, and modern web environments across core architectural subsystems.

&nbsp;

| System Subsystem | Classical Console (Gen 5–7: PS1, PS2, Xbox 360\) | Modern Native Console (PS5, Xbox Series X|S) | Modern Web Application (Wasm, WebGPU, Web Workers) |
| :---- | :---- | :---- | :---- |
| **Execution Environment** | Monolithic bare-metal C/C++ native code; single address space1. | Sandboxed OS virtual machine; native multithreaded C++ engine5. | Sandboxed browser process; WebAssembly bytecode \+ JavaScript thread bridge38. |
| **Memory Management** | Static memory allocation; explicit heap sizing; zero OS paging. | Dynamic OS virtual allocations; unified GDDR6 memory pools5. | Managed heap with browser Garbage Collection (GC); linear Wasm memory arrays. |
| **Primary Graphics API** | Direct hardware registers or platform APIs (e.g., PS2 GS, GCM, Direct3D 9). | Low-level modern APIs: DirectX 12 Ultimate (DirectStorage), PlayStation LibGlass / AGC. | WebGPU / WebGL2 rendering via OffscreenCanvas in background workers38. |
| **Threading Architecture** | Single-core primary thread; manual coprocessor/SPU scheduling (e.g., PS3 Cell). | Preemptive hardware multi-threading across 8-core / 16-thread x86-64 architectures50. | Dedicated Web Workers communicating with the main DOM thread via SharedArrayBuffer and Atomics42. |
| **Asset Streaming Pipeline** | Synchronous CD/DVD/HDD reads; level loading pauses; early background streaming. | DirectStorage / NVMe hardware decompression; near-zero loading times. | Asynchronous HTTP range fetches; asset chunking via Fetch API, Cache API, and Wasm decompression47. |
| **Storage Architecture** | Direct memory card blocks or flat FAT32 disk containers1. | Encrypted platform-managed virtual file systems; atomic saves; secure cloud sync4. | Origin Private File System (OPFS) with FileSystemSyncAccessHandle \+ IndexedDB47. |
| **Input Hardware Loop** | Direct polling of memory-mapped controller ports or SPI bus registers. | High-frequency USB HID/Bluetooth polling with haptic feedback pipelines. | Gamepad API polling in simulation loops; Pointer Lock API; dynamic touch handlers. |
| **Compliance Framework** | Sony TRC, Microsoft TCR, Nintendo Lotcheck1. | Updated TRC, Xbox Requirements (XR), Nintendo Lotcheck, Xbox Accessibility Guidelines5. | W3C Web Accessibility (WCAG 2.2), PWA Installation Manifests, Cross-Origin Isolation policies. |
| **Session Lifecycle Handling** | Reset vectors; loss of system power results in instant state termination27. | Suspend-to-RAM / SSD (Quick Resume); instant resume without losing context4. | Page Lifecycle API (visibilitychange, freeze, resume); tab discard mitigations. |

## **Architectural Synthesis and Implementation Principles**

The technical evolution from classical console hardware to modern cross-platform engines demonstrates a steady movement toward decoupled, resilient state architectures. While historical architectures relied on tightly bound, hardware-specific loops designed for static memory models, modern game engineering demands fault-tolerant systems capable of handling unexpected interruptions across native operating systems and sandboxed browser runtimes.

To deliver robust software across platforms, architectures must isolate persistent engine systems from transient level data. Long-lived services—including user authentication, cloud profile synchronization, dynamic audio routing, and input device registries—must reside within a persistent instance lifecycle to prevent memory fragmentation and data loss across scene boundaries.

Application flow should be managed through formal stack-based Pushdown Automata rather than flat state machines, allowing systems to push temporary overlays—such as pause menus, hardware disconnection alerts, and accessibility configurations—without losing underlying gameplay contexts.

Data persistence must prioritize durability above all else. Because sudden power interruptions, system crashes, and storage ejections remain common failure points, developers should enforce atomic save patterns across both native filesystems and modern browser storage APIs. By writing serialized payloads to temporary buffers, flushing kernel caches via explicit sync barriers, and executing atomic renames, titles eliminate save corruption risks.

Finally, web-based runtimes require strict thread isolation. Decoupling physics integration and rendering from the browser's DOM thread using dedicated Web Workers, OffscreenCanvas, and linear shared memory buffers shields the simulation loop from garbage collection pauses and UI overhead.

Combined with accumulator-driven fixed timesteps and proactive accessibility compliance from early prototyping, these architectural foundations ensure high-performance, deterministic execution whether running bare-metal on dedicated console silicon or inside a sandboxed web browser.

#### **Works cited**

> 1. Technical Requirements Checklist for PlayStation® Software, [https://psx.arthus.net/sdk/Psy-Q/DOCS/TECHNOTE/mtrc13.pdf](https://psx.arthus.net/sdk/Psy-Q/DOCS/TECHNOTE/mtrc13.pdf)  
> 2. Why do games still have "Press start" screens? : r/gamedev \- Reddit, [https://www.reddit.com/r/gamedev/comments/4nm7d4/why\_do\_games\_still\_have\_press\_start\_screens/](https://www.reddit.com/r/gamedev/comments/4nm7d4/why_do_games_still_have_press_start_screens/)  
> 3. Game Development Essentials: Game Qa & Testing \[PDF\] \- Vdoc.pub, [https://vdoc.pub/documents/game-development-essentials-game-qa-testing-5kq0glmr4t40](https://vdoc.pub/documents/game-development-essentials-game-qa-testing-5kq0glmr4t40)  
> 4. The Future of Compliance Game QA for Consoles \- iXie Gaming, [https://www.ixiegaming.com/blog/beyond-the-checklist-the-future-of-compliance-game-qa-for-consoles/](https://www.ixiegaming.com/blog/beyond-the-checklist-the-future-of-compliance-game-qa-for-consoles/)  
> 5. Why Outsourced Console Games Fail TRC and XR Certification, [https://www.juegostudio.com/blog/console-certification-failures-outsourced-games](https://www.juegostudio.com/blog/console-certification-failures-outsourced-games)  
> 6. ELI5: Why do so many games have a "start" screen where ... \- Reddit, [https://www.reddit.com/r/explainlikeimfive/comments/2c8qwj/eli5\_why\_do\_so\_many\_games\_have\_a\_start\_screen/](https://www.reddit.com/r/explainlikeimfive/comments/2c8qwj/eli5_why_do_so_many_games_have_a_start_screen/)  
> 7. What is the purpose of a "press start" screen?, [https://gamedev.stackexchange.com/questions/14182/what-is-the-purpose-of-a-press-start-screen](https://gamedev.stackexchange.com/questions/14182/what-is-the-purpose-of-a-press-start-screen)  
> 8. Just a friendly reminder to Epic, that we still want this horrible, [https://www.reddit.com/r/FortniteBR/comments/a2pfjz/just\_a\_friendly\_reminder\_to\_epic\_that\_we\_still/](https://www.reddit.com/r/FortniteBR/comments/a2pfjz/just_a_friendly_reminder_to_epic_that_we_still/)  
> 9. Composing for Video Games & Interactive Media \- Indiefy, [https://indiefy.net/blog/composing-for-video-games--interactive-media-a-practical-in-depth-guide-for-independent-musicians](https://indiefy.net/blog/composing-for-video-games--interactive-media-a-practical-in-depth-guide-for-independent-musicians)  
> 10. How To Make Music For Video Games \- Game Audio Learning, [https://www.gameaudiolearning.com/knowledgebase/how-to-make-music-for-video-games](https://www.gameaudiolearning.com/knowledgebase/how-to-make-music-for-video-games)  
> 11. Making Your Game's Music More Dynamic: Vertical Layering vs, [https://www.thegameaudioco.com/making-your-game-s-music-more-dynamic-vertical-layering-vs-horizontal-resequencing](https://www.thegameaudioco.com/making-your-game-s-music-more-dynamic-vertical-layering-vs-horizontal-resequencing)  
> 12. Horizontal Resquencing and Song Structure for Game Music, [https://winifredphillips.wpcomstaging.com/2021/08/15/horizontal-resquencing-and-song-structure-for-game-music-composers-from-spyder-to-sackboy-gdc-2021/](https://winifredphillips.wpcomstaging.com/2021/08/15/horizontal-resquencing-and-song-structure-for-game-music-composers-from-spyder-to-sackboy-gdc-2021/)  
> 13. Your system prompt isn't instructions. It's data. \- DEV Community, [https://dev.to/natuworkguy/your-system-prompt-isnt-instructions-its-data-43m8](https://dev.to/natuworkguy/your-system-prompt-isnt-instructions-its-data-43m8)  
> 14. HN Time Capsule \- 2015-12-13, [https://karpathy.ai/hncapsule/2015-12-13/index.html](https://karpathy.ai/hncapsule/2015-12-13/index.html)  
> 15. State · Design Patterns Revisited \- Game Programming Patterns, [https://gameprogrammingpatterns.com/state.html](https://gameprogrammingpatterns.com/state.html)  
> 16. Godot State Machine Complete Tutorial: Game AI Implementation, [https://generalistprogrammer.com/tutorials/godot-state-machine-complete-tutorial-game-ai](https://generalistprogrammer.com/tutorials/godot-state-machine-complete-tutorial-game-ai)  
> 17. Pushdown Automata: Theory & Extensions \- Emergent Mind, [https://www.emergentmind.com/topics/pushdown-automaton-pda](https://www.emergentmind.com/topics/pushdown-automaton-pda)  
> 18. Pushdown Automata: Components & Examples | Vaia, [https://www.vaia.com/en-us/explanations/computer-science/theory-of-computation/pushdown-automata/](https://www.vaia.com/en-us/explanations/computer-science/theory-of-computation/pushdown-automata/)  
> 19. On implementing a Finite State Machine framework, [https://www.patrickvanbergen.com/on\_fsm/on\_fsm.html](https://www.patrickvanbergen.com/on_fsm/on_fsm.html)  
> 20. Game State Gem \- Open 3D Engine \- O3DE, [https://www.docs.o3de.org/docs/user-guide/gems/reference/gameplay/game-state/](https://www.docs.o3de.org/docs/user-guide/gems/reference/gameplay/game-state/)  
> 21. Game Framework: GameMode, State, and PlayerController, [https://cosmiclearn.com/ue5/game-framework-basics.php](https://cosmiclearn.com/ue5/game-framework-basics.php)  
> 22. Unreal Engine \- Jorge Israel Peña, [https://jip.dev/notes/unreal-engine/](https://jip.dev/notes/unreal-engine/)  
> 23. Unreal Engine Online Subsystem and Multiplayer \- Hash Hackers, [https://blog.hashhackers.com/blog/unreal-engine-multiplayer/](https://blog.hashhackers.com/blog/unreal-engine-multiplayer/)  
> 24. The Unreal Engine Game Framework: From int main() to BeginPlay, [https://www.youtube.com/watch?v=IaU2Hue-ApI](https://www.youtube.com/watch?v=IaU2Hue-ApI)  
> 25. Engine | Unreal Engine 5.8 Documentation \- Epic Games Developers, [https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine)  
> 26. Guide to game testing: process, tools, and costs, [https://game-ace.com/blog/guide-to-game-testing/](https://game-ace.com/blog/guide-to-game-testing/)  
> 27. How exactly does a video game get corrupted when turning it off, [https://www.quora.com/How-exactly-does-a-video-game-get-corrupted-when-turning-it-off-while-saving](https://www.quora.com/How-exactly-does-a-video-game-get-corrupted-when-turning-it-off-while-saving)  
> 28. Xbox Accessibility Guideline 103 \- Microsoft Game Dev, [https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/103](https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/103)  
> 29. Updated Xbox Accessibility Guidelines: A Dialogue with Brannon, [https://www.gameaccessibilitynexus.com/blog/2021/02/27/updated-xbox-accessibility-guidelines-a-dialogue-with-brannon-zahand/](https://www.gameaccessibilitynexus.com/blog/2021/02/27/updated-xbox-accessibility-guidelines-a-dialogue-with-brannon-zahand/)  
> 30. The Future of Game Accessibility on Xbox \- XBOX Wire, [https://news.xbox.com/en-us/2021/02/16/xbox-accessibility-guidelines-and-testing/](https://news.xbox.com/en-us/2021/02/16/xbox-accessibility-guidelines-and-testing/)  
> 31. A call for a Standardized Accessibility Framework in Videogames, [https://simplyputpsych.co.uk/gaming-psych/a-call-for-a-standardized-accessibility-framework-in-videogames](https://simplyputpsych.co.uk/gaming-psych/a-call-for-a-standardized-accessibility-framework-in-videogames)  
> 32. Xbox's Accessibility Guidelines tackle the misconception that, [https://www.pcgamer.com/xboxs-accessibility-guidelines-tackle-the-misconception-that-accessibility-is-expensive/](https://www.pcgamer.com/xboxs-accessibility-guidelines-tackle-the-misconception-that-accessibility-is-expensive/)  
> 33. Accessibility Guidelines for VR Games \- A Comparison ... \- Frontiers, [https://www.frontiersin.org/journals/virtual-reality/articles/10.3389/frvir.2021.697504/full](https://www.frontiersin.org/journals/virtual-reality/articles/10.3389/frvir.2021.697504/full)  
> 34. Xbox Accessibility Guideline 107: Input \- Microsoft Learn, [https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/107](https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/107)  
> 35. Xbox Accessibility Guideline 114: UI context \- Microsoft Learn, [https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/114](https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/114)  
> 36. OffscreenCanvas—speed up your canvas operations with a web, [https://web.dev/articles/offscreen-canvas](https://web.dev/articles/offscreen-canvas)  
> 37. OffscreenCanvas: Browser Support, Features, Known Issues, [https://www.testmuai.com/learning-hub/offscreencanvas-browser-support/](https://www.testmuai.com/learning-hub/offscreencanvas-browser-support/)  
> 38. wgpu-example/README.md at main \- GitHub, [https://github.com/matthewjberger/wgpu-example/blob/main/README.md](https://github.com/matthewjberger/wgpu-example/blob/main/README.md)  
> 39. SVG vs Canvas vs WebGL: Which Should You Use? (2026, [https://www.svggenie.com/blog/svg-vs-canvas-vs-webgl-performance-2025](https://www.svggenie.com/blog/svg-vs-canvas-vs-webgl-performance-2025)  
> 40. Building Browser-Based Games in 2026: Why HTML5 Still Dominates, [https://dev.to/kingfoot2020/building-browser-based-games-in-2026-why-html5-still-dominates-45k9](https://dev.to/kingfoot2020/building-browser-based-games-in-2026-why-html5-still-dominates-45k9)  
> 41. Challenges and Optimization Strategies \- VIVERSE Documentation, [https://docs.viverse.com/optimization/challenges-and-optimization-strategies](https://docs.viverse.com/optimization/challenges-and-optimization-strategies)  
> 42. @weed.js/engine \- npm, [https://www.npmjs.com/package/@weed.js/engine](https://www.npmjs.com/package/@weed.js/engine)  
> 43. Fixed Timestep Game Loops in the Browser: Decoupling Simulation, [https://simplified.media/guides/fixed-timestep-loops](https://simplified.media/guides/fixed-timestep-loops)  
> 44. Game Programming Patterns: The Complete Catalog (2026), [https://generalistprogrammer.com/game-design-patterns](https://generalistprogrammer.com/game-design-patterns)  
> 45. A Detailed Explanation of JavaScript Game Loops and Timing, [https://isaacsukin.com/news/2015/01/detailed-explanation-javascript-game-loops-and-timing](https://isaacsukin.com/news/2015/01/detailed-explanation-javascript-game-loops-and-timing)  
> 46. How to Store Files on a User's Device Using OPFS \- Telerik.com, [https://www.telerik.com/blogs/how-store-files-user-device-opfs](https://www.telerik.com/blogs/how-store-files-user-device-opfs)  
> 47. (Almost) everything about storing data on the web \- Patrick Brosset, [https://patrickbrosset.com/articles/2023-01-17-web-storage/](https://patrickbrosset.com/articles/2023-01-17-web-storage/)  
> 48. The Browser Storage API \+ Cheat Sheet | by Tanvi Dadwal | Medium, [https://medium.com/@tanvidadwal799/the-browser-storage-api-cheat-sheet-be6e4afff0c0](https://medium.com/@tanvidadwal799/the-browser-storage-api-cheat-sheet-be6e4afff0c0)  
> 49. File System API \- MDN Web Docs, [https://developer.mozilla.org/en-US/docs/Web/API/File\_System\_API](https://developer.mozilla.org/en-US/docs/Web/API/File_System_API)  
> 50. 4.11 Released\! \- Epic Developer Community Forums \- Unreal Engine, [https://forums.unrealengine.com/t/4-11-released/59818](https://forums.unrealengine.com/t/4-11-released/59818)  
> 51. Xbox Accessibility Guidelines \- Microsoft Game Dev, [https://learn.microsoft.com/en-us/xbox/accessibility/guidelines](https://learn.microsoft.com/en-us/xbox/accessibility/guidelines)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFsAAAAWCAYAAACv8OArAAAAvElEQVR4Xu3SQQrDMAxEUd//0i1ZDJhB32pIF4kzD0qjkWJq0TEiIiKi9Zm+9fyLef7Me6/lS/J6xWe9jgn9k6vMVTN0XgxeTpW5aobOi8HLoVyoT7nM/W52O3RhyoX6lIv3vN4aLYdyoT7lsuptj5ZDuVCfclG/mxOfX31uj34o5UJ9yt3jFvUPdNkqc9UMnUfOzj8aXdazas7rQzU38143vx2/rNcHLcV7Xe28X535ClcufeXdiIiI2/gCaKd2impno2EAAAAASUVORK5CYII=>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFsAAAAWCAYAAACv8OArAAAAq0lEQVR4Xu3SQQrEMAwDwPz/0+3JYIQUO9BLag30EFtZtqJrmZmZ2dZDnq6cP7k3EpaL5wpm8WwJK5fNGJbp3h1JlaPmGdt37lnSKUxl1DzkfZUdoVOCyqh5wB2eR6nKCiqn5mG3G6dbhipVzUPsq1zA/O65xukfVnk1R9cW9QV84U4JbN+5l53mr4dfGStAzRDLZbir8r+CBVdls/nujHDPftMKLszMzH7hBc3ZeIi2NLdMAAAAAElFTkSuQmCC>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAAAWCAYAAAA2CDmeAAAAtElEQVR4Xu3UwQrEIBAD0P7/T7fMQRhCoo72pHnQg5mxy2Zhn8fMzMyO85KnIu9X7xqBP0alVNzHsy3YKZDdZZkV7BTI7rLMClqB1b8bta/ykGe9vautlqR2VR4wx7MRvUIztafyoHIbmClOFa/y0Ga9nQz3e88R1JdReaZ2VJ4dWeYfVCEsY9geyxT1+ddiZbCSWBZmswZn6r3XYoXgObQ9nGGGZ4Sz0f61dovZvW9mZmaLPuBic41IY823AAAAAElFTkSuQmCC>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAD8AAAAWCAYAAAB3/EQhAAAAPUlEQVR4Xu3SgQkAIBDDwO6/tKL40BUkOXCA9E0kSVJZ7+HgwnHBAxeOCx7I6Ia9fMMPcPgT4giXI0j61gZWQBPthxJu0gAAAABJRU5ErkJggg==>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAD8AAAAWCAYAAAB3/EQhAAAAQklEQVR4Xu3TwQkAMAgEweu/aQNBIU+/YXfAAu7URJJgqgcLX8CwiFjA5SUEXAB2+7jgqLAvVHDcWUtw8/PbkT52AL7AHeNUsL2aAAAAAElFTkSuQmCC>

[image6]: <data:image/png;base64,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>

[image7]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAWCAYAAACG9x+sAAAAQklEQVR4Xu3TMQoAIAwEQf//aUVIwNLCwj12IP0dScaQFGHWoEWUaDFlIkpsbuQH6C0gw+MCn3DhkSciPdQ/cDtSWbZQHeOS3OSwAAAAAElFTkSuQmCC>

[image8]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAkUAAABPCAYAAADlerGOAAADCklEQVR4Xu3W24rjMAwA0Pn/n96lDwYjLEtp0yQ7ew4ExtYlaudB/fkBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAE7yJ14kXnnjebp/Zc6u3/RZAPiF5h8JnSV8JPdK1Sxx3ng+In4Hu+ddo/aMXt8QP+fuGeIZAB5ptcRWOjlX281TzVvFM526Kp7p9H6K3ayrWDwDwOOMZbVbWmPJ7XKuVs3zaTzT+S52scontVfazZl9P6s7AHicbGGN+2zR3SWbpTtnN2+lqq3iO5/UXqWaMYtl9wDwKNXCqhbh1bJZunN28zJV/S5WqXrfrZovi1V1AHCbeUGtFlYVv1M2S3fObt7OGT1mo9cnfVf/s3d7ZWLPeM508wDgctVii/Ej5oXceY7Karr9unk7Z/QY5j7v9l3VxfMZ5v/b/FS6eQBwue4i3sXusprnyJxHcjOf1g+rWeK5I9ac1TeKPVbvWenmAcCl4oKK59kudpfVPN05u3mVrMfR/qv8eK5kPea78XfMOyL2HHcdq1oAuF1cTmNhZfdHzf06z1FZTXY/vPu+WdVjF1tZ5a/udlb585wxHs9d1Wff+aQWAL4mLqexsLL7p8lmivNW56M69VU8ivmdd0Sr/LlPjMdz17t1L+98LgD4qtVyWt29ZPd3y2bKfgh0PsfIyfLmePXMsvshxlZ5VY+X2COeZ6tzrImqeOXTegA41bz84oKKS3T1PEU1S5y7yh92ubHf7omy+2FXO3TjI2fOjXXx/JL1n/vGdxzxTg0AUDi6mL+Ve8QZfbs94vcT6+J5yO7P8M3eAPBfO7Jkx4+E+GMh2sXudmS2mFudX1Z3Z/lmbwDgp79sOz+Ivumq98Yff/N7V3dXuOOdAPDfsWyfz/8IAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAODX+QuiY7pUGXWF6gAAAABJRU5ErkJggg==>

[image9]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABEAAAAaCAYAAABRqrc5AAAAYklEQVR4Xu2OQQrAMAzD8v9PbwxWCK2VZOmOFfRiK6Zmhw6Xe5+gI8oXMjHrc8ESJywd6GEhQBcLAbpYCNDFQoAuFhOhF5YvFUcKIysNPChxZHNewh+3Bjy/jmz/anvg0OQGyV5Bv7tBbcIAAAAASUVORK5CYII=>

[image10]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAZCAYAAADuWXTMAAAAQUlEQVR4XmNgGLngPwkYK8ArCQU45QmaTggQoxmvPCED8MmBAUVeoFgz2QCfZnxy+CXxAZpqxKoGOXQJ4VEwwgAA104u0q44XkMAAAAASUVORK5CYII=>

[image11]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIUAAAAaCAYAAACZ6p+qAAABZElEQVR4Xu3SgYrEIAwE0P7/T99SuCxujGZiarVlHhR2dUxS6XEQERERzfP3/9xF+t3Z880uvU9d6JKiDbqXaK3P5l2kt79aa7bWOixdAOT18fZnQfp6+yv05u7twdIFHMiQSGYWr3dvbwVv3pO370KajEJrR3IeJFPyenv7I0brobOguSYpgBZBcye0LpqbJXoHK0Tmi2QrchAtEr08NIvmhJW11iKiM2RFe0Xmi2S/rEP6f5b0QOqiuZlWzBDph86H5irWQf0/y+rREsmWRs9ZsnVkltHHc3WuYh2y1jLQ4dDcTL3+vb2sSG30ntBcxTpkrWV5NYdf4Pg9N1rj5M3Q28vw+mpIHsk06YNoMTQnyrw+F601A9IfydzFmqW8X2sfpgugxeRcNC+/rfWo3rnenla+i/fswppnxzlh5eCPfIHNtD7cx97tYwff0Ks+Cusrp7jX3OUrXmIjvE8iIiIi2s8Ha/X0DJJ4tCoAAAAASUVORK5CYII=>

[image12]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADwAAAAaCAYAAADrCT9ZAAAA0UlEQVR4Xu2SgQrDMAhE+/8/vbFBh3tociZZQ4cPAtXc2bP0OIqiKPbyMOdviRaM+remtVTrbgv29xsJp3h695egBO2hzlB1b/j1U+aAWf+LTI6M9ku4YuEZryWTQ9JGIvZY98jqI6J8RNW5Qtvjs8rpax0FVavqXKGteacy6iNePg9V54paC7OOUHU9lEUUzQcKafbuVTLaFt6cs8e8XWjwagvrK2Am22M/DYdwIGsVG5DvyBDNGJ23btCPWZaTxuiL7mY61/SADdwtb1EUhc4TrxCUbHOeEmAAAAAASUVORK5CYII=>

[image13]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADwAAAAaCAYAAADrCT9ZAAAAwElEQVR4Xu3RWwrEIAwF0O5/0zM04GAzedxEsYI54If1JiT0ukop5X2f7qRYxdabpR+KnwytVvtu8oqsN87rleH19N7/hAsWQmZDMg/hAsFovQSdC8398DC/IzI1HnQRNEekML97onmUNJsEzREpzO8eqceo1hPpi+aIFJS+eTI1lsgScBYOvgCdDc2RUBgws9fN6xeeP1wAan21g+rzvC7ai6SKFtIW3n3uKbTlj7DFwu0PIGfU7H7bO2rZUspBvpjyf4FE3uoRAAAAAElFTkSuQmCC>

[image14]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAbCAYAAACjkdXHAAAAS0lEQVR4Xu2PQQoAIAgE/f+nCw9BLLq2QjcHOpQzQmYDY+GDQjv2sBWfsL3AkeNblmKU8U5B8TmOJCnODiUTypgN/8TsXziLnGGI2ShcMNBJUYsOAAAAAElFTkSuQmCC>

[image15]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABEAAAAbCAYAAACa9mScAAAAUUlEQVR4Xu2NMQoAIAzE+v9PKwiCFc3dpEsDXZpoI4onNHMsKCaXoJBcgkJyCYqsT07R3O37K+uD01ioUHnrmmxkEEajAuUHFJEbzICmKP7TAXjEQMBwjTQTAAAAAElFTkSuQmCC>

[image16]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAkUAAABPCAYAAADlerGOAAAD7klEQVR4Xu3WiYrjOBAA0Pn/n94lsAJRVEnlK8lO3gPTo7osuxt5/vwBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG7yz3T9ml997jt5fwBvMn+wOx+wI7V/s86zx3cU113xna+uo2J/dZ0x+q7OeVJ8zuy6U5xdXbO4BuBh1YE869T8gt3z797RLp/p9OzyK9X8Kr5ztu/dqj0+vf/V/CyexQB4yDikd4dvp+Zvt3v+3Tva5TOd388qt7OaXcV3zva9U7XH1fu4w2p2lnt6PwD8Zxy2q4N3riG3en+zbl2069vlV1a9VXxnNfMbZHt7x55398hyux4AbjIO2+rg3eV/yer5u++nW5fZ9a5yK6u5VbxjNffTsn29Y7/ZPeZ1zA1VHIAbjcM2O6xnu/wvWD1/9/106ypX+zN3z+z+TVViX1zf7en5Q3afuK506wC4QXZgz3b5bzD22L2OWvV0Z3brKlf7M3fOnOecnRt7zs7penr+MO4Tr45uHQA3iR+0WTzA48Ee80PMV3WzXf5Tqn11nmk4Upu50lu5uqchmxPXO1l9nBvXV2SzsthLFjsimxvXlW4dACfFgzZ+eGbdAz3Gun2zXf5Tqn1lz5jp1q1U/VdmX+mdZXPieiXrf5njWf6s1f3i+o77Z/eL60q3DoCT4kFbHfzZYf5SxeZ4XA+r+PzziDGzex216lnlXs7ec9j1r3I7u9ld2YwsVqn2MWIxn9V2xVmzGI/rs1b33DnbB0BTPGjHoV3Foyo2x+N6WMXnn99ktaf4PLv1UbveXX7l6t6GOOPo3Kx+jsV8XHcd7Yu1cd11tu/lSi8AG9mHIYu9ZLGXUT9f0dH4sMt/wmo/837nut1zrN7dy5zfXVEVn636o11tzGV1nRnzv4+s51iMD1Vu1Rdj2TrGok7NypVeAArz4b87qGNdrI3rTNb3UsWHXf4TOvuJ7+tITybOWl1RFR9i/67+ZVfTmXMkP9fFvrgeqvjLvL/qimIsW8fYEGevaitnegB4s85BXR3oWXy3/gZH99St79Z9gzv22pkR/0Z261kVPyPOiuunrZ4TgC/ROairA70Ti+tvcHRP4/mr9/C0T9xzp7un+M6ydaaKn9WZ16k568nZANyg+7GPdVV9jO/qP+nIfjrPsMpd8cTcJ2ZG8Xdf/V28S7WXIYvd5cnZAAD/G/5TBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABwyr/1dYSYrMvC4AAAAABJRU5ErkJggg==>

[image17]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA0AAAAZCAYAAADqrKTxAAAAJ0lEQVR4XmNgGL7gP5EYK8AniUt8KGvCCUY1QQFJmmCK0fEoGMIAACZnKdfzzeeMAAAAAElFTkSuQmCC>

[image18]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAU8AAAAaCAYAAAA3+d4CAAAD1ElEQVR4Xu2TC47kMAhE9/6X3lU0QkIsVXxsp9MZnhT1BAoo7MmfP8MwDMMwDMMwDMMwDK/irw08mMurPFW6dZrV+qHGbz7vR+y+46OJqPS/w88b2XFumR5Rfngecq/feHeP9GwP85TJqK/1IaD4XXjzo3/CKH+SXTMz/lk+U38SdAco/km0J/ZYUFyDNCh+B2gnLy5/21+NrbmNjw02MB8sdxo0N/IU5StU+lS0jIx/ls/UnwZ5QPG7sT7su47Z+IUX06A6IcqfhM22cXYGFyx3nNODWf/s4hnNCdDc6EIvWK5CpU9Fy4h2E5iG5e6A7YDid2I9RH5tzr5rPL0lozkFm63jotOPB4ofh5naAeudnZ3VRezoIUSeWK5CpU9Fy4h2E5iG5e6A7YDiXXb02+WX9dFUdBEZjYbN1nH52/5aUPw4skjWQFZ3wfqynKWq9UBxREZf8dWl0j/Sil/7WFDcEulYzoK0KB4ReXsayKu3h33XeHqPrO4EJ2bv7hciA7PLiC6jvWBalrNUtB6d2kxN9Tw6VHpHWptH3lHcEulYzqOqZ0TedrM6C9V7e9h3jaf3yOoET+vFMlRnZ9jdD+KZt+878OZcSNzLWbI6i9R0ai+ydVldl2z/SBflLRl9dDcsh1i9NyHydoLuPM+rFxNYnNVpsroTnJi9ux/EM2/fd+DNuUBxj4rW0q27yNZmdV2i/nI+GZ38Rloh0mbyHbp1mshbhD7XzlNB6zM9UC6q01S0mm6dZkcPy+5+EG+QF1sFHRKKW7I6D6lbrWcwDctVyPaJdFHektFH98NyiNV7EyJvJ+jM6/hE+myvrO4UJ+bv7gfxBnmxVdghobiG1TM6NZaox2o+S6UP0qI4InvukY7lMqzUR952053XqWN6lrvozBN0XbfHxYoHxO5+EDsou0xWJ0R6ydlLieoYqA7FEUzPchdZ/5EmyluQvhNHOU2kYzkL0qJ4ROTtKXR8Mr3uZ3WdWSc44WN3P4g1nx0sdVU9wuvnxbJ0ahCol/YXPRFMh+IMVOPNse8aT+8R6VhOE+mivEV8Ves+Qccjq9F7a93KebA6lvM4dTe7+z2CzFLowr33O7l79uo/VVSb7V/RIVhu+CF7zh6ZOt0/o/9WXrtbdTGrt+938snZHXb5zX7UTMNyww8rZ1Streq/iTfvVlpOPtzsB3ySJ3iosMtrZm+Wz9QPa1TP+Enf1U7ets9/VBes6k/yFB8ZdnmNzj+TH85TOWe5s0rNN/C2fV7HN13QykfSrdOs1g81fvN5/+bdh2EYhmEYhmEYhmEYhmEYlvgHRO9yqmD8nYEAAAAASUVORK5CYII=>

[image19]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADwAAAAaCAYAAADrCT9ZAAAAtUlEQVR4Xu3RwQ6EMAgE0P7/T2s22V5GBoYU667hJT2AOKKO0VprL3B8D2L9p7B9WN/kDaaCNvD2Yf0La9ALXjFz8aiy8xcsgPVXVOSV71UeWKx8v/LAUZtXtl8mSJ37yOQqyvJYEPZmjX1m5kZHlZ03qSE4g7VFzVYt53kB2I9qRp1TePuGvJuta1G9g7WXhN04+9b1qPZkZj3WXrfBB2GtwA+69QWycDGsX+nn/0prrbV/cgJLQnCQUuZC4wAAAABJRU5ErkJggg==>

[image20]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOAAAAAaCAYAAACuJFCeAAACcElEQVR4Xu2W4W7EIAyD9/4vvYkfkSLLhgBtWe/8SUiL44RAD2k/P8YY82H8pmWMOYQfoDEH8QM0W/jfqD18d2aLlQc46/9k3n4X+fuvnCXXjupH+UZ1npEv8mr9C1YGmvV/Om+/C5wf4x7oxbgx+8NHD8YB6izurePkQWaGmvF+A2++CzZ79fsqH9OCUQ7zuxpD6Y+TB4kDVIar+r6FE3dx1Z6sT/X7Kh/TglGulw9mfK9idLDI52XWmb1L9GE8i6pXOqJ8Sm8ovZHvIi8E88qHzPqq/iVY4+qGFY/ps3KHqoZ9N4wZrK6hdET5lN5QeiPqsof5qz7kKs82OHyml2uMcqP6Ve7qe4qVs4xqZu9I+ZWOKJ/SG0pvqDrUqr5ML5ep+rbobaIOF1Ry0aPnXeHqfrPkc1WXouq7E7W30hHlU3pD6Q1VhzrGgdIbSkeiR6/X7ajNlf4UJ/e+i9kPjv5KjULVKx1RPqU3lN5QdahjHMzqPaJmpbZLpZnaVOlPUd0bL2+0ToD7VmZhHqbNwGqrPZWPacEox/KoYxzM6gz0zdQOiWYzK8O0DOZUrPTe3yw+SW+WXi5gHqZlevn4NrGqMC/rUdUaTAtGOZZHreoLlJ/BfExbIgaZWZmsYa6BGotRQ3IevRifQt3B6H4yLM+0J8B9MW7E2TA3ihHWI4M5jAPUMc6M9swwH9P+JTgoxg2mVdmpvQL8kDgPxm9jZ/6dWka139W+V4OHVLHSEdQxfhp8gAjmMDbmFuKHWVnoxzg0pmP+aXB/nGUUG2M28AM05iDsAWKcwdgYs4EfnDGHiUfIHlvOsbwxxhhjzBfxB5fJ+RX6KDvqAAAAAElFTkSuQmCC>

[image21]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAkUAAABPCAYAAADlerGOAAACtUlEQVR4Xu3Zi27jIBAF0P7/T+8qWlHRuwyGPmI3PkeywgxgYxp1UPv2BgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADb/mQCAOBuHgcihyIA4NbagWj3YLQz9tXZizW73zEAeKpWpHYL1s7YV2cv1ux+xwDgFDt/LVoddwf2Yp29AuCyskCtFq2VMXexumfYJwAuqirmVb531H8nK/vFP/YJgEuqCtRRkT/qv6q27tVr1e74u7JPAPw6R8Xrq/2v5pXfNQ+K1bViddxPOPPZAFzcUZGYFbujvv7zDl71XfPgM7tWrI77CTvrBOBGVgtENW6Ua2Z9Z8tCfnStWB13BWeudWdPAeBpVotTVchGuWbW11T3/Yzvus9n5fOP4jOduZb8mX91LV+d3+zep3+P3bkAXFD7xb56pb4oZH8V52drV+NbO+Oqnfd5llxH1c541O7jfk5+HrUzHrWfbfQ+Ta5xFOfV9x+1Wzzr7+W40dhRDoBfJovL6tWr8g+Zy7g3ukcfZ/+snfd5lmovMu7l2nsZP4xyvbxfxqP2s/X7lOuYxbO+jKt2izPXq+bmvNk9AOCDLBqzOAtOy/XtjEftK5qtb/YeGT+McpXfuGe5rtmaM05Vf+5Lqp5ZzavyAPAuC8UsHhWWWX/VHsVnm61n9z1Wcw8re1bNPUuuZ7TmPj7qH9mZl+0c21R5AHgvIK1YZDzKHfVlezb+aqr19fnPvuPK/KP4KkbvkvlelX8Y5Ufjq2c2Vf8oBwDwLRwwAADeHIoAAPw7CgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPjfX1zJo2sz52Z2AAAAAElFTkSuQmCC>

[image22]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAkUAAABPCAYAAADlerGOAAAEUklEQVR4Xu3W62rkMAwG0H3/l97FPwxGSL4kaTvbnAND40+yY5fBzJ8/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADzsbwyg4LtC5DsB/BrtQnvrpdbP/tbzX/Hm/9ebz17xPwF+lbdfam8//6m3/7/unP3O3E/Uvwun34mTXoBvdeVS+03efPZTb/+uNHfOfmfuU57cQ1/r9Dtx0gvw7U4vtd/kztmvznvKd7/fj6J7Z78z9ylfsYeT78VuH8C3Gy+n3ctq1beqf5pqv1Xererdbt8VX7VuZjzHyZlWfav6p6n2W+Xd7v9sp+eOp9aP63zK+QAuGy+o1aUW63fHVdb0fGd+Jsuz+U3MV+NRlTdxXhx3Y171ZHb7nrJzltGq/6TeZX1NzPs49sZxF/Nsbhfz2BvHoypvYi2Om3iu2bsqp/2Z6r1VPlrVAX5EvMDiOIq12L9Tjz1NlcV8N2uqbCeP455lqrzJalUW379jt+8p8X1x36OYx97VuGdR1tdk+W7W7GZNzLM147ib5VltlVXzZk77M9Uaq/2s6gA/Jl5OswtrVmtW9abqOclinmVNlZ3ko6o+y7NalmfZTO+/+nlKtV6Vd7t7yerVvJOsyqMsa6p8VPXM8qyW5XE80+fvfu5arXO3DvBl4oU4uxyrvFvVm6rnJIt5ljVVdiWv6s0sz2pZnmUzcV+nnyviGrP1qrybzR1l9WreSVblUZY1WT6eqXpHM8uzWpbH8Uzc0+qzY9U3W2tVG/8C/Ljq0qryblVvqp6TLOZZ1lTZTh7HPcvEeeNzNifLs2zHlTlXZe+q9l3lXa/PepqsXs07yao8yrJmzE/Wa+Lc8Tmbk+VxfOrO/Gw/maovy7pZDeBLzS6g7ELLstGq3lQ9J1nMs6ypsp08jnuWifPG52xOlmfZjitzrpjtL6tlWddrVc+YVfUqj6qsyqMsa+Ies76exVqcOz7H3ibL4/jUnfm7c7N9N1nWzWpdte4VT60D/OdWF0tVj/lT4+pdUdabZU3MVu/K9lWNR7FvFOfFcVflO67OOzHbX69l9Zg9MT55V8yaWR7HMevGPOsbs6yWPe+MuyrfdWd+P9vuJ+pZVq/G8W9/rvr7cxxXz3Ed4EX6JZBdBrG20xNdqcfe2JN9sr4o1rPeLM+yMY+qvKnW6mI965k57T+x2lesx55ZrVv1xHrs3cmqzyirxXHMsr6YRbEvytYareo77sy78hlVeROzOB5la4zjWJ89x3UAgJf41B8BcV+zcfZjZlavngEAPk78sTIbxx89PRuf4zh7zsYAAD+m/4jpP1DiOMtWtfg86wcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADgZ/wDjPlpwQrTIlEAAAAASUVORK5CYII=>

[image23]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMoAAAAaCAYAAAD2W8OHAAACFklEQVR4Xu3UgW4DIQwD0P7/T29KpUjIsgMcXFduflKlxYFcoe1eLzMzMzMzM7Nn+MHgP4pL+M8XcdrZP/1+8/sx89yZtceYvYSnWT376v4rPvWZtT+SmefNrD1CHmj2Ip5k9dyr+1fc/bld/X7MrD3C1Yt4kpVzf8u93f0+cv7IM0bXHWn0cO2FsfWqr2rMWY+tUzn2qiypDF8t7LE1YbTf/s3WzVjdn3BO7/3hWdW6o40crO2z9TP9xNYFdtlVhljOsqCyq89JmGMdcn/2qnkzVueo/Spv9frHwQNVl1D1Qq8fWF/tq3KsMQtVjliGqnmrOdY7sOfMUHt7c2f61bpZvecuwcHVw6pe6PUD66t9VY41ZqHKEctQNW81x3oFm79Tb37VzzzXqHVX7Z73poaqA6g89fqB9dW+Kscas1DlSGVtjnXakWN9xY4ZqTeLnSH1ene6Zb4aqg6q8tTrB9ZX+6oca8xClSPM2F6WhR051jPYvBWj89Q6lqWqN0Ltz1z1b1FdAMtTrx9YX+2rcqwxCyxnWcCMrWuztsfWhipHLKuo2Tvk7NEXajPsz9YJZ2aN67Fepg4ZRi9hV109C/PRLGDeexbWVcbmMphjnVT+F9p7GnmhzFi/V4fevrZfrTM7Fn6RsQ69H0oLc6zNjoRfZKwT5qpWudlb/tcdeX0LfE+qTqrGM7U565uZmZmZmZmZmdnrF8Qd0D5Zo1q7AAAAAElFTkSuQmCC>

[image24]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAkUAAABPCAYAAADlerGOAAADcklEQVR4Xu3WAWokOQwF0Ln/pXcpWIP5SLY7nelUbd6DIqUv2e30DDh//gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAN/HPf89c39np+U7n7ujJZwfgBsblPj+szd/TE7630/Odzt3V088PwE24UM5031GXf4e/uffsK3/gvTL7CXc7DwAP9Opl+Ft131GXf4d39n517at/GJ3OfdIdzwTAg7xyEXbeXf8p75yzW1vlVfYV7+xzunaeO/2/cDr3aXc8EwAP8u4Fd7r+ZGb2lfnVml1/6GZeWX86t3KyT9c/WXvJuaw7p3OfdtdzAfAQ3UUy8pNLs8qGXFPVs1FX+dyr3qt61uWXXNfV+VS6/JLrsp6t8tUeWXeqmZO1JzM/4a7nAuAhuotklacqG7KX++76Q+bjPfORVbr8kr1u33wqXX6p1mU9nOa5Z9av2P1ul13/p9z1XAA8RHeRrPJUZZdqj8x2/aHLK93cKs9elaUxk3NZ73TzVd593pxlXVn1d+u7Xvd9fJfd3rs+ACx1F8kqT1V2mS/JfOaZWfaHLh+6/WervHt2qrmsU35GN1/lua7aI+v0Hf3KyKszfYfdnrs+ACx1F8kqT3OW79V8OrlEu36VZz3k2eb3bs1OtTb3nt9z9lJll1w7fnbzw25m1Ru6ParsU7ozDbs+ACx1F8kqT3OW79X8V3R7VXnWQ55tfu/W7FRrc+/5PWcvI8terh0/cy6dzOx0e2SW9Tu6vU5/910fAFrjEqkukiqvssucZT/XdHU+6TTPepZzs1y3q4ddlu85P2dVr3t/pZ6N3ivPLD9ndlpXebVvlefa2a4PAKVxgcxP1+uyWZdfVmuzdzrT9TJPXX7p9hqyX80MXb9afzKbqn2yl3LN6TPr8ktmVZ3ZJbNR53zWadUDgFtbXWKrHns/8f3lZ2Z9Oc0umfujCID/rdUltupxT/lv1tVVPmfzXOa5duhyAHiMvOiy5us+9V2Ozzl5cn6ossyr/qXLAeCRXGx/x2/4Tn/D7wgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA8HD/AsHlVsbLQg83AAAAAElFTkSuQmCC>

[image25]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAkUAAABPCAYAAADlerGOAAAEO0lEQVR4Xu3Y22rsOBAF0Pn/n55BDwKxKV3c7ng66bXAJLWrZNlNoxPOP/8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA8EP+zQAmfFdI7TvhewH8Cd98oPV3/9b3f8U3f17f/O4rPhfgz/j2A+3u+99Z+xvd/bx+u7vvfnf9p+nfhyvvdXUe4DGvHGp/yd13v7P2t/n270pz993vrv8043fi9N2uzAI87psPqbvvfmftOzy5/9V//P6iO+/+1z678V2ufDdO5wAeVR1qO7u5Xf/TrJ53lnertd3JzG8wvseVd9rN7fqfZvW8q15z8rnt+p8kn/Xk/ZqTGYDHjYfT7kDL/t16lnXZ63XOZ91lXq1tqjyzrEer/OQeYz6bmbkye9fJu4x281f6XTXX9Ly6Z5WlKq+yZpa9uk+XedZNX997q/v9tGrf0+c5mQF4VB5gWafs5fxJP2eaKmuq+dOsuZJlPssqV/JZNubVTCXX/bTca7V/5jm7q3uWqrnmNM+6W+Vplt3dZ5ank32eUO3bn6fqdbs+wP8iD6bVYbXqNbt+M5upsqbKZ9ksT7OsytNspspn96zyKlvp869e7zK73ywfnc6k2bpVnnVmzSpPVZZW97ubZ73S159cV6zmd/fb9Xp/NfeK3XMBXy4PxdUBOcu7Xb+ZzVRZU+WzbJanWbbKx6tS5bP5Kq+ylXymq9cr8h6r+83y0elMmq1b5Vln1qzyVGVNv8d4pXfkWa/k86yuK3bzq3vu8lef6cRP3BP4w2aH0Szvdv1mNlNlTZXPslmeZtmYZ91VWZNr+89qvsqr7MSr615R7TPbf5aPTmfSbN0qzzqzZpWnzKq1Vda8I8/6aSf7V8/dzPJmlr/TE3sAv9DqcKgOriob7frNbKbKmiqfZbM8zbIxz7rrWfZybf+Zc02VV9mpV9ddsXq+qldl3cnnU/3erdbN8qwza1Z5yqxaO2Zjr5ptruRZP+1k/+q5m8xnv/+UJ/YAfpk8mNKsn/m76mqvJvPZ7CrPOrMm86wzq3qz31d1N8s/xer5eq/qZ/aOerVX5qdZk/lur6xXWXXfSuZZd7P8CePncnqNxqzqXalHY2/2e1UDX+7kwMprtOo1r/RzdjWzu0ZVb1WP66s8Z7qcG1X3GWW/mtl5Zc2J3XNlP2dWvW43k/1qtspPsvEeTdXLuWpmludMl3Oj6j6jXf+n5f6nVzfLe29VN9W6lPuNsgYA+Dj5B0vWzckfRSt31gIAPCL/YMm6q/IqazLPGgDgo/T/Aep/tMzqblbv8uwDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA8P/4D7stYshPVXf8AAAAAElFTkSuQmCC>

[image26]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAD4AAAAaCAYAAADv/O9kAAAAwElEQVR4Xu2RgQrDQAhD+/8/vXEwIQRzagubXX0gu4spTbrjGIbhybw+8zjOFK/622GlK0Wq/nZggUqZirclGL7yz2d9tyEqhB8n8rbFC50tk/G0ZFdwt1tEu+j5n7ILFgXP7Hae1qjySr8FmeCqoNIrXH3+FBa8MoinIbyzO//y2VB7fq86S7BQdhDUeLfwNIXnRY3Pnn+h9K8SheAyjNrviregEs4rw2XxzPcWWDA1ns/urPPwnu+mDcMwDH/PG5Wqkm7eYvLOAAAAAElFTkSuQmCC>

[image27]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAD0AAAAZCAYAAACCXybJAAAA5UlEQVR4Xu2QQQrDMAwE8/9Pt7hUoEx3bSWkDRQN+KDR2rK9bU3T/DOP96pwde7n8LGsM/SsA3rWt6MupB6u3ICumruV2SWzZx3QVXO3Mrtk9dFnct8gzj81R11QuQE968D5DDNRc9/RuoTapIYP6FkHzmdUpuJU/xBuAwcF9KwD5zOq75yaSV9itsEdSM86cD6j+s6pmXmVWIVdn5514HxG9Z2beddfwk3uILpqTqEyzikfrPov8u/klVFuQFfNKVTGueyZYf+D/EguRfhZZlDNDdRcOrcC5y+jemg11zRN0zTNnifZb8U71mMiMgAAAABJRU5ErkJggg==>

[image28]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAkUAAABPCAYAAADlerGOAAADz0lEQVR4Xu3ZWYrcMBAA0Nz/0gkiCERRpWUWt939Hph2LZJledDP/PkDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwJv6GxN8lN3vv9v37p60D09aK8DLtUPTwfk8P/nNdubyd/Lf0/bhSWsFeLl+yJ8cnie9/I7Tb1bZmWP8G9np7056n+Cp+/Dq5wM8yulBv9vH7/mJb7D7zXvPbn930vsET92H0/UCfKTxoNw9OHf7uL/T79i//c643b4neto+3GENALcWD8oYV3b7uL+d7xh7dr//Ts+TxPd52j7cZR0At5QdkjsH/U4Pa30fx72c5aIsfzK+qfJdNbbKj1b1J6net8qPVvWr3GUdAI/RD/nZAbqqv6NxX3auHVVvzMe4y/K7ua7Kd1V9Nmezqj9N9S6r91zVr3SXdQDczuyAXB3ks1rU5zoZc5VXr6t6fszN+mI+xk3W11X5ldmczXfrT7F6j1X9SndZB8CtrA7qnfqJ1Xyv8up1Vc+PuVlfzMe4yfq6Kt/Mas1q3llt/L271TpX71rVrnaXdQDcys7hWB3mWW6lmuvVTtbVe3evHVVvzM36Yj7GTdbXzfJVbVT1ZbluVrub6v2iqi/Lvcqd1gLwKLuHfIybmMvmivFvqJ7R89m6rlQ9P+ZmfTEf4ybr607zUTV3lutmta6a9yu+M8/u2Gq9We4rqvlPfHc8wNvph+vJNRrj3Vqcp7qP8Wxcj7P6ST7OeaXs+bu5JsvHuMn6uln+5Ip6LqtXcfzt91V/v49xdZ/Nk+VHY8/OFfVcrGdxdh/jbNz4jJlVHeCj9AP09BpV+SbLNVV/E/NjHMfNenscx/R8/43zxd6rjGuN65vlqnyWy66oyn3lGlX5JuZiPMrmGONYn93HeZoq34zvcHKNVvkxzu6jOK7KRTs9APyg6tCNB3J1H+PZuCqOY0YxP+v9FK/Yg/i8WZytb1av7md2+37SybpjLdabLDeqxgHwS6pDd3Ygx1q8j/Eoi8drzPffmI9zfKKr9yA+bxZn32hWr+6zuMlyV/jquuO4MRfzo1kNgF8wHs79EI5xlqt6s/s4z1gbZf0xn9U/1VX7EPc9xlluVYv3s/47iGsa43jFeo+r/Bh3MQbgDTnsf469fF++LcAHcNgDAB+v+lcBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKT+AY20qnKpgPamAAAAAElFTkSuQmCC>

[image29]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADUAAAAaCAYAAAAXHBSTAAAAqUlEQVR4Xu2RWwqAMAwEe/9LKwULy5KnSKqSgX4kG9sJjtE0TSXHdX7FnaWy86WshTKS2flSUC4jmpktB8Uyfyw69wo8WVzcm92CJBQVjcyUY8lb2cTKtmKJfXYpD20xrb+diJQmr/Xv8Nhd66LMQaTegvtYe5lW83ciLBw5iPWgVXOGeO9shSWspTjjfCL1ymEJFkc4k3KpXwpLYM2H81VrfaybpmmacQK9cod5AMYz/wAAAABJRU5ErkJggg==>

[image30]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADEAAAAZCAYAAACYY8ZHAAAAy0lEQVR4Xu2P0QoDIQwE7/9/usWCJbfsJHoV+pIBH5xdo15X0zQVLxWLjHPZWcrIP0KH6Z7QXvaZmcV1DBronOI62TzKfoYGOxehRzk3cO4Y2aXOR1xO55w7Rnap8xV0LnrqRKr8Bg0kX0Fn1OteqfIb9FjyxG5/kPXnvKW5VCJP7HQn1R3LH6ECeUfVo1nkI0sfodA5h+upc3c4F3GZcx9omLqs51ZE9wPXi7jMuRuzkA2PXh+tS9HcdSLarfpflosP2XpM0zRN81fevBiSbrabNqsAAAAASUVORK5CYII=>

[image31]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIEAAAAcCAYAAABGWNzNAAABaklEQVR4Xu2VUW7DMAxDc4Dd/7ob/CFAIEgpXtsttvkAoyJlG4mkoNe1Lt9omLMYA7DaEKz4zI9mxYLOPPPdfcfTFUrllf9p2BCgDpQ/qHJHogoSPhYe/byCrLtYnburld/dz3zcvzVYAIR5A+UP8M5Osxg1O4f7A/RRM/Duo4hi5pVBHSh/gAXtNItRs3Nsv/I78O5jwJedKaDyB1jQTrMYNTuH+wPMRcw8pjG3Nexl0VNa+SzuNItRs3O4P8BcxMxjVLlp4mHyMoeBTfcgHIRqdvZZ3mzE04cg/z159evr+gVxGMkXm81RjVa+AieyW+ZBqIac0qwT3rGFNTs0+rvB3t0cRG5+NQhVziwODoFqtvLNhrBmV8NhFoc1Vnkz/l1eOWveQNUAzKEeMG+Wd9xhXqBqAH7hEeffvIKslZ919QzmD8BGshWgDk/BzrL9zDMLUTUQhyBT5cxC5K87f+V34qzRN8aYf+QHS1Vdvel7pUcAAAAASUVORK5CYII=>

[image32]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA0AAAAcCAYAAAC6YTVCAAAARUlEQVR4Xu2PMQoAMAgD/f+n7aJgY0z34kGXXFLQbFkUTp5kKmTePmlBoY4uXiPqaRiMbhQmHA0DOUJRb0mHHVrCfPmdA79wKtZ4nGDzAAAAAElFTkSuQmCC>

[image33]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAVsAAAAaCAYAAAAZvP+QAAAC/ElEQVR4Xu3XW47lIAwE0N7/pruVDySr2i6bACGPOtLVADbEONGM5udHREREREREREREZJpfXBAREYnc7h+NoyCvqGhd4t5E67JX9F6i9a/K+sFid3WrmlmDWezLWF9YTPaI3km0/lVeL1qPntqrW9XMmshiX5X1JItLbmb/2PtgsS/KepHF7+o2dbMPjsW+KutJFpfczP6x98Fi8t9Te3WbuqNC9CH6WF9Y7O3a3Wf0YHS/xc6aUetbVPpQyblC77dWzVuKFcFiXxb1JVr/Arw39gLjmd78CNZhsdgXVXpRyVkNa8D3iPED5mzRirC/K1z5rNmwX0+9R6Z6r6gHbc2LZc7s8eB7impdbcczDz33reRVclaK7pN9a9G+S+0sYOezRzy17h7t46zcNcqpnmHzKr8eZ/assKuOnudW8io5Fr479quI8rJzWOwSuwvY+eyzdvfsrDM1V/awfrBY5uw+NFLDG/Tcv5JXyVmF3YXFDll8udECRvYecD/Oz2r3qv569OzpyV1tVR3sjiyWObsPjdSQmXFu7xn2Pr17M5XzKjmrsHfJYocsvly1gJaHPxuPxji32pzl2ZzdsM4I5rGxN7fr+Gc2xrk3nomdi/X0OLvP6nl+1Kt2hj3Li9t5NMZ5BPO8XG9tVOXMSs4q7NlRn5osvly1AMxhcxzj3GrzaB3Hu+F9IiwP74Zz5K1ZuB/n3ng2PLvVYevBnExvvgf70YPVjX3FeTT2zmow145xvkrlbKznavjsVo+tC3MOu+suwyJxbuGHUcmt5DwJuzfrj7fHW4uw83rOuYPd9bJv01tr2jvAHG/Nit5VtC9aH7XizDt4zL2wUHzRbIxzq81ZHu55AryPhXfDOaquHdh5ttdPsLtO1i9c8+bZmhePxpjbROsjVpx5B4+4V3vZWKy3jmssHuVG+U/Dah+9f2V/Npf/sEc4t7IYzjHXrmH+IYp7azOtPHuXt91HRF7iTX85vfEfDxF5Ef0FJSJTRf9dFxERERERERERucIf6v8q8lLA0pUAAAAASUVORK5CYII=>

[image34]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAD0AAAAWCAYAAABzCZQcAAAAOklEQVR4Xu3SsQoAIAhAQf//p2sKQiKXIJC7ScHlgREAAPDVSPO+t3SKzHs7t8C2H1CFrNjqDgB4ZwJzcA3zetahaQAAAABJRU5ErkJggg==>

[image35]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADQAAAAWCAYAAACPHL/WAAAASklEQVR4Xu3RMQoAIAxD0d7/0oqDICXqJo38Bx3aKaERAADU0vLB0SixFsm7nV14VSzvJd1CqmJ4bX5hHVuqgLrZOAX/5msA4K8DJE8Z53gOyo0AAAAASUVORK5CYII=>

[image36]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADoAAAAWCAYAAACR1Y9lAAAAOklEQVR4Xu3RgQkAMAzDsP7/dEdhPWEwHAtygEmVJEnP9F2MqNgR+bDBZPhgfOBAR6LjFjoSHSfpfwd7uBTsgy3gEAAAAABJRU5ErkJggg==>

[image37]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAG4AAAAZCAYAAADQfBuCAAABdElEQVR4Xu2Q0WoDQQwD7/9/usUPhq2QZO92LxTqgRA8J/mcPM8wDMMwDMgXCkJkOrmgm/srdO+9nftB/sGdPxqf4xzgHpxX0OP8CW7//kB5BHM4t3FF9cPQ4RywLnMBc5/Cvbt77+1cC1fqvsjlVo9zwtwJJ3tcp3vv7VwLV3IvWj3OCXqcE+WRTmYXt1PdhR7nBJ3LMW9xBbVQ+RWWYS5QvstbXXUX8+nWD7LrLa6gFiq/wp6rnvKKnWyF26Xuqnz1HFHeUhXW59VhiXqmespXnHQQt0PdhV7N2GUuUN7SKeAh7kXKB6qnfMVJB3E71F3ocV5dlQuUt2wXHt2pDlDPlXdkfreHuL66Cz3LBCzHsspbXIEtZE6BOdVlboff9F23ey/OCfZxTpgrcSX2IpyTzOJnhbmAOYXKKl/het17b+ckuYB9kOp5gJlOPr9V5oTuLrzxxr24R+WCzr4rvPGC2/vepnvv7dwwDMMwDMMwDP+bb7ENNdmxKC1NAAAAAElFTkSuQmCC>

[image38]: <data:image/png;base64,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>