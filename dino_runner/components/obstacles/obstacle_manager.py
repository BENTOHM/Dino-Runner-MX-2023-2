import pygame
import random
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS,BIRD, DAMAGE_SOUND
class ObstacleManager:
    def __init__(self):
        self.obstacles = []
        self.damage_sound = DAMAGE_SOUND

    def update(self, game_speed, game):
        if len(self.obstacles) == 0:
            type = random.randint(0,2)
            match type:
                case 0:
                    self.obstacles.append(Bird(BIRD))
                case 1:
                    self.obstacles.append(Cactus(SMALL_CACTUS))
                case 2:
                    self.obstacles.append(Cactus(LARGE_CACTUS))
        for obstacle in self.obstacles:
            obstacle.update(game_speed, self.obstacles)

            if game.player.dino_rect.colliderect(obstacle.rect):
                if not game.player.shield:
                    game.heart_manager.reduce_heart()
                    self.damage_sound.set_volume(self.damage_sound.get_volume() * 5.0)
                    self.damage_sound.play()
                if game.heart_manager.heart_count < 1:
                    self.damage_sound.play()
                    pygame.time.delay(300)
                    game.playing = False
                    break
                if obstacle in self.obstacles:
                    self.obstacles.remove(obstacle)
                else:
                    self.obstacles.remove(obstacle)

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)