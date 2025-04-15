from typing import List
import torch

from dataset.core.aot.tensor_panel import TensorPanel
from dataset.core.rules.base import Rule
from dataset.utils.entity_utils import sample_entity_tensor

class ArithmeticRule(Rule):
    """Rule that combines color or size values from two panels by tensor operations."""
    
    def __init__(self, attr_name, operation="add"):
        """Initialize arithmetic rule.
        
        Args:
            attr_name: Attribute to modify ('type', 'size', 'color', etc.)
            operation: "add" or "subtract" (default: "add")
        """
        if attr_name not in ["size", "color"]:
            raise ValueError(f"ArithmeticRule only supports 'size' or 'color', got {attr_name}")

        super().__init__(attr_name, required_panels=2)
        self.operation = operation

    def apply(self, panels: List[TensorPanel]):
        """Apply arithmetic operation between panels."""
        if len(panels) < 2:
            raise ValueError(f"ArithmeticRule requires 2 panels, got {len(panels)}")
        
        panel1, panel2 = panels[0], panels[1]
        result = self._apply_attribute_arithmetic(panel1, panel2)
        return result
    
    def _apply_attribute_arithmetic(self, panel1, panel2):
        """Apply arithmetic operation between two panels."""

        panel1_tensor = panel1.tensor
        panel2_tensor = panel2.tensor

        # Create a mask for positions where entities exist in both panels
        mask = (panel1_tensor[:, :, 0] == 1) & (panel2_tensor[:, :, 0] == 1)
        
        # For positions where both entities exist
        result_tensor = torch.zeros_like(panel1_tensor)
        for row in range(3):
            for col in range(3):
                if mask[row, col]:
                    
                    if self.operation == "add":
                        new_val = (panel1.tensor[row, col, self.attribute_index] + 
                                  panel2.tensor[row, col, self.attribute_index]) % (self.attribute_max + 1)

                    elif self.operation == "subtract":
                        new_val = (panel1.tensor[row, col, self.attribute_index] - 
                                  panel2.tensor[row, col, self.attribute_index]) % (self.attribute_max + 1)

                    if self.attribute_name == "type":
                        entity = sample_entity_tensor(shape_type=new_val)
                    elif self.attribute_name == "size":
                        entity = sample_entity_tensor(size=new_val)
                    elif self.attribute_name == "color":
                        entity = sample_entity_tensor(color=new_val)
                    elif self.attribute_name == "angle":
                        entity = sample_entity_tensor(angle=new_val)
                    
                    result_tensor[row, col] = entity
        
        return TensorPanel(result_tensor)
    
    def _apply_number_arithmetic(self, panel1, panel2):
        """Apply arithmetic operation to the number of entities."""
        raise NotImplementedError("Number arithmetic is not implemented yet.")
    
    @property
    def name(self):
        """Get the rule name."""
        op_symbol = "+" if self.operation == "add" else "-"
        return f"Arithmetic({self.attr_name} {op_symbol})"
