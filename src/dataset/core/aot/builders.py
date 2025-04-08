# src/dataset/core/aot/operations/builder.py

from dataset.AoT import Component, Layout, Root, Structure
from dataset.constraints import (gen_entity_constraint, gen_layout_constraint)

import dataset.build_tree as build_tree

class AoTBuilder:
    """Handles construction of different And-Or Tree configurations.

    Currently, builder is just a wrapper for build_tree.py functions but it will get replaced later.
    """
    
    @staticmethod
    def build_center_single():
        return build_tree.build_center_single()
        
    @staticmethod
    def build_distribute_four():
        return build_tree.build_distribute_four()
    
    @staticmethod
    def build_distribute_nine():
        return build_tree.build_distribute_nine()
    
    @staticmethod
    def build_left_center_single_right_center_single():
        return build_tree.build_left_center_single_right_center_single()
    
    @staticmethod
    def build_up_center_single_down_center_single():
        return build_tree.build_up_center_single_down_center_single()
    
    @staticmethod
    def build_in_center_single_out_center_single():
        return build_tree.build_in_center_single_out_center_single()
    
    @staticmethod
    def build_in_distribute_four_out_center_single():
        return build_tree.build_in_distribute_four_out_center_single()