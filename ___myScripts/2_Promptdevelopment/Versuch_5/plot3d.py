import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

def create3d_plot(y_labels, x_labels, z):
    # Map to numeric positions
    x = np.arange(len(x_labels))
    y = np.arange(len(y_labels))

    # Meshgrid
    X, Y = np.meshgrid(x, y)
    Z = np.array(z)

    # Flatten for scatter/stems
    X_flat = X.flatten()
    Y_flat = Y.flatten()
    Z_flat = Z.flatten()

    # Plot
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Define custom colormap: grey -> turquoise
    colors = [(0.5, 0.5, 0.5), (0, 1, 1)]  # grey to cyan/turquoise
    cmap_grey_turquoise = LinearSegmentedColormap.from_list("grey_turquoise", colors)

    # Scatter points
    ax.scatter(X_flat, Y_flat, Z_flat, c=Z_flat, cmap=cmap_grey_turquoise, s=30, alpha=0.9)

    # Stems
    for x_val, y_val, z_val in zip(X_flat, Y_flat, Z_flat):
        ax.plot([x_val, x_val], [y_val, y_val], [0, z_val], color=(0.25, 0.25, 0.25), linestyle='-')

    # SURFACE
    ax.plot_surface(X, Y, Z, cmap=cmap_grey_turquoise, alpha=0.4, edgecolor='none')
    ax.plot_wireframe(X, Y, Z, color=(0.25, 0.25, 0.25), linewidth=0.6, alpha=1)
    
    # Set z lim
    ax.set_zlim(0, 100)
    
    # Replace numeric ticks with string labels
    ax.set_xticks(x)
    ax.set_xticklabels(x_labels)
    for label in ax.get_xticklabels():
        label.set_horizontalalignment("left")
    ax.set_yticks(y)
    ax.set_yticklabels(y_labels)

    # ax.zaxis._axinfo["grid"]["linewidth"] = 0

    # Labels and title
    ax.set_xlabel('Generationmodel', labelpad=50)
    ax.set_ylabel('Listingmodel', labelpad=15)
    ax.set_zlabel('Hitrate', labelpad=15)
    ax.set_title('')

    ax.view_init(elev=40, azim=205)

    # --- Highlight highest value ---
    max_idx = np.unravel_index(np.argmax(Z), Z.shape)
    max_y, max_x = max_idx     # row, col
    max_val = Z[max_idx]

    # Mark it with a big red point
    ax.scatter(max_x, max_y, max_val, color="black", s=120, edgecolor="black", zorder=5)

    # Annotate with a special name
    ax.text(max_x, max_y, max_val + 5,  # a little above the point
            f"Best: {round(max_val, 2)}", color="black", fontsize=10, fontweight="bold", zorder=10, ha="center")
    
    plt.show()


    # Save figure
    savepathparts = ["___myScripts", "2_Promptdevelopment", "Versuch_5", "balken", "test.png"]
    savepath = os.path.join(*savepathparts)
    fig.savefig(savepath, bbox_inches='tight', dpi=300)

# Models
x_labels = ["Slot1", "Slot2", "Slot3", "Slot4", "Slot5"]
y_labels = ["A", "B", "C", "D", "E"]

# Z values (same structure as before)
z = [
    [0.1, 0.25, 0.33, 0.75, 0.23],
    [0.15, 0.30, 0.40, 0.65, 0.20],
    [0.20, 0.35, 0.60, 0.55, 0.18],
    [0.25, 0.45, 0.60, 0.20, 0.15],
    [0.30, 0.50, 0.70, 0.45, 0.10]
]

# create3d_plot(x_labels, y_labels, z)