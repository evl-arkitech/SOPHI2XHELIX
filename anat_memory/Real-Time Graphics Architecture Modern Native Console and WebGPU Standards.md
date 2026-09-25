# Real-Time Graphics Architecture: Modern Native Console and WebGPU Standards

Modern real-time graphics engineering has transitioned from legacy fixed-function and standard deferred rasterization models toward compute-centric scheduling, cluster-based geometric acceleration, decoupled visibility representations, and spatiotemporal radiance reconstruction. Across current console platforms—such as the PlayStation 5 and Xbox Series X|S—and the web graphics runtime governed by WebGPU, modern rendering pipelines depend on explicit memory barriers, data-oriented memory layouts, compute-driven culling, and mathematical microfacet models. Implementing a graphics engine across these environments requires strict adherence to low-level hardware characteristics, precise memory alignment rules, and formalized render-graph dependencies.

---

## 1. Contemporary Console Graphics Architecture: The Post-Deferred Pipeline

For more than a decade, traditional G-buffer deferred shading served as the predominant rendering paradigm for high-fidelity interactive software. However, hardware evolution, increasing geometric density, and high display resolutions revealed severe structural bottlenecks within this approach.

Traditional deferred shading forces the rasterization stage to output an extensive array of high-precision intermediate surfaces that capture world-space normal vectors, diffuse albedo, surface roughness, metalness, and sub-surface or material classification identifiers. At native display resolutions such as $3840 \times 2160$, this multi-target write imposes a massive memory bandwidth penalty, consuming between 64 and 160 bits per pixel across multiple render targets.

Furthermore, because rasterization occurs before material and depth resolution, complex geometric scenes with high depth complexity suffer from severe overdraw, causing the graphics hardware to execute pixel shader operations on fragments that are ultimately occluded by foreground geometry.

### 1.1 The Visibility Buffer Pipeline

To resolve the memory bandwidth ceiling and overdraw penalties of deep G-buffers, modern console engines adopt the **Visibility Buffer (VisBuffer)** architecture. Rather than writing full material attributes during the initial rasterization phase, the geometry pass outputs a compact, single-target 64-bit integer surface (typically formatted as `R32G32_UINT`) or a 32-bit compressed buffer.

This visibility surface stores three discrete pieces of geometric data:
1. **A 24-bit Instance Identifier** referencing the transform and material metadata within a global GPU storage array.
2. **A 7-bit to 8-bit Primitive Identifier** indicating the specific local triangle index within the active meshlet.
3. **A 32-bit barycentric coordinate package** (encoded as two 16-bit normalized floats) defining the exact hit position of the pixel within the triangle plane.

Once the hardware generates the visibility buffer and its corresponding depth surface, material and lighting evaluation occurs during a downstream screen-space compute dispatch. The compute shader samples the screen coordinate, unpacks the Instance ID, and indexes directly into an unbounded vertex buffer through programmatic vertex pulling.

The shader fetches the three position vectors, normal vectors, and texture coordinate pairs of the intersected triangle, applying the stored barycentric coordinates to analytically interpolate the surface attributes at the exact pixel center.

Because material evaluation is decoupled from geometric rasterization, expensive bidirectional reflectance distribution functions (BRDFs), dynamic branching, and multi-layer material blends execute strictly once per visible screen pixel. This approach entirely eliminates fragment-shading overdraw, reduces geometric memory bandwidth by more than sixty percent compared to classic G-buffers, and permits the native integration of hardware multisample anti-aliasing (MSAA) over triangle edges.

| Architectural Attribute | Traditional G-Buffer Deferred | Modern Visibility Buffer (VisBuffer) | Clustered Forward+ (Froxel) |
| :--- | :--- | :--- | :--- |
| **Intermediate Memory Bandwidth** | Very High ($64\text{--}160\,\text{bpp}$) | Extremely Low ($32\text{--}64\,\text{bpp}$) | Low (Depth and Motion Vectors only) |
| **Material Overdraw Penalty** | Proportional to Geometric Overdraw | Zero (Evaluates visible pixels exclusively) | High without pre-pass; Minimal with Z-prepass |
| **Hardware MSAA Compatibility** | Complex, requiring sub-pixel custom resolve | Fully native via barycentric sample points | Fully native |
| **Primary Draw Call Model** | Indexed Indirect Draw Instancing | GPU-Driven Indirect Compute / Mesh Shader | Direct / Indirect Batched Dynamic Draws |
| **Primary Platform Alignment** | Legacy APIs, DirectX 11, WebGL2 | DirectX 12, Vulkan 1.3, PlayStation LibGlass/AGC | WebGPU, Mobile Vulkan, Apple Metal |

