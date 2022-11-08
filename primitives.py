from string_stack import StringStack
from abc import ABC, abstractmethod


State = 'State'  # so type hinting works
class State(ABC):
    """State is an abstract class.
    It is not meant to be actually instanciated, but to be inherited from.
    """

    def __init__(self):
        self.check_instant_update_compat()

    def __repr__(self) -> str:
        """Show the name of the state itself."""
        return f"[{type(self).__name__}]"

    def __eq__(self, other) -> bool:
        return repr(self) == repr(other)

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
    # def update(self, msg: str, stack: StringStack) -> State: ...
    """how to transition from the current state to any other, depending on
    the typed command.
    """

    # @abstractmethod
    # def instant(self, stack: StringStack) -> State: ...
    """instantanious transition.
    By default, a state does not have an instantanious transition.
    A state must implement update or instant, BUT NOT BOTH !
    Some states (like pop) does not need to render,
    and then update based on a message.
    They will use this functionnality"""



# Default state. Also the initial one
class MenuState(State):
    def __init__(self, message: str = "Waiting for command"):
        super(MenuState, self).__init__()  # call parent class' constructor
        # has to be defined inside the constructor, because the reference to
        # the class itself (MenuState) will be impossible else
        self.transitions = {
            "push": PushState(), ":": PushState(),
            "pop": PopState(), "x": PopState(),
            "join": JoinState(), ",": JoinState(),
            "repeat": RepeatLastActionState(),
        }
        self.message = message

    def update(self, msg: str, stack: StringStack) -> State:
        if msg == "exit":
            return
        if msg in ["help", "?"]:
            return MenuState(self.get_help_message())
        if msg in self.transitions:
            return self.transitions[msg]
        return MenuState("unknown command")

    def render(self) -> list[str]:
        return self.message.split('\n')

    # FIXME: define as a constant ?
    def get_help_message(self) -> str:
        return f"""- help: display this message",
- exit: exit",
- push: {PushState.__doc__}
- pop: {PopState.__doc__}
    """

# TODO: class that repeats the last action
class RepeatLastActionState(State):
    pass


# TODO: class that shows the contents of the History
# class ShowHistoryState(State):
#     def update(self, msg: str, stack: String, history: list[str, str]) -> State:

class PushState(State):
    """Push string to the stack."""

    def update(self, msg: str, stack: StringStack) -> State:
        stack.push(msg)

        return MenuState()

    def render(self) -> list[str]:
        return [
            "type a word, it will be added to the stack",
        ]


class PopState(State):
    """Pop string from the stack."""

    def instant(self, stack: StringStack) -> State:
        # instantanious transition
        stack.pop()
        return MenuState()

    def render(self) -> list[str]:
        return [
            "if you see this it is a bug",
        ]


class JoinState(State):
    """Join the two top values of the stack.
    This "natural" join puts the top of the stack after the second value of the
    satck, since that is visually just like removing the newline separation
    between both.
    """

    def instant(self, stack: StringStack) -> State:
        top, snd = stack.pop(), stack.pop()
        stack.push(snd + top)
        return MenuState()


class ReverseJoinState(State):
    """Join the two top values of the stack, but reversed.
    Contratly the the "natural" join (`JoinState`), this join pust the top of the stack before the second value of the stack.
    That results in a "reversed" version of the stack.
    """

    def instant(self, stack: StringStack) -> State:
        top, snd = stack.pop(), stack.pop()
        stack.push(top + snd)
        return MenuState()
