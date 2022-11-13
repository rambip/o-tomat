from infra import State, Memory
# NOTE: do not use
# from primitives import MenuState
# otherwise this is a circular import
import primitives

class DirState(State):
    def update(self, msg, stack_top, mem):
        MenuState = primitives.MenuState

        if msg == ".":
            pwd = mem.os.getenv("PWD")
            sep = mem.os.path.sep
            if pwd != sep:
                up = sep.join(pwd.split(sep)[:-1])
                assert(up!='')
                mem.setenv("PWD", up)
                return DirState()
            return DirState()

        try:
            i = int(msg)
            pwd = mem.getenv("PWD")
            files = mem.os.listdir(pwd)
            if i < len(files):
                path = mem.os.path.join(pwd, files[i]) 
                if mem.os.path.isdir(path):
                    mem.setenv("PWD", path)
                    return DirState()
                mem.stack.push(files[i])
                return DirState()
            self.mem.set_carry("invalid number")
            return MenuState()

        except ValueError:
            return MenuState()


    def render(self, mem):
        files = mem.os.listdir(mem.getenv("PWD"))
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
