import copy
import random
import dataset.utils.panel_utils as panel_utils
from dataset.core.rules.progression import ProgressionRule
from dataset.core.aot.attributes import ATTRIBUTES


class TensorPuzzleGenerator:
    """Generates RAVEN puzzles using tensor-based panels with row rules."""
    
    def __init__(self):
        """Initialize the puzzle generator."""
        pass
    
    def generate(self, rules=None, seed_panel=None):
        """Generate a complete 3×3 grid puzzle using the specified rules.
        
        Args:
            rules: List of rules to apply across rows (left-to-right)
            seed_panel: Optional starting panel for position [0,0]
            
        Returns:
            Dictionary containing the complete puzzle grid and metadata
        """
        # Generate or use provided seed panel
        if seed_panel is None:
            seed_panel = self._generate_seed_panel()
        
        if rules is None:
            attributes = ["type", "size", "angle", "color"]
            random_attribute = random.choice(attributes)
            rules = [ProgressionRule(random_attribute, step=1)]
        
        # Generate the complete grid
        grid = self._generate_grid(seed_panel, rules)
        
        # Return the complete puzzle
        return {
            "grid": grid,
            "answer": grid[2][2],  # Bottom-right panel
            "rules": rules
        }
    
    def _generate_grid(self, seed_panel, rules):
        """Generate the complete 3×3 grid by applying rules along rows.
        
        Args:
            seed_panel: Starting panel for position [0,0]
            rules: List of rules to apply across rows
            
        Returns:
            3×3 grid of panels
        """
        # Create empty grid
        grid = [[None for _ in range(3)] for _ in range(3)]
        
        # Place seed panel
        grid[0][0] = seed_panel
        
        # Generate first row by applying rules sequentially
        grid[0][1] = self._apply_rules(grid[0][0], rules)
        grid[0][2] = self._apply_rules(grid[0][1], rules)
        
        # For second row, create a variation of first row
        grid[1][0] = self._generate_seed_panel("gradient")
        grid[1][1] = self._apply_rules(grid[1][0], rules)
        grid[1][2] = self._apply_rules(grid[1][1], rules)
        
        # For third row, create another variation
        grid[2][0] = self._generate_seed_panel("random")
        grid[2][1] = self._apply_rules(grid[2][0], rules)
        grid[2][2] = self._apply_rules(grid[2][1], rules)
        
        return grid
    
    def _apply_rules(self, panel, rules):
        """Apply a sequence of rules to a panel.
        
        Args:
            panel: Source panel
            rules: List of rules to apply
            
        Returns:
            New panel after applying all rules
        """
        result = panel.clone()
        for rule in rules:
            result = rule.apply(result)
        return result
    
    def _generate_seed_panel(self, panel_type=None):
        """Generate a random seed panel.
        
        Returns:
            A TensorPanel to use as the top-left panel
        """
        panel_type = random.choice(["uniform", "gradient", "random"])

        if panel_type is None:
            return panel_utils.get_random_panel(n_entities=random.randint(1, 9))
        
        elif panel_type == "uniform":
            return panel_utils.get_uniform_triangle_panel()
        elif panel_type == "gradient":
            return panel_utils.get_gradient_triangle_panel()
        elif panel_type == "random":
            return panel_utils.get_random_panel(n_entities=random.randint(1, 9))
        else:
            raise ValueError(f"Invalid panel type: {panel_type}")
