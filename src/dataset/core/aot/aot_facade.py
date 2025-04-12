import copy
from dataset.AoT import Root, Structure, Component, Layout, Entity
from dataset.Attribute import Angle

class AoTFacade:
    """Facade providing simplified access to AoT structure."""
    
    def __init__(self, aot_root):
        """Initialize with AoT root node."""
        if not hasattr(aot_root, 'level') or aot_root.level != "Root":
            raise TypeError("Expected Root node, got something else")
        self.root = aot_root
    
    @classmethod
    def create_test_panel(cls, entity_count=1, angle=0, size=1, type_value=1, color=1):
        """Create a panel with specified attributes for testing."""
        from dataset.core.aot.builders import create_test_panel
        root = create_test_panel(entity_count, angle, size, type_value, color)
        return cls(root)
    
    # Entity access
    def get_entity(self, component_idx=0, entity_idx=0):
        """Get entity at specified indices."""
        try:
            component = self.root.children[0].children[component_idx]
            layout = component.children[0]
            return layout.children[entity_idx]
        except (IndexError, AttributeError):
            raise IndexError(f"Entity not found at component {component_idx}, entity {entity_idx}")
    
    def get_entities(self, component_idx=0):
        """Get all entities in component."""
        try:
            component = self.root.children[0].children[component_idx]
            layout = component.children[0]
            return layout.children
        except (IndexError, AttributeError):
            return []
    
    def get_entity_count(self, component_idx=0):
        """Get the number of entities in a component."""
        return len(self.get_entities(component_idx))
    
    def get_layout(self, component_idx=0):
        """Get layout from component."""
        try:
            component = self.root.children[0].children[component_idx]
            return component.children[0]
        except (IndexError, AttributeError):
            raise IndexError(f"Layout not found at component {component_idx}")
    
    # Attribute access
    def get_entity_attribute(self, attr_name, component_idx=0, entity_idx=0):
        """Get attribute value from entity."""
        entity = self.get_entity(component_idx, entity_idx)
        attr_name = attr_name.lower()
        
        if attr_name == "angle":
            return entity.angle.get_value_level()
        elif attr_name == "size":
            return entity.size.get_value_level()
        elif attr_name == "type":
            return entity.type.get_value_level()
        elif attr_name == "color":
            return entity.color.get_value_level()
        else:
            raise ValueError(f"Unknown attribute: {attr_name}")
    
    def set_entity_attribute(self, attr_name, value, component_idx=0, entity_idx=None):
        """Set attribute value on entity/entities."""
        attr_name = attr_name.lower()
        
        if entity_idx is not None:
            # Set for a specific entity
            entity = self.get_entity(component_idx, entity_idx)
            if attr_name == "angle":
                entity.angle.set_value_level(value)
            elif attr_name == "size":
                entity.size.set_value_level(value)
            elif attr_name == "type":
                entity.type.set_value_level(value)
            elif attr_name == "color":
                entity.color.set_value_level(value)
            else:
                raise ValueError(f"Unknown attribute: {attr_name}")
        else:
            # Set for all entities in the component
            entities = self.get_entities(component_idx)
            for entity in entities:
                if attr_name == "angle":
                    entity.angle.set_value_level(value)
                elif attr_name == "size":
                    entity.size.set_value_level(value)
                elif attr_name == "type":
                    entity.type.set_value_level(value)
                elif attr_name == "color":
                    entity.color.set_value_level(value)
                else:
                    raise ValueError(f"Unknown attribute: {attr_name}")
    
    def add_entity(self, component_idx=0, **attributes):
        """Add a new entity to a component and return its index."""
        layout = self.get_layout(component_idx)
        
        # Create default bounding box (placeholder)
        bbox = [0, 0, 50, 50]  # x, y, width, height
        
        # Create new entity with default constraints
        entity_name = f"Entity_{len(layout.children)}"
        entity = Entity(entity_name, bbox, layout.entity_constraint)
        
        # Apply any specified attributes
        for attr_name, value in attributes.items():
            if attr_name.lower() == "angle":
                entity.angle.set_value_level(value)
            elif attr_name.lower() == "size":
                entity.size.set_value_level(value)
            elif attr_name.lower() == "type":
                entity.type.set_value_level(value)
            elif attr_name.lower() == "color":
                entity.color.set_value_level(value)
        
        # Add to layout
        layout._insert(entity)
        
        # Update number and position
        layout.number.set_value(len(layout.children))
        layout.position.sample(layout.number.get_value())
        
        return len(layout.children) - 1
    
    def remove_entity(self, component_idx=0, entity_idx=-1):
        """Remove an entity from a component."""
        layout = self.get_layout(component_idx)
        
        if entity_idx < 0 or entity_idx >= len(layout.children):
            if entity_idx == -1 and layout.children:
                # Remove last entity
                entity_idx = len(layout.children) - 1
            else:
                raise IndexError(f"Entity index {entity_idx} out of range")
        
        # Remove entity
        layout.children.pop(entity_idx)
        
        # Update number and position
        layout.number.set_value(len(layout.children))
        if layout.children:
            layout.position.sample(layout.number.get_value())
            
    # Utility methods
    def clone(self):
        """Create deep copy for transformations."""
        return AoTFacade(copy.deepcopy(self.root))
    
    @property
    def raw(self):
        """Access underlying AoT."""
        return self.root
    
    def get_angle_max_value(self):
        """Get the maximum number of angle values."""
        # Assuming Angle has 8 levels (0-7)
        return 8
    
    def print_summary(self):
        """Print summary of panel."""
        print(f"AoT Panel - Structure: {self.root.children[0].name}")
        print(f"Components: {len(self.root.children[0].children)}")
        
        for comp_idx, component in enumerate(self.root.children[0].children):
            layout = component.children[0]
            print(f"  Component {comp_idx}: {component.name} - {len(layout.children)} entities")
            
            if layout.children:
                entity = layout.children[0]
                print(f"    Sample Entity Attributes:")
                print(f"      Type: {entity.type.get_value_level()}")
                print(f"      Size: {entity.size.get_value_level()}")
                print(f"      Color: {entity.color.get_value_level()}")
                print(f"      Angle: {entity.angle.get_value_level()}")
