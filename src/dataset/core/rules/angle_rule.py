import copy
from dataset.core.handlers.angle_handler import AngleHandler
from dataset.core.operations.angle_operations import AngleAddition, AngleSubtraction
from dataset.legacy.const import ANGLE_VALUES

class AngleRule:
    """Rule specifically for angle rotation"""
    
    def __init__(self, value=1, component_idx=0):
        """Initialize with rotation value and component index"""
        self.value = value
        self.component_idx = component_idx
        self.handler = AngleHandler()
        self.operation = AngleAddition() if value > 0 else AngleSubtraction()
        self.state = {"memory": None}
        self.attr = "Angle"  # For compatibility with existing code
        self.name = "Angle" # For compatibility with existing code
        
    def apply_rule(self, source, target=None):
        """Apply angle rotation rule (compatible with existing interface)"""
        return self.apply(source, target)
        
    def apply(self, source, target=None):
        """Apply angle rotation to generate next panel"""
        if target is None:
            target = copy.deepcopy(source)
            
        source_layout = self._get_layout(source)
        target_layout = self._get_layout(target)
        
        # First application: store angle and set target angle
        if self.state["memory"] is None:
            first_value = self.handler.get_value(source_layout)
            self.state["memory"] = first_value
            
            # For angles, we don't need to adjust constraints
            # Just set a new angle directly
            new_angle = (first_value + self.value) % len(ANGLE_VALUES)
            self.handler.set_value(target_layout, new_angle)
        
        # Second application: calculate from memory and apply
        else:
            first_value = self.state["memory"]
            second_value = self.handler.get_value(source_layout)
            
            # Calculate result using operation
            result = self.operation.apply(first_value, second_value)
            
            # Apply result to target
            self.handler.set_value(target_layout, result)
            
            # Reset for next row
            self.state["memory"] = None
            
        return target
        
    def _get_layout(self, panel):
        """Extract layout from panel"""
        return panel.children[0].children[self.component_idx].children[0]
