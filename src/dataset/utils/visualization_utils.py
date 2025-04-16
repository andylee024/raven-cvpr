import os
import matplotlib.pyplot as plt
import numpy as np


def visualize_comparison(panels, titles, filename, output_dir="output_tests"):
    """Visualize panels side by side for comparison."""
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Calculate grid dimensions
    n_panels = len(panels)
    if n_panels <= 4:
        n_cols = n_panels
        n_rows = 1
    else:
        n_cols = 4
        n_rows = (n_panels + 3) // 4  # Ceiling division
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(5*n_cols, 5*n_rows))
    
    # Handle case of single panel (which would make axes not iterable)
    if n_panels == 1:
        axes = np.array([axes])
    
    # Make axes a 2D array for consistent indexing
    if n_rows == 1:
        axes = axes.reshape(1, -1)
    
    # Plot each panel
    for i, (panel, title) in enumerate(zip(panels, titles)):
        row, col = i // n_cols, i % n_cols
        ax = axes[row, col]
        
        # Convert to AoT for visualization
        aot_panel = panel.to_aot()
        
        # Render the panel
        from dataset.legacy.rendering import render_panel
        img = render_panel(aot_panel.raw)
        
        # Display the image
        ax.imshow(img, cmap='gray')
        ax.set_title(title)
        
        # Remove ticks but keep border
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color('black')
            spine.set_linewidth(2)
    
    # Hide any unused subplots
    for i in range(len(panels), n_rows * n_cols):
        row, col = i // n_cols, i % n_cols
        axes[row, col].axis('off')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, filename), dpi=150)
    plt.close()
    print(f"Saved comparison to {os.path.join(output_dir, filename)}")