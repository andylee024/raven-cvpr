import copy
import random
import dataset.utils.panel_utils as panel_utils
from dataset.core.rules.progression import ProgressionRule
from dataset.core.aot.attributes import ATTRIBUTES

class RowGenerator:
    """Generates a row of panels based on a set of rules."""
    
    def __init__(self, rules):
        """Initialize with seed panels and rules."""
        self.rules = rules
        self._required_panels = max([r.required_panels for r in self.rules])
        self._one_panel_rules = [r for r in self.rules if r.required_panels == 1]
        self._two_panel_rules = [r for r in self.rules if r.required_panels == 2]

    def _validate_num_panels(self, seed_panels):
        """Validate the number of seed panels."""
        if len(seed_panels) < self._required_panels:
            raise ValueError("Not enough seed panels for rule set")

    def generate(self, seed_panels):
        self._validate_num_panels(seed_panels)

        row = [None, None, None]
        row[:len(seed_panels)] = seed_panels[:]

        try:
            if self._one_panel_rules:
                row[0] = seed_panels[0]
                row[1] = self._apply_one_panel_rules(row[0])
                row[2] = self._apply_one_panel_rules(row[1])

            if self._two_panel_rules:
                row[2] = self._apply_two_panel_rules(row[0], row[1])

        except Exception as e:
            raise ValueError(f"Error generating row: {e}")
        
        return row

    def _apply_one_panel_rules(self, panel):
        """Apply rules that require one panel (e.g., progression)."""
        panel = panel.clone()
        for rule in self._one_panel_rules:
            panel = rule.apply([panel])
        return panel

    def _apply_two_panel_rules(self, panel1, panel2):
        """Apply rules that require two panels (e.g., arithmetic)."""
        panel1 = panel1.clone()
        panel2 = panel2.clone()
        for rule in self._two_panel_rules:
            panel = rule.apply([panel1, panel2])
        return panel


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
            # attributes = ["number", "type", "size", "angle", "color"]
            # random_attribute = random.choice(attributes)
            # rules = [ProgressionRule(random_attribute, step=1)]
            rules = [ProgressionRule("type", step=1)]
        
        # Generate the complete grid
        grid = self._generate_grid(rules)
        
        # Return the complete puzzle
        return {
            "grid": grid,
            "answer": grid[2][2],  # Bottom-right panel
            "rules": rules
        }
    
    def _generate_grid(self, rules):
        """Generate the complete 3×3 grid by applying rules along rows.
        
        Args:
            seed_panel: Starting panel for position [0,0]
            rules: List of rules to apply across rows
            
        Returns:
            3×3 grid of panels
        """
        # Create empty grid
        grid = [[None for _ in range(3)] for _ in range(3)]
        
        # Generate first row by applying rules sequentially
        grid[0][0] = self._generate_seed_panel("random")
        grid[0][1] = self._apply_rules(grid[0][0], rules)
        grid[0][2] = self._apply_rules(grid[0][1], rules)
        
        # For second row, create a variation of first row
        grid[1][0] = self._generate_seed_panel("random")
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
        # panel_type = random.choice(["uniform", "gradient", "random"])

        if panel_type is None:
            return panel_utils.get_random_panel(n_entities=random.randint(1, 5))
        
        elif panel_type == "uniform":
            return panel_utils.get_uniform_triangle_panel()
        elif panel_type == "gradient":
            return panel_utils.get_gradient_triangle_panel()
        elif panel_type == "random":
            print("Generating random panel")
            return panel_utils.get_random_panel(n_entities=random.randint(1, 5))
        else:
            raise ValueError(f"Invalid panel type: {panel_type}")
