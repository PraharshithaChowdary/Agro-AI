# -*- coding: utf-8 -*-
"""
AGRO AI — Soil Classification & Agronomic Inference Service
Contains comprehensive knowledge base covering all 12 ICAR Indian Soil Classifications
(Alluvial, Black Cotton / Regur, Red Soil, Yellow Soil, Laterite Soil, Arid & Desert Soil,
Saline & Alkaline / Usar, Peaty & Marshy / Kari, Mountain & Forest Soil, Clay Loam, Sandy Loam, Tarai Soil).
Performs visual soil color, texture, and grain analysis, matches Indian geographical soil groups,
and provides verified Indian crop suitability matrices, soil health management amendments, and fertilizer guidance.
"""

import json
import datetime
from typing import Dict, Any, List
import numpy as np
from app.ml.model_loader import model_registry
from app.ml.preprocessing import (
    load_and_preprocess_image,
    extract_visual_color_features,
    extract_botanical_feature_vector
)

# ===========================================================================
# 12 ICAR INDIAN SOIL CLASSIFICATION & AGRONOMIC KNOWLEDGE BASE
# ===========================================================================
SOIL_KNOWLEDGE_BASE: Dict[str, Dict[str, Any]] = json.loads("""{"Alluvial Soil (Khadar & Bhangar)": {"category": "Alluvial Soil (Khadar - New Silt / Bhangar - Old Clay Loam)", "hindi_name": "जलोढ़ मिट्टी (खादर एवं बांगर)", "geography": "Indo-Gangetic-Brahmaputra plains (Punjab, Haryana, UP, Bihar, WB, Assam, Coastal Deltas of Godavari, Krishna, Mahanadi, Kaveri)", "coverage_india": "45.6% of total geographical area (143 million hectares - Largest soil group)", "pH_range": "6.5 – 8.0 (Neutral to slightly alkaline)", "visual_observations": ["Fine-textured, friable loamy to silty clay grain structure with light grey to yellowish-brown hue.", "High silt content with balanced natural moisture retention and porous capillary aeration.", "Smooth crumb structure indicative of riverine or flood-plain sedimentary deposition."], "suitable_crops": ["Rice / Paddy (Dhan)", "Wheat (Gehun)", "Sugarcane (Ganna)", "Maize / Corn", "Jute (Patson)", "Pulses (Chickpea, Lentil, Pigeon Pea)", "Oilseeds (Mustard, Sesame)", "Vegetables (Potato, Onion, Cauliflower, Tomato)"], "soil_improvement": ["Incorporate seasoned farmyard manure (FYM @ 10 t/ha) or vermicompost to maintain microbial vitality.", "Practice green manuring with Dhaincha (Sesbania aculeata) or Sunn hemp before paddy transplanting.", "Maintain laser land leveling and optimum surface tilling to prevent silt crusting after heavy rains."], "fertilizer_guidance": ["Alluvial soils are rich in Potash and Lime but deficient in Nitrogen and Organic Phosphorus.", "Apply split applications of Urea/Neem-coated nitrogen to avoid leaching in porous sandy-loam tracts.", "Supplement 25 kg/ha Zinc Sulfate in intensive rice-wheat cropping sequences."], "disclaimer": "Visual assessment indicates Alluvial Loam characteristics. Physical color and texture cannot substitute for certified chemical laboratory analysis of available Nitrogen, Phosphorus, Potassium, or micronutrients."}, "Black Cotton Soil (Regur / Vertisol)": {"category": "Black Cotton Soil (Regur / Vertisol / Deccan Lava Basalt)", "hindi_name": "काली मिट्टी / रेगुर मिट्टी (कपास की मिट्टी)", "geography": "Deccan Lava Plateau (Maharashtra, Gujarat, Madhya Pradesh, Karnataka, Telangana, Northern Andhra Pradesh)", "coverage_india": "16.6% of total geographical area (54.6 million hectares)", "pH_range": "7.5 – 8.5 (Mildly to moderately alkaline)", "visual_observations": ["Deep dark brown to charcoal black coloration with high montmorillonite clay matrix density (>40% clay).", "Distinct surface self-ploughing micro-fissures and swelling/cracking patterns upon drying in hot summer.", "Extremely high moisture retention capacity with sticky, plastic, and unworkable texture when wet."], "suitable_crops": ["Cotton (Kapas / White Gold)", "Soybean (Soyabean)", "Sorghum (Jowar)", "Pigeon Pea (Arhar / Toor)", "Chickpea (Chana)", "Sunflower (Surajmukhi)", "Sugarcane (Ganna)", "Citrus (Nagpur Santra, Mosambi)", "Onion & Garlic"], "soil_improvement": ["Improve internal subsoil drainage channels and Broad Bed Furrows (BBF) to prevent monsoon root asphyxiation.", "Apply agricultural gypsum (calcium sulfate @ 2–5 t/ha) if high sodium dispersion or clay sodicity is observed.", "Incorporate coarse organic compost, pressmud, or crop stubble to improve soil friability and workability."], "fertilizer_guidance": ["Vertisols have high Calcium, Magnesium, and Carbonates but poor Nitrogen, Phosphorus, and Zinc.", "Band-place phosphatic fertilizers (SSP/DAP) close to root zones to prevent high phosphorus fixation.", "Apply nitrogen in timed split applications aligned with crop vegetative growth."], "disclaimer": "Visual assessment indicates Vertisol/Black Soil characteristics. Accurate chemical indices (organic carbon %, available P2O5, exchangeable K) require laboratory soil testing."}, "Red Soil (Alfisols / Ferruginous Loam)": {"category": "Red Soil (Alfisols / Ferruginous Sandy-Clay Loam)", "hindi_name": "लाल मिट्टी", "geography": "Tamil Nadu, Karnataka, Southern Andhra Pradesh, Telangana, Odisha, Eastern Madhya Pradesh, Jharkhand, Chhota Nagpur", "coverage_india": "18.5% of total geographical area (61 million hectares)", "pH_range": "5.5 – 7.0 (Slightly acidic to neutral)", "visual_observations": ["Prominent reddish-brown to warm terra cotta color derived from oxidized ferric iron diffusion.", "Light to medium coarse sandy-clay loam texture with rapid water permeability and porous structure.", "Non-retentive granular consistency with low natural water-holding capacity and high drainage."], "suitable_crops": ["Groundnut / Peanut (Mungfali)", "Finger Millet (Ragi / Mandua)", "Pearl Millet (Bajra)", "Pulses (Pigeon Pea, Green Gram, Horse Gram)", "Castor (Arandi)", "Tobacco", "Potato & Sweet Potato", "Cashew Nut & Mango"], "soil_improvement": ["Apply substantial doses of organic mulch (crop residue, dry grass) to conserve moisture in porous root zones.", "Incorporate biochar, vermicompost, and tank silt (pond sediment) to build cation exchange capacity and water holding.", "Adopt contour bunding, vetiver hedge barriers, and trenches to prevent topsoil erosion on slopes."], "fertilizer_guidance": ["Red soils have low native Nitrogen, Phosphorus, and Humus; apply organic compost generously (10 t/ha).", "Phosphorus is easily fixed by iron/aluminium oxides; utilize Single Super Phosphate (SSP) with organic manure.", "Provide balanced potassium and micronutrients (Boron & Zinc) for legume nodulation and oilseed filling."], "disclaimer": "Visual assessment indicates Ferruginous Red Soil. Accurate pH, lime requirement, and nutrient availability must be determined through certified lab analysis."}, "Yellow Soil (Hydrated Red Soil)": {"category": "Yellow Soil (Hydrated Ferric Oxide Alfisol / Ultisol)", "hindi_name": "पीली मिट्टी (जलयोजित लाल मिट्टी)", "geography": "Parts of Odisha, Chhattisgarh (Mahanadi river basin), Eastern MP, Jharkhand, parts of Western Ghats", "coverage_india": "Combined with Red Soil group across high rainfall valleys", "pH_range": "5.0 – 6.5 (Moderately acidic)", "visual_observations": ["Warm yellowish-ochre to golden-tan coloration resulting from hydration of iron oxides (Limonite / Goethite).", "Fine sandy loam to silty clay texture located typically in river valley bottoms and foot-slopes.", "Moderate water retention capacity with high leaching in upper topsoil layers."], "suitable_crops": ["Rice / Paddy (Dhan)", "Maize (Makka)", "Millets (Kodo, Kutki)", "Pulses (Urad, Moong, Kulthi)", "Oilseeds (Sesame, Niger seed)", "Vegetables"], "soil_improvement": ["Apply agricultural lime (calcium carbonate @ 1–2 t/ha) to neutralize subsoil acidity.", "Incorporate green manure crops and well-decomposed farmyard manure.", "Construct field bunds for rainwater harvesting and soil moisture conservation."], "fertilizer_guidance": ["Deficient in Nitrogen, Phosphorus, and Organic Carbon; moderate in Potash.", "Use Rock Phosphate or SSP along with mycorrhizal biofertilizers (VAM) to enhance phosphorus solubility."], "disclaimer": "Visual assessment indicates Hydrated Yellow Loam. Soil laboratory test required for exact exchangeable acidity and NPK levels."}, "Laterite Soil (Oxisols / Leached Earth)": {"category": "Laterite Soil (Oxisols / Ultisols / Tropical Leached Earth)", "hindi_name": "लैटेराइट मिट्टी / ईंट जैसी मिट्टी", "geography": "High rainfall belts: Western Ghats (Kerala, Coastal Karnataka, Goa, Konkan Maharashtra), Eastern Ghats (Odisha), Meghalaya (Khasi-Jaintia hills), Assam", "coverage_india": "7.2% of geographical area (24 million hectares)", "pH_range": "4.5 – 5.8 (Strongly acidic)", "visual_observations": ["Coarse, vesicular, porous brick-red to yellowish honeycomb nodular iron-aluminum oxide structure.", "Highly leached physical consistency resulting from alternating intense tropical monsoon rainfall and dry heat.", "Low water holding capacity with acidic, nutrient-depleted topsoil appearance."], "suitable_crops": ["Tea (Chai)", "Coffee (Arabica & Robusta)", "Natural Rubber (Hevea)", "Cashew Nut (Kaju)", "Areca Nut (Supari)", "Black Pepper (Kali Mirch)", "Cardamom (Elaichi)", "Pineapple & Tapioca (Cassava)", "Coconut"], "soil_improvement": ["Apply agricultural lime (CaCO3) or dolomite (2–3 t/ha once in 3 years) to correct severe soil acidity.", "Apply heavy organic mulch (coir pith, leaf mulch @ 10 t/ha) to protect soil from torrential monsoon sheet erosion.", "Incorporate biochar and composted farmyard manure to build nutrient holding capacity."], "fertilizer_guidance": ["Laterites have high Phosphorus-fixation capacity due to active Aluminum and Iron oxides.", "Apply Rock Phosphate or DAP mixed with organic compost (phosphate-enriched compost) directly into root zones.", "Supplement with Magnesium, Calcium, and micronutrients (Molybdenum and Boron)."], "disclaimer": "Visual assessment indicates Lateritic Oxisol. Accurate soil acidity (pH), buffer capacity, and lime requirement must be confirmed via laboratory analysis."}, "Arid & Desert Soil (Torripsamments / Entisols)": {"category": "Arid & Desert Soil (Aridisols / Sandy Dunes / Desert Sand)", "hindi_name": "मरुस्थलीय / शुष्क रेतीली मिट्टी", "geography": "Thar Desert (Western Rajasthan - Jaisalmer, Barmer, Bikaner, Jodhpur), Southern Punjab, Southern Haryana, Rann of Kutch (Gujarat)", "coverage_india": "8.4% of geographical area (29 million hectares)", "pH_range": "7.5 – 8.8 (Moderately to strongly alkaline)", "visual_observations": ["Light yellowish-brown to sandy buff color with coarse, loose, non-coherent sand grain matrix (>85% sand).", "Very high infiltration rate (>15 cm/hr) with near-zero moisture holding capacity.", "Surface crusting with high soluble salt deposits in depressions."], "suitable_crops": ["Pearl Millet (Bajra)", "Cluster Bean / Guar (Gwar Phali)", "Moth Bean (Matki)", "Mustard & Rapeseed (Sarson)", "Castor (Arandi)", "Cumin (Jeera)", "Isabgol (Psyllium Husk)", "Date Palm (Khajur)", "Ber / Indian Jujube"], "soil_improvement": ["Adopt pressurized Drip and Micro-sprinkler irrigation systems to supply water directly to root zones without percolation losses.", "Incorporate bentonite clay (pond silt) and vermicompost to create an artificial moisture-retentive subsoil barrier.", "Plant shelterbelts of drought-hardy trees (Khejri - Prosopis cineraria, Acacia) to arrest sand dune shifting."], "fertilizer_guidance": ["Extremely deficient in Nitrogen and Organic Humus; moderate to high in Potassium and Soluble Phosphates.", "Apply Nitrogen through fertigation in small frequent doses to prevent leaching through porous sand.", "Supplement with Zinc and Iron chelate sprays for horticultural crops."], "disclaimer": "Visual assessment indicates Arid Sandy Soil. Salinity (ECe), SAR, and boron toxicity should be evaluated through laboratory testing."}, "Saline & Alkaline Soil (Usar / Reh / Kallar)": {"category": "Saline & Sodic Alkaline Soil (Halomorphic / Usar / Reh / Kallar)", "hindi_name": "लवणीय एवं क्षारीय मिट्टी (ऊसर / रेह / कल्लर)", "geography": "Canal irrigated tracts of UP, Haryana, Punjab, Rajasthan, and coastal flats of Gujarat (Rann of Kutch) and Sunderbans", "coverage_india": "6.8 million hectares (Degraded problem soils)", "pH_range": "8.5 – 10.5 (Alkali/Sodic) or pH 7.0–8.2 with high EC > 4 dS/m (Saline)", "visual_observations": ["White, greyish-white, or ash-colored efflorescent salt encrustation (Reh) on the soil surface.", "Hard, compacted, dispersed subsoil structure with impermeable black alkali surface spots.", "Extremely poor drainage and surface water ponding after rain due to clay deflocculation."], "suitable_crops": ["Barley (Jau - highly salt tolerant)", "Salt-tolerant Rice varieties (CSR 10, CSR 36, Basmati CSR 30)", "Sugarbeet", "Cotton", "Spinach & Beetroot", "Bermuda Grass (Doob Ghas) & Karnal Grass (Leptochloa fusca)", "Subabul & Dhaincha"], "soil_improvement": ["Apply agricultural Gypsum (CaSO4.2H2O @ 5–15 t/ha based on Gypsum Requirement) followed by heavy flooding to replace sodium with calcium.", "Leach soluble salts out of root zones through deep subsurface drainage and open collector drains.", "Grow Dhaincha (Sesbania) as green manure and incorporate at 45 DAS to generate carbonic acid that dissolves native calcium carbonate."], "fertilizer_guidance": ["Apply 25% higher Nitrogen dose than normal soils (prefer Ammonium Sulfate over Urea).", "Apply 50 kg/ha Zinc Sulfate to overcome widespread Zinc deficiency caused by high pH.", "Incorporate organic pressmud and farmyard manure to improve physical structure."], "disclaimer": "Visual assessment indicates Saline/Alkaline Soil. Exact Gypsum Requirement (GR), Exchangeable Sodium Percentage (ESP), and EC must be tested in lab."}, "Peaty & Marshy Soil (Kari / Organic Muck)": {"category": "Peaty & Marshy Soil (Histosols / Kari / Wetland Organic Muck)", "hindi_name": "दलदली एवं जैविक मिट्टी (कारी मिट्टी)", "geography": "Kerala backwaters (Kuttanad & Alappuzha Kari soils), Sunderbans delta (WB), Coastal Odisha (Chilika), Tamil Nadu coastal wetlands", "coverage_india": "Wetland and estuarine ecosystems", "pH_range": "3.5 – 5.5 (Highly acidic with potential acid sulfate conditions)", "visual_observations": ["Deep black, dark brownish-grey water-saturated heavy spongy organic mass.", "High accumulation of un-decomposed organic matter and plant residues (>20–40% organic carbon).", "Strong sulfide/marsh odor with pyrite formation in subsoil horizons."], "suitable_crops": ["Deepwater Paddy / Rice (Pokkali & Kuttanad floating rice cultivars)", "Jute", "Taro / Colocasia (Arbi)", "Water Spinach & Aquatic Vegetables", "Mangrove Afforestation & Aquaculture"], "soil_improvement": ["Apply heavy lime (CaCO3 @ 3–5 t/ha) to counter toxic Aluminum, Iron, and Sulfuric acid flushes.", "Maintain controlled water drainage to wash away toxic iron salts before planting.", "Construct bunds with sluice gates (traditional Pokkali farming system: 1 season rice, 1 season shrimp)."], "fertilizer_guidance": ["Rich in organic matter and Nitrogen, but extremely deficient in available Phosphorus and Potash.", "Apply Rock Phosphate and Potassium Sulfate (SOP); avoid sulfur-containing fertilizers in acid sulfate soils."], "disclaimer": "Visual assessment indicates Peaty Marsh Soil. Laboratory analysis for potential acid sulfate (pyrite) and iron toxicity is essential."}, "Mountain & Forest Soil (Himalayan Humus)": {"category": "Mountain & Forest Soil (Inceptisols / Spodosols / Podzolic Humus)", "hindi_name": "पर्वतीय एवं वन मिट्टी (हिमालयी मिट्टी)", "geography": "Himalayan belt: Jammu & Kashmir, Ladakh, Himachal Pradesh, Uttarakhand, Sikkim, Arunachal Pradesh, High Western Ghats", "coverage_india": "8.7% of geographical area (28.5 million hectares)", "pH_range": "5.0 – 6.5 (Acidic under coniferous forest; neutral in broadleaf valleys)", "visual_observations": ["Dark brown to blackish forest topsoil rich in loose leaf litter and decomposed forest humus.", "Heterogeneous profile: stony, gravelly, shallow on ridges; deep and fertile in terraced river valleys.", "High biological activity with rich fungal mycorrhizae and earthworm casts."], "suitable_crops": ["Apple (Seb - Royal Delicious, Gala)", "Walnut & Almond (Akhrot & Badam)", "Peach, Plum, Cherry, Apricot", "Saffron (Kesar - Pampore Karewas of Kashmir)", "Potato & Kidney Bean (Rajma)", "Tea (Kangra & Darjeeling)", "Cardamom & Mountain Spices", "Off-season Temperate Vegetables"], "soil_improvement": ["Build stone-faced contour terrace risers to prevent catastrophic slope runoff and landslide erosion.", "Maintain permanent green ground cover (white clover, orchard grass) between fruit tree rows.", "Apply organic compost and retain forest leaf mulch (Oak/Deodar litter) to maintain topsoil moisture."], "fertilizer_guidance": ["Rich in organic Nitrogen and Humus; deficient in Phosphorus and Calcium.", "Apply bone meal, rock phosphate, and wood ash (natural potassium source) for temperate fruit trees."], "disclaimer": "Visual assessment indicates Mountain/Forest Soil. Topography, slope aspect, and depth vary sharply; laboratory test recommended."}, "Clay Loam Soil (River Valleys)": {"category": "Clay Loam Soil (Balanced Medium-Heavy Arable Soil)", "hindi_name": "चिकनी दोमट मिट्टी", "geography": "Cultivated river valleys, command areas of canal networks across central, northern, and southern India", "coverage_india": "Widespread across irrigated fertile agriculture zones", "pH_range": "6.5 – 7.5 (Optimal neutral range)", "visual_observations": ["Medium to dark brown crumbly soil with balanced 30–35% clay, 35% silt, and 30% sand.", "Excellent tilth when ploughed at optimum moisture (Vapsa condition).", "High nutrient holding capacity (CEC) with moderate to high water retention."], "suitable_crops": ["Rice & Wheat (Rice-Wheat cropping system)", "Sugarcane", "Cotton", "Pulses (Chickpea, Black Gram, Green Gram)", "Vegetables (Tomato, Brinjal, Cabbage, Cauliflower, Okra)", "Oilseeds (Mustard, Groundnut)"], "soil_improvement": ["Practice crop rotation between heavy feeders (cereal) and nitrogen fixers (legumes).", "Incorporate 5–10 t/ha vermicompost or FYM annually to prevent subsoil plow pan compaction.", "Avoid tilling when soil is excessively wet to prevent clod formation."], "fertilizer_guidance": ["Highly responsive to standard balanced NPK 4:2:1 fertilizer application.", "Maintain soil organic carbon >0.75% for optimum microbial enzyme activity."], "disclaimer": "Visual assessment indicates Clay Loam Soil. Comprehensive soil health card parameters require laboratory testing."}, "Sandy Loam Soil (Semi-Arid Plains)": {"category": "Sandy Loam Soil (Light Arable Alluvial Loam)", "hindi_name": "बलुई दोमट मिट्टी", "geography": "North-western plains (Punjab, Haryana, Western UP, Northern Rajasthan, Coastal Plains of AP and Tamil Nadu)", "coverage_india": "Extensive across irrigated plains and riverbanks", "pH_range": "6.5 – 7.8 (Near-neutral)", "visual_observations": ["Light greyish-brown to golden brown gritty friable texture with 60–70% sand and 15–20% clay.", "Easy to plough with rapid seed germination and unhindered root penetration.", "Good aeration with moderate drainage."], "suitable_crops": ["Wheat & Barley", "Maize & Pearl Millet (Bajra)", "Groundnut & Mustard", "Root Vegetables (Carrot, Radish, Turnip, Beetroot, Potato)", "Cucurbits (Watermelon, Muskmelon, Bottle Gourd, Cucumber)", "Pulses (Moong, Cowpea)"], "soil_improvement": ["Apply green manuring (Dhaincha) and FYM (10 t/ha) to build humus and water retention.", "Adopt drip irrigation or mulching to minimize rapid surface evaporation.", "Incorporate biochar to prevent nutrient leaching."], "fertilizer_guidance": ["Apply Nitrogen and Potassium in split applications (3–4 splits) to prevent leaching beyond the root zone.", "Supplement with Zinc and Sulfur for high-yielding oilseeds and vegetables."], "disclaimer": "Visual assessment indicates Sandy Loam Soil. Precise fertilizer recommendations require NPK laboratory testing."}, "Tarai & Sub-Montane Soil (Himalayan Foothills)": {"category": "Tarai & Bhabhar Soil (Sub-Montane Swampy & Coarse Alluvial)", "hindi_name": "तराई एवं भाबर मिट्टी", "geography": "Himalayan foothills belt (Northern UP, Uttarakhand - Pantnagar/Udham Singh Nagar, Northern Bihar, West Bengal Dooars)", "coverage_india": "Narrow sub-Himalayan strip (Highly productive agricultural zone)", "pH_range": "6.5 – 7.5 (Neutral)", "visual_observations": ["Deep, dark grey to black, moisture-rich alluvial loam with high natural organic nitrogen and humus.", "High groundwater table with natural seepage and wet moisture conditions.", "Coarse gravelly Bhabhar in northern edge transitioning to deep fertile silty-clay Tarai in south."], "suitable_crops": ["Sugarcane (Ganna - highest yield zone)", "Rice / Paddy (Dhan - Basmati & High Yielding)", "Wheat (Gehun)", "Jute", "Maize", "Poplar & Eucalyptus Agroforestry", "Mango & Litchi Orchards"], "soil_improvement": ["Maintain deep drainage channels to prevent waterlogging during monsoon.", "Adopt conservation tillage and agroforestry systems.", "Rotate high water-demanding crops with legumes."], "fertilizer_guidance": ["Naturally rich in organic Nitrogen; responsive to Phosphatic and Potassic fertilizers.", "Supplement with Zinc Sulfate (25 kg/ha) for high-yielding rice cultivars."], "disclaimer": "Visual assessment indicates Tarai Soil. Standard soil test recommended for micronutrient and drainage indices."}}""")

