"""Path configuration for the RAVEN-CVPR project."""

import os
from pathlib import Path

# Find the project root (works regardless of current working directory)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent

# Define key directories
OUTPUT_DIR = PROJECT_ROOT / "output"
TEST_OUTPUT_DIR = OUTPUT_DIR / "tests"
PUZZLE_OUTPUT_DIR = OUTPUT_DIR / "puzzles"
RULE_TEST_OUTPUT_DIR = TEST_OUTPUT_DIR / "rules"
DISTRACTOR_TEST_OUTPUT_DIR = TEST_OUTPUT_DIR / "distractors"
CONFIG_DIR = PROJECT_ROOT / "src/dataset/config"

# Create output directories
for directory in [OUTPUT_DIR, TEST_OUTPUT_DIR, PUZZLE_OUTPUT_DIR, 
                 RULE_TEST_OUTPUT_DIR, DISTRACTOR_TEST_OUTPUT_DIR, CONFIG_DIR]:
    os.makedirs(directory, exist_ok=True)

def get_test_output_path(test_name, filename=None):
    """Get output path for a specific test.
    
    Args:
        test_name: Name of the test (used as subdirectory)
        filename: Optional filename to append
        
    Returns:
        Path object for the output directory or file
    """
    test_dir = TEST_OUTPUT_DIR / test_name
    os.makedirs(test_dir, exist_ok=True)
    
    if filename:
        return test_dir / filename
    return test_dir
