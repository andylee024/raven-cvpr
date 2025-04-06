"""Unit tests for the AoTPruner implementation on different node types."""

import unittest
import numpy as np
import copy
from dataset.core.aot.operations.pruner import AoTPruner
from dataset.core.rules.progression import ProgressionRule
from dataset.build_tree import build_distribute_four, build_left_center_single_right_center_single


class TestAoTPruner(unittest.TestCase):
    """Test cases for the AoTPruner class focusing on different node types."""

    def setUp(self):
        """Set up test fixtures."""
        # Set seed for reproducibility
        np.random.seed(42)
        
        # Create AoT structures
        self.root = build_distribute_four()
        self.structure = self.root.children[0]
        self.component = self.structure.children[0]
        self.layout = self.component.children[0]
        
        # Create progression rules for each attribute type
        self.number_rule = ProgressionRule("Number", 1, component_idx=0)
        self.type_rule = ProgressionRule("Type", 1, component_idx=0)
        self.size_rule = ProgressionRule("Size", 1, component_idx=0)
        self.color_rule = ProgressionRule("Color", 1, component_idx=0)
        
        # Create pruner instance for direct testing
        self.pruner = AoTPruner()
    
    def _compare_nodes(self, node1, node2, attribute_name=None):
        """Helper method to compare two nodes for structural equality.
        
        Args:
            node1: First node to compare
            node2: Second node to compare
            attribute_name: Optional attribute to focus on for testing
            
        Returns:
            True if nodes are structurally equivalent, False otherwise
        """
        # Check for None
        if node1 is None and node2 is None:
            return True
        if node1 is None or node2 is None:
            print(f"Discrepancy: One node is None while the other is not")
            return False
        
        # Basic properties should match
        if node1.name != node2.name or node1.level != node2.level:
            print(f"Discrepancy: Node properties don't match - {node1.name}:{node1.level} vs {node2.name}:{node2.level}")
            return False
        
        # Check number of children
        if len(node1.children) != len(node2.children):
            print(f"Discrepancy: Different number of children - {len(node1.children)} vs {len(node2.children)} for {node1.name}")
            return False
        
        # For Layout nodes, compare constraints
        if node1.level == "Layout":
            # Compare layout constraints
            for key in node1.layout_constraint:
                if attribute_name is None or key == attribute_name:
                    if node1.layout_constraint[key] != node2.layout_constraint[key]:
                        print(f"Discrepancy: Layout constraint '{key}' differs - {node1.layout_constraint[key]} vs {node2.layout_constraint[key]}")
                        return False
            
            # Compare entity constraints
            for key in node1.entity_constraint:
                if attribute_name is None or key == attribute_name:
                    if node1.entity_constraint[key] != node2.entity_constraint[key]:
                        print(f"Discrepancy: Entity constraint '{key}' differs - {node1.entity_constraint[key]} vs {node2.entity_constraint[key]}")
                        return False
        
        # Recursively check children
        for i in range(len(node1.children)):
            if not self._compare_nodes(node1.children[i], node2.children[i], attribute_name):
                print(f"Discrepancy: Child {i} of {node1.name} differs")
                return False
        
        return True
        
    def test_root_node_prune(self):
        """Test that old and new root implementations produce identical results."""
        # Create rule groups for each attribute
        rule_tests = [
            {"name": "Number", "rule": self.number_rule},
            {"name": "Type", "rule": self.type_rule},
            {"name": "Size", "rule": self.size_rule},
            {"name": "Color", "rule": self.color_rule}
        ]
        
        for test in rule_tests:
            rule_groups = [[test["rule"]]]
            
            # Deep copy the root to ensure we start from the same state each time
            root_copy = copy.deepcopy(self.root)
            
            # Test both implementations
            result_old = root_copy.prune(rule_groups, new_implementation=False)
            result_new = root_copy.prune(rule_groups, new_implementation=True)
            
            # Both should be None or both should be valid
            self.assertEqual(result_old is None, result_new is None, 
                            f"{test['name']}: One implementation returned None while the other didn't")
            
            # If both results are not None, compare their structure
            if result_old is not None and result_new is not None:
                # Compare the complete nodes using _compare_nodes
                self.assertTrue(self._compare_nodes(result_old, result_new, test["name"]), 
                              f"{test['name']}: Root nodes have different structure")
    
    def test_structure_node_implementation_equality(self):
        """Test that old and new structure implementations produce identical results."""
        rule_groups = [[self.type_rule]]
        
        # Make copies to ensure we're starting from the same state
        structure_copy = copy.deepcopy(self.structure)
        
        # Test both implementations
        result_old = structure_copy._prune(rule_groups, new_implementation=False)
        result_new = structure_copy._prune(rule_groups, new_implementation=True)
        
        # Both should be None or both should be valid
        self.assertEqual(result_old is None, result_new is None, 
                        "One structure implementation returned None while the other didn't")
        
        # If both results are not None, compare them
        if result_old is not None and result_new is not None:
            self.assertTrue(self._compare_nodes(result_old, result_new, "Type"), 
                          "Structure implementations produced different results")
    
    def test_component_node_implementation_equality(self):
        """Test that old and new component implementations produce identical results."""
        rule_group = [self.size_rule]
        
        # Make copies to ensure we're starting from the same state
        component_copy = copy.deepcopy(self.component)
        
        # Test both implementations
        result_old = component_copy._prune(rule_group, new_implementation=False)
        result_new = component_copy._prune(rule_group, new_implementation=True)
        
        # Both should be None or both should be valid
        self.assertEqual(result_old is None, result_new is None, 
                        "One component implementation returned None while the other didn't")
        
        # If both results are not None, compare them
        if result_old is not None and result_new is not None:
            self.assertTrue(self._compare_nodes(result_old, result_new, "Size"), 
                          "Component implementations produced different results")
    
    def test_layout_node_update_constraint_equality(self):
        """Test that Layout._update_constraint and AoTPruner._update_layout_constraints produce identical results."""
        rule_group = [self.color_rule]
        
        # Make copy to ensure we're starting from the same state
        layout_copy = copy.deepcopy(self.layout)
        
        # Test both implementations
        result_old = layout_copy._update_constraint(rule_group)
        result_new = self.pruner._update_layout_constraints(layout_copy, rule_group)
        
        # Both should be None or both should be valid
        self.assertEqual(result_old is None, result_new is None, 
                        "One layout implementation returned None while the other didn't")
        
        # If both results are not None, compare their constraints directly
        if result_old is not None and result_new is not None:
            # Compare layout constraints
            for key in result_old.layout_constraint:
                self.assertEqual(result_old.layout_constraint[key], result_new.layout_constraint[key],
                               f"Layout constraint {key} doesn't match")
            
            # Compare entity constraints
            for key in result_old.entity_constraint:
                self.assertEqual(result_old.entity_constraint[key], result_new.entity_constraint[key],
                               f"Entity constraint {key} doesn't match")
    

if __name__ == "__main__":
    unittest.main() 