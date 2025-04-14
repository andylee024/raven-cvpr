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