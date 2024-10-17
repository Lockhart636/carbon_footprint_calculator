import matplotlib.pyplot as plt
import numpy as np

# Data for each individual
data = {
    'Jonathan': {'Shower': 16380, 'Cleaning Dishes': 4186, 'Washing Machine': 8112, 'Toilet': 7300, 'Fish Tank': 1664},
    'Connor': {'Shower': 32760, 'Cleaning Dishes': 2184, 'Washing Machine': 4680, 'Toilet': 26280, 'Fish Tank': 0},
    'Agnel': {'Shower': 49140, 'Cleaning Dishes': 10192, 'Washing Machine': 2704, 'Toilet': 9125, 'Fish Tank': 0}
}


# Custom function to format autopct, skip 0% values, and avoid overlaps
def autopct_format(values, wedges, min_pct=5):
    total = sum(values)

    def custom_autopct(pct, index):
        if pct < min_pct or wedges[index].theta2 - wedges[index].theta1 < 15:
            return ''  # No label for small sectors or those below min_pct
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


# Helper function to calculate text position outside each wedge
def calculate_external_text_position(wedge, pct_distance=1.4):
    angle = (wedge.theta2 + wedge.theta1) / 2  # Mid-angle of the wedge
    angle_rad = np.deg2rad(angle)

    # Calculate text position outside the wedge (polar coordinates)
    x = pct_distance * np.cos(angle_rad)
    y = pct_distance * np.sin(angle_rad)
    return x, y


# Custom function to control legend distance and text sizes
def plot_pie_charts(data, legend_distance=1.1, title_size=25, name_text_size=20, wedge_gap=1, pct_distance=0.73,
                    min_pct=5, title_y=-0.1, main_title_y=0.9):
    # Define figure and subplots with the title
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('Water Consumption Breakdown', fontsize=title_size, fontweight='bold', y=main_title_y)

    # Define colors (optional, you can customize this)
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']

    # Define hatches for black-and-white printing
    hatches = ['x', '-', '/', '\\', 'o', '|', '+']

    # Loop over each individual and plot their pie chart
    for ax, (name, activities) in zip(axs, data.items()):
        # Extract labels and values
        labels = list(activities.keys())
        values = list(activities.values())

        # Plot the pie chart with white gap between sectors, no explode, and percentage labels inside
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

            # Skip if percentage is 0%
            if pct == 0:
                continue

            pct_text = autopct_format(values, wedges, min_pct=min_pct)(pct, i)

            # Handle specific case for Connor's "Cleaning Dishes" and "Washing Machine" labels
            if name == 'Connor' and labels[i] == 'Cleaning Dishes':
                # Move "Cleaning Dishes" label slightly higher to avoid overlap
                x, y = calculate_external_text_position(wedge, pct_distance=1.2)
                #y += 0.1  # Move up slightly
                ax.text(x, y, f'{pct:.1f}%', ha='center', va='center', fontsize=15, fontweight='bold')
                # Dashed line to label
                angle = (wedge.theta2 + wedge.theta1) / 2
                angle_rad = np.deg2rad(angle)
                line_start_x = 0.9 * np.cos(angle_rad)
                line_start_y = 0.9 * np.sin(angle_rad)
                ax.plot([line_start_x, 0.94 * x], [line_start_y, 0.92 * y], color='black', linestyle='dashed')

            elif name == 'Connor' and labels[i] == 'Washing Machine':
                # Move "Washing Machine" label slightly lower to avoid overlap
                x, y = calculate_external_text_position(wedge, pct_distance=1.2)
                x += 0.1  # Move down slightly
                ax.text(x, y, f'{pct:.1f}%', ha='center', va='center', fontsize=15, fontweight='bold')
                # Dashed line to label
                angle = (wedge.theta2 + wedge.theta1) / 2
                angle_rad = np.deg2rad(angle)
                line_start_x = 0.9 * np.cos(angle_rad)
                line_start_y = 0.9 * np.sin(angle_rad)
                ax.plot([line_start_x, 0.94 * x], [line_start_y, 0.92 * y], color='black', linestyle='dashed')

            elif pct < min_pct or (name == 'Connor' and labels[i] == 'Washing Machine'):
                # For small sectors or Connor's "Washing Machine" sector, place the label outside the pie chart
                x, y = calculate_external_text_position(wedge, pct_distance=1.2)
                ax.text(x, y, f'{pct:.1f}%', ha='center', va='center', fontsize=15, fontweight='bold')

                # Draw a dashed line connecting the wedge to the label
                angle = (wedge.theta2 + wedge.theta1) / 2
                angle_rad = np.deg2rad(angle)
                line_start_x = 0.9 * np.cos(angle_rad)  # Start from near the wedge's edge
                line_start_y = 0.9 * np.sin(angle_rad)
                ax.plot([line_start_x, 0.94 * x], [line_start_y, 0.92 * y], color='black', linestyle='dashed')

            elif pct_text:  # Place text inside the wedge for larger sectors
                x, y = calculate_text_position(wedge, pct_distance)
                ax.text(x, y, pct_text, ha='center', va='center', fontsize=15, fontweight='bold')

    # Add a legend with adjustable distance from the pie charts
    fig.legend(labels, loc='center left', bbox_to_anchor=(0.8, 0.5), fontsize=15, handlelength=2, handleheight=2,
               markerscale=2)

    # Adjust layout to leave more space for the title and prevent cutoff
    plt.tight_layout(rect=[0, 0, 0.75, 0.95])  # Increase space for the legend and title

    # Save the figure as a PNG image with bbox_inches to ensure no cutoffs
    fig.savefig('carbon_footprint_water_consumption.png', bbox_inches='tight')
    fig.savefig('carbon_footprint_water_consumption.svg', bbox_inches='tight')

    # Show the updated figure
    plt.show()


# Call the function with default settings and adjusted main title position
plot_pie_charts(data, title_y=-0.1, main_title_y=0.95)  # Adjust main_title_y to move the main title closer