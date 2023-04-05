import random
from dino_runner.components.obstacles.obstacle import Obstacle
from dino_runner.utils.constants import SMALL_CACTUS

class Cactus(Obstacle):
    POS_Y_CACTUS = 325

    def __init__(self):
        self.image = random.choice(SMALL_CACTUS)
        super().__init__(self.image)
        self.rect.y = self.POS_Y_CACTUS
