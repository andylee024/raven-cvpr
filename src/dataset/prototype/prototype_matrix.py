import copy
import os
import numpy as np
from dataset.core.aot.aot_facade import AoTFacade
from dataset.core.aot.entity_facade import EntityFacade
from dataset.core.puzzle_generator import PuzzleGenerator
from dataset.legacy.AoT import Entity
from dataset.utils.panel_utils import generate_sample_panel, visualize_panel


def create_sample_aot():
    """
    Create a distribute_nine panel with exactly 9 entities.
    
    Returns:
        AoTFacade instance containing a panel with 9 entities
    """
    # First try to generate a panel with 9 entities naturally
    max_attempts = 5
    for _ in range(max_attempts):
        generator = PuzzleGenerator()
        puzzle = generator.generate("distribute_nine")
        if puzzle:
            panel = puzzle['context'][0]  # Take the first context panel
            facade = AoTFacade(panel)
            
            # Check if panel already has 9 entities
            if facade.get_entity_count() == 9:
                return facade
    
    # If we couldn't get one naturally, modify a panel to have 9 entities
    generator = PuzzleGenerator()
    puzzle = generator.generate("distribute_nine")
    panel = puzzle['context'][0]  # Take the first context panel
    
    # Get the layout node
    layout = panel.children[0].children[0].children[0]
    
    # Current number of entities
    current_count = len(layout.children)
    
    if current_count < 9:
        # Need to add entities until we have 9
        # Get the position constraints from layout
        position = layout.position
        
        # Reset number to 9 
        layout.number.set_value_level(9-1)  # 0-indexed so 9 is at index 8
        
        # Resample positions for 9 entities
        position.sample(9)
        
        # Create/update entities based on uniformity setting
        # is_uniform = layout.uniformity.get_value() == 1
        layout.uniformity.set_value_level(1)
        is_uniform = True
        
        # Clear existing entities to create a fresh set
        existing_entities = []
        for i in range(min(current_count, 9)):
            existing_entities.append(layout.children[i])
        
        # Clear all children
        layout.children = []
        
        # Get position values
        positions = position.get_value()
        
        # Use an existing entity as template if available
        template_entity = None
        if existing_entities:
            template_entity = existing_entities[0]
        
        # Create 9 entities
        for i in range(9):
            if i < len(existing_entities):
                # Use existing entity
                entity = existing_entities[i]
                entity.bbox = positions[i]
                layout.children.append(entity)
            else:
                # Create new entity
                if template_entity:
                    # Clone template entity
                    entity = copy.deepcopy(template_entity)
                    entity.name = str(i)
                    entity.bbox = positions[i]
                    if not is_uniform:
                        entity.resample()  # Randomize attributes if not uniform
                else:
                    # Create entity from scratch using constraints
                    entity = Entity(name=str(i), 
                                   bbox=positions[i], 
                                   entity_constraint=layout.entity_constraint)
                layout.children.append(entity)
    
    # Wrap in AoTFacade and return
    return AoTFacade(panel)

def aot_to_matrix(aot_facade):
    """
    Convert an AoTFacade panel into a 3x3xd matrix representation.
    
    Args:
        aot_facade: AoTFacade instance representing a panel
        
    Returns:
        Numpy array with shape (3, 3, 3) where:
        - First two dimensions (3,3) represent a grid of entities
        - Third dimension (3) represents attributes [type, size, angle]
        
    Note: Empty grid positions will be filled with zeros
    """
    # Initialize 3x3 matrix with zeros
    # Each cell has 3 attributes (type, size, angle)
    matrix = np.zeros((3, 3, 3), dtype=int)
    
    # Get all entities from the panel
    entities = aot_facade.get_entities()
    
    # Populate matrix with entity data
    # For simplicity, we'll arrange entities in a grid (row by row)
    for i, entity in enumerate(entities):
        if i >= 9:  # Only handle up to 9 entities (3x3 grid)
            break
            
        # Calculate row and column position
        row = i // 3
        col = i % 3
        
        # Fill matrix with entity attributes
        matrix[row, col, 0] = entity.get_type()   # Shape
        matrix[row, col, 1] = entity.get_size()   # Size
        matrix[row, col, 2] = entity.get_angle()  # Angle
    
    return matrix

