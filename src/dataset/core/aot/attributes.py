class Attribute:
    """Define an attribute with mappings between index values and actual values."""
    def __init__(self, name, index, min_val, max_val, value_map=None):
        self.name = name
        self.index = index          # Position in tensor
        self.min_val = min_val      # Minimum value this attribute can take on
        self.max_val = max_val      # Maximum value this attribute can take on
        self.value_map = value_map  # Maps value levels to actual values 
    
    def validate(self, value):
        """Returns true if input value is between min and max value."""
        possible_values = list(self.value_map.keys())
        if value not in possible_values:
            raise ValueError(f"Invalid value: {value} for attribute: {self.name}. Possible values: {possible_values}. Categorical values: {self.value_map.values()}")
        return value
    
    def next_value(self, value, step=1):
        """Get next value with wrapping within range."""
        range_size = self.max_val - self.min_val + 1
        return self.min_val + ((value - self.min_val + step) % range_size)
    
    def to_categorical(self, value_level):
        """Convert value level to categorical value."""
        if self.value_map and value_level in self.value_map:
            return self.value_map[value_level]
        return value_level
    
    def from_categorical(self, categorical_value):
        """Convert categorical value to value level."""
        if self.value_map:
            # Create reverse mapping
            reverse_map = {v: k for k, v in self.value_map.items()}
            if categorical_value in reverse_map:
                return reverse_map[categorical_value]
        return categorical_value  # Default to the value itself if not found

# Define standard attributes
import dataset.legacy.const as const
from enum import Enum

class CONSTANTS(Enum):
    """Enum representation of attribute constants"""
    TYPE_MIN = const.TYPE_MIN + 1
    TYPE_MAX = const.TYPE_MAX
    SIZE_MIN = const.SIZE_MIN
    SIZE_MAX = const.SIZE_MAX
    ANGLE_MIN = const.ANGLE_MIN
    ANGLE_MAX = const.ANGLE_MAX
    COLOR_MIN = const.COLOR_MIN
    COLOR_MAX = const.COLOR_MAX

ATTRIBUTES = {
    'exists': Attribute(name='exists', 
                        index=0, min_val=0, 
                        max_val=1, value_map={0: False, 1: True}),
    'type': Attribute(name='type', index=1, # min value +1 b/c you don't want empty
                      min_val=CONSTANTS.TYPE_MIN.value+1, max_val=CONSTANTS.TYPE_MAX.value, 
                      value_map={1: 'triangle', 2: 'square', 3: 'pentagon', 4: 'hexagon', 5: 'circle'}),
    'size': Attribute(name='size', index=2, 
                      min_val=CONSTANTS.SIZE_MIN.value, max_val=CONSTANTS.SIZE_MAX.value, 
                      value_map={0: 0.4, 1: 0.5, 2: 0.6, 3: 0.7, 4: 0.8, 5: 0.9}),
    'angle': Attribute(name='angle', index=3, 
                       min_val=CONSTANTS.ANGLE_MIN.value, max_val=CONSTANTS.ANGLE_MAX.value, 
                       value_map={0: 0, 1: 45, 2: 90, 3: 135, 4: 180, 5: 225, 6: 270, 7: 315}),
    'color': Attribute(name='color', index=4, 
                       min_val=CONSTANTS.COLOR_MIN.value, max_val=CONSTANTS.COLOR_MAX.value, 
                       value_map={0: 'red', 1: 'green', 2: 'blue', 3: 'yellow', 4: 'purple', 5: 'orange', 6: 'pink', 7: 'brown', 8: 'gray', 9: 'black'})
}
