import copy
from dataset.core.aot.entity_facade import EntityFacade
from dataset.legacy.AoT import Root, Structure, Component, Layout, Entity
from dataset.legacy.Attribute import Angle

class AoTFacade:
    """Facade providing simplified access to AoT structure."""
    
    def __init__(self, aot_root):
        """Initialize with AoT root node."""
        if not hasattr(aot_root, 'level') or aot_root.level != "Root":
            raise TypeError("Expected Root node, got something else")

        self.root = aot_root
    
    def get_entity(self, component_idx=0, entity_idx=0):
        """Get entity at specified indices (wrapped in EntityFacade)."""
        try:
            layout = self._get_layout(component_idx)
            entity = layout.children[entity_idx]
            return EntityFacade.wrap(entity)
        
        except (IndexError, AttributeError):
            raise IndexError(f"Entity not found at component {component_idx}, entity {entity_idx}")
    
    def get_entities(self, component_idx=0):
        """Get all entities in component (wrapped in EntityFacade)."""
        try:
            layout = self._get_layout(component_idx)
            return [EntityFacade.wrap(entity) for entity in layout.children]

        except (IndexError, AttributeError):
            return []
    
    def get_total_entity_count(self):
        """Get the total number of entities in the panel."""
        total_entities = 0
        for comp_idx in range(len(self._get_structure().children)):
            total_entities += self.get_entity_count(comp_idx)
        return total_entities
    
    def get_entity_count(self, component_idx=0):
        """Get the number of entities in a component."""
        return len(self.get_entities(component_idx))
    
    def get_layout(self, component_idx=0):
        """Get layout from component."""
        return self._get_layout(component_idx)
    
    # Attribute access
    def get_entity_attribute(self, attr_name, component_idx=0, entity_idx=0):
        """Get attribute value from entity."""
        entity_facade = self.get_entity(component_idx, entity_idx)
        attr_name = attr_name.lower()
        
        if attr_name == "angle":
            return entity_facade.get_angle()
        elif attr_name == "size":
            return entity_facade.get_size()
        elif attr_name == "type":
            return entity_facade.get_type()
        elif attr_name == "color":
            return entity_facade.get_color()
        else:
            raise ValueError(f"Unknown attribute: {attr_name}")
    
    def set_entity_attribute(self, attr_name, value, component_idx=0, entity_idx=None):
        """Set attribute value on entity/entities."""
        attr_name = attr_name.lower()
        
        if entity_idx is not None:
            # Set for a specific entity
            entity_facade = self.get_entity(component_idx, entity_idx)
            if attr_name == "angle":
                entity_facade.set_angle(value)
            elif attr_name == "size":
                entity_facade.set_size(value)
            elif attr_name == "type":
                entity_facade.set_type(value)
            elif attr_name == "color":
                entity_facade.set_color(value)
            else:
                raise ValueError(f"Unknown attribute: {attr_name}")
        else:
            # Set for all entities in the component
            entity_facades = self.get_entities(component_idx)
            for entity_facade in entity_facades:
                if attr_name == "angle":
                    entity_facade.set_angle(value)
                elif attr_name == "size":
                    entity_facade.set_size(value)
                elif attr_name == "type":
                    entity_facade.set_type(value)
                elif attr_name == "color":
                    entity_facade.set_color(value)
                else:
                    raise ValueError(f"Unknown attribute: {attr_name}")
    
    # Utility methods
    def clone(self):
        """Create deep copy for transformations."""
        return AoTFacade(copy.deepcopy(self.root))
    
    @property
    def raw(self):
        """Access underlying AoT."""
        return self.root
    
    def print_summary(self, verbose=False):
        """Print minimal panel summary with shape information."""
        # Count total entities across all components
        total_entities = 0
        for comp_idx in range(len(self._get_structure().children)):
            total_entities += self.get_entity_count(comp_idx)
        
        print(f"Total entities: {total_entities}")
        print()
        print("Panel Shape Information:")
        print("========================")
        
        # Print shape information for each entity
        entity_facades = self.get_entities()
        for i, entity in enumerate(entity_facades):
            shape_name = entity.get_shape_name()
            print(f"Entity {i}: {shape_name}")

            if verbose:
                print(f"  Size: {entity.get_size()}")
                print(f"  Color: {entity.get_color()}")
                print(f"  Angle: {entity.get_angle()}")
                print(f"  Type: {entity.get_type()}")
                print(f"  Position: {entity.get_position()}")
        
        print("========================")

    def _get_structure(self):
        """Get the structure node from the root."""
        try:
            return self.root.children[0]
        except (IndexError, AttributeError):
            raise IndexError("Structure not found in AoT")

    def _get_component(self, component_idx=0):
        """Get a component node at the specified index."""
        try:
            structure = self._get_structure()
            return structure.children[component_idx]
        except (IndexError, AttributeError):
            raise IndexError(f"Component not found at index {component_idx}")

    def _get_layout(self, component_idx=0):
        """Get the layout node from a component."""
        try:
            component = self._get_component(component_idx)
            return component.children[0]
        except (IndexError, AttributeError):
            raise IndexError(f"Layout not found in component {component_idx}")

