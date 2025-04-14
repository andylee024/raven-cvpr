import random
import torch
from dataset.core.aot.tensor_panel import TensorPanel
from dataset.core.aot.attributes import ATTRIBUTES, CONSTANTS

class ConstrainedPanelSampler:
    """Samples panels that satisfy given constraints."""
    
    def __init__(self, constraints):
        """
        Initialize with constraints configuration.
        
        Args:
            constraints: Dictionary with min_entities, max_entities, and attribute_ranges
        """
        self.constraints = constraints
    
    def sample_panel(self) -> TensorPanel:
        """
        Generate a panel that satisfies all constraints.
        
        Returns:
            TensorPanel with randomly generated entities conforming to constraints
        """
        # Create empty panel
        panel = TensorPanel()
        
        # Determine entity count within constraints
        n_entities = random.randint(
            self.constraints["min_entities"], 
            self.constraints["max_entities"]
        )
        
        # Sample random positions for entities
        all_positions = [(r, c) for r in range(3) for c in range(3)]
        entity_positions = random.sample(all_positions, n_entities)
        
        # Add entities at sampled positions
        for row, col in entity_positions:
            # Set exists to 1
            panel.set_attr(row, col, 'exists', 1)
            
            # Set other attributes according to constraints
            for attr_name, range_dict in self.constraints["attribute_ranges"].items():
                if attr_name in ATTRIBUTES:
                    min_val = range_dict["min"]
                    max_val = range_dict["max"]
                    attr_value = random.randint(min_val, max_val)
                    panel.set_attr(row, col, attr_name, attr_value)
        
        return panel
    
    def sample_entity_tensor(self):
        """
        Sample a single entity tensor conforming to constraints.
        
        Returns:
            Tensor with shape (5,) representing [exists, type, size, angle, color]
        """
        entity_tensor = torch.zeros(5, dtype=torch.int)
        
        # Set exists to 1
        entity_tensor[0] = 1
        
        # Set other attributes according to constraints
        ranges = self.constraints["attribute_ranges"]
        
        # Type (index 1)
        entity_tensor[1] = random.randint(
            ranges.get("type", {"min": CONSTANTS.TYPE_MIN.value, "max": CONSTANTS.TYPE_MAX.value})["min"],
            ranges.get("type", {"min": CONSTANTS.TYPE_MIN.value, "max": CONSTANTS.TYPE_MAX.value})["max"]
        )
        
        # Size (index 2)
        entity_tensor[2] = random.randint(
            ranges.get("size", {"min": CONSTANTS.SIZE_MIN.value, "max": CONSTANTS.SIZE_MAX.value})["min"],
            ranges.get("size", {"min": CONSTANTS.SIZE_MIN.value, "max": CONSTANTS.SIZE_MAX.value})["max"]
        )
        
        # Angle (index 3)
        entity_tensor[3] = random.randint(
            ranges.get("angle", {"min": CONSTANTS.ANGLE_MIN.value, "max": CONSTANTS.ANGLE_MAX.value})["min"],
            ranges.get("angle", {"min": CONSTANTS.ANGLE_MIN.value, "max": CONSTANTS.ANGLE_MAX.value})["max"]
        )
        
        # Color (index 4)
        entity_tensor[4] = random.randint(
            ranges.get("color", {"min": CONSTANTS.COLOR_MIN.value, "max": CONSTANTS.COLOR_MAX.value})["min"],
            ranges.get("color", {"min": CONSTANTS.COLOR_MIN.value, "max": CONSTANTS.COLOR_MAX.value})["max"]
        )
        
        return entity_tensor
