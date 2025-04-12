from dataset.core.handlers.base import AttributeHandler

class AngleHandler(AttributeHandler):
    """Handler for the Angle attribute"""
    
    def get_value(self, layout):
        """Get angle value from entities"""
        if not layout.children:
            return 0
        return layout.children[0].angle.get_value_level()
        
    def set_value(self, layout, value):
        """Set angle value for all entities in layout"""
        for entity in layout.children:
            entity.angle.set_value_level(value)
            
    def apply_constraints(self, layout, constraints):
        """Apply constraints to angle attribute"""
        layout.entity_constraint["Angle"][:] = constraints
        # Update entity constraints
        for entity in layout.children:
            entity.reset_constraint("Angle", constraints[0], constraints[1])
