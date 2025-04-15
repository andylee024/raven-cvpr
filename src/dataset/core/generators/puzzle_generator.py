import json
import random

from dataset.core.generators.row_generator import RowGenerator
from dataset.core.generators.constrained_panel_sampler import ConstrainedPanelSampler
from dataset.core.generators.distractor_generator import DistractorGenerator
from dataset.core.rules.factory import RuleFactory

class PuzzleGenerator:
    """Generates complete Raven's Progressive Matrix puzzles."""
    
    def __init__(self, config_path):
        """Initialize puzzle generator with config path."""
        self.config_path = config_path
        self.load_config(config_path)

        # load rules and constraints from config
        self.config = self.load_config(config_path)
        self.rules = self._create_rules_from_config(self.config['rules'])
        self.constraints = self.config['constraints']

        self.row_generator = RowGenerator(self.rules)
        self.panel_sampler = ConstrainedPanelSampler(self.constraints)
        self.distractor_generator = DistractorGenerator()
        
    
    def load_config(self, config_path):
        """Load a puzzle configuration from JSON file."""
        with open(config_path, 'r') as f:
            config = json.load(f)
            return config
    
    def _create_rules_from_config(self, rules_config):
        """Create rule instances from config."""
        
        factory = RuleFactory()
        rule_configs = sorted(rules_config, key=lambda r: r["order"])
        
        rules = []
        for rule_config in rule_configs:
            rule = factory.create_from_config(rule_config)
            rules.append(rule)
        
        return rules
    
    def generate(self, num_puzzles=1, max_attempts_per_puzzle=10):
        """Generate multiple complete puzzles."""
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
                    # generate puzzle (context, solution, distractors)
                    grid = self._generate_grid()
                    answer = grid[2][2]
                    candidates, target_idx = self._handle_candidate_creation(answer)
                    context = self._create_context_from_grid(grid)

                    # store puzzle data
                    puzzle = self._format_puzzle_data(context, candidates, target_idx)
                    puzzles.append(puzzle)

                    # stats
                    attempt_stats["successful"] += 1
                    print(f"  Success! (attempt {attempt+1}/{max_attempts_per_puzzle})")
                    break
                    
                except Exception as e:
                    attempt_stats["failed"] += 1
                    print(f"  Attempt {attempt+1}/{max_attempts_per_puzzle} failed: {e}")
                    
                    if attempt == max_attempts_per_puzzle - 1:
                        print(f"  Failed to generate puzzle {i+1} after {max_attempts_per_puzzle} attempts")
                    import traceback
                    traceback.print_exc()  # Add this line to see the full stack trace
        
        # print stats
        self._print_generation_stats(attempt_stats)
        return puzzles
    
    def _handle_candidate_creation(self, answer):
        """Generate and prepare candidates (answer + distractors).
        
        Args:
            answer: The correct answer panel
            
        Returns:
            Tuple of (candidate_panels, target_index)
        """
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
        
        # Convert to format expected by visualize functions
        candidate_panels = [panel.to_aot().raw for panel in shuffled_candidates]
        
        return candidate_panels, target_idx
    
    def _create_context_from_grid(self, grid):
        """Convert a grid to context format (excluding bottom right panel).
        
        Args:
            grid: The 3x3 puzzle grid
            
        Returns:
            List of panels in context format
        """
        context = []
        for row in range(3):
            for col in range(3):
                if not (row == 2 and col == 2):  # Skip bottom right
                    context.append(grid[row][col].to_aot().raw)
        
        return context
    
    def _format_puzzle_data(self, context, candidates, target_idx):
        """Format puzzle data into a standardized dictionary.
        
        Args:
            context: List of panels in the context grid
            candidates: List of candidate panels
            target_idx: Index of the correct answer
            
        Returns:
            Dictionary with formatted puzzle data
        """
        return {
            'context': context,
            'candidates': candidates,
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
    
    def _generate_grid(self):
        """Generate the full 3×3 grid of panels."""
        grid = [[None for _ in range(3)] for _ in range(3)]
        
        for i in range(3):
            seed_panel = self.panel_sampler.sample_panel()
            try:
                row = self.row_generator.generate([seed_panel])
                grid[i] = row
            except Exception as e:
                raise ValueError(f"Failed to generate row {i}: {e}")
        
        return grid
    
    def _print_generation_stats(self, stats):
        """Print generation statistics.
        
        Args:
            stats: Dictionary with generation statistics
        """
        print(f"\nPuzzle generation complete!")
        print(f"Total attempts: {stats['total']}")
        print(f"Successful: {stats['successful']}")
        print(f"Failed: {stats['failed']}")
        
        if stats['total'] > 0:
            success_rate = stats['successful']/stats['total']*100
            print(f"Success rate: {success_rate:.1f}%")
