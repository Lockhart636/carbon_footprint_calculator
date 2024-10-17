import matplotlib.pyplot as plt
import numpy as np

# Helper function to calculate text position for labels outside wedges
def calculate_external_text_position(wedge, pct_distance=1.4):
    angle = (wedge.theta2 + wedge.theta1) / 2
    angle_rad = np.deg2rad(angle)
    x = pct_distance * np.cos(angle_rad)
    y = pct_distance * np.sin(angle_rad)
    return x, y

# Function to adjust the positions of outside labels to avoid overlap
def adjust_label_positions(label_positions, y_spacing=0.2):
    # Sort positions by their y-values
    label_positions.sort(key=lambda pos: pos[1])
    for i in range(1, len(label_positions)):
        prev_x, prev_y = label_positions[i - 1]
        curr_x, curr_y = label_positions[i]
        # If the current label is too close to the previous one
        if abs(curr_y - prev_y) < y_spacing:
            # Adjust the current label's y position to increase the gap
            label_positions[i] = (curr_x, prev_y + y_spacing)
    return label_positions

# Function to plot pie charts with external labels for small sectors and avoid overlap
def plot_pie_charts(data, custom_offsets=None, custom_line_offsets=None, custom_line_lengths=None,
                    legend_distance=1.1, title_size=25, name_text_size=20, wedge_gap=1,
                    pct_distance=0.7, min_pct=5, title_y=-0.05, main_title_y=0.95, label_distance=1.5,
                    y_spacing=0.2, fixed_start_distance=0.9):
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))  # 3 subplots for each individual
    fig.suptitle('Diet Breakdown', fontsize=title_size, fontweight='bold', y=main_title_y)

    # Define colors (you can customize)
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0', '#ffb3e6', '#c4e17f']

    # Define hatches for black-and-white printing
    hatches = ['x', '-', '/', '\\', '|', '+', 'o']

    # Set default custom offsets if none provided
    if custom_offsets is None:
        custom_offsets = {}

    if custom_line_offsets is None:
        custom_line_offsets = {}

    if custom_line_lengths is None:
        custom_line_lengths = {}

    # Loop over each individual and plot their pie chart
    for ax, (name, activities) in zip(axs, data.items()):
        labels = list(activities.keys())
        values = list(activities.values())

        wedges, texts = ax.pie(values, labels=None, colors=colors,
                               startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'},
                               pctdistance=pct_distance,
                               wedgeprops={'edgecolor': 'white', 'linewidth': wedge_gap})

        ax.set_title(name, fontsize=name_text_size, fontweight='bold', y=title_y)

        total_value = sum(values)
        small_label_positions = []  # List to store positions for external labels
        small_labels = []  # List to store actual labels for external labels

        # Loop through each wedge to set the percentage label
        for i, wedge in enumerate(wedges):
            wedge.set_hatch(hatches[i % len(hatches)])  # Cycle through hatches

            pct = 100. * values[i] / total_value

            if pct < 0.1:  # Skip very small values including "0.0%"
                continue

            # Apply custom offsets if provided
            x_offset, y_offset = custom_offsets.get((name, labels[i]), (0, 0))
            line_x_offset, line_y_offset = custom_line_offsets.get((name, labels[i]), (0, 0))
            line_length = custom_line_lengths.get((name, labels[i]), 1.0)  # Length of external portion

            if pct < min_pct:  # For small sectors, place label outside
                # External label position
                x, y = calculate_external_text_position(wedge, pct_distance=label_distance)
                x += x_offset  # Apply custom x offset for label
                y += y_offset  # Apply custom y offset for label

                small_label_positions.append((x, y))
                small_labels.append(f'{pct:.1f}%')

                # Calculate the start point of the dashed line (fixed within the pie boundary)
                angle_rad = np.deg2rad((wedge.theta2 + wedge.theta1) / 2)
                line_start_x = fixed_start_distance * np.cos(angle_rad)
                line_start_y = fixed_start_distance * np.sin(angle_rad)

                # Calculate the end point of the dashed line, modifying only the external portion
                line_end_x = line_start_x + (x - line_start_x) * line_length + line_x_offset
                line_end_y = line_start_y + (y - line_start_y) * line_length + line_y_offset

                # Plot the dashed line
                ax.plot([line_start_x, line_end_x], [line_start_y, line_end_y], color='black', linestyle='dashed')

            else:
                # Regular label placement inside the wedge
                x, y = calculate_external_text_position(wedge, pct_distance=0.6)
                x += x_offset  # Apply custom x offset
                y += y_offset  # Apply custom y offset
                ax.text(x, y, f'{pct:.1f}%', ha='center', va='center', fontsize=15, fontweight='bold')

        # Adjust small sector label positions to avoid overlap
        small_label_positions = adjust_label_positions(small_label_positions, y_spacing=y_spacing)

        # Plot the small sector labels with adjusted positions
        for (x, y), label in zip(small_label_positions, small_labels):
            ax.text(x, y, label, ha='center', va='center', fontsize=15, fontweight='bold')

    # Set legend for each pie chart
    fig.legend(labels, loc='center left', bbox_to_anchor=(0.8, 0.5), fontsize=15, handlelength=2, handleheight=2,
               markerscale=2)

    plt.tight_layout(rect=[0, 0, 0.75, 0.95])

    # Save the figure as a PNG image with bbox_inches to ensure no cutoffs
    fig.savefig('carbon_footprint_diet.png', bbox_inches='tight')

    # Save the figure as a SVG image with bbox_inches to ensure no cutoffs
    fig.savefig('carbon_footprint_diet.svg', bbox_inches='tight')
    plt.show()

