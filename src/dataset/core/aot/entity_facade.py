from dataset.utils.bbox_utils import bbox_to_tensor_coordinate, tensor_coordinate_to_bbox

class EntityFacade:
    """Facade for simplified Entity manipulation."""
    
    def __init__(self, entity):
        """Initialize with an Entity object."""
        # Store the raw entity (not another EntityFacade)
        if isinstance(entity, EntityFacade):
            self.entity = entity.entity  # Extract the raw entity
        else:
            self.entity = entity
    
    @classmethod
    def wrap(cls, entity_or_facade):
        """Create or return an EntityFacade.
        If the input is already an EntityFacade, return it.
        Otherwise, create a new EntityFacade around the entity.
        """
        if isinstance(entity_or_facade, cls):
            return entity_or_facade
        return cls(entity_or_facade)
    
    # Attribute getters
    def get_type(self):
        """Get entity type value."""
        return self.entity.type.get_value_level()
        
    def get_size(self):
        """Get entity size value."""
        return self.entity.size.get_value_level()
        
    def get_color(self):
        """Get entity color value."""
        return self.entity.color.get_value_level()
        
    def get_angle(self):
        """Get entity angle value."""
        return self.entity.angle.get_value_level()
    
    def get_position(self):
        """Get entity position."""
        return bbox_to_tensor_coordinate(self.entity.bbox)
    
    def get_tensor_coordinate(self):
        """Get entity tensor coordinate."""
        return bbox_to_tensor_coordinate(self.entity.bbox)
    
    # Attribute setters
    def set_type(self, value):
        """Set entity type value."""
        self.entity.type.set_value_level(value)
        return self
        
    def set_size(self, value):
        """Set entity size value."""
        self.entity.size.set_value_level(value)
        return self
        
    def set_color(self, value):
        """Set entity color value."""
        self.entity.color.set_value_level(value)
        return self
        
    def set_angle(self, value):
        """Set entity angle value."""
        self.entity.angle.set_value_level(value)
        return self
    
    def set_position(self, value):
        """Set entity position."""
        self.entity.bbox = tensor_coordinate_to_bbox(value)
        return self
    
    # Convenience methods
    def get_shape_name(self):
        """Get readable shape name."""
        type_value = self.get_type()
        names = {1: "triangle", 2: "square", 3: "pentagon", 
                 4: "hexagon", 5: "circle"}
        return names.get(type_value, "unknown")
    
    # Raw access
    @property
    def raw(self):
        """Access the underlying Entity."""
        return self.entity
