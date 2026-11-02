"""
AGRO AI — Advanced Allergy, Intolerance & Restriction Filtering Service
Ensures zero-leakage dietary safety across meals, dishes, compound ingredients, and substitutions.
"""

import re
from typing import List, Dict, Any, Set, Tuple

# Comprehensive synonym and alias mapping for culinary contexts (Indian & International)
SYNONYM_MAP: Dict[str, List[str]] = {
    # Vegetables & Alliums
    "brinjal": ["brinjal", "eggplant", "aubergine", "baingan", "vangi"],
    "eggplant": ["brinjal", "eggplant", "aubergine", "baingan", "vangi"],
    "capsicum": ["capsicum", "bell pepper", "shimla mirch", "sweet pepper"],
    "bell pepper": ["capsicum", "bell pepper", "shimla mirch"],
    "mushroom": ["mushroom", "mushrooms", "khumbi", "button mushroom"],
    "mushrooms": ["mushroom", "mushrooms", "khumbi", "button mushroom"],
    "onion": ["onion", "onions", "pyaz", "shallot", "shallots", "scallion", "scallions", "spring onion"],
    "garlic": ["garlic", "lehsun", "garlic paste"],
    "potato": ["potato", "potatoes", "aloo", "batata"],
    "tomato": ["tomato", "tomatoes", "tamatar"],
    "coriander": ["coriander", "cilantro", "dhania"],
    "ginger": ["ginger", "adrak"],
    "cauliflower": ["cauliflower", "gobi", "gobhi"],
    "cabbage": ["cabbage", "patta gobhi", "bandhgobi"],
    "okra": ["okra", "bhindi", "ladyfinger", "lady's finger"],
    "spinach": ["spinach", "palak"],
    "fenugreek": ["fenugreek", "methi"],
    "bottle gourd": ["bottle gourd", "lauki", "doodhi", "ghiya"],
    "lauki": ["bottle gourd", "lauki", "doodhi", "ghiya"],
    "ridge gourd": ["ridge gourd", "turai", "tori"],
    "drumstick": ["drumstick", "moringa", "sahjan"],
    "corn": ["corn", "sweet corn", "maize", "makka"],
    "peas": ["peas", "green peas", "matar"],

    # Legumes & Pulses
    "peanut": ["peanut", "peanuts", "groundnut", "groundnuts", "moongfali", "singdana"],
    "peanuts": ["peanut", "peanuts", "groundnut", "groundnuts", "moongfali", "singdana"],
    "chickpea": ["chickpea", "chickpeas", "chana", "garbanzo", "besan", "sattu", "kala chana", "kabuli chana"],
    "soy": ["soy", "soya", "tofu", "edamame", "soybean", "soybeans", "soya milk", "soya chunks"],
    "soya": ["soy", "soya", "tofu", "edamame", "soybean", "soybeans", "soya milk", "soya chunks"],
    "lentil": ["lentil", "lentils", "dal", "daal", "dhal", "toor", "moong", "masoor", "urad"],

    # Dairy & Lactose
    "dairy": ["dairy", "milk", "curd", "dahi", "paneer", "ghee", "butter", "cheese", "yogurt", "buttermilk", "chaas", "whey", "casein", "malai", "khoya", "mawa"],
    "milk": ["milk", "dairy", "cow milk", "buffalo milk"],
    "curd": ["curd", "dahi", "yogurt", "buttermilk", "chaas", "dairy"],
    "paneer": ["paneer", "cottage cheese", "dairy", "chenna"],
    "ghee": ["ghee", "desi ghee", "cow ghee", "clarified butter", "dairy"],
    "lactose": ["dairy", "milk", "curd", "dahi", "paneer", "cheese", "whey", "lactose"],

    # Gluten & Grains
    "gluten": ["gluten", "wheat", "atta", "maida", "suji", "semolina", "bread", "roti", "phulka", "paratha", "seviyan", "barley", "rye"],
    "wheat": ["wheat", "gluten", "atta", "maida", "suji", "semolina", "bread", "roti", "phulka", "paratha"],

    # Eggs, Poultry & Meat
    "egg": ["egg", "eggs", "anda", "albumen", "scramble", "bhurji", "omelette"],
    "eggs": ["egg", "eggs", "anda", "albumen", "scramble", "bhurji", "omelette"],
    "chicken": ["chicken", "poultry", "murg", "murgh"],
    "meat": ["meat", "chicken", "poultry", "mutton", "lamb", "beef", "pork"],

    # Seafood
    "seafood": ["seafood", "fish", "prawn", "prawns", "shrimp", "shrimps", "crab", "crabs", "salmon", "rohu", "shellfish", "basa"],
    "fish": ["fish", "seafood", "salmon", "rohu", "basa", "pomfret", "surmai"],
    "shellfish": ["shellfish", "prawn", "prawns", "shrimp", "crab", "lobster", "seafood"],

    # Nuts & Seeds
    "tree_nuts": ["tree_nuts", "almond", "almonds", "walnut", "walnuts", "cashew", "cashews", "kaju", "badam", "akhrot", "pista", "pistachio", "hazelnut"],
    "almond": ["almond", "almonds", "badam", "tree_nuts"],
    "almonds": ["almond", "almonds", "badam", "tree_nuts"],
    "walnut": ["walnut", "walnuts", "akhrot", "tree_nuts"],
    "walnuts": ["walnut", "walnuts", "akhrot", "tree_nuts"],
    "cashew": ["cashew", "cashews", "kaju", "tree_nuts"],
    "cashews": ["cashew", "cashews", "kaju", "tree_nuts"],
    "coconut": ["coconut", "nariyal", "malai", "coconut oil", "coconut milk"],
    "sesame": ["sesame", "til", "tahini", "sesame oil"],
    "mustard": ["mustard", "sarson", "rai", "mustard oil", "mustard seeds"],
}

