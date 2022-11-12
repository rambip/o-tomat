from string_stack import StringStack
from typing import NamedTuple

State = 'State'  # for type hinting

class HistoryItem(NamedTuple):
    command: str
    state: State
    carry: str
    # entire copy of the stack after having done the transition
    stack_after: list[str]


class Memory:
    """Main memory"""
    def __init__(self, first_state, first_carry):
        # the main stack
        self.stack = StringStack()

        # argument to pass to the next state
        self.carry : str = first_carry 

        # history
        self.history = [HistoryItem("", first_state, first_carry, "")]

    def set_carry(self, c):
        self.carry = c

    def get_carry(self) -> str:
        c = self.carry
        # FIXME: bad idea ?
        self.carry = ""
        return c

    def history_add_item(self, command, state):
        self.history.append(
                HistoryItem(command, state, self.carry, self.stack.copy())
        )
