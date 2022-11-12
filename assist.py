import curses
import random
from string_stack import StringStack
from primitives import *
from meta import *
from memory import Memory
import magic_values as magic
import text  # text box functions

MAX_STACK_HEIGHT = 10
STACK_MARGIN_RIGHT = 5
MAX_INFO_WIDTH = 45

INTRO_MESSAGE = \
    """Hi, I'm your assistant !

I will read every word you type,
And respond as well as I can.

Type help for help
Hit space to repeat last command
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


# FIXME: the argument shouldn't be stack_left, but stack_right ?
def display(stdscr,
            state_name: str, state_box: [str],
            stack_box: [str], stack_left=True) -> None:
    """display the content on the screen
    Args:
        stdscr: The curses standard screen object to draw in.
        state_name (str): The displayed name of the current state.
        state_box (list[str]): The text box (list of lines) of the current state.
        stack_box: [str]: The text box (list of lines) representing the stack and its contents.
        stack_left (bool): indicate if we want to display the stack :
                            -> on the right of the state information (True)
                            -> below the state information (False)
                           Please note that if the contents of the stack are
                           tool wide to print, the stack will automatically be
                           placed below.
    """
    state_box = text.wrap(state_box, MAX_INFO_WIDTH)  # wrap long lines

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
            y_prompt = max(text.height(state_box), MAX_STACK_HEIGHT)+2
    else:
        for i, l in enumerate(stack_box[-MAX_STACK_HEIGHT:]):
            stdscr.move(text.height(state_box)+3+i, 0)
            stdscr.addstr(l)
            y_prompt = text.height(state_box) + MAX_STACK_HEIGHT + 3

    # display prompt
    stdscr.move(y_prompt, 2)
    stdscr.addstr(">  ")
    stdscr.refresh()



def main(stdscr):
    state = MenuState()
    mem = Memory(state, INTRO_MESSAGE)
    # TODO: remove the stack
    # stack = StringStack()

    try:
        while True:
            stdscr.clear()

            state_box = state.render(mem)
            stack_box = mem.stack.render()

            # number of columns between the left of the state information and the right of the screen
            space_for_stack = stdscr.getmaxyx()[1] - MAX_INFO_WIDTH

            display(stdscr,
                    str(state),
                    state_box,
                    stack_box,
                    space_for_stack > text.width(
                        stack_box) + STACK_MARGIN_RIGHT
                    )

            # Transition
            # Based on a pushdown automaton
            input_msg = get_input(stdscr)
            if input_msg == "":
                input_msg = "repeat"
                state = RepeatLastActionState()#.instant(mem.stack.head(), mem)
                #mem.history.append(HistoryEntry("repeat",
                 #RepeatLastActionState().last_action_state(mem)))
            else:
                state = state.update(input_msg, mem.stack.head(), mem)

            mem.history_add_item(input_msg, state)

            # Exit if no transition
            # should be before any test on `state`, because else `sate` could
            # be None (and None is not a <State> object)
            if state is None:
                exit()

            # if instantanious transition:
            # also apply all the following instantanious transitions
            while state.has_instant():
                state = state.instant(mem.stack.head(), mem)
                if state is None:
                    exit
                mem.history_add_item("", state)

    except (KeyboardInterrupt, EOFError):
        exit()


if __name__ == "__main__":
    curses.wrapper(main)
