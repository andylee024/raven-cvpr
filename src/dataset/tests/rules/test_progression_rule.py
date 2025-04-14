import os
import unittest

from dataset.core.rules.progression import ProgressionRule
from dataset.utils.panel_utils import visualize_panel, get_random_panel, get_uniform_triangle_panel

class TestProgressionRule(unittest.TestCase):
    """Test suite for comparing old and new progression rule implementations."""
    
    def setUp(self):
        """Set up test fixtures before each test."""
        self.output_dir = "test_output"
        os.makedirs(self.output_dir, exist_ok=True)

        self.uniform_triangle_panel = get_uniform_triangle_panel()
        self.random_panel = get_random_panel(n_entities=9)

    def test_size_progression_on_triangles(self):
        """Test applying size progression to uniform triangles."""
        # Create a uniform triangle panel
        rule = ProgressionRule(attr_name='size', step=2)
        source_panel = self.uniform_triangle_panel
        result_panel = rule.apply([source_panel])
        
        source_path = os.path.join(self.output_dir, "source_size_triangles.png")
        result_path = os.path.join(self.output_dir, "progression_size_triangles.png")
        visualize_panel(source_panel.to_aot(), source_path)
        visualize_panel(result_panel.to_aot(), result_path)

    def test_color_progression_on_triangles(self):
        """Test applying size progression to uniform triangles."""
        # Create a uniform triangle panel
        rule = ProgressionRule(attr_name='color', step=2)
        source_panel = self.uniform_triangle_panel
        result_panel = rule.apply([source_panel])
        
        source_path = os.path.join(self.output_dir, "source_color_triangles.png")
        result_path = os.path.join(self.output_dir, "progression_color_triangles.png")
        visualize_panel(source_panel.to_aot(), source_path)
        visualize_panel(result_panel.to_aot(), result_path)

if __name__ == "__main__":
    unittest.main()
