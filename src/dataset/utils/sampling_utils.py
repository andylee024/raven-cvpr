import random

def get_random_positions(n_entities=None):
    """Generate a list of random positions."""
    if n_entities is None:
        n_entities = random.randint(1, 9)
    return random.sample([(r, c) for r in range(3) for c in range(3)], n_entities)
