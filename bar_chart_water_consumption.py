import matplotlib.pyplot as plt
import numpy as np

# Water usage emissions data for each person in tonnes
jonathan_values_tonnes = [0.013]
connor_values_tonnes = [0.022]
agnel_values_tonnes = [0.024]

# Names for the x-axis in the total chart
names = ['Jonathan', 'Connor', 'Agnel']

# Total emissions (since it's only water usage, each person's total is just their water value)
total_emissions = [jonathan_values_tonnes[0], connor_values_tonnes[0], agnel_values_tonnes[0]]

# Set a variable for subtitle font size
subtitle_fontsize = 14

# Main chart: Create total emissions bar chart for water usage
plt.figure(figsize=(12, 6))
bars = plt.bar(names, total_emissions, color=['#ff9999', '#66b3ff', '#99ff99'])

# Find the maximum total emissions and set y-axis limit 15% higher
max_total_emission = max(total_emissions)
plt.ylim(0, max_total_emission * 1.15)  # Set y-limit 15% above the maximum value

# Add title and labels to the total chart
plt.title('Water Consumption Carbon Footprint Comparison', fontsize=25, fontweight='bold', pad=20, y=1.05)
plt.xlabel('Group Member', fontsize=20, fontweight='bold')
plt.ylabel('GHG Emissions (tCO₂e)', fontsize=20, fontweight='bold')

# Display values above each bar
for bar, value in zip(bars, total_emissions):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
             f'{value:.3f}', ha='center', va='bottom', fontweight='bold', fontsize=18)

# Increase font size of x-axis names (Group Member names) and y-axis ticks (numbers)
plt.xticks(fontsize=18)  # Increase x-axis label font size
plt.yticks(fontsize=16)  # Increase y-axis tick font size

# Add grid and adjust layout to ensure consistency
plt.grid(True)
plt.tight_layout(rect=[0, 0, 1, 0.95])

# Save the plot as an image file
plt.savefig("carbon_footprint_comparison_bar_chart_water.png")
plt.savefig("carbon_footprint_comparison_bar_chart_water.svg")

# Show the plot
plt.show()