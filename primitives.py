from string_stack import StringStack
from abc import ABC, abstractmethod
from memory import Memory


# so type hinting works
State = 'State'
History = 'History'


class State(ABC):
    """State is an abstract class.
    It is not meant to be actually instanciated, but to be inherited from.
    """

    def __init__(self):
        if hasattr(self, "pre_init"):
            self.pre_init()
        self.check_instant_update_compat()

    def pre_init(self) -> None:
        """Method called before the __init__ method is executed."""

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


# Default state. Also the initial one
MenuState = 'MenuState'  # for type hinting
class MenuState(State):

    def with_message(self, message: str) -> MenuState:
        """Change the message the menu will show."""
        self.message_box = str(message).split('\n')
        return self

    def with_message_box(self, message_box: str) -> MenuState:
        self.message_box = list(message_box)
        return self

    @property
    def transitions(self):
        return {
            "push": PushState(), ":": PushState(),
            "pop": PopState(), "x": PopState(),
            "join": JoinState(), ",": JoinState(),
            "history": ShowHistoryState(),
        }

    def update(self, msg: str, stack_top: str, mem: Memory) -> State:
        self.mem = mem
        if msg == "exit":
            return
        if msg in ("help", "?"):
            return MenuState().with_message(self.HELP_MESSAGE)
        if msg in self.transitions:
            return self.transitions[msg]
        return MenuState().with_message("unknown command")

    def render(self) -> list[str]:
        if hasattr(self, 'message_box'):
            return self.message_box
        # default mesage
        return ["Waiting for command"]

    @property
    def HELP_MESSAGE(self) -> str:
        return f"""- help: display this message",
- exit: exit",
- push: {PushState.__doc__}
- pop: {PopState.__doc__}
    """

# TODO: class that repeats the last action
class RepeatLastActionState(State):
    def instant(self, stack_top: str, mem: Memory) -> State:
        return self.last_action_state(mem)

    def last_action_state(self, mem: Memory) -> State:
        history = mem.meta.history
        current_state = history[-1].state
        for i in reversed(range(len(history) - 1)):
            if history[i].state == current_state:
                return history[i+1].state
        return MenuState().with_message("there is no last command to repeat")



# TODO: class that shows the contents of the History
class ShowHistoryState(State):
    def instant(self, stack_top: str, mem: Memory) -> State:
        return MenuState().with_message_box(self.render_history(mem.meta.history))

    def render_history(self, history: History) -> [str]:
        res = list()
        for entry in history:
            res.append(entry.command + " -> " + repr(entry.state))
        return res




class PushState(State):
    """Push string to the stack."""

    def update(self, msg: str, stack_top: str, mem: Memory) -> State:
        mem.stack.push(msg)

        return MenuState()

    def render(self) -> list[str]:
        return [
            "type a word, it will be added to the stack",
        ]


class PopState(State):
    """Pop string from the stack."""

    def instant(self, stack_top: str, mem: Memory) -> State:
        # instantanious transition
        mem.stack.pop()
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

    def instant(self, stack_top: str, mem: Memory) -> State:
        mem.stack.push(stack_top + mem.stack.pop())
        return MenuState()


class ReverseJoinState(State):
    """Join the two top values of the stack, but reversed.
    Contratly the the "natural" join (`JoinState`), this join pust the top of the stack before the second value of the stack.
    That results in a "reversed" version of the stack.
    """

    def instant(self, stack_top: str, mem: Memory) -> State:
        mem.stack.push(mem.stack.pop() + stack_top)
        return MenuState()




