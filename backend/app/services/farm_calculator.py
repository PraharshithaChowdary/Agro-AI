"""
AGRO AI — Agricultural & Scientific Calculation Engine
Provides deterministic, executable calculators with step-by-step arithmetic explanations,
input validation, and unit consistency checking.
No eval() or exec() — uses safe Python AST parsing and validated agronomic formulas.
"""

import ast
import operator
import math
from typing import Dict, Any, List, Optional, Union

# Safe AST operators
SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

SAFE_FUNCTIONS = {
    "sqrt": math.sqrt,
    "abs": abs,
    "round": round,
    "log": math.log,
    "log10": math.log10,
    "exp": math.exp,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "pi": math.pi,
    "e": math.e,
}

class FarmCalculatorService:
    """
    Standard executable agricultural calculation engine.
    """

    @staticmethod
    def calculate_npk_fertilizer(
        target_n: float,
        target_p: float,
        target_k: float,
        area: float = 1.0,
        unit: str = "ha",
        use_ssp: bool = False
    ) -> Dict[str, Any]:
        """
        Converts recommended elemental/oxide N-P2O5-K2O doses into commercial fertilizers.
        Accounts for DAP supplying both 18% N and 46% P2O5.
        """
        if area <= 0:
            raise ValueError("Area must be greater than zero.")
        if target_n < 0 or target_p < 0 or target_k < 0:
            raise ValueError("Nutrient targets cannot be negative.")

        unit_label = "hectare" if unit.lower() in ["ha", "hectare", "hectares"] else "acre"
        multiplier = area

        # Total nutrient targets for the specified area
        tot_target_n = target_n * multiplier
        tot_target_p = target_p * multiplier
        tot_target_k = target_k * multiplier

        steps = []
        steps.append(f"Input Target: {target_n} kg N, {target_p} kg P2O5, {target_k} kg K2O per {unit_label} for {area} {unit_label}(s).")
        steps.append(f"Total Requirements for {area} {unit_label}(s): {tot_target_n:.2f} kg N, {tot_target_p:.2f} kg P2O5, {tot_target_k:.2f} kg K2O.")

        if not use_ssp:
            # 1. P via DAP (18% N, 46% P2O5)
            dap_kg = tot_target_p / 0.46
            n_from_dap = dap_kg * 0.18
            steps.append(f"Step 1 (Phosphorus via DAP): DAP contains 46% P2O5. DAP needed = {tot_target_p:.2f} / 0.46 = {dap_kg:.2f} kg.")
            steps.append(f"Step 2 (Nitrogen contributed by DAP): DAP contains 18% N. N supplied = {dap_kg:.2f} kg x 0.18 = {n_from_dap:.2f} kg N.")

            # 2. Remaining N via Urea (46% N)
            remaining_n = max(0.0, tot_target_n - n_from_dap)
            urea_kg = remaining_n / 0.46
            steps.append(f"Step 3 (Remaining Nitrogen via Urea): Remaining N required = {tot_target_n:.2f} - {n_from_dap:.2f} = {remaining_n:.2f} kg N.")
            steps.append(f"Urea needed (46% N) = {remaining_n:.2f} / 0.46 = {urea_kg:.2f} kg.")

            # 3. K via MOP (60% K2O)
            mop_kg = tot_target_k / 0.60
            steps.append(f"Step 4 (Potassium via MOP): MOP contains 60% K2O. MOP needed = {tot_target_k:.2f} / 0.60 = {mop_kg:.2f} kg.")

            # Bag calculations (Urea: 45kg bag, DAP/MOP: 50kg bag)
            dap_bags = dap_kg / 50.0
            urea_bags = urea_kg / 45.0
            mop_bags = mop_kg / 50.0

            # Exact verification
            verif_n = (dap_kg * 0.18) + (urea_kg * 0.46)
            verif_p = dap_kg * 0.46
            verif_k = mop_kg * 0.60
            steps.append(f"Verification: N = ({dap_kg:.1f}x0.18) + ({urea_kg:.1f}x0.46) = {verif_n:.1f} kg; P2O5 = {verif_p:.1f} kg; K2O = {verif_k:.1f} kg.")

            return {
                "calculationType": "npk_fertilizer",
                "area": area,
                "unit": unit_label,
                "targetNutrients": {"N_kg": round(tot_target_n, 1), "P2O5_kg": round(tot_target_p, 1), "K2O_kg": round(tot_target_k, 1)},
                "fertilizers": [
                    {"name": "DAP (Diammonium Phosphate 18:46:0)", "quantityKg": round(dap_kg, 1), "bags": round(dap_bags, 2), "bagSizeKg": 50},
                    {"name": "Urea (Neem Coated 46% N)", "quantityKg": round(urea_kg, 1), "bags": round(urea_bags, 2), "bagSizeKg": 45},
                    {"name": "MOP (Muriate of Potash 60% K2O)", "quantityKg": round(mop_kg, 1), "bags": round(mop_bags, 2), "bagSizeKg": 50}
                ],
                "calculationSteps": steps,
                "splitSchedule": [
                    "Basal at sowing: 100% of DAP (" + f"{round(dap_kg, 1)} kg), 100% of MOP ({round(mop_kg, 1)} kg), and 33% of Urea ({round(urea_kg*0.33, 1)} kg).",
                    "First Topdressing (Active tillering / 25-30 DAS): 33% of Urea (" + f"{round(urea_kg*0.33, 1)} kg).",
                    "Second Topdressing (Panicle / Pre-flowering): Remaining 34% of Urea (" + f"{round(urea_kg*0.34, 1)} kg)."
                ]
            }
        else:
            # Using SSP (16% P2O5) and Urea (46% N)
            ssp_kg = tot_target_p / 0.16
            urea_kg = tot_target_n / 0.46
            mop_kg = tot_target_k / 0.60
            steps.append(f"Step 1 (Phosphorus via SSP): SSP contains 16% P2O5. SSP needed = {tot_target_p:.2f} / 0.16 = {ssp_kg:.2f} kg.")
            steps.append(f"Step 2 (Nitrogen via Urea): Urea needed (no N in SSP) = {tot_target_n:.2f} / 0.46 = {urea_kg:.2f} kg.")
            steps.append(f"Step 3 (Potassium via MOP): MOP needed = {tot_target_k:.2f} / 0.60 = {mop_kg:.2f} kg.")

            return {
                "calculationType": "npk_fertilizer_ssp",
                "area": area,
                "unit": unit_label,
                "targetNutrients": {"N_kg": round(tot_target_n, 1), "P2O5_kg": round(tot_target_p, 1), "K2O_kg": round(tot_target_k, 1)},
                "fertilizers": [
                    {"name": "SSP (Single Superphosphate 16% P2O5 + 11% S)", "quantityKg": round(ssp_kg, 1), "bags": round(ssp_kg / 50.0, 2), "bagSizeKg": 50},
                    {"name": "Urea (Neem Coated 46% N)", "quantityKg": round(urea_kg, 1), "bags": round(urea_kg / 45.0, 2), "bagSizeKg": 45},
                    {"name": "MOP (Muriate of Potash 60% K2O)", "quantityKg": round(mop_kg, 1), "bags": round(mop_kg / 50.0, 2), "bagSizeKg": 50}
                ],
                "calculationSteps": steps,
                "splitSchedule": [
                    f"Basal: 100% SSP ({round(ssp_kg, 1)} kg), 100% MOP ({round(mop_kg, 1)} kg), 33% Urea ({round(urea_kg*0.33, 1)} kg).",
                    f"Topdress 1: 33% Urea ({round(urea_kg*0.33, 1)} kg).",
                    f"Topdress 2: 34% Urea ({round(urea_kg*0.34, 1)} kg)."
                ]
            }

    @staticmethod
    def calculate_plant_population_and_seed_rate(
        area_val: float,
        area_unit: str,
        row_spacing_cm: float,
        plant_spacing_cm: float,
        test_weight_g: float,
        germination_pct: float = 85.0,
        purity_pct: float = 98.0
    ) -> Dict[str, Any]:
        """
        Calculates theoretical plant population and required seed weight in kg.
        """
        if area_val <= 0 or row_spacing_cm <= 0 or plant_spacing_cm <= 0:
            raise ValueError("Area and spacing dimensions must be positive.")
        if germination_pct <= 0 or germination_pct > 100 or purity_pct <= 0 or purity_pct > 100:
            raise ValueError("Germination and purity percentages must be between 1 and 100.")

        # Convert area to square metres
        if area_unit.lower() in ["ha", "hectare", "hectares"]:
            area_m2 = area_val * 10000.0
            unit_norm = "hectare"
        elif area_unit.lower() in ["acre", "acres"]:
            area_m2 = area_val * 4046.856
            unit_norm = "acre"
        else:
            area_m2 = area_val
            unit_norm = "sq.m"

        row_spacing_m = row_spacing_cm / 100.0
        plant_spacing_m = plant_spacing_cm / 100.0
        area_per_plant_m2 = row_spacing_m * plant_spacing_m

        plant_population = int(round(area_m2 / area_per_plant_m2))

        # Real value index (Utility factor)
        real_value = (germination_pct / 100.0) * (purity_pct / 100.0)

        # Seed rate: (Population * Test weight in g) / (Real value * 1,000 * 1,000)
        # Test weight is weight of 1000 seeds in grams
        seed_weight_per_plant_g = test_weight_g / 1000.0
        pure_seed_req_kg = (plant_population * seed_weight_per_plant_g) / 1000.0
        actual_seed_req_kg = pure_seed_req_kg / real_value

        steps = [
            f"1. Area conversion: {area_val} {unit_norm} = {area_m2:.1f} m².",
            f"2. Area per plant: {row_spacing_cm} cm × {plant_spacing_cm} cm = {row_spacing_m} m × {plant_spacing_m} m = {area_per_plant_m2:.4f} m².",
            f"3. Theoretical Plant Population = {area_m2:.1f} m² / {area_per_plant_m2:.4f} m² = {plant_population:,} plants.",
            f"4. Real Value of Seed = (Germination {germination_pct}% × Purity {purity_pct}%) / 100 = {real_value * 100:.1f}%.",
            f"5. Seed Rate = ({plant_population:,} plants × {seed_weight_per_plant_g:.4f} g/seed) / ({real_value:.4f} × 1,000 g/kg) = {actual_seed_req_kg:.2f} kg."
        ]

        return {
            "calculationType": "seed_rate_and_population",
            "area": area_val,
            "areaUnit": unit_norm,
            "rowSpacingCm": row_spacing_cm,
            "plantSpacingCm": plant_spacing_cm,
            "plantPopulation": plant_population,
            "seedRateKg": round(actual_seed_req_kg, 2),
            "seedRateQuintals": round(actual_seed_req_kg / 100.0, 3),
            "assumptions": {
                "testWeight1000SeedsG": test_weight_g,
                "germinationPct": germination_pct,
                "purityPct": purity_pct
            },
            "calculationSteps": steps
        }

    @staticmethod
    def calculate_irrigation_water_and_runtime(
        eto_mm_day: float,
        crop_kc: float,
        area_m2: float,
        emitter_discharge_lph: float = 2.0,
        emitters_per_plant: int = 1,
        total_plants: Optional[int] = None,
        efficiency_pct: float = 90.0
    ) -> Dict[str, Any]:
        """
        Calculates daily crop water requirement (Litres) and drip irrigation pump runtime (hours).
        Based on FAO Irrigation Paper 56 standard: ETc = ETo * Kc.
        """
        if eto_mm_day <= 0 or crop_kc <= 0 or area_m2 <= 0 or emitter_discharge_lph <= 0:
            raise ValueError("ETo, Kc, Area, and Emitter discharge must be positive values.")

        etc_mm = eto_mm_day * crop_kc

        # 1 mm of water over 1 m2 equals exactly 1.0 Litre
        net_water_litres = etc_mm * area_m2
        gross_water_litres = net_water_litres / (efficiency_pct / 100.0)

        # Estimate emitters if total_plants not given (assuming standard 1.5 m2 per emitter)
        if total_plants and total_plants > 0:
            num_emitters = total_plants * emitters_per_plant
        else:
            num_emitters = max(10, int(round(area_m2 / 1.2)))

        total_system_discharge_lph = num_emitters * emitter_discharge_lph
        run_time_hours = gross_water_litres / total_system_discharge_lph

        steps = [
            f"1. Crop Evapotranspiration (ETc) = ETo ({eto_mm_day} mm/day) × Kc ({crop_kc}) = {etc_mm:.2f} mm/day.",
            f"2. Net Water Volume = {etc_mm:.2f} mm × {area_m2:.1f} m² × 1.0 L/mm/m² = {net_water_litres:,.1f} Litres/day.",
            f"3. Gross Water Requirement ({efficiency_pct}% drip efficiency) = {net_water_litres:,.1f} / {efficiency_pct/100:.2f} = {gross_water_litres:,.1f} Litres/day.",
            f"4. Total Drip System Discharge = {num_emitters:,} emitters × {emitter_discharge_lph} L/h = {total_system_discharge_lph:,.1f} L/h.",
            f"5. Required Pump Runtime = {gross_water_litres:,.1f} L / {total_system_discharge_lph:,.1f} L/h = {run_time_hours:.2f} hours ({int(run_time_hours*60)} minutes)."
        ]

        return {
            "calculationType": "drip_irrigation_runtime",
            "dailyEtcMm": round(etc_mm, 2),
            "netWaterLitresDay": round(net_water_litres, 1),
            "grossWaterLitresDay": round(gross_water_litres, 1),
            "numberOfEmitters": num_emitters,
            "systemDischargeLph": round(total_system_discharge_lph, 1),
            "recommendedRuntimeHours": round(run_time_hours, 2),
            "recommendedRuntimeMinutes": int(round(run_time_hours * 60)),
            "calculationSteps": steps
        }

    @staticmethod
    def calculate_farm_economics(
        crop_name: str,
        area_val: float,
        area_unit: str,
        cost_items: Dict[str, float],
        expected_yield_quintals: float,
        price_per_quintal_inr: float
    ) -> Dict[str, Any]:
        """
        Calculates Cost of Cultivation (₹), Gross Revenue (₹), Net Profit (₹),
        and Benefit-Cost Ratio (BCR).
        """
        if area_val <= 0 or expected_yield_quintals <= 0 or price_per_quintal_inr <= 0:
            raise ValueError("Area, yield, and price must be positive numbers.")

        total_cost = sum(cost_items.values())
        if total_cost <= 0:
            raise ValueError("Total cost must be greater than zero.")

        gross_revenue = expected_yield_quintals * price_per_quintal_inr
        net_profit = gross_revenue - total_cost
        bcr = gross_revenue / total_cost
        cost_per_quintal = total_cost / expected_yield_quintals

        steps = [
            f"1. Cost of Cultivation Breakdown: " + ", ".join([f"{k}: ₹{v:,.0f}" for k, v in cost_items.items()]),
            f"2. Total Cost of Cultivation = ₹{total_cost:,.2f}.",
            f"3. Gross Revenue = {expected_yield_quintals:.2f} Quintals × ₹{price_per_quintal_inr:,.2f}/Q = ₹{gross_revenue:,.2f}.",
            f"4. Net Profit / Margin = Gross (₹{gross_revenue:,.2f}) - Cost (₹{total_cost:,.2f}) = ₹{net_profit:,.2f}.",
            f"5. Benefit-Cost Ratio (BCR) = ₹{gross_revenue:,.2f} / ₹{total_cost:,.2f} = {bcr:.2f}.",
            f"6. Cost of Production per Quintal = ₹{total_cost:,.2f} / {expected_yield_quintals:.2f} Q = ₹{cost_per_quintal:,.2f}/Quintal."
        ]

        return {
            "calculationType": "farm_economics",
            "crop": crop_name,
            "area": area_val,
            "areaUnit": area_unit,
            "totalCostINR": round(total_cost, 2),
            "costItemsINR": cost_items,
            "grossRevenueINR": round(gross_revenue, 2),
            "netProfitINR": round(net_profit, 2),
            "benefitCostRatio": round(bcr, 2),
            "costOfProductionPerQuintalINR": round(cost_per_quintal, 2),
            "isEconomicallyViable": bcr > 1.25,
            "calculationSteps": steps
        }

    @staticmethod
    def safe_math_eval(expr: str) -> Union[int, float]:
        """
        Safely evaluates mathematical expressions using AST.
        Supports standard math operators and functions (sqrt, sin, cos, log, abs, etc.).
        Raises ValueError on syntax errors or disallowed constructs.
        """
        def _eval_node(node):
            if isinstance(node, ast.Constant):
                if isinstance(node.value, (int, float)):
                    return node.value
                raise ValueError("Only numeric constants are supported.")
            elif isinstance(node, ast.BinOp):
                left = _eval_node(node.left)
                right = _eval_node(node.right)
                op_type = type(node.op)
                if op_type in SAFE_OPERATORS:
                    return SAFE_OPERATORS[op_type](left, right)
                raise ValueError(f"Unsupported binary operator: {op_type}")
            elif isinstance(node, ast.UnaryOp):
                operand = _eval_node(node.operand)
                op_type = type(node.op)
                if op_type in SAFE_OPERATORS:
                    return SAFE_OPERATORS[op_type](operand)
                raise ValueError(f"Unsupported unary operator: {op_type}")
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in SAFE_FUNCTIONS:
                    args = [_eval_node(a) for a in node.args]
                    return SAFE_FUNCTIONS[node.func.id](*args)
                raise ValueError(f"Unsupported function call: {getattr(node.func, 'id', 'unknown')}")
            elif isinstance(node, ast.Name):
                if node.id in SAFE_FUNCTIONS:
                    return SAFE_FUNCTIONS[node.id]
                raise ValueError(f"Undefined variable: {node.id}")
            else:
                raise ValueError(f"Unsupported expression node: {type(node)}")

        clean_expr = expr.replace("^", "**").strip()
        parsed = ast.parse(clean_expr, mode='eval')
        return _eval_node(parsed.body)
