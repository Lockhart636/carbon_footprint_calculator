import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch  # Import Patch from matplotlib.patches

# New data for transport distances
data = {
    'Jonathan': {'Car': 2217.35, 'Train': 115.45},
    'Connor': {'Car': 0.00, 'Train': 40.28},  # Connor didn't use the car
    'Agnel': {'Walking': 100.0}  # Agnel walks everywhere
}

# Define the consistent labels for all transport modes
all_labels = ['Car', 'Train', 'Walking']

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

    # Use polar coordinates (r, theta) to calculate (x, y) position
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
def plot_pie_charts(data, legend_distance=1.1, title_size=25, name_text_size=20, wedge_gap=1, pct_distance=0.75, min_pct=5, title_y=-0.1, main_title_y=0.9):
    # Define figure and subplots with the title
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('Transport Breakdown', fontsize=title_size, fontweight='bold', y=main_title_y)

    # Define unique colors for Car, Train, and Walking
    colors = {
        'Car': '#ff9999',  # Light red
        'Train': '#66b3ff',  # Light blue
        'Walking': '#99ff99'  # Light green
    }

    # Define custom hatches for each transport mode
    hatches = {
        'Car': 'x',         # Car gets the 'x' hatch
        'Train': '-',       # Train gets the '-' hatch
        'Walking': '/'      # Walking gets the '/' hatch
    }

    # Loop over each individual and plot their pie chart
    for ax, (name, activities) in zip(axs, data.items()):
        # Filter out any categories with zero values (e.g., Connor's car)
        filtered_labels = [label for label in all_labels if activities.get(label, 0) > 0]
        filtered_values = [activities.get(label, 0) for label in filtered_labels]

        # Plot the pie chart for non-zero values only
        wedges, texts = ax.pie(filtered_values, labels=None, colors=[colors[label] for label in filtered_labels],
                               startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'},
                               pctdistance=pct_distance,
                               wedgeprops={'edgecolor': 'white', 'linewidth': wedge_gap})

        # Set title (individual name) with adjustable font size, bold font, and customizable vertical position (y)
        ax.set_title(name, fontsize=name_text_size, fontweight='bold', y=title_y)

        # Manually set percentage labels for each wedge
        for i, wedge in enumerate(wedges):
            label = filtered_labels[i]  # Get the transport mode
            if hatches[label]:  # Apply hatch only if defined
                wedge.set_hatch(hatches[label])

            pct = 100. * filtered_values[i] / sum(filtered_values)
            if pct < min_pct:
                # For small sectors, place the label outside the pie chart
                x, y = calculate_external_text_position(wedge, pct_distance=1.2)  # Set distance for label
                ax.text(x, y, f'{pct:.1f}%', ha='center', va='center', fontsize=15, fontweight='bold')

                # Draw dashed line from the wedge to the label, shortened by 95% (to avoid overlapping with text)
                angle = (wedge.theta2 + wedge.theta1) / 2
                angle_rad = np.deg2rad(angle)
                line_start_x = 0.9 * np.cos(angle_rad)  # Start from near the wedge's edge
                line_start_y = 0.9 * np.sin(angle_rad)
                ax.plot([line_start_x, 0.95 * x], [line_start_y, 0.94 * y], color='black', linestyle='dashed')
            else:
                # Regular label placement inside the wedge for larger sectors
                x, y = calculate_text_position(wedge, pct_distance)
                ax.text(x, y, f'{pct:.1f}%', ha='center', va='center', fontsize=15, fontweight='bold')

    # Create legend with both correct colors and hatches, ensuring the hatch lines are white
    legend_handles = [Patch(facecolor=colors[label], label=label, hatch=hatches[label] if hatches[label] else '', edgecolor='white')
                      for label in all_labels]

    # Add a legend for all transport modes (even if not used by all individuals)
    fig.legend(handles=legend_handles, loc='center left', bbox_to_anchor=(0.8, 0.5), fontsize=15,
               handlelength=2, handleheight=2, markerscale=2)

    # Adjust layout to leave more space for the title and prevent cutoff
    plt.tight_layout(rect=[0, 0, 0.75, 0.95])  # Increase space for the legend and title

    # Save the figure as a PNG image with bbox_inches to ensure no cutoffs
    fig.savefig('carbon_footprint_transport.png', bbox_inches='tight')
    fig.savefig('carbon_footprint_transport.svg', bbox_inches='tight')

    # Show the updated figure
    plt.show()

# Call the function with default settings and adjusted main title position
plot_pie_charts(data, title_y=-0.1, main_title_y=0.95)