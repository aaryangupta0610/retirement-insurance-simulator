def estimate_life_premium(life_gap: float, age: int) -> tuple:
 
    if life_gap <= 0:
        return (0, 0)

    units = life_gap / 10_00_000

    if age < 30:
        rate_range = (500, 800)
    elif age <= 45:
        rate_range = (800, 1200)
    else:
        rate_range = (1500, 2500)

    low = round(units * rate_range[0])
    high = round(units * rate_range[1])

    return (low, high)


def estimate_health_premium(health_gap: float, age: int) -> tuple:


    if health_gap <= 0:
        return (0, 0)

    units = health_gap / 10_00_000

    if age < 30:
        rate_range = (6000, 8000)
    elif age <= 45:
        rate_range = (8000, 12000)
    else:
        rate_range = (15000, 25000)

    low = round(units * rate_range[0])
    high = round(units * rate_range[1])

    return (low, high)
