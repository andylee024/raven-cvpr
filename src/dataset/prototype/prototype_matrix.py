import os
import torch

import dataset.utils.bbox_utils as bbox_utils
from dataset.utils.panel_utils import visualize_panel, generate_sample_panel



def main():
    """Create and visualize a panel of all triangles using tensor representation."""
    
    # Create output directory
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Hardcode a tensor with 9 triangles - shape (3, 3, 5)
    # Format is [exists, type, size, angle, color]
    tensor = torch.zeros((3, 3, 5), dtype=torch.int)
    
    # Set all positions to have triangles (type=1)
    from dataset.core.aot.converters import tensor_to_aot
    for row in range(3):
        for col in range(3):
            # Calculate position index
            position_idx = bbox_utils.tensor_coordinate_to_position_index(row, col)
            
            tensor[row, col, 0] = 1       # exists = True
            tensor[row, col, 1] = 1       # type = 1 (triangle)
            tensor[row, col, 2] = 3       # size = 3 (medium)
            tensor[row, col, 3] = 0       # angle = 0 (upright)
            tensor[row, col, 4] = row + 1 # color varies by row
    
    print("Created tensor with triangles:")
    print(f"Exists:\n{tensor[:,:,0]}")
    print(f"Types (1=triangle):\n{tensor[:,:,1]}")
    print(f"Sizes:\n{tensor[:,:,2]}")
    print(f"Angles:\n{tensor[:,:,3]}")
    print(f"Colors:\n{tensor[:,:,4]}")
    
    # Convert tensor to AoT
    triangle_panel = tensor_to_aot(tensor)
    
    # Print panel summary
    print("\nPanel summary:")
    triangle_panel.print_summary()
    
    # Visualize the panel
    output_path = f"{output_dir}/triangle_demo.png"
    visualize_panel(triangle_panel, output_path)
    
    return triangle_panel

if __name__ == "__main__":
    main()