class AllergyFilterService:
    @staticmethod
    def parse_custom_allergies(raw_text: str) -> List[str]:
        """
        Parses comma-, semicolon-, or newline-separated free-text allergies into normalized tokens.
        """
        if not raw_text:
            return []

        tokens = re.split(r'[,;\n/]+', raw_text)
        cleaned = []
        for t in tokens:
            norm = t.strip().lower()
            # Remove leading/trailing non-alphanumeric
            norm = re.sub(r'^[^\w]+|[^\w]+$', '', norm)
            if norm and len(norm) > 1:
                cleaned.append(norm)
        return list(dict.fromkeys(cleaned))

    @staticmethod
    def expand_tokens_with_synonyms(tokens: List[str]) -> Set[str]:
        """
        Expands allergen tokens using the verified synonym map.
        """
        expanded = set()
        for tok in tokens:
            norm_tok = tok.lower().strip()
            if not norm_tok:
                continue
            expanded.add(norm_tok)
            # Add singular / plural variations
            if norm_tok.endswith("s") and len(norm_tok) > 3:
                expanded.add(norm_tok[:-1])
            else:
                expanded.add(norm_tok + "s")

            # Check direct match in synonym map
            for key, syns in SYNONYM_MAP.items():
                if norm_tok == key or norm_tok in syns:
                    expanded.update(syns)
        return expanded

    @staticmethod
    def _text_matches_token(text: str, token: str) -> bool:
        """
        Checks whether token appears in text as a whole word or boundary-bounded phrase,
        preventing false substring matches (e.g. 'egg' in 'veggie' or 'pea' in 'peanuts').
        """
        if not text or not token:
            return False
        text_lower = text.lower()
        token_lower = token.lower().strip()

        # Build regex matching word boundaries
        pattern = r'(?<![a-z0-9])' + re.escape(token_lower) + r'(?![a-z0-9])'
        return bool(re.search(pattern, text_lower))

    @staticmethod
    def is_food_compliant(
        food: Dict[str, Any],
        food_preference: str,
        allergies: List[str],
        custom_allergies_text: str = "",
        intolerances: List[str] = None,
        dietary_focus: List[str] = None
    ) -> Tuple[bool, str]:
        """
        Validates if a food item complies with dietary preference, common allergens,
        free-text custom allergies, intolerances, and strict cultural rules (e.g., Jain).
        Returns (is_compliant, reason_if_not).
        """
        intolerances = [i.lower().strip() for i in (intolerances or [])]
        dietary_focus = [d.lower().strip() for d in (dietary_focus or [])]
        pref = (food_preference or "vegetarian").lower().strip()

        user_allergies = {a.lower().strip() for a in allergies if a}
        custom_tokens = AllergyFilterService.parse_custom_allergies(custom_allergies_text)
        all_excluded_tokens = AllergyFilterService.expand_tokens_with_synonyms(
            list(user_allergies.union(custom_tokens))
        )

        food_name = food.get("name", "")
        food_allergens = {a.lower().strip() for a in food.get("allergens", [])}
        ingredients = food.get("ingredients", [])

        is_veg = food.get("is_veg", food.get("isVegetarian", False))
        is_vegan = food.get("is_vegan", food.get("isVegan", False))
        is_jain = food.get("is_jain", food.get("isJain", False))
        is_pesca = food.get("is_pescatarian", food.get("isPescatarian", False)) or ("seafood" in food_allergens)

        # ---------------------------------------------------------------------
        # 1. Dietary Preference Check
        # ---------------------------------------------------------------------
        if pref == "vegan":
            if not is_vegan:
                return False, f"Dish '{food_name}' contains animal-derived ingredients (not vegan)."
        elif pref == "jain" or "jain" in dietary_focus:
            if not is_jain:
                return False, f"Dish '{food_name}' is not Jain-compliant (contains onion, garlic, or root tubers)."
        elif pref == "vegetarian":
            if not is_veg:
                return False, f"Dish '{food_name}' is not vegetarian."
        elif pref == "eggetarian":
            has_egg = "eggs" in food_allergens
            if not is_veg and not has_egg:
                return False, f"Dish '{food_name}' contains meat or seafood."
            if "seafood" in food_allergens or is_pesca:
                return False, f"Dish '{food_name}' contains seafood."
        elif pref == "pescatarian":
            if not is_veg and not is_pesca:
                return False, f"Dish '{food_name}' contains meat or poultry."

        # ---------------------------------------------------------------------
        # 2. Strict Standard Declared Allergens Check
        # ---------------------------------------------------------------------
        for alg in user_allergies:
            if alg in food_allergens:
                return False, f"Dish '{food_name}' contains declared allergen '{alg}'."
            # Also check synonyms in food allergens
            for syn in SYNONYM_MAP.get(alg, []):
                if syn in food_allergens:
                    return False, f"Dish '{food_name}' contains declared allergen '{alg}' (matched tag '{syn}')."

        # ---------------------------------------------------------------------
        # 3. Dietary Focus & Intolerances Specific Exclusions
        # ---------------------------------------------------------------------
        # Dairy / Lactose
        if any(x in dietary_focus for x in ["dairy_free", "lactose_free"]) or "lactose" in intolerances:
            if "dairy" in food_allergens or not is_vegan:
                for ing in ingredients:
                    if "dairy" in [a.lower() for a in ing.get("allergens", [])]:
                        return False, f"Dish '{food_name}' contains dairy ingredient '{ing.get('name')}'."
            # If dish is not vegan and has dairy allergen
            if "dairy" in food_allergens:
                return False, f"Dish '{food_name}' contains dairy."

        # Gluten
        if "gluten_free" in dietary_focus or "gluten" in intolerances:
            if "gluten" in food_allergens:
                return False, f"Dish '{food_name}' contains gluten."

        # Eggs
        if "egg_free" in dietary_focus:
            if "eggs" in food_allergens:
                return False, f"Dish '{food_name}' contains eggs."

        # ---------------------------------------------------------------------
        # 4. Ingredient-Level & Custom Free-Text Check (with exact boundary matching)
        # ---------------------------------------------------------------------
        for token in all_excluded_tokens:
            if not token or len(token) < 2:
                continue

            # Check dish name
            if AllergyFilterService._text_matches_token(food_name, token):
                return False, f"Dish '{food_name}' matches excluded food '{token}'."

            # Check each individual ingredient
            for ing in ingredients:
                ing_name = ing.get("name", "")
                ing_allergens = [a.lower().strip() for a in ing.get("allergens", [])]

                if AllergyFilterService._text_matches_token(ing_name, token):
                    return False, f"Dish '{food_name}' contains excluded ingredient '{ing_name}' (matched '{token}')."

                if token in ing_allergens:
                    return False, f"Dish '{food_name}' contains excluded allergen '{token}' in ingredient '{ing_name}'."

        return True, ""

    @staticmethod
    def filter_safe_foods(
        foods: List[Dict[str, Any]],
        food_preference: str,
        allergies: List[str],
        custom_allergies_text: str = "",
        intolerances: List[str] = None,
        dietary_focus: List[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Filters a collection of foods, returning only those that satisfy all exclusion criteria.
        """
        safe_list = []
        for food in foods:
            compliant, _ = AllergyFilterService.is_food_compliant(
                food=food,
                food_preference=food_preference,
                allergies=allergies,
                custom_allergies_text=custom_allergies_text,
                intolerances=intolerances,
                dietary_focus=dietary_focus
            )
            if compliant:
                safe_list.append(food)
        return safe_list

    @staticmethod
    def contains_disliked_food(food: Dict[str, Any], disliked_foods_text: str) -> Tuple[bool, str]:
        """
        Checks whether a dish or any of its constituent ingredients matches the user's
        specified disliked foods or ingredients.
        Returns (contains_disliked, matched_item_name).
        """
        if not disliked_foods_text or not disliked_foods_text.strip():
            return False, ""

        tokens = AllergyFilterService.parse_custom_allergies(disliked_foods_text)
        expanded_tokens = AllergyFilterService.expand_tokens_with_synonyms(tokens)

        food_name = food.get("name", "")
        ingredients = food.get("ingredients", [])

        for token in expanded_tokens:
            if not token or len(token) < 2:
                continue
            if AllergyFilterService._text_matches_token(food_name, token):
                return True, food_name
            for ing in ingredients:
                ing_name = ing.get("name", "")
                if AllergyFilterService._text_matches_token(ing_name, token):
                    return True, ing_name

        return False, ""

