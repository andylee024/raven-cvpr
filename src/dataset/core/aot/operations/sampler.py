import random
import copy
import numpy as np

class AoTSampler:
    """Handles AoT sampling operations."""
    
    def sample_root(self, root):
        """Sample a concrete panel from an AoT.
        
        Args:
            root: Root node of the AoT
            
        Returns:
            New sampled root node
        """
        if root.is_pg:
            raise ValueError("Could not sample on a PG")
        
        new_node = type(root)(root.name, True)
        selected = np.random.choice(root.children)
        new_child = self.sample_structure(selected)
        new_node.insert(new_child)
        return new_node
    
    def sample_structure(self, structure):
        """Sample from a structure node.
        
        Args:
            structure: Structure node to sample from
            
        Returns:
            New sampled structure node
        """
        if structure.is_pg:
            raise ValueError("Could not sample on a PG")
            
        new_node = type(structure)(structure.name, True)
        for child in structure.children:
            new_child = self.sample_component(child)
            new_node.insert(new_child)
        return new_node
    
    def sample_component(self, component):
        """Sample from a component node.
        
        Args:
            component: Component node to sample from
            
        Returns:
            New sampled component node
        """
        if component.is_pg:
            raise ValueError("Could not sample on a PG")
            
        new_node = type(component)(component.name, True)
        selected = np.random.choice(component.children)
        new_child = self.sample_layout(selected)
        new_node.insert(new_child)
        return new_node
    
    def sample_layout(self, layout):
        """Sample from a layout node.
        
        Args:
            layout: Layout node to sample from
            
        Returns:
            New sampled layout node with entities
        """
        if layout.is_pg:
            raise ValueError("Could not sample on a PG")
            
        new_node = copy.deepcopy(layout)
        new_node.is_pg = True
        
        # Sample number of objects
        new_node.number.sample()
        num_objects = new_node.number.get_value()
        
        # Sample positions
        new_node.position.sample(num_objects)
        positions = new_node.position.get_value()
        
        # Sample uniformity
        new_node.uniformity.sample()
        
        # Create entities based on sampled values
        if new_node.uniformity.get_value():
            # Create identical entities
            node = self.create_entity("0", positions[0], new_node.entity_constraint)
            new_node.insert(node)
            for i in range(1, len(positions)):
                # Copy the first entity for others (same attributes)
                node_copy = copy.deepcopy(node)
                node_copy.name = str(i)
                node_copy.bbox = positions[i]
                new_node.insert(node_copy)
        else:
            # Create different entities
            for i in range(len(positions)):
                # Create new entity with independent attributes
                node = self.create_entity(str(i), positions[i], new_node.entity_constraint)
                new_node.insert(node)
        
        return new_node
    
    def create_entity(self, name, bbox, entity_constraint):
        """Create a new entity with sampled attributes.
        
        Args:
            name: Entity name
            bbox: Entity bounding box
            entity_constraint: Constraints for entity attributes
            
        Returns:
            New entity with sampled attributes
        """
        from dataset.legacy.AoT import Entity
        entity = Entity(name, bbox, entity_constraint)
        
        # Sample attributes
        entity.type.sample()
        entity.size.sample()
        entity.color.sample()
        entity.angle.sample()
        
        return entity
    
    def resample_root(self, root, change_number=False):
        """Resample an existing root node.
        
        Args:
            root: Root node to resample
            change_number: Whether to allow changing the number of entities
            
        Returns:
            The modified root node
        """
        if not root.is_pg:
            raise ValueError("Can only resample a PG (concrete node)")
        
        for child in root.children:
            self.resample_structure(child, change_number)
        
        return root
    
    def resample_structure(self, structure, change_number=False):
        """Resample an existing structure node.
        
        Args:
            structure: Structure node to resample
            change_number: Whether to allow changing the number of entities
        """
        if not structure.is_pg:
            raise ValueError("Can only resample a PG (concrete node)")
        
        for child in structure.children:
            self.resample_component(child, change_number)
    
    def resample_component(self, component, change_number=False):
        """Resample an existing component node.
        
        Args:
            component: Component node to resample
            change_number: Whether to allow changing the number of entities
        """
        if not component.is_pg:
            raise ValueError("Can only resample a PG (concrete node)")
        
        for child in component.children:
            self.resample_layout(child, change_number)
    
    def resample_layout(self, layout, change_number=False):
        """Resample an existing layout node.
        
        Args:
            layout: Layout node to resample
            change_number: Whether to allow changing the number of entities
        """
        if not layout.is_pg:
            raise ValueError("Can only resample a PG (concrete node)")
        
        # Resample number if allowed
        if change_number:
            layout.number.sample()
        
        # Clear existing entities
        del layout.children[:]
        
        # Resample positions based on number
        layout.position.sample(layout.number.get_value())
        positions = layout.position.get_value()
        
        # Create new entities
        if layout.uniformity.get_value():
            # Create identical entities
            node = self.create_entity("0", positions[0], layout.entity_constraint)
            layout.insert(node)
            for i in range(1, len(positions)):
                # Copy the first entity for others (same attributes)
                node_copy = copy.deepcopy(node)
                node_copy.name = str(i)
                node_copy.bbox = positions[i]
                layout.insert(node_copy)
        else:
            # Create different entities
            for i in range(len(positions)):
                # Create new entity with independent attributes
                node = self.create_entity(str(i), positions[i], layout.entity_constraint)
                layout.insert(node)

    # Other sampling methods
