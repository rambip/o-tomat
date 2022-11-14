from infra import State, Memory
# NOTE: do not use
# from primitives import MenuState
# otherwise this is a circular import
import primitives

class DirState(State):
    def init(self, path):
        self.path = path

    def update(self, msg, stack_top, mem):
        MenuState = primitives.MenuState

        if msg == ".":
            sep = mem.os.path.sep
            if self.path != sep:
                up = sep.join(self.path.split(sep)[:-1])
                return DirState(up)
            return self

        try:
            i = int(msg)
            files = mem.os.listdir(self.path)
            if i < len(files):
                f = mem.os.path.join(self.path, files[i]) 
                if mem.os.path.isdir(f):
                    return DirState(f)
                mem.stack.push(files[i])

                return self
            return MenuState("invalid number")

        except ValueError:
            return MenuState("not a number")


    def render(self, mem):
        files = mem.os.listdir(self.path)
        # FIXME: when too many files
        lines = [f"{i} --> {f}" for i, f in enumerate(files)]
        helpmsg = [
                "",
                "type the number associated to a file",
                "if this is a directory, it visits it",
                "otherwise it is pushed onto the stack",
                "type . to go up"
                ]
        lines.extend(helpmsg)

        return lines
