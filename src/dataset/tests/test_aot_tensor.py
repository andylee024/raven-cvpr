#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest
import torch

from dataset.core.aot.tensor_panel import TensorPanel
from dataset.utils.panel_utils import visualize_panel


class TestTensorPanel(unittest.TestCase):
    """Test suite for the TensorPanel class."""

    def setUp(self):
        self.output_dir = "test_output"
        os.makedirs(self.output_dir, exist_ok=True)

    def test_uniform_triangles(self):
        """Test creating a panel with uniform triangles."""
        
        panel = TensorPanel()
        for row in range(3):
            for col in range(3):
                panel.set_attr(row, col, 'exists', 1)       # exists = True
                panel.set_attr(row, col, 'type', 1)         # type = 1 (triangle)
                panel.set_attr(row, col, 'size', 3)         # size = 3 (medium)
                panel.set_attr(row, col, 'angle', 0)        # angle = 0 (upright)
                panel.set_attr(row, col, 'color', 1)        # color = 1 (same for all)
        
        aot_panel = panel.to_aot()
        entities = aot_panel.get_entities()
        
        self.assertEqual(len(entities), 9)
        for entity in entities:
            self.assertEqual(entity.get_type(), 1)
            self.assertEqual(entity.get_size(), 3)
            self.assertEqual(entity.get_angle(), 0)
            self.assertEqual(entity.get_color(), 1)
        
        for row in range(3):
            for col in range(3):
                self.assertEqual(panel.get_shape(row, col), 'triangle')
                self.assertEqual(panel.get_angles(row, col), 0)
        
        output_path = os.path.join(self.output_dir, "uniform_triangles.png")
        visualize_panel(aot_panel, output_path)
    
    def test_color_gradient_triangles(self):
        """Test creating a panel with triangles having a color gradient."""
        
        panel = TensorPanel()
        for row in range(3):
            for col in range(3):
                panel.set_attr(row, col, 'exists', 1)       # exists = True
                panel.set_attr(row, col, 'type', 1)         # type = 1 (triangle)
                panel.set_attr(row, col, 'size', 3)         # size = 3 (medium)
                panel.set_attr(row, col, 'angle', 0)        # angle = 0 (upright)
                panel.set_attr(row, col, 'color', row * 3 + col + 1)  # gradient color (1-9)
        
        for row in range(3):
            for col in range(3):
                expected_color = row * 3 + col + 1
                self.assertEqual(panel.get_attr(row, col, 'color'), expected_color)
        
        aot_panel = panel.to_aot()
        output_path = os.path.join(self.output_dir, "color_gradient_triangles.png")
        visualize_panel(aot_panel, output_path)


if __name__ == "__main__":
    unittest.main()
