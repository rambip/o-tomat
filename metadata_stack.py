from stack import Stack

# TODO: implement what is a metadata item


class MetaData:
    def __init__(self):
        pass


class MetaStack(Stack):
    @property
    def stack_contents_type(self):
        return MetaData

    @property
    def bottom_of_pile_symbol(self):
        return None

    def render(self) -> [str]:
        # TODO: render or __str__
