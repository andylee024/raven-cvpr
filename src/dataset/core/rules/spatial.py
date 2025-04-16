from dataset.core.rules.base import Rule
from dataset.core.tensors.tensor_transforms import (
    rotate_90_clockwise, rotate_90_counterclockwise, 
    rotate_180, shift_entities_right, shift_entities_down,
    shift_diagonal
)

class SpatialRule(Rule):
    """Base class for rules that transform entity positions."""
    
    def __init__(self, transform_type, required_panels=1, **params):
        """Initialize a spatial rule.
        
        Args:
            transform_type: Type of spatial transformation
            required_panels: Number of panels required to apply the rule
            params: Additional parameters for the transformation
        """
        super().__init__(rule_type="spatial", required_panels=required_panels)
        self.transform_type = transform_type
        self.params = params
        
    @property
    def name(self):
        """Get the rule name with transform type."""
        name = self.__class__.__name__
        if name.endswith("Rule"):
            name = name[:-4]
        return f"{name} {self.transform_type}"

# 
# Spatial Specific Rules
# 
class RotationRule(SpatialRule):
    """Rule that rotates the panel."""
    
    def __init__(self, step=1, clockwise=True):
        """Initialize rotation rule.
        
        Args:
            step: Number of 90° increments to rotate (1=90°, 2=180°, 3=270°)
            clockwise: Direction of rotation
        """
        self.step = step
        self.clockwise = clockwise
        transform_type = f"{self.step} shifts {'clockwise' if self.clockwise else 'counterclockwise'}"
        super().__init__(transform_type=transform_type)
    
    def apply(self, panels):
        """Apply rotation to the panel."""
        result = panels[0].clone()
        if self.clockwise:
            result.tensor = rotate_90_clockwise(result.tensor, self.step)
        else:
            result.tensor = rotate_90_counterclockwise(result.tensor, self.step)
            
        return result

class ShiftRule(SpatialRule):
    """Rule that shifts entities in the panel."""
    
    def __init__(self, direction="right", step=1):
        """Initialize shift rule.
        
        Args:
            direction: Direction to shift ("right", "down", "diagonal")
            step: Number of positions to shift
        """
        transform_type = f"{direction} shift by {step}"
        super().__init__(transform_type=transform_type)
        self.direction = direction
        self.step = step
    
    def apply(self, panels):
        """Apply shift to the panel."""
        result = panels[0].clone()
        
        if self.direction == "right":
            result.tensor = shift_entities_right(result.tensor, self.step)
        elif self.direction == "left":
            result.tensor = shift_entities_right(result.tensor, -self.step)
        elif self.direction == "up":
            result.tensor = shift_entities_down(result.tensor, -self.step)
        elif self.direction == "down":
            result.tensor = shift_entities_down(result.tensor, self.step)
        elif self.direction == "diagonal":
            result.tensor = shift_diagonal(result.tensor, self.step)
        elif self.direction == "reverse_diagonal":
            result.tensor = shift_diagonal(result.tensor, -self.step)
        else:
            raise ValueError(f"Invalid direction: {self.direction}")
        return result