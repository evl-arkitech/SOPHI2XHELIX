"""Generate photorealistic PBR textures for exterior grounds, asphalt driveway, wet lawn, and perimeter fence."""
import os
import numpy as np
from PIL import Image, ImageFilter

TEXTURE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'textures', 'pbr')

def make_normal_map(height_map: np.ndarray, strength: float = 3.0) -> np.ndarray:
    """Generate tangent-space normal map using Sobel filter."""
    h = height_map.astype(np.float32) / 255.0
    # Sobel kernels
    dx = np.zeros_like(h)
    dy = np.zeros_like(h)
    dx[:, :-1] = h[:, 1:] - h[:, :-1]
    dx[:, -1] = dx[:, -2]
    dy[:-1, :] = h[1:, :] - h[:-1, :]
    dy[-1, :] = dy[-2, :]
    
    nx = -dx * strength
    ny = -dy * strength
    nz = np.ones_like(h)
    
    length = np.sqrt(nx*nx + ny*ny + nz*nz)
    nx /= length
    ny /= length
    nz /= length
    
    rgb = np.zeros((h.shape[0], h.shape[1], 3), dtype=np.uint8)
    rgb[..., 0] = ((nx * 0.5 + 0.5) * 255).astype(np.uint8)
    rgb[..., 1] = ((ny * 0.5 + 0.5) * 255).astype(np.uint8)
    rgb[..., 2] = ((nz * 0.5 + 0.5) * 255).astype(np.uint8)
    return rgb

def generate_wet_asphalt(size=1024):
    out_dir = os.path.join(TEXTURE_DIR, 'terrain')
    os.makedirs(out_dir, exist_ok=True)
    
    # Asphalt Diffuse: Dark charcoal, gravel speckling, moisture darkening
    np.random.seed(42)
    noise = np.random.normal(0, 1, (size, size))
    noise = (noise - noise.min()) / (noise.max() - noise.min())
    
    gravel = np.random.uniform(0.12, 0.22, (size, size))
    # Add high frequency speckles
    speckles = (np.random.rand(size, size) > 0.88).astype(np.float32) * 0.08
    base_lum = gravel + speckles
    
    diff_rgb = np.zeros((size, size, 3), dtype=np.uint8)
    diff_rgb[..., 0] = (base_lum * 220).astype(np.uint8)
    diff_rgb[..., 1] = (base_lum * 230).astype(np.uint8)
    diff_rgb[..., 2] = (base_lum * 245).astype(np.uint8)
    
    Image.fromarray(diff_rgb).save(os.path.join(out_dir, 'asphalt_wet_diffuse_2k.jpg'), quality=92)
    
    # Asphalt Normal map
    norm_rgb = make_normal_map((base_lum * 255).astype(np.uint8), strength=2.5)
    Image.fromarray(norm_rgb).save(os.path.join(out_dir, 'asphalt_wet_normal_2k.jpg'), quality=92)
    
    # Roughness: Low roughness (0.15 - 0.35) due to standing rainwater sheen
    rough = (base_lum * 110 + 40).astype(np.uint8)
    Image.fromarray(rough).save(os.path.join(out_dir, 'asphalt_wet_roughness_2k.jpg'), quality=92)
    print("Generated wet asphalt PBR maps.")

def generate_wet_lawn(size=1024):
    out_dir = os.path.join(TEXTURE_DIR, 'terrain')
    os.makedirs(out_dir, exist_ok=True)
    
    np.random.seed(101)
    # Directional grass blades and mud variation
    base = np.random.normal(0.4, 0.1, (size, size))
    base = np.clip(base, 0.1, 0.8)
    
    diff_rgb = np.zeros((size, size, 3), dtype=np.uint8)
    # Dark nocturnal wet grass: deep forest green / muddy earth
    diff_rgb[..., 0] = (base * 50 + 15).astype(np.uint8)
    diff_rgb[..., 1] = (base * 95 + 25).astype(np.uint8)
    diff_rgb[..., 2] = (base * 40 + 12).astype(np.uint8)
    
    Image.fromarray(diff_rgb).save(os.path.join(out_dir, 'lawn_wet_diffuse_2k.jpg'), quality=92)
    
    norm_rgb = make_normal_map((base * 255).astype(np.uint8), strength=3.2)
    Image.fromarray(norm_rgb).save(os.path.join(out_dir, 'lawn_wet_normal_2k.jpg'), quality=92)
    
    rough = (base * 100 + 70).astype(np.uint8)
    Image.fromarray(rough).save(os.path.join(out_dir, 'lawn_wet_roughness_2k.jpg'), quality=92)
    print("Generated wet lawn PBR maps.")

def generate_perimeter_fence(size=1024):
    out_dir = os.path.join(TEXTURE_DIR, 'fence')
    os.makedirs(out_dir, exist_ok=True)
    
    np.random.seed(202)
    # Vertical wood planks
    plank_width = 64
    planks = np.zeros((size, size), dtype=np.float32)
    for x in range(0, size, plank_width):
        tint = np.random.uniform(0.75, 1.0)
        planks[:, x:x+plank_width-2] = tint
        planks[:, x+plank_width-2:x+plank_width] = 0.25 # Gap between pickets
        
    wood_grain = np.random.normal(0, 0.05, (size, size))
    planks = np.clip(planks + wood_grain, 0, 1)
    
    diff_rgb = np.zeros((size, size, 3), dtype=np.uint8)
    diff_rgb[..., 0] = (planks * 70).astype(np.uint8)
    diff_rgb[..., 1] = (planks * 55).astype(np.uint8)
    diff_rgb[..., 2] = (planks * 42).astype(np.uint8)
    
    Image.fromarray(diff_rgb).save(os.path.join(out_dir, 'fence_diffuse_2k.jpg'), quality=92)
    
    norm_rgb = make_normal_map((planks * 255).astype(np.uint8), strength=3.0)
    Image.fromarray(norm_rgb).save(os.path.join(out_dir, 'fence_normal_2k.jpg'), quality=92)
    
    rough = (planks * 120 + 80).astype(np.uint8)
    Image.fromarray(rough).save(os.path.join(out_dir, 'fence_roughness_2k.jpg'), quality=92)
    print("Generated perimeter fence PBR maps.")

if __name__ == '__main__':
    generate_wet_asphalt()
    generate_wet_lawn()
    generate_perimeter_fence()
