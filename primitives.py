from infra import State
from infra.memory import Memory, HistoryItem
from file_states import DirState


# Default state. Also the initial one
MenuState = 'MenuState'  # for type hinting
class MenuState(State):
    @property
    def transitions(self):
        return {
            "push": PushState(), ":": PushState(),
            "pop": PopState(), "x": PopState(),
            "join": PopJoinState(), ",": PopJoinState(),
            "history": ShowHistoryState(),
            "dir": DirState(),
        }

    def init(self, init_msg="unknown comand"):
        self.info = init_msg.split('\n')

    def update(self, msg: str, stack_top: str, mem: Memory) -> State:
        if msg == "exit":
            return
        if msg in ("help", "?"):
            return MenuState(self.HELP_MESSAGE)
        if msg in self.transitions:
            return self.transitions[msg]
        return MenuState()

    def render(self, mem) -> list[str]:
        return self.info

    @property
    def HELP_MESSAGE(self) -> str:
        return f"""- help: display this message",
- exit: exit",
- push: {PushState.__doc__}
- pop: {PopState.__doc__}
    """


class PushState(State):
    """Push string to the stack."""

    def update(self, msg: str, stack_top: str, mem: Memory) -> State:
        mem.stack.push(msg)

        return MenuState()

    def render(self, mem) -> list[str]:
        return [
            "type a word, it will be added to the stack",
        ]


class PopState(State):
    """Pop string from the stack."""

    def instant(self, stack_top: str, mem: Memory) -> State:
        # instantanious transition
        mem.stack.pop()
        return MenuState()

    def render(self, mem) -> list[str]:
        return [
            "if you see this it is a bug",
        ]


class PopJoinState(State):
    """Join the two top values of the stack.
    This "natural" join puts the top of the stack after the second value of the
    satck, since that is visually just like removing the newline separation
    between both.
    """
    def instant(self, stack_top: str, mem: Memory) -> State:
        val = mem.stack.pop()
        return JoinState(val)

class JoinState(State):
    """Join the top of the stack with the carry
    """
    def init(self, concat_right):
        self.concat_right = concat_right

    def instant(self, stack_top: str, mem: Memory) -> State:
        mem.stack.pop()
        mem.stack.push(stack_top + self.concat_right)
        return MenuState()



class ShowHistoryState(State):
    def instant(self, stack_top: str, mem: Memory) -> State:
        info = "\n".join(self.render_history(mem.history))
        return MenuState(info)

    def render_history(self, history: list[HistoryItem]) -> [str]:
        res = list()
        for entry in history:
            res.append(f"{entry.command} -> {entry.state}")
        return res
