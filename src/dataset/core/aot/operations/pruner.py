from dataset.constraints import rule_constraint
import copy

class AoTPruner:
    """Handles AoT pruning operations."""
    
    def prune_root(self, root, rule_groups):
        """Prune an AoT according to rule constraints.
        
        Args:
            root: Root node of the AoT
            rule_groups: List of rule groups, each applied to a component
            
        Returns:
            New pruned root node, or None if no valid configurations
        """
        new_node = type(root)(root.name)
        for structure in root.children:
            if len(structure.children) == len(rule_groups):
                new_child = self.prune_structure(structure, rule_groups)
                if new_child is not None:
                    new_node.insert(new_child)
        
        # During real execution, this should never happen
        if len(new_node.children) == 0:
            new_node = None
        return new_node
        
    def prune_structure(self, structure, rule_groups):
        """Prune a structure node.
        
        Args:
            structure: Structure node to prune
            rule_groups: List of rule groups for each component
            
        Returns:
            New pruned structure node, or None if invalid
        """
        new_node = type(structure)(structure.name)
        for i in range(len(structure.children)):
            child = structure.children[i]
            # If any of the components fails to satisfy the constraint
            # the structure could not be chosen
            new_child = self.prune_component(child, rule_groups[i])
            if new_child is None:
                return None
            new_node.insert(new_child)
        return new_node
    
    def prune_component(self, component, rule_group):
        """Prune a component node.
        
        Args:
            component: Component node to prune
            rule_group: Rule group for this component
            
        Returns:
            New pruned component node, or None if invalid
        """
        new_node = type(component)(component.name)
        for child in component.children:
            new_child = self._update_layout_constraints(child, rule_group)
            if new_child is not None:
                new_node.insert(new_child)
        if len(new_node.children) == 0:
            new_node = None
        return new_node
    
    def _update_layout_constraints(self, layout, rule_group):
        """Update layout constraints based on rules.
        
        Args:
            layout: Layout node to update constraints for
            rule_group: Rules to apply to this layout
            
        Returns:
            New layout with updated constraints, or None if invalid
        """
        # Extract current constraints
        num_min = layout.layout_constraint["Number"][0]
        num_max = layout.layout_constraint["Number"][1]
        uni_min = layout.layout_constraint["Uni"][0]
        uni_max = layout.layout_constraint["Uni"][1]
        type_min = layout.entity_constraint["Type"][0]
        type_max = layout.entity_constraint["Type"][1]
        size_min = layout.entity_constraint["Size"][0]
        size_max = layout.entity_constraint["Size"][1]
        color_min = layout.entity_constraint["Color"][0]
        color_max = layout.entity_constraint["Color"][1]
        
        # Apply rule constraints
        new_constraints = rule_constraint(rule_group, num_min, num_max, 
                                          uni_min, uni_max,
                                          type_min, type_max,
                                          size_min, size_max,
                                          color_min, color_max)
        new_layout_constraint, new_entity_constraint = new_constraints
        
        # Validate constraints
        if not self._validate_constraints(new_layout_constraint, new_entity_constraint):
            return None
        
        # Create new layout with updated constraints
        new_layout_constraint_copy = copy.deepcopy(layout.layout_constraint)
        new_layout_constraint_copy["Number"][:] = new_layout_constraint["Number"]
        new_layout_constraint_copy["Uni"][:] = new_layout_constraint["Uni"]
        
        new_entity_constraint_copy = copy.deepcopy(layout.entity_constraint)
        new_entity_constraint_copy["Type"][:] = new_entity_constraint["Type"]
        new_entity_constraint_copy["Size"][:] = new_entity_constraint["Size"]
        new_entity_constraint_copy["Color"][:] = new_entity_constraint["Color"]
        
        return type(layout)(layout.name, 
                           new_layout_constraint_copy, 
                           new_entity_constraint_copy,
                           layout.orig_layout_constraint, 
                           layout.orig_entity_constraint,
                           layout.sample_new_num_count)
    
    def _validate_constraints(self, new_layout_constraint, new_entity_constraint):
        """Validate that updated constraints are satisfiable.
        
        Args:
            new_layout_constraint: Updated layout constraints
            new_entity_constraint: Updated entity constraints
            
        Returns:
            Boolean indicating if constraints are valid
        """
        # Check Number constraints
        new_num_min = new_layout_constraint["Number"][0]
        new_num_max = new_layout_constraint["Number"][1]
        if new_num_min > new_num_max:
            return False
            
        # Check Uniformity constraints
        new_uni_min = new_layout_constraint["Uni"][0]
        new_uni_max = new_layout_constraint["Uni"][1]
        if new_uni_min > new_uni_max:
            return False
            
        # Check Type constraints
        new_type_min = new_entity_constraint["Type"][0]
        new_type_max = new_entity_constraint["Type"][1]
        if new_type_min > new_type_max:
            return False
            
        # Check Size constraints
        new_size_min = new_entity_constraint["Size"][0]
        new_size_max = new_entity_constraint["Size"][1]
        if new_size_min > new_size_max:
            return False
            
        # Check Color constraints
        new_color_min = new_entity_constraint["Color"][0]
        new_color_max = new_entity_constraint["Color"][1]
        if new_color_min > new_color_max:
            return False
            
        return True
