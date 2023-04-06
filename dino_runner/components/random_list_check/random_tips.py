import time
import random

tips = [
    "DIOS PERDONA LOS CACTUS NO",
    "LOS ESCUDOS SERAN TUS MEJORES AMIGOS",
    "LES CAES GORDO A LOS PTEROSAURIOS",
    "CADA DIA MAS INGENIERO",
    "MI CORAZON ES DELICADO TUTUTUTU",
    "TODOS VUELAN GEORGIE",
    "ALCANZA LOS 3500 PNTS",
    "NO DIGAS ESO MI AMOR",
]

class RandomTips:
    def __init__(self):
        self.current_tip_index = 0
        self.last_tip_change_time = time.time()

    def get_tip(self):
        now = time.time()
        if now - self.last_tip_change_time >= 50:
            self.current_tip_index = random.randint(0, len(tips) - 1)
            self.last_tip_change_time = now
        return tips[self.current_tip_index]
