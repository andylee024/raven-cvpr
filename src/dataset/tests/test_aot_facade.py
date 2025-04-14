#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Utility function to generate and visualize a distribute_nine panel.
"""

from dataset.utils.panel_utils import get_random_panel, visualize_panel


if __name__ == "__main__":
    # Generate and get a sample panel
    panel = get_random_panel(n_entities=5)

    # convert to AoT to access summary
    panel = panel.to_aot()
    panel.print_summary(verbose=False)
    
    # Visualize the panel
    visualize_panel(panel, "test_output/sample_panel.png")