class SoilInferenceService:
    @staticmethod
    def get_all_soil_types() -> List[Dict[str, Any]]:
        """
        Returns structured list of all 12 ICAR Indian Soil types with descriptions,
        geographies, and crop suitability.
        """
        result = []
        for name, info in SOIL_KNOWLEDGE_BASE.items():
            result.append({
                "soilType": name,
                "category": info["category"],
                "hindiName": info.get("hindi_name", ""),
                "geography": info.get("geography", "Pan-India"),
                "coverageIndia": info.get("coverage_india", ""),
                "pHRange": info.get("pH_range", "6.5 - 7.5"),
                "suitableCrops": info["suitable_crops"],
                "visualObservations": info["visual_observations"],
                "soilImprovement": info["soil_improvement"],
                "fertilizerGuidance": info["fertilizer_guidance"]
            })
        return result

    @classmethod
    def analyze_soil_image(cls, image_bytes: bytes) -> Dict[str, Any]:
        """
        Analyzes uploaded soil photograph and categorizes across 12 Indian Soil groups.
        """
        color_feats = extract_visual_color_features(image_bytes)
        feature_vec = extract_botanical_feature_vector(image_bytes).reshape(1, -1)

        # 1. Try ML Model first if available
        predicted_category = None
        confidence = 0.0
        used_trained_feature_model = False

        soil_model = model_registry.get_model("soil_classifier")
        if soil_model:
            try:
                raw_pred = soil_model.predict(feature_vec)[0]
                probas = np.asarray(soil_model.predict_proba(feature_vec), dtype=np.float64).reshape(-1)
                probas = probas[np.isfinite(probas)]
                confidence = float(np.clip(np.max(probas), 0.0, 1.0)) if probas.size else 0.0
                used_trained_feature_model = True

                # Map model classes to Indian categories
                pred_clean = raw_pred.replace("_", " ").strip()
                if "Black" in pred_clean:
                    predicted_category = "Black Cotton Soil (Regur / Vertisol)"
                elif "Red" in pred_clean:
                    predicted_category = "Red Soil (Alfisols / Ferruginous Loam)"
                elif "Yellow" in pred_clean:
                    predicted_category = "Yellow Soil (Hydrated Red Soil)"
                elif "Laterite" in pred_clean:
                    predicted_category = "Laterite Soil (Oxisols / Leached Earth)"
                elif "Arid" in pred_clean or "Sand" in pred_clean:
                    predicted_category = "Arid & Desert Soil (Torripsamments / Entisols)"
                elif "Saline" in pred_clean or "Alkali" in pred_clean:
                    predicted_category = "Saline & Alkaline Soil (Usar / Reh / Kallar)"
                elif "Peat" in pred_clean or "Marsh" in pred_clean:
                    predicted_category = "Peaty & Marshy Soil (Kari / Organic Muck)"
                elif "Mountain" in pred_clean or "Forest" in pred_clean:
                    predicted_category = "Mountain & Forest Soil (Himalayan Humus)"
                elif "Clay" in pred_clean:
                    predicted_category = "Clay Loam Soil (River Valleys)"
                elif "Sandy Loam" in pred_clean:
                    predicted_category = "Sandy Loam Soil (Semi-Arid Plains)"
                else:
                    predicted_category = "Alluvial Soil (Khadar & Bhangar)"
            except Exception:
                pass

        # 2. Rule-Based Fallback using multi-channel color features
        if not predicted_category or predicted_category not in SOIL_KNOWLEDGE_BASE:
            brown = float(color_feats["brown_ratio"])
            red = float(color_feats["red_ratio"])
            yellow = float(color_feats["yellow_ratio"])
            white = float(color_feats["white_ratio"])
            brightness = float(color_feats["brightness"])

            if white > 0.22 and brightness > 160:
                predicted_category = "Saline & Alkaline Soil (Usar / Reh / Kallar)"
                confidence = 0.0
            elif brown < 0.15 and brightness < 70:
                predicted_category = "Black Cotton Soil (Regur / Vertisol)"
                confidence = 0.0
            elif red > 0.22 and brown > 0.18:
                predicted_category = "Red Soil (Alfisols / Ferruginous Loam)"
                confidence = 0.0
            elif red > 0.25 and brightness < 110:
                predicted_category = "Laterite Soil (Oxisols / Leached Earth)"
                confidence = 0.0
            elif yellow > 0.22 and brightness > 140:
                predicted_category = "Arid & Desert Soil (Torripsamments / Entisols)"
                confidence = 0.0
            elif yellow > 0.18 and red > 0.12:
                predicted_category = "Yellow Soil (Hydrated Red Soil)"
                confidence = 0.0
            elif brown > 0.28 and brightness < 90:
                predicted_category = "Mountain & Forest Soil (Himalayan Humus)"
                confidence = 0.0
            elif brown > 0.20 and brightness < 120:
                predicted_category = "Clay Loam Soil (River Valleys)"
                confidence = 0.0
            elif yellow > 0.14 and brightness > 130:
                predicted_category = "Sandy Loam Soil (Semi-Arid Plains)"
                confidence = 0.0
            else:
                predicted_category = "Alluvial Soil (Khadar & Bhangar)"
                confidence = 0.0

        soil_info = SOIL_KNOWLEDGE_BASE.get(predicted_category, SOIL_KNOWLEDGE_BASE["Alluvial Soil (Khadar & Bhangar)"])

        return {
            "isAgricultural": True,
            "predictedSoilCategory": soil_info["category"],
            "hindiName": soil_info.get("hindi_name", ""),
            "confidence": round(confidence, 2),
            "geography": soil_info.get("geography", ""),
            "coverageIndia": soil_info.get("coverage_india", ""),
            "pHRange": soil_info.get("pH_range", "6.5 - 7.5"),
            "visualObservations": soil_info["visual_observations"],
            "suitableCrops": soil_info["suitable_crops"],
            "soilImprovementGuidance": soil_info["soil_improvement"],
            "fertilizerGuidance": soil_info["fertilizer_guidance"],
            "limitationsDisclaimer": (
                soil_info["disclaimer"] + " Visual photographs cannot reliably establish soil pH, nutrient levels, "
                "salinity, or fertility. This archive does not contain an independently verified real-photo holdout "
                "benchmark for this model. Treat the category as a preliminary visual candidate and use a soil test "
                "before making lime, fertilizer, or other amendment decisions."
            ),
            "modelStatus": "unvalidated_feature_vector_screening" if used_trained_feature_model else "visual_rule_based_unvalidated",
            "analysisTimestamp": datetime.datetime.now().isoformat()
        }
