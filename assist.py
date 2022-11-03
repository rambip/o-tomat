import curses
import random
from string_stack import StringStack

MAX_STACK_HEIGHT = 5
MAX_INFO_WIDTH = 40

INTRO_MESSAGE = \
"""Hi, I'm your assistant !

I will read every word you type,
And respond as well as I can.

Type help for help
"""

class State:
    def __repr__(self):
        return type(self).__name__


# Default state. Also the initial one
class MenuState(State):
    def __init__(self, message: str = "Waiting for command"):
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

    def update(self, msg: str, pile):
        """
        Args:
            msg
        """
        if msg in self.transitions:
            return self.transitions[msg]()
        return MenuState("unknown command")

    def render(self) -> [str]:
        return self.message.split('\n')


class HelpState(State):
    def update(self, msg, pile):
        if msg == "help":
            return HelpState()
        return MenuState()

    def render(self) -> [str]:
        return [
        "- help: display this message",
        "- exit: exit",
        "- push: {PushState.__doc__}",
        "- pop: {PopState.__doc__}",
        "type any key to go home,",
        "then enter another command",
        ]


class PushState(State):
    """Push string to the stack."""

    def update(self, msg, pile):
        if msg == "":
            return MenuState()
        pile.push(msg)
        return self

    def render(self) -> [str]:
        return [
        "every word will be added to the stack",
        "type empty word to exit"
        ]


class PopState(State):
    """Pop string from the stack."""

    def update(self, msg, pile):
        if msg == "":
            pile.pop()
            return self

        return MenuState()

    def render(self) -> [str]:
        return [
        "every <Space> will pop",
        "the top of the stack",
        "",
        "type any word to exit",
        ]


def get_input(stdscr, until_quote = False) -> str :
    """Get input from the user
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
                return get_input(stdscr, until_quote = True)

        if char == '\n' or char == ' ' and not until_quote:
            # end of input
            return res

        elif ord(char) in [curses.KEY_BACKSPACE, 127]:
            if res != "":
                y, x = stdscr.getyx()
                stdscr.move(y, x-1)
                stdscr.delch()
                res = res[0:-1]

        else:
            # print the letter for the user
            res += char
            stdscr.addch(char)


def main(stdscr):
    state = MenuState(INTRO_MESSAGE)
    stack = StringStack()

    while True:
        stdscr.clear()

        state_box = state.render()
        state_name_box = [f"[{repr(state)}]"]
        stack_box = stack.render(MAX_STACK_HEIGHT)

        # display debug information
        for i, l in enumerate(state_name_box):
            stdscr.move(i, 0)
            stdscr.addstr(l)

        # display state for user
        for i, l in enumerate(state_box):
            stdscr.move(i+2, 0)
            stdscr.addstr(l)

        # display the stack
        for i, l in enumerate(stack_box):
            stdscr.move(i, MAX_INFO_WIDTH)
            stdscr.addstr(l)

        # display prompt
        y = max(len(state_name_box) + len(state_box), MAX_STACK_HEIGHT)+2
        stdscr.move(y, 2)
        stdscr.addstr(">  ")
        stdscr.refresh()

        # Transition
        # Based on a pushdown automaton
        input_msg = get_input(stdscr)
        state = state.update(input_msg, stack)
        # Exit if no transition
        if state is None:
            exit()


if __name__ == "__main__":
    curses.wrapper(main)
