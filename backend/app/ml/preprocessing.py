import io
import math
from PIL import Image
import numpy as np

TARGET_IMAGE_SIZE = (224, 224)
FEATURE_DIM = 48

def load_and_preprocess_image(image_bytes: bytes, target_size=TARGET_IMAGE_SIZE) -> np.ndarray:
    """
    Safely opens image bytes, converts to RGB, resizes to target_size,
    and returns normalized float32 array in [0, 1].
    """
    image = Image.open(io.BytesIO(image_bytes))
    if image.mode != "RGB":
        image = image.convert("RGB")
    
    image = image.resize(target_size, Image.Resampling.BILINEAR)
    img_array = np.array(image, dtype=np.float32) / 255.0
    
    # Add batch dimension: (1, 224, 224, 3)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def extract_botanical_feature_vector(image_bytes: bytes) -> np.ndarray:
    """
    Extracts a 48-dimensional botanical and agricultural feature vector from image bytes.
    Captures:
    - Multi-spectral RGB & HSV moments (12)
    - 12-bin saturated Hue distribution (12)
    - Vegetation, carotenoid, anthocyanin indices (4)
    - Morphological blade linearity, serration, and gradient entropy (6)
    - Foliar, stem, floral, and fruit biomarkers (6)
    - Pedological soil color and texture signatures (4)
    - Rejection signals for human skin, UI screenshots, and neutral screens (4)
    """
    try:
        image = Image.open(io.BytesIO(image_bytes))
        if image.mode != "RGB":
            image = image.convert("RGB")
    except Exception:
        # Return fallback zero vector if unreadable
        return np.zeros(FEATURE_DIM, dtype=np.float32)

    width, height = image.size
    aspect_ratio = float(width) / float(height) if height > 0 else 1.0

    # Resize to 128x128 for efficient and consistent feature computation
    thumb = image.resize((128, 128), Image.Resampling.BILINEAR)
    arr = np.array(thumb, dtype=np.float32) / 255.0  # normalized [0, 1]
    
    r = arr[:, :, 0]
    g = arr[:, :, 1]
    b = arr[:, :, 2]
    
    total_pixels = 128 * 128
    
    # 1. Background vs Foreground Foliage Segmentation
    is_bright_neutral = (r > 0.82) & (g > 0.82) & (b > 0.82) & (np.abs(r - g) < 0.08) & (np.abs(r - b) < 0.08)
    is_dark_neutral = (r < 0.06) & (g < 0.06) & (b < 0.06)
    is_neutral_bg = is_bright_neutral | is_dark_neutral
    
    # Foliage mask: plant green tissue
    green_mask = (g > r * 1.02) & (g > b * 1.01) & (g > 0.12) & (~is_neutral_bg)
    foliar_mask = (g > 0.10) & (~is_neutral_bg)
    if np.sum(foliar_mask) < 40:
        foliar_mask = np.ones((128, 128), dtype=bool)
    
    fg_ratio = float(np.sum(foliar_mask) / total_pixels)

    # 2. RGB Moments on Foreground Plant Tissue
    r_fg, g_fg, b_fg = r[foliar_mask], g[foliar_mask], b[foliar_mask]
    r_mean, g_mean, b_mean = float(np.mean(r_fg)), float(np.mean(g_fg)), float(np.mean(b_fg))
    r_std, g_std, b_std = float(np.std(r_fg)), float(np.std(g_fg)), float(np.std(b_fg))
    
    # 3. Vectorized RGB to HSV conversion
    max_c = np.maximum(np.maximum(r, g), b)
    min_c = np.minimum(np.minimum(r, g), b)
    delta = max_c - min_c
    
    v = max_c
    s = np.where(max_c > 1e-5, delta / (max_c + 1e-5), 0.0)
    
    h = np.zeros_like(max_c)
    mask_r = (max_c == r) & (delta > 1e-5)
    mask_g = (max_c == g) & (delta > 1e-5)
    mask_b = (max_c == b) & (delta > 1e-5)
    
    h[mask_r] = ((g[mask_r] - b[mask_r]) / delta[mask_r]) % 6.0
    h[mask_g] = ((b[mask_g] - r[mask_g]) / delta[mask_g]) + 2.0
    h[mask_b] = ((r[mask_b] - g[mask_b]) / delta[mask_b]) + 4.0
    h = h / 6.0  # Normalize H to [0, 1]
    
    h_fg, s_fg, v_fg = h[foliar_mask], s[foliar_mask], v[foliar_mask]
    h_mean, s_mean, v_mean = float(np.mean(h_fg)), float(np.mean(s_fg)), float(np.mean(v_fg))
    h_std, s_std, v_std = float(np.std(h_fg)), float(np.std(s_fg)), float(np.std(v_fg))
    
    # 4. 12-bin Hue Distribution on Saturated Plant Tissue
    sat_mask = (s > 0.12) & (v > 0.10) & foliar_mask
    sat_h = h[sat_mask]
    
    hue_bins = np.zeros(12, dtype=np.float32)
    if len(sat_h) > 10:
        bin_edges = [0.0, 0.08, 0.12, 0.16, 0.20, 0.25, 0.33, 0.42, 0.50, 0.60, 0.75, 0.88, 1.0]
        for i in range(12):
            hue_bins[i] = np.sum((sat_h >= bin_edges[i]) & (sat_h < bin_edges[i+1]))
        total_sat = np.sum(hue_bins)
        if total_sat > 0:
            hue_bins = hue_bins / total_sat
    else:
        hue_bins[6] = 0.5
        hue_bins[5] = 0.3
        hue_bins[7] = 0.2

    # 5. Color & Vegetation Indices
    veg_index = (g_mean - r_mean) / (g_mean + r_mean + 1e-5)
    excess_green = (2.0 * g_mean - r_mean - b_mean)
    anthocyanin_index = (r_mean - g_mean) / (r_mean + g_mean + 1e-5)
    carotenoid_index = (r_mean + g_mean - 2.0 * b_mean) / (r_mean + g_mean + 2.0 * b_mean + 1e-5)

    # 6. Spatial Gradients, Textures & Linearity
    dx = np.diff(g * 255.0, axis=1)
    dy = np.diff(g * 255.0, axis=0)
    grad_mag = float((np.mean(np.abs(dx)) + np.mean(np.abs(dy))) / 255.0)
    mean_dx = float(np.mean(np.abs(dx)))
    mean_dy = float(np.mean(np.abs(dy)))
    anisotropy = float(max(mean_dx, mean_dy) / (min(mean_dx, mean_dy) + 1e-4))

    # Elongation is orientation-invariant length/width ratio
    elongation = max(float(width), float(height)) / max(1.0, min(float(width), float(height)))

    # Linear blade index: elongated leaf with prominent parallel directional venation (cereals, monocots, grasses)
    if elongation > 2.0 and (anisotropy > 1.20 or elongation > 2.8):
        linear_blade_index = float(min(1.0, 0.50 + (elongation - 2.0) * 0.15 + (anisotropy - 1.0) * 0.1))
    else:
        linear_blade_index = float(min(0.35, 0.10 + elongation * 0.04))

    vert_dom = linear_blade_index

    # Gradient Directional Entropy
    dx_sub = dx[:-1, :]
    dy_sub = dy[:, :-1]
    angles = np.arctan2(dy_sub, dx_sub)
    angle_bins, _ = np.histogram(angles, bins=8, range=(-np.pi, np.pi))
    angle_probs = angle_bins / (np.sum(angle_bins) + 1e-6)
    angle_probs = angle_probs[angle_probs > 0]
    grad_entropy = float(-np.sum(angle_probs * np.log2(angle_probs)) / 3.0)  # normalized to [0, 1]

    # Leaf serrations / margin roughness
    diff_green_x = np.diff(green_mask.astype(np.float32), axis=1)
    diff_green_y = np.diff(green_mask.astype(np.float32), axis=0)
    edge_transitions = np.sum(np.abs(diff_green_x)) + np.sum(np.abs(diff_green_y))
    serration_index = float(edge_transitions / (np.sum(green_mask) + 1e-4) * 1.5)
    serration_index = max(0.0, min(1.0, serration_index))

    # 7. Organ and Health Biomarkers
    total_fg_pixels = max(10, np.sum(foliar_mask))
    
    # Necrosis (dark brown spots / dried margins)
    necrotic_mask = (r > 0.22) & (g > 0.10) & (b < 0.22) & (r > g * 1.12) & foliar_mask
    necrotic_brown = float(np.sum(necrotic_mask) / total_fg_pixels)

    # Chlorosis (yellowing between veins or margins)
    chlorotic_mask = (r > 0.45) & (g > 0.40) & (b < 0.35) & (np.abs(r - g) < 0.18) & (g >= b * 1.1) & foliar_mask
    chlorotic_yellow = float(np.sum(chlorotic_mask) / total_fg_pixels)

    # Powdery Mildew (chalky white spots)
    mildew_mask = (r > 0.70) & (g > 0.70) & (b > 0.70) & (s < 0.20) & foliar_mask & (~is_bright_neutral)
    mildew_white = float(np.sum(mildew_mask) / total_fg_pixels)

    # Stem & Woody Branch (woody brown/grey fibrous stalk)
    woody_mask = (r > 0.28) & (g > 0.20) & (b < 0.25) & (r > g) & (g > b) & (r - b > 0.08)
    stem_woody_ratio = float(np.sum(woody_mask) / total_pixels)

    # Floral Petal Pigments (pink, violet, bright red, golden yellow)
    floral_mask = (
        ((r > 0.50) & (b > 0.25) & (g < 0.35)) |
        ((r > 0.40) & (b > 0.45) & (g < 0.30)) |
        ((r > 0.65) & (g > 0.50) & (b < 0.25))
    ) & (~is_neutral_bg)
    floral_petal_ratio = float(np.sum(floral_mask) / total_pixels)

    # Fleshy Fruit Pigments (tomato red, citrus orange, berry purple)
    fruit_mask = (
        ((r > 0.65) & (g < 0.28) & (b < 0.28)) |
        ((r > 0.70) & (g > 0.35) & (g < 0.60) & (b < 0.20))
    ) & (~is_neutral_bg)
    fruit_pigment_ratio = float(np.sum(fruit_mask) / total_pixels)

    # 8. Pedological Soil Signatures
    dark_humus_mask = (r < 0.30) & (g < 0.30) & (b < 0.30) & (r > 0.05) & (g > 0.05) & (r >= g) & (~is_neutral_bg)
    dark_humus = float(np.sum(dark_humus_mask) / total_pixels)

    ferric_red_mask = (r > 0.45) & (g < 0.35) & (b < 0.30) & (r > g * 1.25) & (~is_neutral_bg)
    ferric_red = float(np.sum(ferric_red_mask) / total_pixels)

    sandy_buff_mask = (r > 0.50) & (g > 0.42) & (b > 0.30) & (r > g) & (g > b) & (~is_bright_neutral)
    sandy_buff = float(np.sum(sandy_buff_mask) / total_pixels)

    soil_grain_texture = float(np.std(r) + np.std(g))

    # 9. Non-Agriculture Rejection Signals
    skin_px = (
        (r > 0.50) & (g > 0.35) & (b > 0.25) &
        (r > g) & (g > b) &
        ((r - g) > 0.08) & ((r - b) > 0.15) &
        ((r - g) < 0.35) & (~woody_mask) & (~ferric_red_mask)
    )
    skin_tone_ratio = float(np.mean(skin_px))

    ui_neon_blue = float(np.mean((b > 0.55) & (b > g * 1.25) & (b > r * 1.15)))
    diff_rg = np.abs(r - g)
    diff_rb = np.abs(r - b)
    diff_gb = np.abs(g - b)
    is_neutral = (diff_rg < 0.06) & (diff_rb < 0.06) & (diff_gb < 0.06)
    neutral_screen_ratio = float(np.mean(is_neutral | is_bright_neutral | is_dark_neutral))
    grid_edge_density = float(np.mean(np.abs(np.diff(r, axis=0)) > 0.30))

    # Assemble 48-dimensional feature vector
    vec = np.zeros(FEATURE_DIM, dtype=np.float32)
    vec[0] = r_mean
    vec[1] = g_mean
    vec[2] = b_mean
    vec[3] = r_std
    vec[4] = g_std
    vec[5] = b_std
    vec[6] = h_mean
    vec[7] = s_mean
    vec[8] = v_mean
    vec[9] = h_std
    vec[10] = s_std
    vec[11] = v_std
    vec[12:24] = hue_bins
    vec[24] = veg_index
    vec[25] = excess_green
    vec[26] = anthocyanin_index
    vec[27] = carotenoid_index
    vec[28] = fg_ratio
    vec[29] = min(5.0, max(0.5, elongation))
    vec[30] = grad_mag
    vec[31] = grad_entropy
    vec[32] = linear_blade_index
    vec[33] = serration_index
    vec[34] = necrotic_brown
    vec[35] = chlorotic_yellow
    vec[36] = mildew_white
    vec[37] = stem_woody_ratio
    vec[38] = floral_petal_ratio
    vec[39] = fruit_pigment_ratio
    vec[40] = dark_humus
    vec[41] = ferric_red
    vec[42] = sandy_buff
    vec[43] = soil_grain_texture
    vec[44] = skin_tone_ratio
    vec[45] = ui_neon_blue
    vec[46] = neutral_screen_ratio
    vec[47] = grid_edge_density

    return vec

