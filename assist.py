import curses
import random
from string_stack import StringStack
from primitives import *
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
def display(stdscr, state_name, state_box, stack_box, stack_left=True) -> None:
    """display the content on the screen
    Args:
        - stack_left: indicate if we want to display the stack
                                -> on the right of the state information
                                -> below the state information
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


def last_transition_from(history, state) -> (str, State):
    for i in reversed(range(len(history)-1)):
        if history[i][1] == state:
            return history[i+1]
    return ("", MenuState("there is no last command to repeat"))


def main(stdscr):
    state = MenuState(INTRO_MESSAGE)
    stack = StringStack()

    # history of all the (word, state) transitions
    # word is "" if in is an instantanious transition
    history = [("", state)]

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
                    space_for_stack > text.width(
                        stack_box) + STACK_MARGIN_RIGHT
                    )

            # Transition
            # Based on a pushdown automaton
            # TODO: gestion of HistoricalStates
            input_msg = get_input(stdscr)
            if input_msg == "":
                _, state = last_transition_from(history, state)
            else:
                state = state.update(input_msg, stack)

            history.append((input_msg, state))

            # Exit if no transition
            # should be before any test on `state`, because else `sate` could
            # be None (and None is not a <State> object)
            if state is None:
                exit()

            # if instantanious transition:
            # also apply all the following instantanious transitions
            while state.has_instant():
                state = state.instant(stack)
                history.append(("", state))

    except (KeyboardInterrupt, EOFError):
        exit()


if __name__ == "__main__":
    curses.wrapper(main)
