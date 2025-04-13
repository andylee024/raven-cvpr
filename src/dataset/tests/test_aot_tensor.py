#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest
import torch

from dataset.core.aot import aot_facade
from dataset.core.aot.converters import tensor_to_aot
from dataset.utils.panel_utils import visualize_panel


class TestAoTTensor(unittest.TestCase):
    """Test suite for the AoTTensor class."""

    def setUp(self):
        self.output_dir = "test_output/aot_tensor"
        os.makedirs(self.output_dir, exist_ok=True)

    def test_uniform_triangles(self):
        """Test creating a panel with uniform triangles."""
        
        aot_tensor = torch.zeros((3, 3, 5), dtype=torch.int)
        for row in range(3):
            for col in range(3):
                aot_tensor[row, col, 0] = 1       # exists = True
                aot_tensor[row, col, 1] = 1       # type = 1 (triangle)
                aot_tensor[row, col, 2] = 3       # size = 3 (medium)
                aot_tensor[row, col, 3] = 0       # angle = 0 (upright)
                aot_tensor[row, col, 4] = 1       # color = 1 (same for all)
        
        panel = tensor_to_aot(aot_tensor)

        entities = panel.get_entities()
        self.assertEqual(len(entities), 9)

        for entity in entities:
            self.assertEqual(entity.get_type(), 1)
            self.assertEqual(entity.get_size(), 3)
            self.assertEqual(entity.get_angle(), 0)
            self.assertEqual(entity.get_color(), 1)
        
        output_path = os.path.join(self.output_dir, "uniform_triangles.png")
        visualize_panel(panel, output_path)

    # @unittest.skip("Skipping color gradient triangles test")
    def test_color_gradient_triangles(self):
        """Test creating a panel with triangles having a color gradient."""
        
        # Create a tensor with triangles of varying colors
        tensor = torch.zeros((3, 3, 5), dtype=torch.int)
        for row in range(3):
            for col in range(3):
                tensor[row, col, 0] = 1       # exists = True
                tensor[row, col, 1] = 1       # type = 1 (triangle)
                tensor[row, col, 2] = 3       # size = 3 (medium)
                tensor[row, col, 3] = 0       # angle = 0 (upright)
                tensor[row, col, 4] = row * 3 + col + 1  # gradient color (1-9)
        
        panel = tensor_to_aot(tensor)
        output_path = os.path.join(self.output_dir, "color_gradient_triangles.png")
        visualize_panel(panel, output_path)

    # @unittest.skip("Skipping size and angle variations test")
    def test_size_and_angle_variations(self):
        """Test creating a panel with triangles of varying sizes and angles."""
        
        tensor = torch.zeros((3, 3, 5), dtype=torch.int)
        for row in range(3):
            for col in range(3):
                tensor[row, col, 0] = 1       # exists = True
                tensor[row, col, 1] = 1       # type = 1 (triangle)
                tensor[row, col, 2] = row + 2  # size increases with row (2-4)
                tensor[row, col, 3] = col * 2  # angle increases with column (0, 2, 4)
                tensor[row, col, 4] = 1       # same color
        
        panel = tensor_to_aot(tensor)
        output_path = os.path.join(self.output_dir, "size_angle_variations.png")
        visualize_panel(panel, output_path)


if __name__ == "__main__":
    unittest.main()
