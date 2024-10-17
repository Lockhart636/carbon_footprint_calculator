import matplotlib.pyplot as plt
import numpy as np

# Data for food consumption (in kgCO₂e)
data = {
    'Jonathan': {
        'Beef': 7800.00,
        'Pig Meat': 0.00,
        'Fish': 873.60,
        'Poultry': 936.00,
        'Rice': 10.92,
        'Potatoes': 30.28,
        'Pasta': 312.00
    },
    'Connor': {
        'Beef': 3900.00,
        'Pig Meat': 1560.00,
        'Fish': 312.00,
        'Poultry': 1248.00,
        'Rice': 21.84,
        'Potatoes': 43.26,
        'Pasta': 208.00
    },
    'Agnel': {
        'Beef': 23400.00,
        'Pig Meat': 0.00,
        'Fish': 0.00,
        'Poultry': 6240.00,
        'Rice': 10.92,
        'Potatoes': 69.22,
        'Pasta': 1456.00
    }
}

# Define colors (you can customize)
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0', '#ffb3e6', '#c4e17f']

# Convert all values from kgCO₂e to tCO₂e
for person, food_data in data.items():
    for food, value in food_data.items():
        data[person][food] = value / 1000  # Convert kg to tonnes (tCO₂e)

# Extract activities (food categories) dynamically from data
activities = list(data['Jonathan'].keys())  # Assuming all individuals have the same food categories

# Create a 2x2 grid layout for the bar charts
fig, axs = plt.subplots(2, 2, figsize=(18, 12))

# Plotting function with values displayed above bars
def plot_bars(ax, values, title, xtick_size=15, ytick_size=15):
    # Handle missing (None) values
    values_with_default = [v if v is not None else 0 for v in values]  # Replace None with 0 for plotting
    bars = ax.bar(activities, values_with_default, color=colors)

    ax.set_title(title, fontsize=20, fontweight='bold')
    ax.set_xlabel('Food', fontweight='bold', fontsize=20)
    ax.set_ylabel('GHG Emission (tCO₂e)', fontweight='bold', fontsize=20)
    ax.grid(True)

    # Find the maximum valid value (ignoring None) to adjust y-axis limit
    max_value = max([v for v in values if v is not None], default=1)
    ax.set_ylim(0, max_value * 1.15)  # Increase the limit by 15% above the max value

    # Display values or 'N/A' above each bar
    for bar, value in zip(bars, values):
        if value is None:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max_value * 0.02, 'N/A',
                    ha='center', va='bottom', fontweight='bold', fontsize=15)
        else:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max_value * 0.02, f'{value:.2f}',
                    ha='center', va='bottom', fontweight='bold', fontsize=15)

    # Set the size of x-axis and y-axis ticks
    ax.tick_params(axis='x', labelsize=xtick_size)
    ax.tick_params(axis='y', labelsize=ytick_size)

# Extract values for each individual (already converted to tCO₂e)
jonathan_values = list(data['Jonathan'].values())
connor_values = list(data['Connor'].values())
agnel_values = list(data['Agnel'].values())

# Bar chart for Jonathan (top-left)
plot_bars(axs[0, 0], jonathan_values, 'Jonathan')

# Bar chart for Connor (top-right)
plot_bars(axs[0, 1], connor_values, 'Connor')

# Bar chart for Agnel (bottom-left)
plot_bars(axs[1, 0], agnel_values, 'Agnel')

# Remove the bottom-right empty subplot
fig.delaxes(axs[1, 1])

# Main title at 95% height (larger and bold)
fig.suptitle('Diet Carbon Footprint Comparison', fontsize=25, fontweight='bold', y=0.95)

# Adjust layout with hspace control within tight_layout
plt.tight_layout(rect=[0, 0, 1, 0.95], h_pad=2.5)  # h_pad adjusts the space between rows

# Save the plot as an image file
plt.savefig("carbon_footprint_bar_chart_diet_tonnes.png")
plt.savefig("carbon_footprint_bar_chart_diet_tonnes.svg")

# Show the plot
plt.show()