### 1.2 Meshlet Processing via Task and Mesh Shading

The integration of Visibility Buffers coincides with the replacement of fixed-function input assembly stages by compute-like geometry pipelines comprising Task (Amplification) and Mesh Shaders. Under the legacy input assembly model, the CPU submits index buffers that the hardware rasterizer processes as unpartitioned streams, placing geometric culling burdens on the vertex shader or CPU thread pools.

Modern native architectures partition 3D meshes offline into micro-mesh clusters, or **meshlets**, containing up to 64 or 128 vertices and 126 triangles.

During execution, the Task Shader processes an array of meshlet descriptors in parallel. Each thread evaluates a meshlet's bounding sphere against the view frustum, tests normal cones to cull clusters facing away from the camera, and measures screen-space projection areas to discard sub-pixel geometry. Surviving clusters dispatch corresponding Mesh Shaders directly on-chip.

The Mesh Shader workgroup cooperatively loads localized vertex data into high-speed Local Data Share (LDS), transforms positions into clip space, and generates primitives without host CPU intervention.

In hierarchical systems such as Epic's Nanite, this architecture expands into a directed acyclic graph (DAG) of continuous level-of-detail (LOD) nodes. Clusters continuously swap LOD levels on a per-meshlet basis based on perceptual pixel-error metrics, ensuring constant geometric resolution across the scene and eliminating traditional distance-based LOD pop artifacts.

---

## 2. Dynamic Illumination, Virtual Shadows, and Radiance Caching

Hardware ray-tracing pipelines on modern console silicon operate within strict computational budgets, typically executing between 0.5 and 1.0 rays per screen pixel at 60Hz. These operational constraints have driven the adoption of Virtual Shadow Maps and spatiotemporal radiance filtering.

### 2.1 Virtual Shadow Maps (VSM)

Cascaded shadow maps require multi-pass scene rasterization across independent frustum splits, producing high draw-call volumes, CPU overhead, and edge-filtering swimming artifacts. Virtual Shadow Maps replace cascades by allocating a unified, multi-level virtual texture atlas—frequently configured up to $16384 \times 16384$ addressing space—backed by a physical GPU page pool composed of uniform $128 \times 128$ texel tiles.

During the primary geometry pass, pixels project their world positions into the light's view-projection space to flag active virtual pages within a resolution-matched hierarchical mipmap. Only pages containing visible, un-occluded geometry are allocated in physical memory and rasterized.

For static environmental geometry, unchanged physical pages persist across multiple frames, enabling the engine to reduce real-time shadow rasterization down to dynamic entity footprints.

### 2.2 Spatiotemporal Reservoir Reconstruction (ReSTIR)

To achieve realistic indirect illumination and area lighting under limited ray budgets, engines deploy Spatiotemporal Reservoir Importance Sampling (ReSTIR). ReSTIR treats sample generation as a dynamic data stream governed by small mathematical reservoirs. Each reservoir retains a selected candidate light sample $y$, an aggregated weight sum $w_{\text{sum}}$, the total number of evaluated samples $M$, and an unbiased normalizer $W$:

$$W = \frac{w_{\text{sum}}}{M \cdot \hat{p}(y)}$$

- **Temporal Pass**: The engine reprojects the surface position from frame $t-1$ into the current frame using screen-space velocity vectors, merging historical reservoirs with newly traced primary samples.
- **Spatial Pass**: Compute kernels execute cross-bilateral evaluations across neighboring pixels sharing matching world-space geometric normals and depth planes. By pooling reservoirs across spatial neighborhoods without tracing additional shadow rays, the system evaluates hundreds of candidate illumination samples per pixel, producing stable path-traced lighting on console-grade hardware.

---

## 3. Temporal Super-Resolution, Anti-Aliasing, and Upscaling

