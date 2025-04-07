from dataset.core.rules.base import Rule
import copy
import numpy as np

class DistributeThreeRule(Rule):
    """Ternary operator where three values across columns form a fixed set.
    
    This rule selects three distinct values and distributes them across
    the matrix in a specific pattern, cycling through rows.
    """
    
    def __init__(self, attr):
        """Initialize a distribute three rule.
        
        Args:
            attr: Attribute to distribute (Number, Position, Type, Size, Color)
        """
        super().__init__(attr=attr)
        self.state = {
            "value_levels": [],  # Stores the three values for each row
            "count": 0           # Tracks application count for sequencing
        }
    
    def apply(self, source, target=None):
        """Apply distribute three rule to create target panel.
        
        Args:
            source: Source panel to apply rule from
            target: Optional target panel (created if None)
            
        Returns:
            Modified panel after rule application
        """
        if target is None:
            target = copy.deepcopy(source)
            
        current_layout = source.children[0].children[self.component_idx].children[0]
        second_layout = target.children[0].children[self.component_idx].children[0]
        
        # Handle attribute-specific distribution logic
        if self.attr == "Number":
            if self.state["count"] == 0:
                # First application: select three distinct values
                all_value_levels = list(range(
                    current_layout.layout_constraint["Number"][0], 
                    current_layout.layout_constraint["Number"][1] + 1
                ))
                current_value_level = current_layout.number.get_value_level()
                idx = all_value_levels.index(current_value_level)
                all_value_levels.pop(idx)
                
                # Randomly select two more values
                three_value_levels = np.random.choice(all_value_levels, 2, False)
                three_value_levels = np.insert(three_value_levels, 0, current_value_level)
                
                # Set up value patterns for all rows
                self._setup_value_patterns(three_value_levels)
                
                # Apply to the second panel
                second_layout.number.set_value_level(self.state["value_levels"][0][1])
            else:
                # Handle subsequent applications
                row, col = divmod(self.state["count"], 2)
                if col == 0:
                    # First column of a new row
                    current_layout.number.set_value_level(self.state["value_levels"][row][0])
                    current_layout.resample()
                    # Create a new second layout reflecting the change
                    target = copy.deepcopy(source)
                    second_layout = target.children[0].children[self.component_idx].children[0]
                    second_layout.number.set_value_level(self.state["value_levels"][row][1])
                else:
                    # Third column
                    second_layout.number.set_value_level(self.state["value_levels"][row][2])
            
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
            if self.state["count"] == 0:
                # First application: select three distinct position patterns
                num = current_layout.number.get_value()
                pos_0 = current_layout.position.get_value_idx()
                pos_1 = current_layout.position.sample_new(num)
                pos_2 = current_layout.position.sample_new(num, [pos_1])
                
                three_value_levels = np.array([pos_0, pos_1, pos_2])
                self._setup_value_patterns(three_value_levels)
                
                # Apply to the second panel
                second_layout.position.set_value_idx(self.state["value_levels"][0][1])
            else:
                # Handle subsequent applications
                row, col = divmod(self.state["count"], 2)
                if col == 0:
                    # First column of a new row
                    current_layout.number.set_value_level(len(self.state["value_levels"][row][0]) - 1)
                    current_layout.resample()
                    current_layout.position.set_value_idx(self.state["value_levels"][row][0])
                    
                    # Update entity positions
                    pos = current_layout.position.get_value()
                    for i in range(len(pos)):
                        entity = current_layout.children[i]
                        entity.bbox = pos[i]
                    
                    # Create a new second layout reflecting the change
                    target = copy.deepcopy(source)
                    second_layout = target.children[0].children[self.component_idx].children[0]
                    second_layout.position.set_value_idx(self.state["value_levels"][row][1])            
                else:
                    # Third column
                    second_layout.position.set_value_idx(self.state["value_levels"][row][2])
            
            # Update entity positions
            pos = second_layout.position.get_value()
            for i in range(len(pos)):
                entity = second_layout.children[i]
                entity.bbox = pos[i]
                
        elif self.attr == "Type":
            if self.state["count"] == 0:
                # First application: select three distinct type values
                all_value_levels = range(
                    current_layout.entity_constraint["Type"][0], 
                    current_layout.entity_constraint["Type"][1] + 1
                )
                three_value_levels = np.random.choice(list(all_value_levels), 3, False)
                np.random.shuffle(three_value_levels)
                
                self._setup_value_patterns(three_value_levels)
                
                # Apply to current and second panel
                for entity in current_layout.children:
                    entity.type.set_value_level(self.state["value_levels"][0][0])
                for entity in second_layout.children:
                    entity.type.set_value_level(self.state["value_levels"][0][1])
            else:
                # Handle subsequent applications
                row, col = divmod(self.state["count"], 2)
                if col == 0:
                    # First column of a new row
                    value_level = self.state["value_levels"][row][0]
                    for entity in current_layout.children:
                        entity.type.set_value_level(value_level)
                    
                    value_level = self.state["value_levels"][row][1]
                    for entity in second_layout.children:
                        entity.type.set_value_level(value_level)
                else:
                    # Third column
                    value_level = self.state["value_levels"][row][2]
                    for entity in second_layout.children:
                        entity.type.set_value_level(value_level)
                        
        elif self.attr == "Size":
            if self.state["count"] == 0:
                # First application: select three distinct size values
                all_value_levels = range(
                    current_layout.entity_constraint["Size"][0], 
                    current_layout.entity_constraint["Size"][1] + 1
                )
                three_value_levels = np.random.choice(list(all_value_levels), 3, False)
                
                self._setup_value_patterns(three_value_levels)
                
                # Apply to current and second panel
                for entity in current_layout.children:
                    entity.size.set_value_level(self.state["value_levels"][0][0])
                for entity in second_layout.children:
                    entity.size.set_value_level(self.state["value_levels"][0][1])
            else:
                # Handle subsequent applications
                row, col = divmod(self.state["count"], 2)
                if col == 0:
                    # First column of a new row
                    value_level = self.state["value_levels"][row][0]
                    for entity in current_layout.children:
                        entity.size.set_value_level(value_level)
                    
                    value_level = self.state["value_levels"][row][1]
                    for entity in second_layout.children:
                        entity.size.set_value_level(value_level)
                else:
                    # Third column
                    value_level = self.state["value_levels"][row][2]
                    for entity in second_layout.children:
                        entity.size.set_value_level(value_level)
                        
        elif self.attr == "Color":
            if self.state["count"] == 0:
                # First application: select three distinct color values
                all_value_levels = range(
                    current_layout.entity_constraint["Color"][0], 
                    current_layout.entity_constraint["Color"][1] + 1
                )
                three_value_levels = np.random.choice(list(all_value_levels), 3, False)
                
                self._setup_value_patterns(three_value_levels)
                
                # Apply to current and second panel
                for entity in current_layout.children:
                    entity.color.set_value_level(self.state["value_levels"][0][0])
                for entity in second_layout.children:
                    entity.color.set_value_level(self.state["value_levels"][0][1])
            else:
                # Handle subsequent applications
                row, col = divmod(self.state["count"], 2)
                if col == 0:
                    # First column of a new row
                    value_level = self.state["value_levels"][row][0]
                    for entity in current_layout.children:
                        entity.color.set_value_level(value_level)
                    
                    value_level = self.state["value_levels"][row][1]
                    for entity in second_layout.children:
                        entity.color.set_value_level(value_level)
                else:
                    # Third column
                    value_level = self.state["value_levels"][row][2]
                    for entity in second_layout.children:
                        entity.color.set_value_level(value_level)
        else:
            raise ValueError(f"Unsupported attribute: {self.attr}")
            
        # Update application counter (cycles through 6 states for 3 rows x 2 columns)
        self.state["count"] = (self.state["count"] + 1) % 6
        
        return target
    
    def _setup_value_patterns(self, three_value_levels):
        """Set up the patterns of values for all rows.
        
        Args:
            three_value_levels: Array of three values to distribute
        """
        # First row always uses original order
        self.state["value_levels"] = []
        self.state["value_levels"].append(three_value_levels[[0, 1, 2]])
        
        # Randomly choose between two possible cycling patterns for rows 2-3
        if np.random.uniform() >= 0.5:
            self.state["value_levels"].append(three_value_levels[[1, 2, 0]])
            self.state["value_levels"].append(three_value_levels[[2, 0, 1]])
        else:
            self.state["value_levels"].append(three_value_levels[[2, 0, 1]])
            self.state["value_levels"].append(three_value_levels[[1, 2, 0]])
