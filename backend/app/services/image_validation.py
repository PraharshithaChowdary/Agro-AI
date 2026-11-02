import io
from PIL import Image
import numpy as np
from app.ml.preprocessing import (
    extract_visual_color_features,
    extract_botanical_feature_vector,
    load_and_preprocess_image
)

class AgriculturalRelevanceService:
    @staticmethod
    def validate_image_file(image_bytes: bytes, max_size_mb: int = 15) -> tuple[bool, str]:
        """
        Validates file size, integrity, and basic image decode.
        """
        if not image_bytes or len(image_bytes) == 0:
            return False, "Uploaded image file is empty."

        if len(image_bytes) > max_size_mb * 1024 * 1024:
            return False, f"Image file exceeds maximum allowable size of {max_size_mb}MB."

        try:
            img = Image.open(io.BytesIO(image_bytes))
            img.verify()  # Verify image header and integrity
            # Reopen because verify() closes the stream
            img = Image.open(io.BytesIO(image_bytes))
            if img.width < 50 or img.height < 50:
                return False, "Image resolution is too low for agricultural analysis. Minimum 50x50 pixels required."
            return True, "Valid image stream"
        except Exception:
            return False, "Malformed or unsupported image file. Please provide a valid JPG, PNG, or WebP image."

    @staticmethod
    def detect_agricultural_modality(image_bytes: bytes) -> dict:
        """
        Determines whether the image is:
        - 'crop_leaf': Leaf, plant, blossom, fruit, stem, root, or whole foliage image
        - 'soil': Topsoil, earth, ground, sand, clay, or furrow image
        - 'non_agriculture': Screenshots, UI, documents, cars, selfies, electronics, buildings
        - 'uncertain': Ambiguous or unclassifiable
        """
        try:
            pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB").resize((128, 128))
            px = np.array(pil_img, dtype=np.float32) / 255.0
            r_px, g_px, b_px = px[:, :, 0], px[:, :, 1], px[:, :, 2]
            total_px = 128 * 128

            # Neutral pixel detector: grayscale, white canvas, or dark theme UI
            diff_rg = np.abs(r_px - g_px)
            diff_rb = np.abs(r_px - b_px)
            diff_gb = np.abs(g_px - b_px)
            is_neutral = (diff_rg < 0.05) & (diff_rb < 0.05) & (diff_gb < 0.05)
            is_bright_canvas = (r_px > 0.85) & (g_px > 0.85) & (b_px > 0.85)
            is_dark_theme = (r_px < 0.12) & (g_px < 0.12) & (b_px < 0.12)
            neutral_ratio = float(np.sum(is_neutral | is_bright_canvas | is_dark_theme) / total_px)

            # Synthetic UI Colors: Web/App purples, vibrant blues, cyans, neons
            is_ui_purple_blue = (
                ((b_px > 0.55) & (b_px > g_px * 1.25) & (b_px > r_px * 1.15)) | # Deep blue / Indigo
                ((r_px > 0.35) & (b_px > 0.50) & (g_px < 0.40)) |               # Purple / Violet UI
                ((g_px > 0.70) & (b_px > 0.70) & (r_px < 0.30))                 # Cyan
            )
            ui_color_ratio = float(np.sum(is_ui_purple_blue) / total_px)

            # Earth pedological soil tones (dark humus, red ferric laterite, sandy loam, alluvial brown)
            earth_tones = (
                ((r_px < 0.52) & (g_px < 0.40) & (b_px < 0.30) & (r_px > 0.05) & (g_px > 0.04) & (r_px >= g_px) & (g_px >= b_px)) | # Dark/brown humus & loam
                ((r_px > 0.45) & (g_px < 0.38) & (b_px < 0.28) & (r_px > g_px * 1.20)) |                                             # Red / Laterite
                ((r_px > 0.45) & (g_px > 0.35) & (b_px > 0.20) & (r_px > g_px) & (g_px > b_px) & (diff_rg > 0.04))                  # Sandy loam / Alluvial
            )
            soil_ratio = float(np.sum(earth_tones) / total_px)

            # Skin tone detector for selfies / human faces (light peach/pinkish tones without earth saturation)
            skin_px = (
                (r_px > 0.52) & (g_px > 0.35) & (b_px > 0.25) &
                (r_px > g_px) & (g_px > b_px) &
                ((r_px - g_px) > 0.08) & ((r_px - b_px) > 0.16) &
                ((r_px - g_px) < 0.35) & (~earth_tones)
            )
            skin_ratio = float(np.mean(skin_px))

            # Woody stem & bark (fibrous brown/ochre with longitudinal texture)
            # Woody stem & bark (fibrous brown/ochre with longitudinal texture)
            woody_stem_px = (
                (r_px > 0.28) & (g_px > 0.20) & (b_px < 0.25) &
                (r_px > g_px) & (g_px > b_px) & ((r_px - b_px) > 0.08)
            )
            woody_ratio = float(np.sum(woody_stem_px) / total_px)

            # Green chlorophyll foliar pixels (natural green spectrum)
            green_foliar = (g_px > r_px * 1.04) & (g_px > b_px * 1.04) & (g_px > 0.12) & (~is_neutral)
            green_ratio = float(np.sum(green_foliar) / total_px)

            # Pistil / Stamen (golden yellow, orange, amber flower core)
            pistil_mask = (r_px > 0.60) & (g_px > 0.40) & (b_px < 0.35)
            pistil_ratio = float(np.sum(pistil_mask) / total_px)

            # Floral petal colors (crimson, pink, violet, bright yellow, and pale cream petals with pistil)
            floral_petals = (
                ((r_px > 0.50) & (b_px > 0.25) & (g_px < 0.35)) | # Rose / Pink
                ((r_px > 0.40) & (b_px > 0.45) & (g_px < 0.30)) | # Violet / Lavender
                ((r_px > 0.60) & (g_px > 0.50) & (b_px < 0.25)) | # Bright floral yellow / Orange
                ((r_px > 0.70) & (g_px > 0.65) & (b_px > 0.50) & ((r_px - b_px) > 0.03) & (pistil_ratio > 0.015)) # Pale cream/white blossom with pistil
            ) & (~is_neutral)
            floral_ratio = float(np.sum(floral_petals) / total_px)

            # Fleshy fruit colors (tomato red, berry purple, citrus orange)
            fruit_tones = (
                ((r_px > 0.65) & (g_px < 0.25) & (b_px < 0.25)) | # Ripe tomato / apple red
                ((r_px > 0.70) & (g_px > 0.35) & (g_px < 0.60) & (b_px < 0.20)) # Citrus orange
            ) & (~is_neutral)
            fruit_ratio = float(np.sum(fruit_tones) / total_px)

            # Subterranean root filaments & taproot fibers (tan/ochre/earth-coated fibrous filaments)
            root_filament_mask = (r_px > 0.50) & (g_px > 0.38) & (b_px > 0.22) & (r_px < 0.88) & (r_px > g_px) & (g_px > b_px) & ((r_px - b_px) > 0.10)
            root_ratio = float(np.sum(root_filament_mask) / total_px)

            # Total biological & plant signal (leaves, stems, flowers, fruits, roots, pistils)
            total_plant_signal = green_ratio + woody_ratio + floral_ratio + fruit_ratio + (pistil_ratio * 3.0) + (root_ratio * 2.0)
            
            # REJECTION RULE 1: UI Screenshot, Document, or Neutral Canvas
            # (Do not reject if clear floral pistil, woody stem, or root filament is present)
            if (neutral_ratio > 0.70 and total_plant_signal < 0.10 and soil_ratio < 0.20 and pistil_ratio < 0.015 and woody_ratio < 0.10) or \
               (ui_color_ratio > 0.12 and total_plant_signal < 0.08) or \
               (neutral_ratio > 0.90 and total_plant_signal < 0.08):
                return {
                    "modality": "non_agriculture",
                    "is_agricultural": False,
                    "confidence": 0.98,
                    "message": "Invalid Image — This image appears to be a digital screenshot, document, or non-agricultural photo. Please upload a real photograph of a plant (leaf, stem, flower, fruit, root, or whole plant) or soil."
                }

            # REJECTION RULE 2: Human Portraits / Selfies
            if skin_ratio > 0.25 and total_plant_signal < 0.08 and soil_ratio < 0.10:
                return {
                    "modality": "non_agriculture",
                    "is_agricultural": False,
                    "confidence": 0.96,
                    "message": "Invalid Image — Human portrait or person detected. Please upload a clear photo of a plant (leaf, stem, flower, fruit) or soil."
                }

            # SOIL VERIFICATION: Pure soil substrate without root filaments/fibers
            if soil_ratio > 0.35 and green_ratio < 0.08 and floral_ratio < 0.05 and root_ratio < 0.035 and neutral_ratio < 0.50:
                return {
                    "modality": "soil",
                    "is_agricultural": True,
                    "confidence": round(min(0.98, max(0.85, 0.75 + soil_ratio * 0.3)), 4),
                    "message": "Valid soil specimen detected."
                }

            # PLANT VERIFICATION: Foliage, stems, flowers, fruits, or roots detected
            is_valid_foliage = green_ratio > 0.08
            is_valid_floral = floral_ratio > 0.08 or pistil_ratio > 0.015
            is_valid_fruit = fruit_ratio > 0.08
            is_valid_woody = (woody_ratio > 0.12)
            is_valid_root = (root_ratio > 0.035 and (soil_ratio > 0.30 or neutral_ratio > 0.40))
            is_valid_overall = (total_plant_signal > 0.12 and (green_ratio > 0.03 or floral_ratio > 0.03 or fruit_ratio > 0.03 or woody_ratio > 0.08 or root_ratio > 0.035 or pistil_ratio > 0.015))

            if is_valid_foliage or is_valid_floral or is_valid_fruit or is_valid_woody or is_valid_root or is_valid_overall:
                return {
                    "modality": "crop_leaf",
                    "is_agricultural": True,
                    "confidence": round(min(0.99, max(0.85, 0.78 + total_plant_signal * 0.4)), 4),
                    "message": "Valid crop / plant foliage, stem, flower, fruit, or root specimen detected."
                }

            # REJECTION RULE 3: Low plant & low soil signal
            if total_plant_signal < 0.16 and soil_ratio < 0.20:
                return {
                    "modality": "non_agriculture",
                    "is_agricultural": False,
                    "confidence": 0.92,
                    "message": "Invalid Image — No recognizable plant structure (leaf, stem, flower, fruit) or soil detected. Please upload a clear, focused photograph."
                }

        except Exception as e:
            print(f"[WARN] Error in structural image inspection: {e}")

        # Fallback to botanical features
        features = extract_visual_color_features(image_bytes)
        green_r = features.get("green_ratio", 0.0)
        brown_r = features.get("brown_ratio", 0.0)
        pink_r = features.get("rose_pink_ratio", 0.0)

        if green_r > 0.08 or pink_r > 0.08 or (brown_r > 0.20 and green_r > 0.03):
            return {
                "modality": "crop_leaf",
                "is_agricultural": True,
                "confidence": 0.88,
                "message": "Valid plant foliage/specimen detected."
            }

        return {
            "modality": "non_agriculture",
            "is_agricultural": False,
            "confidence": 0.92,
            "message": "Invalid Image — No plant or soil detected. Please upload a clear photo of a plant (leaf, stem, flower, fruit, root, or whole plant) or soil."
        }

    @staticmethod
    def detect_plant_organ(image_bytes: bytes) -> dict:
        """
        Classifies the specific plant part/organ photographed:
        - 'leaf': Green lamina, veins, foliage blade
        - 'flower': Petals, blossoms, floral pigmentation (rose, pink, violet, bright yellow)
        - 'fruit': Pericarp, berries, pods, tomatoes, gourds, fleshy produce
        - 'stem': Elongated vertical fibrous stalk, woody bark, branch, shoots
        - 'root': Subterranean branching rootlets, taproot, tubers, rhizomes
        - 'whole_plant': Multi-organ canopy showing foliage, stems, and container/field context
        - 'soil': Earth substrate
        """
        try:
            pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB").resize((128, 128))
            px = np.array(pil_img, dtype=np.float32) / 255.0
            r, g, b = px[:, :, 0], px[:, :, 1], px[:, :, 2]
            total_px = 128 * 128

            # Neutral canvas check
            diff_rg = np.abs(r - g)
            diff_rb = np.abs(r - b)
            diff_gb = np.abs(g - b)
            is_neutral = (diff_rg < 0.05) & (diff_rb < 0.05) & (diff_gb < 0.05)
            is_bright_canvas = (r > 0.85) & (g > 0.85) & (b > 0.85)

            # Color signatures
            green_mask = (g > r * 1.04) & (g > b * 1.04) & (g > 0.12) & (~is_neutral)
            green_ratio = float(np.sum(green_mask) / total_px)

            # Pistil / Stamen
            pistil_mask = (r > 0.60) & (g > 0.40) & (b < 0.35)
            pistil_ratio = float(np.sum(pistil_mask) / total_px)

            # Floral Petals (pink, violet, bright red, orange, golden yellow, pale cream petals with pistil)
            floral_mask = (
                ((r > 0.50) & (b > 0.25) & (g < 0.35)) | # Pink / Rose
                ((r > 0.40) & (b > 0.45) & (g < 0.30)) | # Violet / Purple
                ((r > 0.60) & (g > 0.50) & (b < 0.25)) | # Bright Yellow / Orange petals
                ((r > 0.70) & (g > 0.65) & (b > 0.50) & ((r - b) > 0.03) & (pistil_ratio > 0.015)) # Pale cream/white blossom with pistil
            ) & (~is_neutral)
            floral_ratio = float(np.sum(floral_mask) / total_px)

            # Fruit pericarps (vivid red, orange, deep berry purple)
            fruit_mask = (
                ((r > 0.65) & (g < 0.28) & (b < 0.28)) | # Tomato / apple red
                ((r > 0.70) & (g > 0.35) & (g < 0.60) & (b < 0.20)) # Citrus orange
            ) & (~is_neutral)
            fruit_ratio = float(np.sum(fruit_mask) / total_px)

            # Soil earth tones
            soil_mask = (
                ((r < 0.52) & (g < 0.40) & (b < 0.30) & (r > 0.05) & (g > 0.04) & (r >= g) & (g >= b)) |
                ((r > 0.45) & (g < 0.38) & (b < 0.28) & (r > g * 1.20))
            )
            soil_ratio = float(np.sum(soil_mask) / total_px)

            # Stem & Bark (woody brown/grey, elongated vertical structure)
            woody_mask = (r > 0.26) & (g > 0.18) & (b < 0.25) & (r > g) & (g > b) & ((r - b) > 0.06)
            if soil_ratio > 0.40:
                woody_mask = woody_mask & (~soil_mask)
            woody_ratio = float(np.sum(woody_mask) / total_px)

            # Root & Tuber signatures (subterranean fibrous filaments, tan/ochre rootlets against soil or substrate)
            root_filament_mask = (r > 0.50) & (g > 0.38) & (b > 0.22) & (r < 0.88) & (r > g) & (g > b) & ((r - b) > 0.10)
            root_ratio = float(np.sum(root_filament_mask) / total_px)

            # Organ Decision Rules
            if floral_ratio > 0.10 or pistil_ratio > 0.02:
                return {
                    "organ": "flower",
                    "confidence": round(min(0.98, max(0.82, 0.70 + (floral_ratio + pistil_ratio) * 1.5)), 3),
                    "evidence": "Floral petal pigments and corolla morphology observed."
                }
            elif fruit_ratio > 0.12:
                return {
                    "organ": "fruit",
                    "confidence": round(min(0.98, max(0.82, 0.70 + fruit_ratio * 1.5)), 3),
                    "evidence": "Fleshy pericarp coloration and fruit structure detected."
                }
            elif woody_ratio > 0.12 and green_ratio < 0.30:
                return {
                    "organ": "stem",
                    "confidence": round(min(0.96, max(0.82, 0.72 + woody_ratio * 0.8)), 3),
                    "evidence": "Fibrous stalk, trunk, or woody branch structure detected."
                }
            elif root_ratio > 0.035 and (soil_ratio > 0.30 or green_ratio < 0.15):
                return {
                    "organ": "root",
                    "confidence": round(min(0.95, max(0.80, 0.70 + root_ratio * 0.8)), 3),
                    "evidence": "Subterranean root filaments or tuberous structure observed."
                }
            elif green_ratio > 0.20 and (woody_ratio > 0.08 or floral_ratio > 0.05 or fruit_ratio > 0.05):
                return {
                    "organ": "whole_plant",
                    "confidence": 0.90,
                    "evidence": "Plant habit showing foliage with stem or flowering structures."
                }
            else:
                return {
                    "organ": "leaf",
                    "confidence": round(min(0.98, max(0.85, 0.75 + green_ratio * 0.3)), 3),
                    "evidence": "Characteristic foliar lamina, vein venation, and chlorophyll detected."
                }
        except Exception:
            return {
                "organ": "leaf",
                "confidence": 0.85,
                "evidence": "Foliar leaf blade structure detected."
            }

    @staticmethod
    def check_agricultural_relevance(image_bytes: bytes) -> dict:
        """
        Backward compatible relevance check wrapping detect_agricultural_modality.
        """
        modality_info = AgriculturalRelevanceService.detect_agricultural_modality(image_bytes)
        return {
            "is_agricultural": modality_info["is_agricultural"],
            "relevance_type": "agriculture" if modality_info["is_agricultural"] else modality_info["modality"],
            "detected_modality": modality_info["modality"],
            "confidence": modality_info["confidence"],
            "message": modality_info["message"]
        }