def matrix_to_aot(matrix, template_panel=None):
    """
    Convert a matrix representation back to an AoTFacade panel.
    
    Args:
        matrix: Numpy array with shape (3, 3, 3)
        template_panel: Optional template panel to use for creating the new panel
                       (preserves positions, colors, or other properties)
    
    Returns:
        AoTFacade instance
    """
    # Create template panel if not provided
    if template_panel is None:
        # Count non-zero cells to determine number of entities
        entity_positions = np.where(np.sum(matrix, axis=2) > 0)
        n_entities = len(entity_positions[0])
        template_panel = AoTFacade.create_test_panel(num_entities=n_entities)
    
    # Clone the template panel
    panel = template_panel.clone()
    
    # Get all entities from the panel
    entities = panel.get_entities()
    entity_count = len(entities)
    
    # Populate entities with matrix data
    entity_idx = 0
    for row in range(3):
        for col in range(3):
            # Check if this cell has entity data (any non-zero attribute)
            if np.sum(matrix[row, col]) > 0:
                if entity_idx < entity_count:
                    # Set entity attributes
                    entities[entity_idx].set_type(int(matrix[row, col, 0]))
                    entities[entity_idx].set_size(int(matrix[row, col, 1]))
                    entities[entity_idx].set_angle(int(matrix[row, col, 2]))
                    entity_idx += 1
    
    return panel

def create_triangle_panel():
    """
    Create a panel with 9 entities, all set to be triangles.
    
    Returns:
        AoTFacade instance with 9 triangle entities
    """
    # 1. Create a sample panel with 9 entities
    panel = create_sample_aot()
    
    # 2. Convert to matrix representation
    matrix = aot_to_matrix(panel)
    
    # 3. Set all entity types to triangle (type 1)
    # Find all non-empty cells (where at least one attribute is non-zero)
    non_empty_mask = np.sum(matrix, axis=2) > 0
    
    # Set type to 1 (triangle) for all non-empty cells
    matrix[non_empty_mask, 0] = 1
    
    # 4. Convert back to panel
    triangle_panel = matrix_to_aot(matrix, panel)
    
    return triangle_panel


def main():
    # 1. Generate a sample panel
    panel = generate_sample_panel()
    # panel = create_triangle_panel()

    # 2. Print the panel summary
    print("Panel Summary:")
    print("-" * 50)
    panel.print_summary(verbose=True)
    print("-" * 50)

    # 3. Convert to matrix form
    matrix = aot_to_matrix(panel)

    # 4. Print the matrix representation
    print("\nMatrix Representation (3x3x3):")
    print("-" * 50)
    print("Format: [type, size, angle]")
    print("-" * 50)

    # Print matrix in a more readable format
    for row in range(3):
        for col in range(3):
            attributes = matrix[row, col]
            # Skip empty cells (all zeros)
            if np.sum(attributes) > 0:
                print(f"Position [{row},{col}]: {attributes} (type={attributes[0]}, size={attributes[1]}, angle={attributes[2]})")
            else:
                print(f"Position [{row},{col}]: Empty")
        print("-" * 30)

    # 5. Show a more compact representation
    print("\nCompact Matrix View:")
    print("-" * 50)
    print("Type values:")
    print(matrix[:,:,0])
    print("\nSize values:")
    print(matrix[:,:,1])
    print("\nAngle values:")
    print(matrix[:,:,2])

    # 5. Visualize the original panel
    output_dir = "output/matrix_demo"
    os.makedirs(output_dir, exist_ok=True)
    original_path = f"{output_dir}/original_panel.png"
    visualize_panel(panel, original_path)

    # 6. Create a transformed panel by rotating all shapes
    transformed_matrix = matrix.copy()
    
    # Apply rotation: add 2 to all angles and take modulo 8
    # transformed_matrix[:,:,2] = (matrix[:,:,2] + 2) % 8
   
    # Apply transform : change all shapes to triangles
    transformed_matrix[:,:,0] = 1

    # 7. Convert the transformed matrix back to a panel
    transformed_panel = matrix_to_aot(transformed_matrix, panel)

    # 8. Visualize the transformed panel
    transformed_path = f"{output_dir}/transformed_panel.png"
    visualize_panel(transformed_panel, transformed_path)

    print(f"\nOriginal panel visualization saved to: {original_path}")
    print(f"Transformed panel visualization saved to: {transformed_path}")



if __name__ == "__main__":
    main()
