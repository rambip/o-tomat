import curses
import random
from string_stack import StringStack

MAX_STACK_HEIGHT = 6
STACK_MARGIN_RIGHT = 5
MAX_INFO_WIDTH = 40

INTRO_MESSAGE = \
"""Hi, I'm your assistant !

I will read every word you type,
And respond as well as I can.

Type help for help
"""

class State:
    def __init__(self):
        self.check_instant_update_compat()

    def __repr__(self) -> str:
        """Show the name of the state itself."""
        return f"[{type(self).__name__}]"

    def check_instant_update_compat(self):
        """Check if the obect has a `update` or an `instant` method but not both.
        Raises:
            TypeError: If the object has no `update` or `instant` method.
                       If the object has both `update` and `instant` methods.
        """
        if self.has_instant() and self.has_update():
            raise TypeError("State object can have an `update` or an `instant` method, but not both.")
        if (not self.has_instant()) and (not self.has_update()):
            raise TypeError("State object must have an `update` or an `instant` method.")

    def has_instant(self) -> bool:
        return hasattr(self, 'instant')

    def has_update(self) -> bool:
        return hasattr(self, 'update')

    # def update(self, msg: str, stack: StringStack):
        """how to transition from the current state to any other, depending on
        the typed command.
        """

    #def instant(self, stack):
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
            "help": HelpState, "?": HelpState,
            "": MenuState,
            "exit": lambda: None,
            "push": PushState,
            "pop": PopState,
        }
        self.message = message

    def update(self, msg: str, stack: StringStack) -> State:
        if msg in self.transitions:
            return self.transitions[msg]()
        return MenuState("unknown command")

    # def instant(self, stack: StringStack) -> State:
    #     pass

    def render(self) -> list[str]:
        return self.message.split('\n')


class HelpState(State):
    def update(self, msg, stack: StringStack) -> State:
        if msg == "help":
            return HelpState()
        return MenuState()

    def render(self) -> list[str]:
        return [
        "- help: display this message",
        "- exit: exit",
        f"- push: {PushState.__doc__}",
        f"- pop: {PopState.__doc__}",
        "type any key to go home,",
        "then enter another command",
        ]


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


def get_input(stdscr, until_quote=False) -> str:
    """Get input from the user.
    either: - string of characters between quotes marks
            - word between two spaces
    """
    res = ""
    while True:
        char = chr(stdscr.getch())

        if char == '"':
            if until_quote:
                return res
            else:
                stdscr.addch(char)
                return get_input(stdscr, until_quote=True)

        if char == '\n' or char == ' ' and not until_quote:
            # end of input
            return res

        elif ord(char) in [curses.KEY_BACKSPACE, 127]:
            # backspace key (127 is for some strange terminals)
            if res != "":
                y, x = stdscr.getyx()
                stdscr.move(y, x-1)
                stdscr.delch()
                res = res[:-1]

        else:
            # print the letter for the user
            res += char
            stdscr.addch(char)

def width(b) -> int:
    """width of a box of text"""
    return max([len(line) for line in b])


def height(b) -> int:
    """height of a box of text"""
    return len(b)


def display(stdscr, state_name, state_box, stack_box, stack_left = True):
    """display the content on the screen
    Args:
       - stack_left: indicate if we want to display the stack
                                -> on the right of the state information
                                -> below the state information
    """
    # display debug information
    stdscr.move(0, 0)
    stdscr.addstr(state_name)

    # display state for user
    for i, l in enumerate(state_box):
        stdscr.move(i+2, 0)
        stdscr.addstr(l)

    # display the stack
    if stack_left:
        for i, l in enumerate(stack_box[-MAX_STACK_HEIGHT:]):
            stdscr.move(i, MAX_INFO_WIDTH)
            stdscr.addstr(l)
            y_prompt = max(height(state_box), MAX_STACK_HEIGHT)+2
    else:
        for i, l in enumerate(stack_box[-MAX_STACK_HEIGHT:]):
            stdscr.move(height(state_box)+3+i, 0)
            stdscr.addstr(l)
            y_prompt = height(state_box)+ MAX_STACK_HEIGHT+3


    # display prompt
    stdscr.move(y_prompt, 2)
    stdscr.addstr(">  ")
    stdscr.refresh()



def main(stdscr):
    state = MenuState(INTRO_MESSAGE)
    stack = StringStack()

    try:
        while True:
            stdscr.clear()

            state_box = state.render()
            stack_box = stack.render()

            # number of columns between the left of the state information and the right of the screen
            space_for_stack = stdscr.getmaxyx()[1] - MAX_INFO_WIDTH

            display(stdscr,
                    repr(state),
                    state_box,
                    stack_box,
                    space_for_stack > width(stack_box) + STACK_MARGIN_RIGHT
            )


            # Transition
            # Based on a pushdown automaton
            input_msg = get_input(stdscr)
            state = state.update(input_msg, stack)
            # if instantanious transition:
            while hasattr(state, "instant"):
                state = state.instant(stack)

            # Exit if no transition
            if state is None:
                exit()
    except (KeyboardInterrupt, EOFError):
        exit()


if __name__ == "__main__":
    curses.wrapper(main)