Modern native console architectures rarely execute shading passes at native $3840 \times 2160$ resolutions. Internal rendering targets are maintained at dynamic fractions of the display canvas—typically $1080\text{p}$ or $1440\text{p}$—and reconstructed via temporal super-resolution frameworks such as NVIDIA DLSS, AMD FSR 2/3, Unreal Engine TSR, and Sony PlayStation Spectral Super Resolution (PSSR).

### 3.1 Camera Sub-Pixel Jittering

To extract spatial high-frequency details from sub-pixel offsets across successive frames, the perspective projection matrix applies a frame-indexed spatial phase shift. This displacement is guided by low-discrepancy sequences, primarily the two-dimensional Halton $(2, 3)$ sequence, evaluated across an execution phase cycle of length $N = 8 \times (\text{ScaleFactor})^2$:

$$\Delta x = \frac{\text{Halton}(i, 2) - 0.5}{\text{RenderWidth}} \cdot 2.0, \quad \Delta y = \frac{\text{Halton}(i, 3) - 0.5}{\text{RenderHeight}} \cdot 2.0$$

The temporal accumulation pass aggregates these jittered frames over time, resolving sub-pixel edge boundaries and fine geometry without introducing the high-frequency blurring associated with basic post-process spatial filters.

### 3.2 Motion Vectors and Disocclusion Processing

Temporal reconstruction requires access to precision-aligned pixel motion vectors representing the spatial offset between a fragment's current clip-space position and its position in the previous frame:

$$\vec{v} = \text{ScreenPos}_{\text{current}} - \text{ScreenPos}_{\text{previous}}$$

To avoid quantization errors that induce jitter in distant background geometry, motion vectors are written to an `R16G16_FLOAT` texture target. Dynamic skeletal meshes evaluate bone transformations from both the current simulation tick and the prior tick within the vertex or mesh shader, guaranteeing that fast-moving characters emit motion vectors that account for physical skeletal displacement.

Disocclusion boundaries are detected by calculating depth differentials between the reprojected historical depth and the newly rasterized depth surface:

$$\Delta z = \left\vert z_{\text{reprojected}} - z_{\text{current}} \right\vert$$

If $\Delta z$ exceeds a calibrated geometric threshold, the temporal history is discarded, and the accumulation algorithm transitions to spatial clamping to prevent visual ghosting across high-contrast edges.

### 3.3 Reactive and Transparency Masks

Alpha-blended surfaces (such as volumetric smoke, transparent glass, fire particles, and particle ribbons) do not write to the primary depth buffer, precluding accurate velocity vector generation. If raw color buffers containing semi-transparent effects are fed directly into a temporal accumulator, moving particles leave visible trails across static backgrounds.

To prevent this distortion, the rendering engine rasterizes an auxiliary single-channel surface termed the **Reactive Mask** (`R8_UNORM`). Transparent particle shaders write normalized opacity and luminance values into this buffer.

During the temporal reconstruction pass, high values in the reactive mask reduce the temporal accumulation weighting of historical frames, forcing the algorithm to favor current-frame color data and preventing temporal smearing across non-opaque surfaces.

---

## 4. Modern Web Graphics Architecture: WebGPU and Clustered Shading

The introduction of the WebGPU API replaces the single-threaded, CPU-bound state machine of WebGL2 with a modern, compute-oriented model that maps directly onto Vulkan, DirectX 12, and Metal. WebGPU provides browser environments with access to explicit pipeline state objects, bind group allocation, and generalized compute shaders executed directly on the graphics processor.

### 4.1 Multithreaded Web Execution via OffscreenCanvas

The primary structural bottleneck in browser game execution is the single-threaded JavaScript execution context, where DOM operations, style reflows, garbage collection sweeps, and window event listeners compete for frame time. Attempting to issue draw commands directly from this UI thread leads to dropped frames and severe input latency.

Modern web rendering engines decouple the graphics pipeline from the DOM using an `OffscreenCanvas` hosted inside a dedicated Web Worker. During application initialization, the main thread captures the canvas node via `canvas.transferControlToOffscreen()` and transfers the handle across the worker boundary.

The Web Worker initializes the WebGPU device context and drives the rendering loop independently. Communication between the main thread (processing browser events) and the worker threads (running physics, audio, and graphics) utilizes shared memory blocks allocated via `SharedArrayBuffer`. Thread execution is synchronized through non-blocking `Atomics` operations, bypassing the structural serialization latency and memory allocation overhead of standard `postMessage` pipelines.

