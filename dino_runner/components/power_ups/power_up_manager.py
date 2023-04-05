from dino_runner.components.power_ups.shield import Shield

class PowerUpManager:
    POINTS = 200

    def __init__(self):
        self.power_ups = []

    def update(self, game_speed, points):
        if len(self.power_ups) == 0 and points % self.POINTS == 0:
            self.power_ups.append(Shield())
        for power_up in self.power_ups:
            if power_up.rect.x < -power_up.rect.width:
                self.power_ups.pop()
            power_up.update(game_speed)


    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)