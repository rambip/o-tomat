"""
Functions about text box : list of strings.
Text boxes are what the UI manipulates.
"""

def width(txt: list[str]) -> int:
    """width of a box of text"""
    return max([len(line) for line in txt])


def height(txt: list[str]) -> int:
    """height of a box of text"""
    return len(txt)





