import copy
from dataset.core.rules.base import Rule

class ProgressionRule(Rule):
    """Rule that creates a progression on an attribute.
    
    For example, a ProgressionRule on "Number" with value=1 will 
    increase the number of entities by 1 in each subsequent panel.
    """
    
    def __init__(self, attr, value, component_idx=0):
        """Initialize a progression rule.
        
        Args:
            attr (str): The attribute to apply progression to
            value (int): The progression value (e.g., +1, -1)
            component_idx (int): The component to apply this rule to
        """
        super().__init__(attr, value, component_idx)
        self.state["first_col"] = True  # Flag for tracking first application
        self.name = "Progression" # Maintains backwards compatibility
    
    def apply(self, source_panel, target_panel=None):
        """Apply progression to generate the next panel.
        
        Args:
            source_panel: The source panel AoT
            target_panel: Optional pre-existing target panel
            
        Returns:
            The modified target panel AoT
        """
        # Get the layouts
        source_layout = self._get_layout(source_panel)
        
        # Create a copy of the target if it's not provided
        target_panel = self._copy_if_none(source_panel, target_panel)
        target_layout = self._get_layout(target_panel)
        
        # Apply progression based on attribute type
        if self.attr == "Number":
            self._apply_to_number(source_layout, target_layout)
        elif self.attr == "Position":
            self._apply_to_position(target_layout)
        elif self.attr in ["Type", "Size", "Color"]:
            self._apply_to_entity_attribute(source_layout, target_layout, self.attr.lower())
        else:
            raise ValueError(f"Unsupported attribute: {self.attr}")
        
        # Toggle the first_col flag for the next application
        self.state["first_col"] = not self.state["first_col"]
        
        return target_panel
    
    def apply_rule(self, source_panel, target_panel=None):
        return self.apply(source_panel, target_panel)
    
    def _apply_to_number(self, source_layout, target_layout):
        """Apply progression to the Number attribute.
        
        Args:
            source_layout: The source layout node
            target_layout: The target layout node to modify
        """
        # Update number value level
        target_layout.number.set_value_level(target_layout.number.get_value_level() + self.value)
        
        # Update position based on new number
        target_layout.position.sample(target_layout.number.get_value())
        pos = target_layout.position.get_value()
        
        # Clear existing entities and create new ones
        del target_layout.children[:]
        for i in range(len(pos)):
            # Copy the first entity from source and adjust its properties
            entity = copy.deepcopy(source_layout.children[0])
            entity.name = str(i)
            entity.bbox = pos[i]
            
            # Resample entity attributes if not uniform
            if not source_layout.uniformity.get_value():
                entity.resample()
                
            target_layout.insert(entity)
    
    def _apply_to_position(self, target_layout):
        """Apply progression to the Position attribute.
        
        Args:
            target_layout: The target layout node to modify
        """
        # Calculate new position index
        position_values_length = len(target_layout.position.values)
        current_idx = target_layout.position.get_value_idx()
        second_pos_idx = (current_idx + self.value) % position_values_length
        target_layout.position.set_value_idx(second_pos_idx)
        
        # Update entity positions
        second_bbox = target_layout.position.get_value()
        for i in range(len(second_bbox)):
            target_layout.children[i].bbox = second_bbox[i]
    
    def _apply_to_entity_attribute(self, source_layout, target_layout, attr_name):
        """Apply progression to an entity attribute (Type, Size, Color).
        
        Args:
            source_layout: The source layout node
            target_layout: The target layout node to modify
            attr_name: The attribute name in lowercase
        """
        # Get current value level from first entity
        old_value_level = getattr(source_layout.children[0], attr_name).get_value_level()
        
        # Enforce consistency if needed
        if self.state["first_col"] and not source_layout.uniformity.get_value():
            for entity in source_layout.children:
                getattr(entity, attr_name).set_value_level(old_value_level)
        
        # Update the attribute for all entities in the target
        for entity in target_layout.children:
            getattr(entity, attr_name).set_value_level(old_value_level + self.value)
