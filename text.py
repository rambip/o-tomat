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


def wrap(txt: list[str], max_width: int) -> list[str]:
    """wrap a text to limit idx width."""
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


