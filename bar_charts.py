import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec

# Data for each person in tonnes
jonathan_values_tonnes = [8.986, 0.013, 2.333, 9.963]
connor_values_tonnes = [5.611, 0.022, 0.040, 7.293]
agnel_values_tonnes = [0.318, 0.024, 0.000, 31.176]

activities_updated = ['Residential\nEnergy', 'Water', 'Transport', 'Diet']
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']

# Create a 2x2 grid layout
fig, axs = plt.subplots(2, 2, figsize=(18, 12))

# Plotting function with values displayed above bars
def plot_bars(ax, values, title, xtick_size=20, ytick_size=20):
    bars = ax.bar(activities_updated, values, color=colors)
    ax.set_title(title, fontsize=20, fontweight='bold')
    ax.set_xlabel('Activity', fontweight='bold', fontsize=20)
    ax.set_ylabel('GHG Emission (tCO₂e)', fontweight='bold', fontsize=20)
    ax.grid(True)

    # Set the y-axis limit to give more space above the highest bar
    max_value = max(values)
    ax.set_ylim(0, max_value * 1.15)  # Increase the limit by 15% above the max value

    # Display values above each bar
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max_value * 0.02,  # Offset text by 2% of max value
                f'{value:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=20)

    # Set the size of x-axis and y-axis ticks
    ax.tick_params(axis='x', labelsize=xtick_size)
    ax.tick_params(axis='y', labelsize=ytick_size)

# Bar chart for Jonathan (top-left)
plot_bars(axs[0, 0], jonathan_values_tonnes, 'Jonathan')

# Bar chart for Connor (top-right)
plot_bars(axs[0, 1], connor_values_tonnes, 'Connor')

# Bar chart for Agnel (bottom-left)
plot_bars(axs[1, 0], agnel_values_tonnes, 'Agnel')

# Remove the bottom-right empty subplot
fig.delaxes(axs[1, 1])

# Main title at 95% height (larger and bold)
fig.suptitle('Carbon Footprint Comparison', fontsize=25, fontweight='bold', y=0.95)

# Adjust layout with hspace control within tight_layout
plt.tight_layout(rect=[0, 0, 1, 0.95], h_pad=2.5)  # h_pad adjusts the space between rows

# Save the plot as an image file
plt.savefig("carbon_footprint_comparison.png")
plt.savefig("carbon_footprint_comparison.svg")

# Show the plot
plt.show()