### 4.2 Compute-Driven Clustered Forward+ (Froxel) Shading

Due to memory bandwidth constraints, diverse mobile hardware profiles, and sandboxed memory quotas in web environments, browser runtimes avoid wide G-buffer layouts. The standard architecture for WebGPU illumination is **Clustered Forward+ Shading**.

The camera view frustum is discretized into a 3D grid of view-space bounding volumes, known as **Froxels** (typically configured as a $16 \times 9 \times 24$ voxel matrix across the $X, Y, \text{and } Z$ dimensions).

Subdivision along the depth axis ($Z$) follows an exponential progression to compensate for perspective foreshortening:

$$Z_{\text{slice}} = \left\lfloor \frac{\log\left(\frac{Z}{Z_{\text{near}}}\right)}{\log\left(\frac{Z_{\text{far}}}{Z_{\text{near}}}\right)} \cdot N_z \right\rfloor$$

The clustered shading pipeline executes through three stages:
1. **Cluster Generation Pass**: Runs during initialization or when camera projection matrices change. A compute shader evaluates the view-space $AABB$ (Axis-Aligned Bounding Box) for every cluster voxel and writes the resulting bounding planes to a uniform storage buffer.
2. **Light Culling Pass**: Runs every frame as a compute dispatch. Each compute workgroup processes an individual cluster volume, evaluating dynamic point and spot light spheres against the cluster's view-space $AABB$. The compute shader maintains a global light index list and an atomic allocation counter. When a light volume intersects a cluster, its index is appended to the global list, and the cluster's offset and light count parameters are updated.
3. **Forward Shading Pass**: Executes as a single-pass fragment shader over scene geometry. Each fragment evaluates its screen-space position and linear view depth to determine its assigned cluster index. The shader fetches only the specific light indices bound to that cluster volume, iterating through intersecting light sources without evaluating inactive or non-intersecting lights.

This architecture allows web applications to render scenes containing hundreds of dynamic light sources while maintaining strict 60fps frame deadlines on mobile and integrated graphics hardware.

---

## 5. Asset Pipelines, Texture Compression, and Ingestion Architectures

Data streaming across modern native platforms relies on high-speed NVMe flash buses running hardware-accelerated decompression pipelines. Conversely, web environments are fundamentally constrained by network bandwidth, necessitating runtime transcode workflows.

### 5.1 Texture Compression: Block Encoding and Universal Transcoding

Graphics processors do not sample directly from standard raster formats such as PNG or JPEG; doing so requires whole-image decompression into uncompressed RGBA8 memory, rapidly exceeding VRAM budgets and saturating memory bandwidth. Dedicated hardware block compression divides images into $4 \times 4$ texel blocks, providing constant-time, hardware-level random access to compressed color data:

| Compression Format | Block Dimensions | Effective Footprint | Hardware Targets | Primary Surface Applications |
| :--- | :--- | :--- | :--- | :--- |
| **BC1 (DXT1)** | $4 \times 4$ pixels | $4\,\text{bpp}$ (64 bits/block) | Desktop PC, Xbox, PlayStation | Opaque Albedo, Diffuse Base Color |
| **BC5 (RGTC)** | $4 \times 4$ pixels | $8\,\text{bpp}$ (128 bits/block) | Desktop PC, Xbox, PlayStation | Two-channel Tangent Normal Maps ($X, Y$) |
| **BC7 (BPTC)** | $4 \times 4$ pixels | $8\,\text{bpp}$ (128 bits/block) | Desktop PC, Xbox, PlayStation | High-fidelity Albedo + Alpha, Smoothness/Metalness |
| **ASTC ($4 \times 4$ to $8 \times 8$)** | Flexible ($4\times4\text{ to }12\times12$) | $8.0\,\text{bpp}$ down to $0.89\,\text{bpp}$ | Mobile, Apple Silicon, Switch | Universal Mobile and Cross-Platform PBR Surfaces |
| **Basis Universal (.ktx2)** | Adaptive UASTC / ETC1S | $1.0\text{--}1.5\,\text{bpp}$ (Transmission) | WebGPU, Wasm Runtime Transcoders | Universal distribution; transcoded on the fly |

