
class StringStack(list):
    """The string stack is like a normal stack, except it is never empty.
    It always contains at least the empty string."""

    def head(self) -> str:
        """Get the head of the stack"""
        l = len(self)
        if l == 0:
            return ""
        return l[l-1]

    def pop(self) -> str:
        """Pop the first string from the stack.
        Returns:
            str: The top element of the stack (it is removed from the stack). None if the stack is empty.
        """
        if len(self) != 0:
            list.pop(self)

    def push(self, word: str) -> None:
        """Push a string onto the stack.
        The empty string is ignored.
        """
        if word != "":
            self.append(word)

    def __str__(self) -> str:
        """Render the stack as a string."""
        # return "[\t"+"\n\t".join(self) + "\n]"
        res = " ┏\n ┃  "
        res += "\n ┃  ".join(self)
        res += "\n ┗"
        return res
