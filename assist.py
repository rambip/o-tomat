import curses
import random
from string_stack import StringStack

INTRO_MESSAGE = """
        Hi, I'm your assistant !

        I will read every word you type,
        And respond as well as I can.

        Type help for help
        """


class State:
    def update(self, msg: str, pile: StringStack):
        if msg in self.transitions:
            return self.transitions[msg]()
        return self("      unknown command")

    def __repr__(self) -> str:
        """Show the name of the state itself."""
        return f"[{type(self).__name__}]"



# Default state. Also the initial one
class MenuState(State):
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

    def update(self, msg: str, pile: StringStack) -> State:
        if msg in self.transitions:
            return self.transitions[msg]()
        return MenuState("      unknown command")

    def __str__(self) -> str:
        return self.message


class HelpState(State):
    def update(self, msg: str, pile: StringStack) -> State:
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


class PushState(State):
    """Push string to the stack."""

    def update(self, msg: str, pile: StringStack) -> State:
        if msg == "":
            return MenuState()
        pile.push(msg)
        return self

    def __str__(self) -> str:
        return """
        every word will be added to the stack

        type empty word to exit
        """


class PopState(State):
    """Pop string from the stack."""

    def update(self, msg: str, pile: StringStack) -> State:
        if msg == "":
            pile.pop()
            return self

        return MenuState()

    def __str__(self) -> str:
        return """
        every time you hit <Space>, I will remove a word from the stack

        Hit a word to exit
        """


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
            if res != "":
                y, x = stdscr.getyx()
                stdscr.move(y, x-1)
                stdscr.delch()
                res = res[:-1]

        else:
            # print the letter for the user
            res += char
            stdscr.addch(char)


def main(stdscr):
    state = MenuState(INTRO_MESSAGE)
    stack = StringStack()

    while True:
        # display current state
        stdscr.clear()
        stdscr.addstr(repr(state))  # repr is state's name
        stdscr.addstr(str(state))  # str is state's main text
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
    curses.wrapper(main)
