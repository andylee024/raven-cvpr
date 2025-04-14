import random

from dataset.core.aot.tensor_panel import TensorPanel
from dataset.utils import panel_utils

class DistractorGenerator:
    """Generates distractor panels by perturbing a solution panel."""
    
    def __init__(self, difficulty=0.5):
        """
        Initialize distractor generator.
        
        Args:
            strategies: List of strategies to use for generating distractors
                       Default strategies include: 
                       - "attribute_swap": Change one attribute value
                       - "entity_remove": Remove one entity
                       - "entity_add": Add one entity
                       - "wrong_rule": Apply wrong rule
            difficulty: Float between 0-1 controlling how challenging distractors should be
        """
        self.difficulty = difficulty
    
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
            distractor = self._apply_strategy(solution_panel, strategy)
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

    def _swap_entity(self, panel, n_times=1):
        """Swap two random entities."""

        filled_positions = panel.get_filled_positions()
        if len(filled_positions) < 2:
            return panel

        panel_tensor = panel.tensor
        for _ in range(n_times):
            # get positions to swap
            e1_pos, e2_pos = random.sample(filled_positions, 2)
            e1_x, e1_y = e1_pos 
            e2_x, e2_y = e2_pos

            # get entities to swap
            e1 = panel_tensor[e1_x, e1_y, :]
            e2 = panel_tensor[e2_x, e2_y, :]

            # swap entities
            panel_tensor[e1_x, e1_y, :] = e2
            panel_tensor[e2_x, e2_y, :] = e1

        panel.tensor = panel_tensor
        return TensorPanel(panel_tensor)

        
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

        print("panel_tensor add \n", panel_tensor[row, col, :])
        panel.tensor = panel_tensor
        return TensorPanel(panel_tensor)
        
    