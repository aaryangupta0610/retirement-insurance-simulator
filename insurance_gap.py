from insurance_inputs import InsuranceInputs
from life_insurance import calculate_required_life_cover
from health_insurance import calculate_required_health_cover

def calculate_insurance_gap(inputs: InsuranceInputs) -> dict:

    # Required coverage
    required_life = calculate_required_life_cover(inputs)
    required_health = calculate_required_health_cover(inputs)

    # Gap calculation (never negative)
    life_gap = max(0, required_life - inputs.existing_life_cover)
    health_gap = max(0, required_health - inputs.existing_health_cover)

    return {
        "required_life_cover": required_life,
        "required_health_cover": required_health,
        "existing_life_cover": inputs.existing_life_cover,
        "existing_health_cover": inputs.existing_health_cover,
        "life_gap": life_gap,
        "health_gap": health_gap,
        "life_status": "Adequate" if life_gap == 0 else "Underinsured",
        "health_status": "Adequate" if health_gap == 0 else "Underinsured"
    }
