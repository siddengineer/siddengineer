import numpy as np
import matplotlib.pyplot as plt

def project_economic_growth():
    # Predefined values
    current_gdp = 3.7  # in trillion USD
    growth_rate = 8    # annual growth rate in percentage
    target_gdp = 30    # target GDP in trillion USD

    # Initialize variables
    years = 0
    gdp_progression = [current_gdp]
    years_list = [years]

    # Calculate GDP progression
    while current_gdp < target_gdp:
        current_gdp *= (1 + growth_rate / 100)  # Growth formula: GDP = GDP * (1 + growth rate)
        years += 1
        gdp_progression.append(current_gdp)
        years_list.append(years)

    # Output the results
    print(f"It will take {years} years to reach a GDP of {target_gdp} trillion USD.")

    # Plotting the GDP progression
    plt.figure(figsize=(10,6))
    plt.plot(years_list, gdp_progression, marker='o', linestyle='-', color='b')
    plt.title("India's Economic Growth Projection")
    plt.xlabel("Years")
    plt.ylabel("GDP (in Trillions USD)")
    plt.grid(True)
    plt.xticks(np.arange(0, years+1, 2))
    plt.yticks(np.arange(current_gdp * 0.5, target_gdp + 5, 5))
    plt.axhline(y=target_gdp, color='r', linestyle='--', label=f"Target GDP: {target_gdp} Trillions")
    plt.legend()
    plt.show()

# Run the project
project_economic_growth()