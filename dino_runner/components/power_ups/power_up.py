from dino_runner.utils.constants import SCREEN_HEIGHT

class PowerUp:
    POS_Y_POWER_UP = 125

    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_HEIGHT
        self.rect.y = self.POS_Y_POWER_UP

    def update(self, game_speed):
        self.rect.x -= game_speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

