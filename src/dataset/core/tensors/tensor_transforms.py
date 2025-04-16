import torch

# Transpose (swap rows and columns)
def transpose(tensor):
    return tensor.transpose(0, 1)

# 90° clockwise rotation
def rotate_90_clockwise(tensor, shifts=1):
    normalized_shifts = shifts % 4
    for _ in range(normalized_shifts):
        tensor = tensor.transpose(0, 1).flip(0)
    return tensor

# 90° counterclockwise rotation
def rotate_90_counterclockwise(tensor, shifts=1):
    normalized_shifts = shifts % 4
    for _ in range(normalized_shifts):
        tensor = tensor.transpose(0, 1).flip(1)
    return tensor
    
# 180° rotation
def rotate_180(tensor):
    return tensor.flip(0).flip(1)

# Horizontal reflection (mirror across vertical axis)
def reflect_horizontal(tensor):
    return tensor.flip(1)  # Flip columns

# Vertical reflection (mirror across horizontal axis)
def reflect_vertical(tensor):
    return tensor.flip(0)  # Flip rows

# Diagonal reflection (mirror across main diagonal)
def reflect_diagonal(tensor):
    return tensor.transpose(0, 1)

# Swap specified rows
def swap_rows(tensor, row1=0, row2=1):
    result = tensor.clone()
    result[row1], result[row2] = result[row2].clone(), result[row1].clone()
    return result

# Swap specified columns
def swap_columns(tensor, col1=0, col2=1):
    result = tensor.clone()
    result[:, col1], result[:, col2] = result[:, col2].clone(), result[:, col1].clone()
    return result

# Shift entities to the right
def shift_entities_right(tensor, shifts=1):
    """Shift tensor RIGHT with wrapping.
    
    Positive shifts move elements to the RIGHT.
    Negative shifts move elements to the LEFT.
    """
    # Make sure we're shifting in the correct direction (dim=1 is columns)
    return torch.roll(tensor, shifts=shifts, dims=1)

# Shift entities down
def shift_entities_down(tensor, shifts=1):
    return torch.roll(tensor, shifts=shifts, dims=0)

# Diagonal shift (down and right)
def shift_diagonal(tensor, shifts=1):

    if isinstance(shifts, (int, float)):
        shifts_tuple = (shifts, shifts)
    else:
        shifts_tuple = shifts
    return torch.roll(tensor, shifts=shifts_tuple, dims=(0, 1))
