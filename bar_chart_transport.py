import matplotlib.pyplot as plt
import numpy as np

# Data for each person in tonnes
jonathan_values_tonnes = [0.115, 2.217]
connor_values_tonnes = [0.040, 0.000]

activities_updated = ['Train', 'Car']
colors = ['#ff9999', '#66b3ff']

# Create a 1x2 grid layout (for Jonathan and Connor)
fig, axs = plt.subplots(1, 2, figsize=(18, 8))  # Changed to 1x2 layout


# Plotting function with values displayed above bars
def plot_bars(ax, values, title, xtick_size=20, ytick_size=20):
    # Handle missing (None) values and keep 0 as valid data
    values_with_default = [v if v is not None else 0 for v in values]  # Replace None with 0 for plotting
    bars = ax.bar(activities_updated, values_with_default, color=colors)

    ax.set_title(title, fontsize=20, fontweight='bold')
    ax.set_xlabel('Activity', fontweight='bold', fontsize=20)
    ax.set_ylabel('GHG Emission (tCO₂e)', fontweight='bold', fontsize=20)
    ax.grid(True)

    # Find the maximum valid value (ignoring None) to adjust y-axis limit
    max_value = max([v for v in values if v is not None], default=0)

    # If max_value is 0, set a small default y-limit
    if max_value == 0:
        ax.set_ylim(0, 0.1)  # Set a small default y-limit for all zero data
    else:
        ax.set_ylim(0, max_value * 1.15)  # Increase the limit by 15% above the max value

    # Display values above each bar, handling 'None' as 'N/A' and showing all values with 3 decimal places
    for bar, value in zip(bars, values):
        if value is None:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max_value * 0.02, 'N/A',
                    ha='center', va='bottom', fontweight='bold', fontsize=20)
        else:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max_value * 0.02, f'{value:.2f}',
                    ha='center', va='bottom', fontweight='bold', fontsize=20)

    # Set the size of x-axis and y-axis ticks
    ax.tick_params(axis='x', labelsize=xtick_size)
    ax.tick_params(axis='y', labelsize=ytick_size)


# Bar chart for Jonathan (left)
plot_bars(axs[0], jonathan_values_tonnes, 'Jonathan')

# Bar chart for Connor (right)
plot_bars(axs[1], connor_values_tonnes, 'Connor')

# Main title at 95% height (larger and bold)
fig.suptitle('Transport Carbon Footprint Comparison', fontsize=25, fontweight='bold', y=0.95)

# Adjust layout with hspace control within tight_layout
plt.tight_layout(rect=[0, 0, 1, 0.95], h_pad=2.5)  # h_pad adjusts the space between rows

# Save the plot as an image file
plt.savefig("carbon_footprint_bar_chart_transport.png")
plt.savefig("carbon_footprint_bar_chart_transport.svg")

# Show the plot
plt.show()