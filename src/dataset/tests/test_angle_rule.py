import unittest
from dataset.core.rules.angle_rule import AngleRule
from dataset.const import ANGLE_VALUES
from dataset.AoT import Root, Structure, Component, Layout, Entity
import copy

class TestAngleRule(unittest.TestCase):
    
    def create_test_panel(self):
        """Create a test panel with entities that have angles"""
        # Create a simple panel with 2 entities
        root = Root("test", is_pg=True)
        structure = Structure("test_structure", is_pg=True)
        component = Component("test_component", is_pg=True)
        
        # Generate layout constraints and entity constraints
        from dataset.constraints import gen_layout_constraint, gen_entity_constraint
        layout_constraint = gen_layout_constraint("planar", [
            [0.2, 0.2, 0.1, 0.1], 
            [0.5, 0.5, 0.1, 0.1],
            [0.8, 0.2, 0.1, 0.1], 
            [0.8, 0.5, 0.1, 0.1],
            # Add more positions as needed
        ], num_min=0, num_max=4)
        entity_constraint = gen_entity_constraint()
        
        layout = Layout("test_layout", layout_constraint, entity_constraint, is_pg=True)
        
        # Create two entities with known angles
        entity1 = Entity("0", layout.position.get_value()[0], entity_constraint)
        entity2 = Entity("1", layout.position.get_value()[1], entity_constraint)
        
        # Set angles explicitly for testing
        entity1.angle.set_value_level(0)  # First angle value
        entity2.angle.set_value_level(0)  # Same angle
        
        # Build the structure
        layout.insert(entity1)
        layout.insert(entity2)
        component.insert(layout)
        structure.insert(component)
        root.insert(structure)
        
        return root

    def test_angle_rule_application(self):
        """Test that angle rule correctly rotates angles"""
        # Create a test panel with known angles
        panel = self.create_test_panel()
        
        # Create angle rotation rule (rotate by 1 step)
        rule = AngleRule(value=1)
        
        # Apply rule to generate second panel
        second_panel = rule.apply(panel)
        
        # Apply rule again to generate third panel
        third_panel = rule.apply(second_panel)
        
        # Check initial angle
        initial_angle = panel.children[0].children[0].children[0].children[0].angle.get_value_level()
        print(f"Initial angle: {initial_angle}")
        self.assertEqual(initial_angle, 0)
        
        # Check second panel angle
        second_angle = second_panel.children[0].children[0].children[0].children[0].angle.get_value_level()
        print(f"Second panel angle: {second_angle}")
        self.assertEqual(second_angle, 1)  # Initial + 1
        
        # Check third panel angle
        third_angle = third_panel.children[0].children[0].children[0].children[0].angle.get_value_level()
        print(f"Third panel angle: {third_angle}")
        self.assertEqual(third_angle, 2)  # Initial + 2

        # Also verify all entities have the same angle in each panel
        for entity in second_panel.children[0].children[0].children[0].children:
            self.assertEqual(entity.angle.get_value_level(), 1)
            
        for entity in third_panel.children[0].children[0].children[0].children:
            self.assertEqual(entity.angle.get_value_level(), 2)


if __name__ == '__main__':
    unittest.main()
