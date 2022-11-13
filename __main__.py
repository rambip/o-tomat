from infra import Automat, Memory
from primitives import MenuState

INTRO_MESSAGE = \
    """Hi, I'm your assistant !

I will read every word you type,
And respond as well as I can.

Type help for help
Hit space to repeat last command
"""

A = Automat(
        init_state = MenuState(),
        init_msg = INTRO_MESSAGE
        )
A.start()
