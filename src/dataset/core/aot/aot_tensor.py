import torch
from dataset.core.aot.aot_facade import AoTFacade

class AoTTensor:
    """Panel representation as a 3x3x5 tensor using PyTorch."""
    
    def __init__(self, tensor=None):
        """
        Initialize with optional tensor.
        
        Args:
            tensor: Shape (3, 3, 5) with dimensions:
                   - exists flag (0/1)
                   - type (1-5)
                   - size (1-6)
                   - angle (0-7)
                   - color (0-9)
        """
        if tensor is None:
            self.tensor = torch.zeros((3, 3, 5), dtype=torch.int)
        else:
            self.tensor = tensor.clone()
    
    def get_attribute_layer(self, attr_idx):
        """Get the layer for a specific attribute."""
        return self.tensor[:, :, attr_idx]
    
    def set_attribute_layer(self, attr_idx, values):
        """Set values for an attribute layer."""
        self.tensor[:, :, attr_idx] = values
        return self
    
    def get_entity(self, row, col):
        """Get attribute vector for entity at position."""
        return self.tensor[row, col]
    
    def set_entity(self, row, col, values):
        """Set attribute values for entity at position."""
        self.tensor[row, col] = values
        return self
    
    def has_entity(self, row, col):
        """Check if position has an entity."""
        return bool(self.tensor[row, col, 0] == 1)
    
    def to_aot(self, template=None):
        """Convert to AoTFacade."""
        from dataset.core.aot.converters import tensor_to_aot
        return tensor_to_aot(self.tensor, template)
    
    @classmethod
    def from_aot(cls, aot_facade):
        """Create from AoTFacade."""
        from dataset.core.aot.converters import aot_to_tensor
        return cls(aot_to_tensor(aot_facade))
    
    def clone(self):
        """Create a copy of this panel."""
        return AoTTensor(self.tensor.clone())
    
    def entity_positions(self):
        """Get positions of all entities as (row, col) tuples."""
        exists_mask = self.tensor[:, :, 0] == 1
        positions = torch.nonzero(exists_mask, as_tuple=True)
        return list(zip(positions[0].tolist(), positions[1].tolist()))
    
    def entity_count(self):
        """Get the total number of entities in the panel."""
        return torch.sum(self.tensor[:, :, 0]).item()
    
    def apply_to_attribute(self, attr_idx, func):
        """Apply a function to all entity values of a specific attribute."""
        exists_mask = self.tensor[:, :, 0] == 1
        self.tensor[exists_mask, attr_idx] = func(self.tensor[exists_mask, attr_idx])
        return self
    
    def to_numpy(self):
        """Convert tensor to numpy array for compatibility."""
        return self.tensor.cpu().numpy()
    
    @classmethod
    def from_numpy(cls, numpy_array):
        """Create from numpy array."""
        tensor = torch.from_numpy(numpy_array)
        return cls(tensor)
    
    def __repr__(self):
        """String representation showing panel dimensions and entity count."""
        return f"TensorPanel(entities={self.entity_count()}, shape={tuple(self.tensor.shape)})"
