from abc import ABC, abstractmethod
from .string_stack import StringStack
from .memory import Memory

# so type hinting works
State = 'State'
History = 'History'


class State(ABC):
    """State is an abstract class.
    It is not meant to be actually instanciated, but to be inherited from.
    """

    def __init__(self, init_string=""):
        self.check_instant_update_compat()
        self.init(init_string)

    def init(self, init_string):
        """
        init the class with a "carry" string.
        Is meant to be overriden
        """
        pass

    def __str__(self) -> str:
        """Show the name of the state itself."""
        return f"[{type(self).__name__}]"

    def __eq__(self, other) -> bool:
        return str(self) == str(other)

    def check_instant_update_compat(self):
        """Check if the obect has a `update` or an `instant` method but not both.
        Raises:
            TypeError: If the object has no `update` or `instant` method.
                       If the object has both `update` and `instant` methods.
        """
        if self.has_instant() and self.has_update():
            raise TypeError(
                "State object can have an `update` or an `instant` method, but not both.")
        if (not self.has_instant()) and (not self.has_update()):
            raise TypeError(
                "State object must have an `update` or an `instant` method.")

    def has_instant(self) -> bool:
        return hasattr(self, 'instant')

    def has_update(self) -> bool:
        return hasattr(self, 'update')

    # @abstractmethod
    # def update(self, msg: str, stack_head: str, mem: Memory) -> State: ...
    """how to transition from the current state to any other, depending on
    the typed command.
    """

    # @abstractmethod
    # def instant(self, stack_head: str, mem: Memory) -> State: ...
    """instantanious transition.
    By default, a state does not have an instantanious transition.
    A state must implement update or instant, BUT NOT BOTH !
    Some states (like pop) does not need to render,
    and then update based on a message.
    They will use this functionnality"""

    # @abstractmethod
    # def render(self, mem: Memory) -> list[str]: ...
    """render the state as text
    It can use the "memory" object
    It returns a text box, in a form of a list of strings
    """
