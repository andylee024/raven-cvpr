
POSITION_TO_BBOX = {
    0: (0.16, 0.16, 0.33, 0.33),  # 0: Top-left
    1: (0.16, 0.5, 0.33, 0.33),   # 1: Top-center
    2: (0.16, 0.83, 0.33, 0.33),  # 2: Top-right
    3: (0.5, 0.16, 0.33, 0.33),   # 3: Middle-left
    4: (0.5, 0.5, 0.33, 0.33),    # 4: Middle-center
    5: (0.5, 0.83, 0.33, 0.33),   # 5: Middle-right
    6: (0.83, 0.16, 0.33, 0.33),  # 6: Bottom-left
    7: (0.83, 0.5, 0.33, 0.33),   # 7: Bottom-center
    8: (0.83, 0.83, 0.33, 0.33)   # 8: Bottom-right
}

POSITION_TO_TENSOR_COORDINATE = {
    0: (0, 0),  # Top-left
    1: (0, 1),  # Top-center
    2: (0, 2),  # Top-right
    3: (1, 0),  # Middle-left
    4: (1, 1),  # Middle-center
    5: (1, 2),  # Middle-right
    6: (2, 0),  # Bottom-left
    7: (2, 1),  # Bottom-center
    8: (2, 2)   # Bottom-right
}

def bbox_to_position_index(bbox):
    """Convert a bbox to position index (0-8)."""
    bbox_to_position = {v: k for k, v in POSITION_TO_BBOX.items()}
    return bbox_to_position.get(bbox)

def position_index_to_bbox(position):
    """Convert position index (0-8) to bbox."""
    return POSITION_TO_BBOX[position]

def position_index_to_tensor_coordinate(position):
    """Convert position index (0-8) to tensor coordinate (row, col)."""
    return POSITION_TO_TENSOR_COORDINATE[position]

def tensor_coordinate_to_position_index(row, col):
    """Convert tensor coordinate (row, col) to position index (0-8)."""
    tensor_to_position = {v: k for k, v in POSITION_TO_TENSOR_COORDINATE.items()}
    return tensor_to_position.get((row, col))

def tensor_coordinate_to_bbox(row, col):
    """Convert tensor coordinate (row, col) to bbox."""
    p = tensor_coordinate_to_position_index(row, col)
    return position_index_to_bbox(p)

def bbox_to_tensor_coordinate(bbox):
    """Convert bbox to tensor coordinate (row, col)."""
    p = bbox_to_position_index(bbox)
    return position_index_to_tensor_coordinate(p)
