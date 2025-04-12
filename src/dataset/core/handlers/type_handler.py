from dataset.core.handlers.base import AttributeHandler

class TypeHandler():
    """Handler for the Type attribute (shapes)"""
    
    def get_value(self, facade, component_idx=0, entity_idx=None):
        """Get type value from entities"""
        #self._check_facade(facade)
        
        if entity_idx is not None:
            # Get type for specific entity
            return facade.get_entity_attribute("type", component_idx, entity_idx)
        
        else:
            # Get type for first entity or default value
            if facade.get_entity_count(component_idx) > 0:
                return facade.get_entity_attribute("type", component_idx, 0)
            return 1  # Default type (triangle)
        
    def set_entity_value(self, facade, value, component_idx=0, entity_idx=0):
        """Set type value for a specific entity.
        
        Args:
            facade: AoTFacade instance
            value: New type value (1-5)
            component_idx: Component index
            entity_idx: Entity index
            
        Returns:
            The facade for method chaining
        """
        # self._check_facade(facade)
        
        # Ensure value is within valid range (1-5 for shapes)
        value = max(1, min(5, value))
        
        try:
            # Use the facade to set the attribute value for a specific entity
            facade.set_entity_attribute("type", value, component_idx, entity_idx)
        except IndexError as e:
            raise ValueError(f"Cannot set type value: {str(e)}")
            
        return facade

    def set_panel_value(self, facade, value, component_idx=0):
        """Set the same type value for all entities in the panel/component.
        
        Args:
            facade: AoTFacade instance
            value: New type value (1-5)
            component_idx: Component index
            
        Returns:
            The facade for method chaining
        """
        # self._check_facade(facade)
        
        # Ensure value is within valid range (1-5 for shapes)
        value = max(1, min(5, value))
        
        try:
            # Set type for all entities in the component
            entity_count = facade.get_entity_count(component_idx)
            for idx in range(entity_count):
                facade.set_entity_attribute("type", value, component_idx, idx)
        except Exception as e:
            raise ValueError(f"Failed to set panel value: {str(e)}")
            
        return facade

    def apply_constraints(self, facade, constraints, component_idx=0):
        """Apply constraints to type attribute"""
        self._check_facade(facade)
        
        try:
            # Get the layout through the facade
            layout = facade.get_layout(component_idx)
            layout.entity_constraint["Type"][:] = constraints
            
            # Apply to all entities using the facade's access methods
            for i in range(facade.get_entity_count(component_idx)):
                entity = facade.get_entity(component_idx, i)
                entity.reset_constraint("Type", constraints[0], constraints[1])
        except Exception as e:
            raise ValueError(f"Failed to apply constraints: {str(e)}")
    
    def next_shape(self, facade, steps=1, component_idx=0, entity_idx=None):
        """Change to next shape type (cycling through available shapes)"""
        #self._check_facade(facade)
        
        # Get the total number of shape types
        SHAPE_COUNT = 5
        
        if entity_idx is not None:
            # Change specific entity
            current = self.get_value(facade, component_idx, entity_idx)
            new_value = ((current - 1 + steps) % SHAPE_COUNT) + 1  # Cycle between 1-5
            self.set_entity_value(facade, new_value, component_idx, entity_idx)

        else:
            # Change all entities
            entity_count = facade.get_entity_count(component_idx)
            for idx in range(entity_count):
                current = self.get_value(facade, component_idx, idx)
                new_value = ((current - 1 + steps) % SHAPE_COUNT) + 1  # Cycle between 1-5
                self.set_entity_value(facade, new_value, component_idx, idx)
                
        # Return the updated facade for method chaining
        return facade

    def get_shape_name(self, shape_index):
        # Map of shape indices to names
        shape_index = int(shape_index)
        SHAPE_NAMES = {
            1: "triangle",
            2: "square",
            3: "pentagon",
            4: "hexagon",
            5: "circle"
        }
        
        # Validate input
        if not isinstance(shape_index, int) or shape_index < 1 or shape_index > 5:
            raise ValueError(f"Invalid shape index: {shape_index}. Must be an integer between 1-5.")
        
        return SHAPE_NAMES.get(shape_index)
