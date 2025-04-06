from abc import ABC, abstractmethod
import copy

class Rule(ABC):
    """Base abstract class for all rules in the RAVEN system.
    
    Rules define how attributes change between panels in a puzzle.
    Each rule operates on a specific attribute and component.
    """
    
    def __init__(self, attr, value=None, component_idx=0):
        """Initialize a rule.
        
        Args:
            attr (str): The attribute this rule applies to ('Number', 'Position', 'Type', etc.)
            value (any): The value parameter for this rule (meaning depends on rule type)
            component_idx (int): The component index this rule applies to
        """
        self.attr = attr
        self.value = value
        self.component_idx = component_idx
        self.state = {}  # Storage for rule-specific state (e.g., memory between applications)
    
    @abstractmethod
    def apply(self, source_panel, target_panel=None):
        """Apply this rule to generate a new panel.
        
        Args:
            source_panel: The source panel AoT
            target_panel: Optional pre-existing target panel to modify
                          (if None, a copy of source_panel will be created)
                          
        Returns:
            The modified target panel AoT
        """
        pass
    
    def _get_layout(self, panel):
        """Helper method to get the layout of the component this rule applies to.
        
        Args:
            panel: An AoT panel
            
        Returns:
            The layout node of the relevant component
        """
        return panel.children[0].children[self.component_idx].children[0]
    
    def _copy_if_none(self, source_panel, target_panel):
        """Create a copy of source_panel if target_panel is None.
        
        Args:
            source_panel: The source panel AoT
            target_panel: Optional target panel AoT
            
        Returns:
            A target panel (either the provided one or a copy)
        """
        if target_panel is None:
            return copy.deepcopy(source_panel)
        return target_panel
    
    def __str__(self):
        """Return a string representation of this rule."""
        return f"{self.__class__.__name__}(attr={self.attr}, value={self.value}, component={self.component_idx})"
