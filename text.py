"""
Functions about text box : list of strings.
Text boxes are what the UI manipulates.
"""

def width(b) -> int:
    """width of a box of text"""
    return max([len(line) for line in b])


def height(b) -> int:
    """height of a box of text"""
    return len(b)
