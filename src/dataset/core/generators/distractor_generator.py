import random

from dataset.core.aot.tensor_panel import TensorPanel
from dataset.utils import panel_utils

class DistractorGenerator:
    """Generates distractor panels by perturbing a solution panel with controllable difficulty."""
    
    def __init__(self, difficulty="medium"):
        """
        Initialize distractor generator with specified difficulty.
        
        Args:
            difficulty: String indicating difficulty level ("easy", "medium", "hard")
                       - "easy": Very obvious differences (easy to spot)
                       - "medium": Moderate differences
                       - "hard": Subtle differences (hard to spot)
        """
        # Convert string difficulty to numerical value
        self.difficulty_mapping = {
            "easy": 0.8,    # High numerical value = more obvious changes
            "medium": 0.5,  # Medium numerical value = balanced changes
            "hard": 0.2     # Low numerical value = subtle changes
        }
        
        self.difficulty = self.difficulty_mapping.get(difficulty, 0.5)
        
        # Organize strategies by difficulty
        self.strategies_by_difficulty = {
            # Hard difficulty (subtle changes)
            "hard": [
                "attribute_perturb",     # Change individual attributes
                "entity_swap"            # Swap entity positions
            ],
            
            # Medium difficulty (noticeable changes)
            "medium": [
                "global_attribute_change",  # Change same attribute for all entities
                "rotate_all_entities",      # Rotate all entities consistently
                "swap_attributes",          # Swap attributes between entities
                "entity_add",               # Add an entity
                "entity_remove"             # Remove an entity
            ],
            
            # Easy difficulty (obvious changes)
            "easy": [
                "reflect_panel",         # Reflect entire panel
                "scramble_positions"     # Completely rearrange entities
            ]
        }
    
    def generate(self, solution_panel, count=7, rule_info=None):
        """
        Generate distractor panels by perturbing a solution panel.
        
        Args:
            solution_panel: The correct answer panel
            count: Number of distractor panels to generate
            rule_info: Optional dict with information about the rule type
            
        Returns:
            List of distractor panels
        """
        distractors = []
        
        # Determine strategy weights based on difficulty
        difficulty_level = self._get_difficulty_level()
        
        # Calculate weights for each difficulty category
        weights = self._calculate_strategy_weights(difficulty_level)
        
        # Generate distractors
        for i in range(count):
            # Select strategy category based on weights
            category = random.choices(
                ["hard", "medium", "easy"], 
                weights=[weights["hard"], weights["medium"], weights["easy"]], 
                k=1
            )[0]
            
            # Select a specific strategy from the chosen category
            strategy = random.choice(self.strategies_by_difficulty[category])
            
            # Apply the strategy to generate a distractor
            distractor = self.apply_strategy(solution_panel, strategy, rule_info)
            distractors.append(distractor)
            
        return distractors
    
    def _get_difficulty_level(self):
        """Convert numerical difficulty to string level."""
        if self.difficulty <= 0.3:
            return "hard"
        elif self.difficulty <= 0.7:
            return "medium"
        else:
            return "easy"
    
    def _calculate_strategy_weights(self, difficulty_level):
        """Calculate weights for each strategy category based on difficulty."""
        if difficulty_level == "hard":
            return {
                "hard": 0.7,     # Mostly subtle changes
                "medium": 0.25,
                "easy": 0.05
            }
        elif difficulty_level == "medium":
            return {
                "hard": 0.3,
                "medium": 0.5,   # Mostly medium changes
                "easy": 0.2
            }
        else:  # easy
            return {
                "hard": 0.05,
                "medium": 0.35,
                "easy": 0.6      # Mostly obvious changes
            }
    
    def apply_strategy(self, panel, strategy, rule_info=None):
        """
        Apply a specific perturbation strategy to generate a distractor.
        
        Args:
            panel: Solution panel to perturb
            strategy: Strategy to apply
            rule_info: Optional information about rules
            
        Returns:
            Perturbed panel
        """
        result = panel.clone()
        
        # Apply the chosen strategy
        if strategy == "attribute_perturb":
            # For hard difficulty, make fewer perturbations
            n_perturbations = max(1, int(self.difficulty * 5))
            return self._perturb_attribute(result, n_perturbations)
        
        elif strategy == "entity_swap":
            return self._swap_entity(result)
        
        elif strategy == "entity_remove":
            # For easier difficulty, remove more entities
            n_entities = max(1, int(self.difficulty * 2))
            return self._remove_entity(result, n_entities)
        
        elif strategy == "entity_add":
            # For easier difficulty, add more entities
            n_entities = max(1, int(self.difficulty * 2))
            return self._add_entity(result, n_entities)
        
        elif strategy == "reflect_panel":
            return self._reflect_panel(result)
            
        elif strategy == "global_attribute_change":
            return self._global_attribute_change(result)
            
        elif strategy == "rotate_all_entities":
            return self._rotate_all_entities(result)
            
        elif strategy == "scramble_positions":
            return self._scramble_positions(result)
            
        elif strategy == "swap_attributes":
            return self._swap_attributes(result)
        
        return result
    
    # Strategy implementation methods
    def _perturb_attribute(self, panel, n_perturbations=3):
        """Change random attributes of random entities."""
        result_panel = panel.clone()
        
        # Apply multiple perturbations
        for _ in range(n_perturbations):
            result_panel = panel_utils.perturb_attribute(result_panel)
        
        return result_panel

    def _swap_entity(self, panel):
        """Swap two entities in the panel while preserving all attributes."""
        # First get the filled positions
        filled_positions = panel.get_filled_positions()
        
        # Check if we have at least 2 entities to swap
        if len(filled_positions) < 2:
            return panel  # Cannot swap with fewer than 2 entities
        
        # Select two random positions to swap
        pos1, pos2 = random.sample(filled_positions, 2)
        
        # Get row and column for each position
        row1, col1 = pos1
        row2, col2 = pos2
        
        # Create complete copies of the tensor slices
        entity1 = panel.tensor[row1, col1].clone()
        entity2 = panel.tensor[row2, col2].clone()
        
        # Swap the entities by exchanging their tensor values
        panel.tensor[row1, col1] = entity2
        panel.tensor[row2, col2] = entity1
        
        return panel

    def _remove_entity(self, panel, n_entities=1):
        """Remove a random entity from the panel."""
        filled_positions = panel.get_filled_positions()
        n_entities = min(n_entities, len(filled_positions))
        entities_to_remove = random.sample(filled_positions, n_entities)

        panel_tensor = panel.tensor
        for row, col in entities_to_remove:
            panel_tensor[row, col, 0] = 0
        panel.tensor = panel_tensor
        return TensorPanel(panel_tensor)
        
    def _add_entity(self, panel, n_entities=1):
        """Add a random entity to the panel."""
        # Find all positions with entities
        empty_positions = panel.get_empty_positions()
        n_entities = min(n_entities, len(empty_positions))
        entities_to_add = random.sample(empty_positions, n_entities)

        panel_tensor = panel.tensor
        for row, col in entities_to_add:
            panel_tensor[row, col, :] = panel_utils.sample_entity_tensor()

        panel.tensor = panel_tensor
        return TensorPanel(panel_tensor)

    def _reflect_panel(self, panel):
        """Reflect the panel horizontally or vertically."""
        result = panel.clone()
        tensor = result.tensor.clone()
    
        # Determine reflection axis
        horizontal = random.choice([True, False])
    
        if horizontal:
            # Reflect horizontally (swap rows)
            for row in range(3):
                tensor[2-row, :, :] = result.tensor[row, :, :]
        else:
            # Reflect vertically (swap columns)
            for col in range(3):
                tensor[:, 2-col, :] = result.tensor[:, col, :]

        return TensorPanel(tensor)
    
    def _global_attribute_change(self, panel):
        """Change the same attribute for all entities in the panel."""
        result = panel.clone()
        filled_positions = result.get_filled_positions()
        
        if not filled_positions:
            return result
        
        # Select a random attribute to modify
        attribute = random.choice(['type', 'size', 'angle', 'color'])
        
        # Determine the change to apply (consistent across entities)
        attr_obj = result._attributes[attribute]
        change_amount = random.randint(1, 3)  # Medium to significant change
        change_direction = random.choice([-1, 1])
        change = change_amount * change_direction
        
        # Apply the same change to all entities
        for row, col in filled_positions:
            current_value = result.get_attr(row, col, attribute)
            # Apply change with wrapping (modulo)
            new_value = (current_value + change) % (attr_obj.max_val + 1)
            # Ensure value is in valid range
            if new_value < attr_obj.min_val:
                new_value = attr_obj.max_val - (attr_obj.min_val - new_value - 1)
            
            result.set_attr(row, col, attribute, new_value)
        
        return result

    def _rotate_all_entities(self, panel):
        """Rotate all entities by a consistent amount."""
        result = panel.clone()
        filled_positions = result.get_filled_positions()

        # Choose a rotation increment (medium to significant)
        rotation = random.choice([2, 3, 4, 6])  # 90°, 135°, 180°, or 270°

        # Apply rotation to all entities
        for row, col in filled_positions:
            current_angle = result.get_attr(row, col, 'angle')
            new_angle = (current_angle + rotation) % 8  # Assuming 8 possible angles (0-7)
            result.set_attr(row, col, 'angle', new_angle)

        return result
    
    def _scramble_positions(self, panel):
        """Scramble entity positions."""
        result = panel.clone()
        filled_positions = result.get_filled_positions()
    
        if len(filled_positions) <= 1:
            return result
    
        # Create new tensor with zeros
        new_tensor = result.tensor.clone()
        new_tensor[:, :, :] = 0
    
        # Extract all entities
        entities = [result.tensor[row, col].clone() for row, col in filled_positions]
    
        # Shuffle entities
        random.shuffle(entities)
    
        # Randomize position mapping
        new_positions = filled_positions.copy()
        random.shuffle(new_positions)
    
        # Place shuffled entities at shuffled positions
        for entity, (row, col) in zip(entities, new_positions):
            new_tensor[row, col] = entity
    
        return TensorPanel(new_tensor)

    def _swap_attributes(self, panel):
        """Swap attributes between entities."""
        result = panel.clone()
        filled_positions = result.get_filled_positions()
        
        # Need at least 2 entities
        if len(filled_positions) < 2:
            return result
        
        # Choose attribute to swap
        attribute = random.choice(['type', 'size', 'angle', 'color'])
        
        # Select positions to swap attributes between
        num_swaps = min(len(filled_positions) // 2, 2 + int(self.difficulty * 3))
        positions_to_swap = []
        
        # Create pairs of positions
        available_positions = filled_positions.copy()
        for _ in range(num_swaps):
            if len(available_positions) < 2:
                break
            
            # Pick two positions
            pos1 = random.choice(available_positions)
            available_positions.remove(pos1)
            
            pos2 = random.choice(available_positions)
            available_positions.remove(pos2)
            
            positions_to_swap.append((pos1, pos2))
        
        # Swap the attributes
        for pos1, pos2 in positions_to_swap:
            row1, col1 = pos1
            row2, col2 = pos2
            
            # Get values
            value1 = result.get_attr(row1, col1, attribute)
            value2 = result.get_attr(row2, col2, attribute)
            
            # Swap values
            result.set_attr(row1, col1, attribute, value2)
            result.set_attr(row2, col2, attribute, value1)
        
        return result