For web graphics pipelines, asset repositories standardize network distribution on Basis Universal encapsulated in KTX2 containers (`.ktx2`). A Basis Universal texture is packaged as an intermediate representation (such as UASTC) that provides high compression ratios over the wire.

Upon asset ingestion, a WebAssembly-compiled transcoder inspects the local device profile. On desktop architectures supporting modern Direct3D or Vulkan runtimes, the Wasm module unpacks the texture directly into native BC7 or BC5 surfaces; on mobile devices or Apple Silicon, it transcodes into native ASTC textures.

This ensures that the web distribution pipeline delivers minimal over-the-wire payloads without requiring developers to pre-compile and host divergent texture asset pools.

### 5.2 Mesh Quantization and Compression Formats

Modern geometry delivery pipelines avoid transmitting uncompressed 32-bit floating-point vertex attributes. Runtimes optimize mesh payloads using standardized compression and quantization passes:
- **Coordinate Quantization**: Vertex positions are normalized into local bounding boxes and quantized into signed 16-bit integers ($S16$), reducing positional memory bandwidth by 50 percent compared to standard 32-bit floating-point arrays.
- **Octahedral Normal Encoding**: Surface normals and tangent spaces are calculated according to MikkTSpace conventions. Instead of transmitting full three-component floating-point vectors ($3 \times 32\,\text{bits}$), vectors are projected onto the surface of an octahedron and packed into two signed 8-bit or 16-bit values, significantly reducing input assembler memory traffic.
- **EXT_meshopt_compression**: Static level geometry and skeletal meshes are packaged using mesh optimization libraries that reorder triangle and index streams to maximize hardware vertex cache efficiency (FIFO vertex caches) while compressing index buffers for rapid WebAssembly-driven decoding.

---

## 6. Cross-Platform Technical Comparison and Sandbox Environments

The execution environments of dedicated console platforms and sandboxed web engines present stark architectural contrasts in memory models, resource binding capabilities, and hardware access:

| Subsystem | Native Console Platforms (PS5, Xbox Series X\|S) | Modern WebGPU Applications (Wasm Core) |
| :--- | :--- | :--- |
| **Physical Memory Space** | Unified 16GB GDDR6 memory architecture; direct GPU access. | Sandboxed memory; dynamic browser tab quotas ($2\text{--}4\,\text{GB}$). |
| **Hardware Binding Model** | Fully Bindless Descriptors (Tier 3: millions of concurrent textures). | `GPUBindGroup` structures; limited direct resource slots per stage. |
| **Memory Synchronization** | Explicit pipeline memory barriers (`vkCmdPipelineBarrier`, Split Barriers). | Managed tracking; browser runtime guarantees race-free passes. |
| **Geometric Primitive Engine** | Hardware Task and Mesh Shaders; cluster-level hardware culling. | Traditional Draw Calls; Compute-driven emulation via storage buffers. |
| **Threading Framework** | Native C++ worker thread pools with core affinity control. | Dedicated Web Workers communicating via `SharedArrayBuffer`. |
| **Asset Streaming Input** | DirectStorage / NVMe streaming directly into VRAM allocations. | Chunked range requests via Fetch API and Origin Private File System. |
| **Shading Language** | HLSL (Shader Model 6.6+), Slang, PlayStation PSSL. | WebGPU Shading Language (WGSL). |

---

## 7. Implementation Specifications and Technical Contracts

### Contract 1: Standard PBR Cook-Torrance Specular BRDF Formulation

To ensure consistent material evaluation, all lighting passes must evaluate the physical Cook-Torrance microfacet specular model combined with the Lambertian diffuse model. The surface evaluation function is defined as:

$$f_r(\vec{p}, \vec{\omega}_i, \vec{\omega}_o) = k_d \cdot f_{\text{diffuse}} + k_s \cdot f_{\text{specular}}$$

Where the vector relationships are established using the surface normal $\vec{n}$, the view direction vector pointing toward the camera $\vec{v}$, the incident light vector pointing toward the light source $\vec{l}$, and the halfway vector:

$$\vec{h} = \frac{\vec{v} + \vec{l}}{\Vert \vec{v} + \vec{l} \Vert}$$

The individual components of the reflection model evaluate as follows:

1. **The Lambertian Diffuse Formulation**:
   $$f_{\text{diffuse}} = \frac{c_{\text{albedo}}}{\pi}$$

