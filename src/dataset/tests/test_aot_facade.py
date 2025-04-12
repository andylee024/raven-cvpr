#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Utility function to generate and visualize a distribute_nine panel.
"""

from dataset.utils.panel_utils import generate_sample_panel, visualize_panel
from dataset.core.handlers.type_handler import TypeHandler


if __name__ == "__main__":
    # Generate and get a sample panel
    panel = generate_sample_panel()
    
    # Print panel summary from AoTFacade
    panel.print_summary(verbose=False)
    
    # Visualize the panel
    visualize_panel(panel, "test_output/sample_panel.png")
