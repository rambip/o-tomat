from stack import Stack


class StringStack(Stack):
    """The string stack is like a normal stack, except it is never empty.
    It always contains at least the empty string."""

    @property
    def stack_contents_type(self):
        return str

    @property
    def bottom_of_pile_symbol(self):
        return ""

    def push(self, word: str) -> None:
        """Push a string onto the stack.
        The empty string is ignored.
        """
        if not isinstance(word, str):
            raise TypeError(
                f"Cannot push a non-string ({type(word)}) into a StringStack.")
        if word != "":
            self.append(word)

    def render(self) -> [str]:
        """Render the stack as a string.
        """
        res = []
        res.append(" ┏")
        res.extend([" ┃ " + e for e in self])
        res.append(" ┗")
        return res
