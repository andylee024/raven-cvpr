import os
import json
import random
import time
from dataset.core.aot.tensor_panel import TensorPanel
from dataset.core.generators.row_generator import RowGenerator
from dataset.core.generators.constrained_panel_sampler import ConstrainedPanelSampler
from dataset.core.generators.distractor_generator import DistractorGenerator
import dataset.utils.panel_utils as panel_utils

class PuzzleGenerator:
    """Generates complete Raven's Progressive Matrix puzzles."""
    
    def __init__(self, config_path=None):
        """Initialize puzzle generator with optional config path."""
        self.config_path = config_path
        self.config = None
        self.rules = None
        self.constraints = None
        self.row_generator = None
        self.panel_sampler = None
        self.distractor_generator = DistractorGenerator()
        
        # If config path provided, load it immediately
        if config_path:
            self.load_config(config_path)
    
    def load_config(self, config_path):
        """Load a puzzle configuration from JSON file."""
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        # Extract components from config
        self.constraints = self.config['constraints']
        self.rules = self._create_rules_from_config()
        
        # Initialize components
        self.row_generator = RowGenerator(self.rules)
        self.panel_sampler = ConstrainedPanelSampler(self.constraints)
        
        print(f"Loaded puzzle config: {self.config['puzzle_info']['name']}")
        print(f"Difficulty: {self.config['puzzle_info']['difficulty']}")
        print(f"Description: {self.config['puzzle_info']['description']}")
        print(f"Rules: {[rule.name for rule in self.rules]}")
        print(f"Constraints: {self.constraints}")
    
    def _create_rules_from_config(self):
        """Create rule instances from config."""
        from dataset.core.rules.progression import ProgressionRule
        from dataset.core.rules.arithmetic import ArithmeticRule
        from dataset.core.rules.constant import ConstantRule
        from dataset.core.rules.distribute_three import DistributeThreeRule
        
        rule_map = {
            "progression": ProgressionRule,
            "arithmetic": ArithmeticRule,
            "constant": ConstantRule,
            "distribute_three": DistributeThreeRule
        }
        
        rules = []
        rule_configs = sorted(self.config["rules"], key=lambda r: r["order"])
        
        for rule_config in rule_configs:
            rule_type = rule_config["type"]
            rule_class = rule_map[rule_type]
            rule = rule_class(**rule_config["parameters"])
            rules.append(rule)
        
        return rules
    
    def generate(self, num_puzzles=1, max_attempts_per_puzzle=10):
        """Generate multiple complete puzzles.
        
        Args:
            num_puzzles: Number of puzzles to generate
            max_attempts_per_puzzle: Maximum attempts per puzzle
            
        Returns:
            List of generated puzzles
        """
        if not self.config:
            raise ValueError("No puzzle configuration loaded. Call load_config first.")
        
        puzzles = []
        attempt_stats = {"total": 0, "successful": 0, "failed": 0}
        
        for i in range(num_puzzles):
            print(f"Generating puzzle {i+1}/{num_puzzles}...")
            
            # Try generating a valid puzzle with multiple attempts
            for attempt in range(max_attempts_per_puzzle):
                attempt_stats["total"] += 1
                
                try:
                    # Generate the 3x3 grid
                    grid = self._generate_grid()
                    
                    # Get the correct answer (bottom right panel)
                    answer = grid[2][2]
                    
                    # Generate distractors
                    distractors = self.distractor_generator.generate(answer, count=7)
                    
                    # Combine answer and distractors into candidates
                    candidates = [answer] + distractors
                    
                    # Shuffle candidates and track correct answer index
                    indices = list(range(len(candidates)))
                    random.shuffle(indices)
                    
                    # Find where the correct answer ended up after shuffling
                    target_idx = indices.index(0)
                    
                    # Create shuffled candidates 
                    shuffled_candidates = [candidates[idx] for idx in indices]
                    
                    # Convert grid to format expected by visualize functions
                    context = []
                    for row in range(3):
                        for col in range(3):
                            if not (row == 2 and col == 2):  # Skip bottom right
                                context.append(grid[row][col].to_aot().raw)
                    
                    # Convert candidates to format expected by visualize functions
                    candidate_panels = [panel.to_aot().raw for panel in shuffled_candidates]
                    
                    # Package puzzle data in raven_2.py format
                    puzzle = {
                        'context': context,
                        'candidates': candidate_panels,
                        'target': target_idx,
                        'rule_type': self.config['rules'][0]['type'].capitalize(),
                        'attr': self.config['rules'][0]['parameters']['attr_name'],
                        'value': self.config['rules'][0]['parameters'].get('step', 0),
                        'config': self.config['puzzle_info']['name'],
                        'metadata': {
                            'name': self.config['puzzle_info']['name'],
                            'difficulty': self.config['puzzle_info']['difficulty'],
                            'description': self.config['puzzle_info']['description'],
                            'rule_types': [rule_config['type'] for rule_config in self.config['rules']]
                        }
                    }
                    
                    puzzles.append(puzzle)
                    attempt_stats["successful"] += 1
                    print(f"  Success! (attempt {attempt+1}/{max_attempts_per_puzzle})")
                    break
                    
                except Exception as e:
                    attempt_stats["failed"] += 1
                    print(f"  Attempt {attempt+1}/{max_attempts_per_puzzle} failed: {e}")
                    
                    if attempt == max_attempts_per_puzzle - 1:
                        print(f"  Failed to generate puzzle {i+1} after {max_attempts_per_puzzle} attempts")
        
        # Print statistics
        print(f"\nPuzzle generation complete!")
        print(f"Total attempts: {attempt_stats['total']}")
        print(f"Successful: {attempt_stats['successful']}")
        print(f"Failed: {attempt_stats['failed']}")
        print(f"Success rate: {attempt_stats['successful']/attempt_stats['total']*100:.1f}%")
        
        return puzzles
    
    def _generate_grid(self):
        """Generate the full 3×3 grid of panels."""
        # Create empty grid
        grid = [[None for _ in range(3)] for _ in range(3)]
        
        # For each row, generate a sequence using the row_generator
        for i in range(3):
            # Generate seed panel with constraints
            seed_panel = self.panel_sampler.sample_panel()
            
            # Generate the row
            try:
                row = self.row_generator.generate([seed_panel])
                grid[i] = row
            except Exception as e:
                raise ValueError(f"Failed to generate row {i}: {e}")
        
        return grid
