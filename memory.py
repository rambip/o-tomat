from string_stack import StringStack
from metadata_stack import MetaStack
from typing import NamedTuple

State = 'State'  # for type hinting

class HistoryEntry(NamedTuple):
    command: str
    state: State


class Memory:
    """Main memory"""
    def __init__(self):
        # the main stack
        self.stack = StringStack()

        # argument to pass to the next state
        self.carry : str = ""

        # message that the next state has to show
        self.next_message : str = ""

        # metadata
        self.meta = Meta()


class Meta:
    """Metadata"""
    def __init__(self):
        # list of states
        State = 'State'  # for type hinting
        self.history: list[HistoryEntry] = [HistoryEntry("", None)]




