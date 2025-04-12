from dataset.core.operations.base import Operation
from dataset.const import ANGLE_VALUES

class AngleAddition(Operation):
    """Adds angle values (rotation)"""
    def apply(self, first_value, second_value):
        max_angles = len(ANGLE_VALUES)
        return (first_value + second_value) % max_angles
        
    def adjust_constraints(self, constraints, first_value):
        """No adjustment needed for angle constraints"""
        return constraints  # Angles can cycle, so constraints remain the same
        
class AngleSubtraction(Operation):
    """Subtracts angle values (reverse rotation)"""
    def apply(self, first_value, second_value):
        max_angles = len(ANGLE_VALUES)
        return (first_value - second_value) % max_angles
        
    def adjust_constraints(self, constraints, first_value):
        """No adjustment needed for angle constraints"""
        return constraints  # Angles can cycle, so constraints remain the same