def extract_visual_color_features(image_bytes: bytes) -> dict:
    """
    Extracts high-level color, texture, and health metrics from image bytes.
    """
    vec = extract_botanical_feature_vector(image_bytes)
    
    r_mean, g_mean, b_mean = float(vec[0]), float(vec[1]), float(vec[2])
    hue_bins = vec[12:24]
    
    green_ratio = float(np.sum(hue_bins[5:8])) * float(vec[28])
    if green_ratio < 0.05 and vec[24] > 0.05:
        green_ratio = float(vec[28]) * 0.7
        
    deep_green_ratio = float(hue_bins[7])
    yellow_green_ratio = float(hue_bins[4])
    yellow_ratio = float(vec[35])
    brown_ratio = float(vec[34])
    white_mildew_ratio = float(vec[36])
    rose_pink_ratio = float(vec[38])
    violet_ratio = float(hue_bins[10])
    
    dark_earth_ratio = float(vec[40])
    red_earth_ratio = float(vec[41])
    sandy_ratio = float(vec[42])
    
    gradient_magnitude = float(vec[30])
    aspect_ratio = float(vec[29])
    linear_blade_index = float(vec[32])
    
    # Calculate health vs infection severity
    necrotic_tissue = brown_ratio + (yellow_ratio * 0.6) + (white_mildew_ratio * 0.7)
    total_foliar = max(0.05, green_ratio + necrotic_tissue + float(vec[37]))
    infection_pct = min(92.0, max(3.0, (necrotic_tissue / total_foliar) * 100.0))
    health_pct = max(8.0, min(98.0, 100.0 - infection_pct))
    
    return {
        "green_ratio": green_ratio,
        "deep_green_ratio": deep_green_ratio,
        "yellow_green_ratio": yellow_green_ratio,
        "yellow_ratio": yellow_ratio,
        "brown_ratio": brown_ratio,
        "white_mildew_ratio": white_mildew_ratio,
        "rose_pink_ratio": rose_pink_ratio,
        "violet_ratio": violet_ratio,
        "dark_earth_ratio": dark_earth_ratio,
        "red_earth_ratio": red_earth_ratio,
        "sandy_ratio": sandy_ratio,
        "gradient_magnitude": gradient_magnitude,
        "edge_density": gradient_magnitude,
        "std_contrast": float(np.std(vec[:3])),
        "color_std": float(np.std(vec[:3])),
        "linear_blade_index": linear_blade_index,
        "aspect_ratio": aspect_ratio,
        "health_percentage": round(health_pct, 1),
        "damage_severity_percentage": round(infection_pct, 1),
        "white_ratio": white_mildew_ratio,
        "red_ratio": red_earth_ratio,
        "brightness": float((r_mean + g_mean + b_mean) / 3.0 * 255.0),
        "mean_brightness": float((r_mean + g_mean + b_mean) / 3.0 * 255.0),
        "feature_vector": vec
    }
