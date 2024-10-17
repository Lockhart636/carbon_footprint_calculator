import matplotlib.pyplot as plt
import numpy as np

# Updated data for each individual
data = {
    'Jonathan': {'Electricity': 311.20, 'Heating Oil': 8674.61},
    'Connor': {'Electricity': 149.56, 'Heating Oil': 5461.32},
    'Agnel': {'Electricity': 317.50, 'Heating Oil': None}  # Missing data for Agnel
}

# Custom function to format autopct, skip 0% values, and avoid overlaps
def autopct_format(values, wedges, min_pct=5):
    total = sum(values)
    def custom_autopct(pct, index):
        # Skip small wedges (< 15 degrees) or percentages less than min_pct
        if pct < min_pct or wedges[index].theta2 - wedges[index].theta1 < 15:
            return ''  # No label for small sectors
        else:
            return '%1.1f%%' % pct  # Display percentage for larger sectors
    return custom_autopct

# Helper function to calculate text position inside each wedge
def calculate_text_position(wedge, pct_distance=0.75):
    angle = (wedge.theta2 + wedge.theta1) / 2  # Calculate the angle in degrees
    angle_rad = np.deg2rad(angle)  # Convert angle to radians

    # Use polar coordinates (r, theta) to calculate (x, y) position
    x = pct_distance * np.cos(angle_rad)
    y = pct_distance * np.sin(angle_rad)

    return x, y

# Custom function to control legend distance and text sizes
def plot_pie_charts(data, legend_distance=1.1, title_size=25, name_text_size=16, wedge_gap=1, pct_distance=0.75, min_pct=5, title_y=-0.1, main_title_y=0.9, unavailable_text='Data Unavailable'):
    # Define figure and subplots with the title
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('Energy Usage', fontsize=title_size, fontweight='bold', y=main_title_y)

    # Define colors (optional, you can customize this)
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']

    # Loop over each individual and plot their pie chart
    for ax, (name, activities) in zip(axs, data.items()):
        labels = list(activities.keys())
        values = list(activities.values())

        # Check for missing data (e.g., for Agnel's Heating Oil)
        if None in values:
            # Plot a grey circle with custom "unavailable_text" in the center
            ax.pie([1], colors=['#d3d3d3'], startangle=90, wedgeprops={'edgecolor': 'white', 'linewidth': wedge_gap})
            # Place the custom "unavailable_text" text at the center of the pie
            ax.text(0, 0, unavailable_text, ha='center', va='center', fontsize=14, fontweight='bold')
            ax.set_title(name, fontsize=name_text_size, fontweight='bold', y=title_y)
            continue

        # Plot the pie chart for valid data
        wedges, texts = ax.pie(values, labels=None, colors=colors,
                               startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'},
                               pctdistance=pct_distance,
                               wedgeprops={'edgecolor': 'white', 'linewidth': wedge_gap})

        # Set title (individual name) with adjustable font size, bold font, and customizable vertical position (y)
        ax.set_title(name, fontsize=name_text_size, fontweight='bold', y=title_y)

        # Manually set percentage labels for each wedge
        for i, wedge in enumerate(wedges):
            pct = 100. * values[i] / sum(values)
            pct_text = autopct_format(values, wedges, min_pct=min_pct)(pct, i)
            if pct_text:  # Only place text if it's not empty (i.e., for larger sectors)
                x, y = calculate_text_position(wedge, pct_distance)
                ax.text(x, y, pct_text, ha='center', va='center', fontsize=12, fontweight='bold')

    # Add a legend with adjustable distance from the pie charts
    fig.legend(labels, loc='center left', bbox_to_anchor=(0.8, 0.5), fontsize=15)

    # Adjust layout to leave more space for the title and prevent cutoff
    plt.tight_layout(rect=[0, 0, 0.75, 0.95])  # Increase space for the legend and title

    # Save the figure as a PNG image with bbox_inches to ensure no cutoffs
    fig.savefig('energy_usage_pie_charts.png', bbox_inches='tight')

    # Show the updated figure
    plt.show()

# Call the function with default settings, custom text for unavailable data, and adjusted main title position
plot_pie_charts(data, title_y=-0.1, main_title_y=0.9, unavailable_text='N/A')  # You can pass different text here