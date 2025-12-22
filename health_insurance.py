from insurance_inputs import InsuranceInputs

def calculate_required_health_cover(inputs: InsuranceInputs) -> float:
    age = inputs.age
    dependents = inputs.dependents
    city_tier = inputs.city_tier
    lifestyle = inputs.lifestyle_risks or []

    if age < 30:
        base_cover = 1000000
    elif age <= 45:
        base_cover = 1500000
    else:
        base_cover = 2500000

    if dependents >= 2:
        base_cover += 500000

    if city_tier == "Tier_1":
        base_cover += 500000
    elif city_tier == "Tier_2":
        base_cover += 250000
    else:
        base_cover += 0
    

    if "smoking" in lifestyle:
        base_cover += 500000
    if "sedentary" in lifestyle:
        base_cover += 250000
    if "high_stress" in lifestyle:
        base_cover += 250000

    return base_cover
