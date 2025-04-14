import random

from dataset.core.aot.tensor_panel import TensorPanel
from dataset.utils import panel_utils

class DistractorGenerator:
    """Generates distractor panels by perturbing a solution panel."""
    
    def __init__(self, difficulty=0.5):
        """
        Initialize distractor generator.
        
        Args:
            difficulty: Float between 0-1 controlling how challenging distractors should be
        """
        self.difficulty = difficulty
        self.strategies = [
            "attribute_perturb",
            "entity_swap",
            "entity_remove",
            "entity_add"
        ]
    
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
        
        # Generate distractors using different strategies
        for i in range(count):
            strategy = random.choice(self.strategies)
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
        if strategy == "attribute_perturb":
            self._perturb_attribute(result)
        elif strategy == "entity_swap":
            self._swap_entity(result)
        elif strategy == "entity_remove":
            self._remove_entity(result)
        elif strategy == "entity_add":
            self._add_entity(result)
            
        return result
    
    # Strategy implementation methods
    def _perturb_attribute(self, panel, n_perturbations=3):
        """Change a random attribute of a random entity."""
        filled_positions = panel.get_filled_positions()

        # pick an entity to perturb
        pos = random.sample(filled_positions, 1)

        # perturb a single attribute (n times)
        panel_tensor = panel.tensor
        for _ in range(n_perturbations):
            attribute_index, attribute_value = panel_utils.sample_random_attribute_index_and_value()
            panel_tensor[pos[0], pos[1], attribute_index] = attribute_value

        return TensorPanel(panel_tensor)

    def _swap_entity(self, panel):
        """Swap two entities in the panel while preserving all attributes.
        
        Args:
            panel: The panel to modify
            
        Returns:
            Modified panel with two entities swapped
        """
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
            panel_tensor[row, col, :] = panel_utils.sample_entity()

        panel.tensor = panel_tensor
        return TensorPanel(panel_tensor)
        
    