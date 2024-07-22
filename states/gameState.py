from enum import Enum

class GameState(Enum):
    GAMEPLAY = 0
    PAUSE = 1 
    GAMEOVER = 2
    STARTMENU = 3
    HELPMENU = 4