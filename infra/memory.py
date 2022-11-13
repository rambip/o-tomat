from .string_stack import StringStack
from typing import NamedTuple
import os

State = 'State'  # for type hinting

class HistoryItem(NamedTuple):
    command: str
    state: State
    # entire copy of the stack after having done the transition
    stack_after: list[str]


class Memory:
    """Main memory"""
    def __init__(self, first_state):
        # the main stack
        self.stack = StringStack()

        # history
        self.history = [HistoryItem("", first_state, "")]

        self.os = os

        self.env = os.environ

    def setenv(self, name, val):
        # TODO: way to undo
        self.env[name] = val

    def getenv(self, name):
        if name in self.env:
            return self.env[name]
        return ""

    def history_add_item(self, command, state):
        self.history.append(
                HistoryItem(command, state, self.stack.copy())
        )
