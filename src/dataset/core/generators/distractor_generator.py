import random

from dataset.core.aot.tensor_panel import TensorPanel
from dataset.utils import panel_utils

class DistractorGenerator:
    """Generates distractor panels by perturbing a solution panel."""
    
    def __init__(self, difficulty="medium"):
        """
        Initialize distractor generator with specified difficulty.
        
        Args:
            difficulty: String indicating difficulty level ("easy", "medium", "hard")
        """
        self.difficulty = difficulty
    
    @property
    def strategies(self):
        """
        Define strategies by category.
        
        Returns:
            Dictionary of strategy categories and their corresponding strategies
        """
        return {
            # Hard strategies (subtle changes)
            "hard": [
                "attribute_perturb",        # Small attribute changes
                "entity_swap",              # Swap entity positions
                "global_attribute_change",  # Change same attribute for all entities
                "swap_attributes"          # Swap attributes between entities
            ],
            
            # Medium strategies
            "medium": [
                "rotate_all_entities",  # Rotate all entities
                "entity_add",           # Add an entity
                "entity_remove"         # Remove an entity
            ],
            
            # Easy strategies (obvious changes)
            "easy": [
                "reflect_panel",        # Reflect entire panel
                "scramble_positions"    # Completely rearrange entities
            ]
        }
    
    def _sample_strategy_based_on_distribution(self):
        """Sample a strategy based on the difficulty distribution."""
        
        # Define strategy distributions for each difficulty level
        strategy_distributions = {
            "hard": [
                ("hard", 0.7),     # 70% hard strategies
                ("medium", 0.25),  # 25% medium strategies
                ("easy", 0.05)     # 5% easy strategies
            ],
            "medium": [
                ("hard", 0.3),     # 30% hard strategies
                ("medium", 0.5),   # 50% medium strategies
                ("easy", 0.2)      # 20% easy strategies
            ],
            "easy": [
                ("hard", 0.05),    # 5% hard strategies
                ("medium", 0.35),  # 35% medium strategies
                ("easy", 0.6)      # 60% easy strategies
            ]
        }
        
        # Get distribution for the specified difficulty
        distribution = strategy_distributions[self.difficulty]
        categories, weights = zip(*distribution)
        category = random.choices(categories, weights=weights, k=1)[0]
        strategy = random.choice(self.strategies[category])
        
        return strategy
    
    def generate(self, solution_panel, count=7):
        """
        Generate distractor panels by perturbing a solution panel.
        
        Args:
            solution_panel: The correct answer panel
            count: Number of distractor panels to generate
            
        Returns:
            List of distractor panels
        """
        distractors = []
        for _ in range(count):
            strategy = self._sample_strategy_based_on_distribution()
            distractor = self.apply_strategy(solution_panel, strategy)
            distractors.append(distractor)
            
        return distractors
    
    def apply_strategy(self, panel, strategy):
        """
        Apply a specific perturbation strategy to generate a distractor.
        
        Args:
            panel: Solution panel to perturb
            strategy: Strategy to apply
            
        Returns:
            Perturbed panel
        """
        result = panel.clone()
        
        # Apply the chosen strategy
        if strategy == "attribute_perturb":
            return self._perturb_attribute(result)
        
        elif strategy == "entity_swap":
            return self._swap_entity(result)
        
        elif strategy == "entity_remove":
            return self._remove_entity(result)
        
        elif strategy == "entity_add":
            return self._add_entity(result)
        
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
    def _perturb_attribute(self, panel):
        """Change random attributes of random entities."""
        result_panel = panel.clone()
        
        # Apply multiple perturbations
        for _ in range(3):
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

    def _remove_entity(self, panel):
        """Remove a random entity from the panel."""
        filled_positions = panel.get_filled_positions()
        n_entities = min(2, len(filled_positions))
        entities_to_remove = random.sample(filled_positions, n_entities)

        panel_tensor = panel.tensor
        for row, col in entities_to_remove:
            panel_tensor[row, col, 0] = 0
        panel.tensor = panel_tensor
        return TensorPanel(panel_tensor)
        
    def _add_entity(self, panel):
        """Add a random entity to the panel."""
        # Find all positions with entities
        empty_positions = panel.get_empty_positions()
        n_entities = min(2, len(empty_positions))
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
        num_swaps = min(len(filled_positions) // 2, 2)
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
