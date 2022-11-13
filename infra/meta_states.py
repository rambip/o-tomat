from .state import State
from .memory import Memory

class RepeatLastActionState(State):
    def instant(self, stack_top: str, mem: Memory) -> State:
        return self.last_action_state(mem)

    def last_action_state(self, mem: Memory) -> State:
        history = mem.history
        current_state = history[-2].state
        for i in reversed(range(len(history) - 2)):
            if history[i].state == current_state:
                return history[i+1].state
        mem.set_carry("there is no last command to repeat")
        return MenuState()

