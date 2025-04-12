from dataset.core.rules.base import Rule
import copy
import numpy as np
from dataset.legacy.const import COLOR_MAX, COLOR_MIN

class ArithmeticRule(Rule):
    """Binary arithmetic operation between panel attributes.
    
    For attributes like Number/Size/Color: Panel_3 = Panel_1 + Panel_2
    For Position: + means SET_UNION and - means SET_DIFF
    """
    
    def __init__(self, attr, value):
        super().__init__(attr=attr, value=value)
        self.state = {"memory": [], "color_count": 0, "color_white_alarm": False}
    
    def apply(self, source, target=None):
        """Apply arithmetic rule between panels."""
        if target is None:
            target = copy.deepcopy(source)
            
        current_layout = source.children[0].children[self.component_idx].children[0]
        second_layout = target.children[0].children[self.component_idx].children[0]
        
        if self.attr == "Number":
            # Handle third column (using memory)
            if len(self.state["memory"]) > 0:
                first_layout_number_level = self.state["memory"].pop()
                if self.value > 0:
                    total = first_layout_number_level + 1 + current_layout.number.get_value()
                else:
                    total = first_layout_number_level + 1 - current_layout.number.get_value()
                second_layout.number.set_value_level(total - 1)
            # Handle second column (store in memory)
            else:
                old_value_level = current_layout.number.get_value_level()
                self.state["memory"].append(old_value_level)
                if self.value > 0:
                    num_max_level_orig = sum(current_layout.layout_constraint["Number"]) + 1
                    new_num_max_level = num_max_level_orig - old_value_level - 1
                    second_layout.layout_constraint["Number"][1] = new_num_max_level
                else:
                    num_min_level_orig = (second_layout.layout_constraint["Number"][0] - 1) / 2
                    new_num_max_level = old_value_level - num_min_level_orig - 1
                    second_layout.layout_constraint["Number"][:] = [num_min_level_orig, new_num_max_level]
                second_layout.reset_constraint("Number")
                second_layout.number.sample()
                
            # Update positions and entities based on number
            second_layout.position.sample(second_layout.number.get_value())
            pos = second_layout.position.get_value()
            del second_layout.children[:]
            for i in range(len(pos)):
                entity = copy.deepcopy(current_layout.children[0])
                entity.name = str(i)
                entity.bbox = pos[i]
                if not current_layout.uniformity.get_value():
                    entity.resample()
                second_layout.insert(entity)
                
        elif self.attr == "Position":
            # Handle SET_UNION or SET_DIFF operations
            if len(self.state["memory"]) > 0:
                # Third column
                first_layout_value_idx = self.state["memory"].pop()
                if self.value > 0:  # UNION
                    new_pos_idx = set(first_layout_value_idx) | set(current_layout.position.get_value_idx())
                else:  # DIFF
                    new_pos_idx = set(first_layout_value_idx) - set(current_layout.position.get_value_idx())
                second_layout.number.set_value_level(len(new_pos_idx) - 1)
                second_layout.position.set_value_idx(np.array(list(new_pos_idx)))
            else:
                # Second column
                current_layout_value_idx = current_layout.position.get_value_idx()
                self.state["memory"].append(current_layout_value_idx)
                while True:
                    second_layout.number.sample()
                    second_layout.position.sample(second_layout.number.get_value())
                    if self.value > 0:  # UNION
                        if not (set(current_layout_value_idx) >= set(second_layout.position.get_value_idx())):
                            break
                    else:  # DIFF
                        if not (set(current_layout_value_idx) <= set(second_layout.position.get_value_idx())):
                            break
                            
            # Update entities based on positions
            pos = second_layout.position.get_value()
            del second_layout.children[:]
            for i in range(len(pos)):
                entity = copy.deepcopy(current_layout.children[0])
                entity.name = str(i)
                entity.bbox = pos[i]
                if not current_layout.uniformity.get_value():
                    entity.resample()
                second_layout.insert(entity)
                
        elif self.attr == "Size":
            if len(self.state["memory"]) > 0:
                # Third column
                first_layout_size_level = self.state["memory"].pop()
                if self.value > 0:
                    new_size_value_level = first_layout_size_level + current_layout.children[0].size.get_value_level() + 1
                else:
                    new_size_value_level = first_layout_size_level - current_layout.children[0].size.get_value_level() - 1
                for entity in second_layout.children:
                    entity.size.set_value_level(new_size_value_level)
            else:
                # Second column
                old_value_level = current_layout.children[0].size.get_value_level()
                self.state["memory"].append(old_value_level)
                
                # Enforce value consistency if needed
                if not current_layout.uniformity.get_value():
                    for entity in current_layout.children:
                        entity.size.set_value_level(old_value_level)
                        
                # Update constraints
                if self.value > 0:
                    size_max_level_orig = sum(current_layout.entity_constraint["Size"]) + 1
                    new_size_max_level = size_max_level_orig - old_value_level - 1
                    second_layout.entity_constraint["Size"][1] = new_size_max_level
                else:
                    size_min_level_orig = (current_layout.entity_constraint["Size"][0] - 1) / 2
                    new_size_max_level = old_value_level - size_min_level_orig - 1
                    second_layout.entity_constraint["Size"] = [size_min_level_orig, new_size_max_level]
                    
                # Sample and apply new sizes
                new_size_min_level, new_size_max_level = second_layout.entity_constraint["Size"]
                the_child = second_layout.children[0]
                the_child.reset_constraint("Size", new_size_min_level, new_size_max_level)
                the_child.size.sample()
                new_size_value_level = the_child.size.get_value_level()
                
                for idx in range(1, len(second_layout.children)):
                    entity = second_layout.children[idx]
                    entity.reset_constraint("Size", new_size_min_level, new_size_max_level)
                    entity.size.set_value_level(new_size_value_level)
                    
        elif self.attr == "Color":
            self.state["color_count"] += 1
            if len(self.state["memory"]) > 0:
                # Third column
                first_layout_color_level = self.state["memory"].pop()
                if self.value > 0:
                    new_color_value_level = first_layout_color_level + current_layout.children[0].color.get_value_level()
                else:
                    new_color_value_level = first_layout_color_level - current_layout.children[0].color.get_value_level()
                for entity in second_layout.children:
                    entity.color.set_value_level(new_color_value_level)
            else:
                # Handle complex color logic for second column
                old_value_level = current_layout.children[0].color.get_value_level()
                
                # Handle special cases to avoid impossible combinations
                reset_current_layout = False
                if self.state["color_count"] == 3 and self.state["color_white_alarm"]:
                    if self.value > 0 and old_value_level == COLOR_MAX:
                        old_value_level = current_layout.children[0].color.sample_new()
                        reset_current_layout = True
                    if self.value < 0 and old_value_level == COLOR_MIN:
                        old_value_level = current_layout.children[0].color.sample_new()
                        reset_current_layout = True
                        
                self.state["memory"].append(old_value_level)
                
                # Ensure consistency
                if reset_current_layout or not current_layout.uniformity.get_value():
                    for entity in current_layout.children:
                        entity.color.set_value_level(old_value_level)
                
                # Update constraints
                if self.value > 0:
                    color_max_level_orig = sum(current_layout.entity_constraint["Color"])
                    new_color_max_level = color_max_level_orig - old_value_level
                    second_layout.entity_constraint["Color"][1] = new_color_max_level
                else:
                    color_min_level_orig = second_layout.entity_constraint["Color"][0] / 2
                    new_color_max_level = old_value_level
                    second_layout.entity_constraint["Color"][:] = [color_min_level_orig, new_color_max_level]
                
                # Sample and apply new colors
                new_color_min_level, new_color_max_level = second_layout.entity_constraint["Color"]
                the_child = second_layout.children[0]
                the_child.reset_constraint("Color", new_color_min_level, new_color_max_level)
                the_child.color.sample()
                new_color_value_level = the_child.color.get_value_level()
                
                # Handle special case with white color
                if self.state["color_count"] == 1:
                    self.state["color_white_alarm"] = (new_color_value_level == 0)
                if self.state["color_count"] == 3 and self.state["color_white_alarm"] and new_color_value_level == 0:
                    new_color_value_level = the_child.color.sample_new()
                    the_child.color.set_value_level(new_color_value_level)
                
                for idx in range(1, len(second_layout.children)):
                    entity = second_layout.children[idx]
                    entity.reset_constraint("Color", new_color_min_level, new_color_max_level)
                    entity.color.set_value_level(new_color_value_level)
        elif self.attr == "Type":
            if len(self.state["memory"]) > 0:
                # Third column
                first_layout_type_level = self.state["memory"].pop()
                if self.value > 0:
                    new_type_value_level = first_layout_type_level + current_layout.children[0].type.get_value_level()
                else:
                    new_type_value_level = first_layout_type_level - current_layout.children[0].type.get_value_level()
                for entity in second_layout.children:
                    entity.type.set_value_level(new_type_value_level)
            else:
                # Second column
                old_value_level = current_layout.children[0].type.get_value_level()
                
                # Ensure consistency
                if not current_layout.uniformity.get_value():
                    for entity in current_layout.children:
                        entity.type.set_value_level(old_value_level)
                
                self.state["memory"].append(old_value_level)
                
                # Update constraints
                if self.value > 0:
                    type_max_level_orig = sum(current_layout.entity_constraint["Type"])
                    new_type_max_level = type_max_level_orig - old_value_level
                    second_layout.entity_constraint["Type"][1] = new_type_max_level
                else:
                    type_min_level_orig = second_layout.entity_constraint["Type"][0] / 2
                    new_type_max_level = old_value_level
                    second_layout.entity_constraint["Type"][:] = [type_min_level_orig, new_type_max_level]
                
                # Sample and apply new types
                new_type_min_level, new_type_max_level = second_layout.entity_constraint["Type"]
                the_child = second_layout.children[0]
                the_child.reset_constraint("Type", new_type_min_level, new_type_max_level)
                the_child.type.sample()
                new_type_value_level = the_child.type.get_value_level()
                
                for idx in range(1, len(second_layout.children)):
                    entity = second_layout.children[idx]
                    entity.reset_constraint("Type", new_type_min_level, new_type_max_level)
                    entity.type.set_value_level(new_type_value_level)
        else:
            raise ValueError(f"Unsupported attribute: {self.attr}")
            
        return target
