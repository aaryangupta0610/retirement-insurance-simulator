from insurance_inputs import InsuranceInputs

def calculate_required_life_cover(inputs: InsuranceInputs) -> float:

    income = inputs.annual_income
    dependents = inputs.dependents

    if dependents >= 3:
        multiplier = 15
    elif dependents >= 1:
        multiplier = 12
    else:
        multiplier = 10

    return income * multiplier