2. **The Cook-Torrance Specular Model**:
   $$f_{\text{specular}} = \frac{D(\vec{h}) \cdot F(\vec{v}, \vec{h}) \cdot G(\vec{l}, \vec{v})}{4 \cdot (\vec{n} \cdot \vec{l}) \cdot (\vec{n} \cdot \vec{v})}$$

3. **The Normal Distribution Function ($D$ using Trowbridge-Reitz GGX)**:
   $$D(\vec{h}) = \frac{\alpha^2}{\pi \left( (\vec{n} \cdot \vec{h})^2 (\alpha^2 - 1) + 1 \right)^2}, \quad \alpha = \text{Roughness}^2$$

4. **The Fresnel Reflectance ($F$ using the Fresnel-Schlick Approximation)**:
   $$F(\vec{v}, \vec{h}) = F_0 + (1.0 - F_0) \cdot (1.0 - (\vec{v} \cdot \vec{h}))^5$$
   $$F_0 = (1.0 - \text{Metallic}) \cdot 0.04 + \text{Metallic} \cdot c_{\text{albedo}}$$

5. **The Geometric Attenuation ($G$ using the Smith Model with Schlick-GGX)**:
   $$G(\vec{l}, \vec{v}) = G_1(\vec{v}) \cdot G_1(\vec{l})$$
   $$G_1(\vec{x}) = \frac{\vec{n} \cdot \vec{x}}{(\vec{n} \cdot \vec{x})(1 - k) + k}, \quad k = \frac{(\text{Roughness} + 1)^2}{8}$$

### Contract 2: WebGPU Clustered Light-Culling Compute Shader (WGSL)

The following WGSL compute kernel accepts a pre-calculated uniform cluster buffer, evaluates spherical point light bounds against each cluster's view-space Axis-Aligned Bounding Box ($AABB$), and writes the resulting light indices to a global storage buffer:

```wgsl
struct PointLight {
    position: vec3<f32>,
    radius: f32,
    color: vec3<f32>,
    intensity: f32,
};

struct ClusterAABB {
    min_point: vec4<f32>,
    max_point: vec4<f32>,
};

struct LightGrid {
    offset: u32,
    count: u32,
};

@group(0) @binding(0) var<storage, read> clusters: array<ClusterAABB>;
@group(0) @binding(1) var<storage, read> lights: array<PointLight>;
@group(0) @binding(2) var<storage, read_write> globalLightIndexList: array<u32>;
@group(0) @binding(3) var<storage, read_write> clusterLightGrids: array<LightGrid>;
@group(0) @binding(4) var<storage, read_write> globalIndexCounter: atomic<u32>;

const MAX_LIGHTS_PER_CLUSTER: u32 = 64u;

@compute @workgroup_size(16, 1, 1)
fn main(@builtin(GlobalInvocationID) global_id: vec3<u32>) {
    let clusterIndex = global_id.x;
    if (clusterIndex >= arrayLength(&clusters)) {
        return;
    }

    let aabb = clusters[clusterIndex];
    var visibleLightCount: u32 = 0u;
    var localLightIndices: array<u32, MAX_LIGHTS_PER_CLUSTER>;

    let totalLights = arrayLength(&lights);
    for (var i: u32 = 0u; i < totalLights; i = i + 1u) {
        let light = lights[i];
        
        let closestPoint = clamp(
            light.position,
            aabb.min_point.xyz,
            aabb.max_point.xyz
        );
        
        let delta = light.position - closestPoint;
        let distanceSquared = dot(delta, delta);

        if (distanceSquared <= (light.radius * light.radius)) {
            if (visibleLightCount < MAX_LIGHTS_PER_CLUSTER) {
                localLightIndices[visibleLightCount] = i;
                visibleLightCount = visibleLightCount + 1u;
            }
        }
    }

    let baseOffset = atomicAdd(&globalIndexCounter, visibleLightCount);

    for (var j: u32 = 0u; j < visibleLightCount; j = j + 1u) {
        globalLightIndexList[baseOffset + j] = localLightIndices[j];
    }

    clusterLightGrids[clusterIndex].offset = baseOffset;
    clusterLightGrids[clusterIndex].count = visibleLightCount;
}
```

### Contract 3: Render Graph Execution Topology

