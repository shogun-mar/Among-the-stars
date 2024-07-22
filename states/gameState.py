from enum import Enum

class GameState(Enum):
    GAMEPLAY = 0
    HYPERSPACE = 1
    PAUSE = 2 
    GAMEOVER = 3
    STARTMENU = 4
    HELPMENU = 5