# Data for food consumption
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

# Custom offsets for specific labels (x_offset, y_offset)
custom_offsets = {
    ('Jonathan', 'Fish'): (0.1, 0),  # Move Fish label right by 0.1
    ('Jonathan', 'Poultry'): (0.1, 0.1),  # Move Poultry label right by 0.1 and up by 0.1
    ('Jonathan', 'Pasta'): (-0.3, 0),  # Move Pasta label left by 0.3
    ('Jonathan', 'Rice'): (0.4, 0),  # Move Rice label right by 0.4
    ('Connor', 'Fish'): (0.2, -0.05),  # Move Fish label right by 0.2
    ('Connor', 'Pasta'): (-0.3, 0),  # Move Pasta label left by 0.3
    ('Connor', 'Rice'): (0.4, 0),  # Move Rice label right by 0.4
    ('Agnel', 'Potatoes'): (0.3, 0),  # Move Potatoes label right by 0.3
}

# Custom line offsets for specific labels (x_offset, y_offset)
custom_line_offsets = {
    ('Jonathan', 'Pasta'): (0.1, 0),  # Adjust the dashed line for Pasta
    ('Jonathan', 'Rice'): (0, 0),  # Adjust the dashed line for Pasta
    ('Connor', 'Fish'): (0.2, 0),  # Adjust the dashed line for Fish
    ('Connor', 'Rice'): (0, 0),  # Adjust the dashed line for Fish
    ('Connor', 'Pasta'): (0, 0.1),  # Adjust the dashed line for Fish
    ('Agnel', 'Potatoes'): (-0.1, -0.05),  # Adjust the dashed line for Potatoes
}

# Custom dashed line lengths for specific labels (external portion only)
custom_line_lengths = {
    ('Jonathan', 'Pasta'): 1.7,  # Make the dashed line for Pasta a bit longer
    ('Jonathan', 'Rice'): 0.7,  # Adjust the dashed line for Pasta
    ('Connor', 'Fish'): 0.2,  # Make the dashed line for Fish a bit longer
    ('Connor', 'Rice'): 0.7,  # Adjust the dashed line for Fish
    ('Connor', 'Pasta'): 1.3,  # Adjust the dashed line for Fish
    ('Agnel', 'Potatoes'): 0.9,  # Make the dashed line for Potatoes shorter
}

# Call the function to plot pie charts with custom label distance, offsets, and control over dashed lines
plot_pie_charts(data, custom_offsets=custom_offsets, custom_line_offsets=custom_line_offsets,
                custom_line_lengths=custom_line_lengths, label_distance=1.2, y_spacing=0.15, fixed_start_distance=0.85)