from abc import ABC, abstractmethod, abstractproperty

StackValue = "StackValue"  # type hinting


class Stack(list, ABC):
    """Abstract class representing a strictly typed stack.
    Any element added into the stack will be passed through type checking to
    see if it matches the type.s contained in `stack_contents_type`.
    """

    @property
    @abstractproperty
    def stack_contents_type(self):
        """Type of the stack contents.
        Can be a tuple containing all the possible types (union of types).
        """

    @property
    @abstractproperty
    def bottom_of_pile_symbol(self):
        """Symbol returned when the stack is empty"""
        return None

    def is_of_correct_type(self, value) -> bool:
        """Check if value is of correct type for the stack.
        """
        return isinstance(value, self.stack_contents_type)

    def head(self) -> StackValue:
        """Get the top of the stack."""
        if len(self) == 0:
            return self.bottom_of_pile_symbol
        return l[-1]  # return last element -> top of the stack

    def push(self, value: StackValue) -> None:
        """Put a value into the top of the stack."""
        # do not accept values of incorrect type
        if not self.is_of_correct_type(value):
            raise TypeError(
                f"Type {type(value)} is not acceptable in this stack.")
        self.append(value)

    def pop(self) -> StackValue:
        """Get the top of the stack """
        # empty list : return the bottom-of-stack symbol
        if len(self) == 0:
            return self.bottom_of_pile_symbol
        # basic action : pop from the list
        return list.pop(self)
