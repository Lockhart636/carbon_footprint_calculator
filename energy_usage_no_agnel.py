import matplotlib.pyplot as plt
import numpy as np

# Updated data for Jonathan and Connor only
data = {
    'Jonathan': {'Heating Oil': 8674.61, 'Electricity': 311.20},
    'Connor': {'Heating Oil': 5461.32, 'Electricity': 149.56}
}

# Custom function to format autopct, skip 0% values, and avoid overlaps
def autopct_format(values, wedges, min_pct=5):
    total = sum(values)
    def custom_autopct(pct, index):
        if pct < min_pct or wedges[index].theta2 - wedges[index].theta1 < 15:
            return ''  # No label for small sectors
        else:
            return '%1.1f%%' % pct  # Display percentage for larger sectors
    return custom_autopct

# Helper function to calculate text position inside each wedge
def calculate_text_position(wedge, pct_distance=0.75):
    angle = (wedge.theta2 + wedge.theta1) / 2  # Calculate the angle in degrees
    angle_rad = np.deg2rad(angle)  # Convert angle to radians

    x = pct_distance * np.cos(angle_rad)
    y = pct_distance * np.sin(angle_rad)
    return x, y

# Helper function to calculate text position outside each wedge
def calculate_external_text_position(wedge, pct_distance=1.4):
    angle = (wedge.theta2 + wedge.theta1) / 2
    angle_rad = np.deg2rad(angle)
    x = pct_distance * np.cos(angle_rad)
    y = pct_distance * np.sin(angle_rad)
    return x, y

# Custom function to control legend distance and text sizes
def plot_pie_charts(data, legend_distance=1.1, title_size=25, name_text_size=20, wedge_gap=1, pct_distance=0.75,
                    min_pct=5, title_y=-0.1, main_title_y=0.9):
    # Define figure and subplots with the title
    fig, axs = plt.subplots(1, 2, figsize=(11, 5))  # Now only 2 subplots for Jonathan and Connor
    fig.suptitle('Residential Energy Consumption Breakdown', fontsize=title_size, fontweight='bold', y=main_title_y)

    # Define colors (optional, you can customize this)
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']

    # Define hatches for black-and-white printing
    hatches = ['x', '-', '/', '\\', '|',  '+', 'o']

    # Loop over each individual and plot their pie chart
    for ax, (name, activities) in zip(axs, data.items()):
        labels = list(activities.keys())
        values = list(activities.values())

        # Plot the pie chart for valid data
        wedges, texts = ax.pie(values, labels=None, colors=colors,
                               startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'},
                               pctdistance=pct_distance,
                               wedgeprops={'edgecolor': 'white', 'linewidth': wedge_gap})

        # Set title (individual name) with adjustable font size, bold font, and customizable vertical position (y)
        ax.set_title(name, fontsize=name_text_size, fontweight='bold', y=title_y)

        # Manually set percentage labels for each wedge
        for i, wedge in enumerate(wedges):
            wedge.set_hatch(hatches[i % len(hatches)])  # Cycle through hatches
            pct = 100. * values[i] / sum(values)
            pct_text = autopct_format(values, wedges, min_pct=min_pct)(pct, i)

            if pct < min_pct:
                # For small sectors, place the label outside the pie chart
                x, y = calculate_external_text_position(wedge, pct_distance=1.2)  # Set distance for label
                ax.text(x, y, f'{pct:.1f}%', ha='center', va='center', fontsize=15, fontweight='bold')

                # Draw dashed line from the wedge to the label, shortened by 95% (to avoid overlapping with text)
                angle = (wedge.theta2 + wedge.theta1) / 2
                angle_rad = np.deg2rad(angle)
                line_start_x = 0.9 * np.cos(angle_rad)  # Start from near the wedge's edge
                line_start_y = 0.9 * np.sin(angle_rad)
                ax.plot([line_start_x, 0.95 * x], [line_start_y, 0.95 * y], color='black', linestyle='dashed')

            elif pct_text:  # Place text inside the wedge for larger sectors
                x, y = calculate_text_position(wedge, pct_distance)
                ax.text(x, y, pct_text, ha='center', va='center', fontsize=15, fontweight='bold')

    # Add a legend with adjustable distance from the pie charts
    fig.legend(labels, loc='center left', bbox_to_anchor=(0.8, 0.5), fontsize=15, handlelength=2, handleheight=2, markerscale=2)

    # Adjust layout to leave more space for the title and prevent cutoff
    plt.tight_layout(rect=[0, 0, 0.75, 0.95])  # Increase space for the legend and title

    # Save the figure as a PNG and SVG image
    fig.savefig('carbon_footprint_residential_energy_usage.png', bbox_inches='tight')
    fig.savefig('carbon_footprint_residential_energy_usage.svg', bbox_inches='tight')

    # Show the updated figure
    plt.show()

# Call the function with default settings
plot_pie_charts(data, title_y=-0.1, main_title_y=0.95)