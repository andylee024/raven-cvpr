import torch
from dataset.core.aot.converters import tensor_to_aot
from dataset.core.aot.attributes import ATTRIBUTES

class TensorPanel:
    """Represents a panel using tensor representation."""
    
    def __init__(self, tensor=None):
        """Initialize with optional tensor (3,3,5)."""
        if tensor:
            self.tensor = tensor
        else:
            self.tensor = torch.zeros((3, 3, 5), dtype=torch.int)
        self._attributes = ATTRIBUTES

    # Attribute access 
    def get_attr(self, row, col, attr_name):
        """Get attribute value level."""
        attr = self._attributes[attr_name]
        return self.tensor[row, col, attr.index].item()
    
    def set_attr(self, row, col, attr_name, value):
        """Set attribute value level with validation."""
        attr = self._attributes[attr_name]
        valid_value = attr.validate(value)
        self.tensor[row, col, attr.index] = valid_value
        return self

    def get_attr_categorical(self, row, col, attr_name):
        """Get categorical value for attribute."""
        attr = self._attributes[attr_name]
        value_level = self.tensor[row, col, attr.index].item()
        return attr.to_categorical(value_level)

     # Type-specific convenience methods
    def get_shape(self, row, col):
        """Get type as string name (triangle, square, etc.)."""
        return self.get_attr_categorical(row, col, 'type')
    
    def get_angles(self, row, col):
        """Get angle in degrees (0-315)."""
        return self.get_attr_categorical(row, col, 'angle')
    
    def get_size(self, row, col):
        """Get size as float (0.4-0.9)."""
        return self.get_attr_categorical(row, col, 'size')
    
    def get_color(self, row, col):
        """Get color as string name (red, green, etc.)."""
        return self.get_attr_categorical(row, col, 'color')

    # Transformation utility
    def to_aot(self):
        """Convert to AoT for visualization."""
        return tensor_to_aot(self.tensor)
    
    def clone(self):
        return TensorPanel(self.tensor.clone())