Modern rendering architectures structure frame operations as a Directed Acyclic Graph (DAG). Render passes declare their explicit read and write resource dependencies, allowing the engine to schedule execution barriers, eliminate redundant render targets, and manage memory synchronization across pipelines:

| Pass Identifier | Pipeline Type | Primary Resource Inputs | Primary Resource Outputs | Resource State Transition Barrier |
| :--- | :--- | :--- | :--- | :--- |
| **01. Depth & VisBuffer** | Rasterization | Mesh Storage, Scene Transforms | `VisBuffer_R32G32`, `SceneDepth_D32F` | `RESOURCE_STATE_DEPTH_WRITE` |
| **02. Velocity Buffer** | Rasterization | Current/Previous Bone Transforms | `Velocity_R16G16F` | `RESOURCE_STATE_RENDER_TARGET` |
| **03. Cluster Culling** | Compute | `SceneDepth_D32F`, Global Light Array | `ClusterLightGrid`, `LightIndexList` | `UAV_BARRIER` / `COMPUTE_RESOURCE` |
| **04. Material Shading** | Compute / Raster | `VisBuffer`, `LightIndexList`, Textures | `SceneColor_RGBA16F` | `RESOURCE_STATE_UNORDERED_ACCESS` |
| **05. Temporal Upscale** | Compute | `SceneColor`, `SceneDepth`, `Velocity` | `ResolvedColor_RGBA16F` | `RESOURCE_STATE_COMPUTE_READ_WRITE` |
| **06. Post-Process Composite** | Rasterization | `ResolvedColor`, Color LUTs | Swapchain Present Surface | `RESOURCE_STATE_PRESENT` |

### Contract 4: Camera Jitter Offset and Motion Vector Structs

Engines implementing temporal super-resolution must manage sub-pixel projection offsets and motion vector calculations using normalized device coordinates ($NDC$):

```cpp
struct TemporalFrameContext {
    uint32_t frame_index;
    float render_width;
    float render_height;
    float display_width;
    float display_height;
    
    float jitter_x;
    float jitter_y;
    
    Matrix4x4 view_matrix;
    Matrix4x4 projection_matrix_unjittered;
    Matrix4x4 projection_matrix_jittered;
    Matrix4x4 view_projection_matrix_jittered;
    
    Matrix4x4 prev_view_matrix;
    Matrix4x4 prev_projection_matrix_unjittered;
    Matrix4x4 prev_view_projection_matrix_unjittered;
};

vec2 CalculateScreenSpaceMotionVector(vec4 current_clip_pos, vec4 previous_clip_pos) {
    vec2 current_ndc = current_clip_pos.xy / current_clip_pos.w;
    vec2 previous_ndc = previous_clip_pos.xy / previous_clip_pos.w;
    
    vec2 current_uv = current_ndc * 0.5 + 0.5;
    vec2 previous_uv = previous_ndc * 0.5 + 0.5;
    
    #if TARGET_VULKAN_OR_WEBGPU
    current_uv.y = 1.0 - current_uv.y;
    previous_uv.y = 1.0 - previous_uv.y;
    #endif
    
    return current_uv - previous_uv;
}
```

---

## 8. Architectural Conclusions

The modern graphics landscape has consolidated around compute-centric workflows that separate geometric rasterization from material illumination. For native console targets, the standard implementation path relies on Visibility Buffers paired with Mesh Shaders and programmatic vertex pulling, minimizing memory bandwidth bottlenecks and eliminating fragment overdraw. Hardware ray-tracing limitations are balanced through Virtual Shadow Maps and spatiotemporal reservoir sampling (ReSTIR), which decouple lighting evaluation from per-frame ray budgets.

For web architectures, WebGPU enables console-adjacent rendering techniques within sandboxed browser environments. Decoupling rendering to Web Workers via `OffscreenCanvas` protects framerates from main-thread browser latency, while Clustered Forward+ compute pipelines efficiently bin hundreds of dynamic light sources across disparate hardware profiles.

Asset distribution across both paradigms reflects these architectural demands: native systems maximize uncompressed streaming throughput over direct storage buses, while web engines rely on universal intermediate containers like Basis Universal KTX2, transcoding textures on the fly to match local GPU architectures. Implementing these systems through formalized Render Graph topologies ensures reproducible, high-performance rendering pipelines across both dedicated console silicon and modern web runtimes.
