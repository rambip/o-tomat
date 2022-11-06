"""
Functions about text box : list of strings.
Text boxes are what the UI manipulates.
"""

def width(txt: list[str]) -> int:
    """width of a box of text"""
    return max(map(len, txt))


def height(txt: list[str]) -> int:
    """height of a box of text"""
    return len(txt)


def wrap(txt: list[str], max_width: int) -> list[str]:
    """wrap a text to limit its width.
    Args:
        txt (list[str]): The text to wrap.
        max_width (int): The width that you wrap at.
            Lines shorter won't be touched
            lines longer will be split in lines of this length (or less for the
            last one).
    Returns:
        list[str]: The text, but split into lines of length less or equal to
            `max_width`.
    """
    res = []
    for line in txt:
        if len(line) < max_width:  # nothing to wrap
            res.append(line)
        else:
            # (len(line) // max_width) is the number of lines you'll get
            # splitting the current one
            for i in range(len(line) // max_width):
                res.append(line[max_width*i:max_width*(i+1)])
    return res


