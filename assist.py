from curses import wrapper
from string_stack import StringStack
import random

INTRO_MESSAGE = """
        Hi, I'm your assistant !

        I will read every word you type,
        And respond as well as I can.

        Type help for help
        """


# Default state. Also the initial one
class MenuState:
    def __init__(self, message: str = "      Waiting for command"):
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
        return MenuState("      unknown command")

    def __str__(self) -> str:
        return self.message


class HelpState:
    def update(self, msg, pile):
        if msg == "help":
            return HelpState()
        return MenuState()

    def __str__(self) -> str:
        return f"""
        - help: display this message
        - exit: exit
        - push: {PushState.__doc__}
        - pop: {PopState.__doc__}

        type any key to go home, then enter command
        """


class PushState:
    """Push string to the stack."""

    def update(self, msg, pile):
        if msg == "":
            return MenuState()
        pile.push(msg)
        return self

    def __str__(self) -> str:
        return """
        every word will be added to the stack

        type empty word to exit
        """


class PopState:
    """Pop string from the stack."""

    def update(self, msg, pile):
        if msg == "":
            pile.pop()
            return self

        return MenuState()

    def __str__(self) -> str:
        return """
        every time you hit <Space>, I will remove a word from the stack

        Hit a word to exit
        """

# Get a word from the user
# TODO: use " to escape spaces ?


def get_input(stdscr):
    res = ""
    while True:
        c = chr(stdscr.getch())
        if c in [' ', '\n']:
            # end of word
            return res

        elif ord(c) == 263:
            # backspace key
            if res != "":
                y, x = stdscr.getyx()
                stdscr.move(y, x-1)
                stdscr.delch()
                res = res[0:-1]

        else:
            # print the letter for the user
            res = res + c
            stdscr.addch(c)


def state_name(s):
    # debug information
    return type(s).__name__


def main(stdscr):
    state = MenuState(INTRO_MESSAGE)
    stack = StringStack()

    while True:
        # display current state
        stdscr.clear()
        stdscr.addstr(f"[{state_name(state)}]\n")
        stdscr.addstr(str(state))
        stdscr.addstr("\n\n")

        # display the stack
        stdscr.addstr(str(stack))

        stdscr.addstr("\n\n>  ")
        stdscr.refresh()

        # Transition
        # Based on a pushdown automaton
        input_msg = get_input(stdscr)
        state = state.update(input_msg, stack)
        # Exit if no transition
        if state is None:
            exit()


if __name__ == "__main__":
    wrapper(main)
