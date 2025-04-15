from typing import List
from dataset.core.aot.tensor_panel import TensorPanel
from dataset.core.rules.base import Rule
from dataset.core.aot.attributes import CONSTANTS
from dataset.utils.panel_utils import add_entities_to_panel, remove_entities_from_panel

class ProgressionRule(Rule):
    """Rule that increments/decrements an attribute by a fixed step."""
    
    def __init__(self, attr_name, step=1):
        """Initialize progression rule.
        
        Args:
            attr_name: Attribute to modify ('type', 'size', etc.)
            step: Amount to increment/decrement (default: 1)
        """
        super().__init__(attr_name)
        self.step = step
     
    def apply(self, panels : List[TensorPanel]):
        """Apply progression to generate next panel."""

        if self.attribute_name in ["type", "size", "color", "angle"]:
            return self._apply_attribute_progression(panels[0])
        elif self.attribute_name == "number":
            return self._apply_number_progression(panels[0])
        else:
            raise ValueError(f"Unsupported attribute: {self.attr_name}")
    
    def _apply_attribute_progression(self, panel):
        """Apply progression to attribute attribute."""
        result = panel.clone()
        attr = result._attributes[self.attribute_name]
        
        for row in range(3):
            for col in range(3):
                if panel.exists(row, col):
                    current_value = panel.get_attr(row, col, self.attribute_name)
                    next_value = attr.next_value(current_value, self.step)
                    result.set_attr(row, col, self.attribute_name, next_value)
        
        return result

    def _apply_number_progression(self, panel):
        """Apply progression to the number of entities in the panel."""
        current_count = panel.total_entities
        target_count = current_count + self.step
        
        assert target_count >= CONSTANTS.MIN_ENTITIES.value
        assert target_count <= CONSTANTS.MAX_ENTITIES.value
        
        delta = target_count - current_count
        if delta > 0:
            return add_entities_to_panel(panel, n=delta)
        elif delta < 0:
            return remove_entities_from_panel(panel, n=abs(delta))
        else:
            return panel.clone()
