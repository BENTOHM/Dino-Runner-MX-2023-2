import pygame
import sys
from random import randint
from dino_runner.utils.constants import (
    BG, 
    ICON, 
    SCREEN_HEIGHT, 
    SCREEN_WIDTH, 
    TITLE, 
    FPS,
    )
from dino_runner.components.dinosaur import Dinosaur 
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.player_hearts.heart_manager import HeartManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager
from dino_runner.components.list_score.best_score import save_best_score
from dino_runner.utils.constants import CLOUD

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur() #dinosaurio
        self.obstacle_manager = ObstacleManager()
        self.heart_manager = HeartManager()
        self.power_up_manager = PowerUpManager()
        self.points = 0
        pygame.mixer.music.load("dino_runner/assets/Main_resources/Game_song.mp3")
        self.font = pygame.font.Font('dino_runner/assets/Main_resources/Main_font.ttf', 25)
        self.font_gameover = pygame.font.Font('dino_runner/assets/Main_resources/Main_font.ttf', 60)
        self.is_day = True
        self.mode_change_points = 400
        self.clouds = []

    def increase_score(self):
        self.points += 1
        if self.points % 100 == 0:
            self.game_speed += 1
            self.player.check_invincibility()

    def run(self):
        pygame.mixer.music.play(-1)
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            if self.check_game_over():
                self.game_over()
                break
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def change_mode(self):
        if self.points >= self.mode_change_points:
            self.is_day = not self.is_day
            if self.is_day:
                self.screen.fill((255, 255, 255))
                self.font = pygame.font.Font('dino_runner/assets/Main_resources/Main_font.ttf', 25)
            else:
                self.screen.fill((0, 0, 0))
                self.font = pygame.font.Font('dino_runner/assets/Main_resources/Main_font.ttf', 25)
            self.mode_change_points += 400
            self.draw_score() 

    def check_game_over(self):
        if self.heart_manager.heart_count == 0:
            return True
        return False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self.game_speed, self)
        self.power_up_manager.update(self.points, self.game_speed, self.player)
        self.change_mode()
        self.increase_score()
        save_best_score(self.points)
        self.update_clouds()

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_score()
        self.draw_best_score()
        self.draw_text_game()
        self.power_up_manager.draw(self.screen)
        self.heart_manager.draw(self.screen)
        self.draw_clouds()
        pygame.display.update() #update objects inside
        pygame.display.flip() #display/show

    def draw_background(self):
        self.update_clouds()
        if self.is_day:
            bg_color = (255, 255, 255)
            bg_image = BG
        else:
            bg_color = (0, 0, 0)
            bg_image = pygame.transform.flip(BG, False, True)
        self.screen.fill(bg_color)
        image_width = bg_image.get_width()
        self.screen.blit(bg_image, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(bg_image, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(bg_image, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_score(self):
        if self.is_day:
            color = (0, 0, 0)
        else:
            color = (255, 255, 255)
        text = f"SCORE: {self.points}"
        surface = self.font.render(text, True, color)
        rect = surface.get_rect()
        rect.x = 850
        rect.y = 10
        self.screen.blit(surface, rect)

    def draw_best_score(self):
        if self.is_day:
            color = (0, 0, 0)
        else:
            color = (255, 255, 255)
        with open('dino_runner/components/list_score/score_text.txt', 'r') as f:
            best_score = f.read()
        text = f'BEST SCORE: {best_score}'
        surface = self.font.render(text, True, color)
        rect = surface.get_rect()
        rect.x = 735
        rect.y = 35
        self.screen.blit(surface, rect)

    def draw_text_game(self):
        if self.is_day:
            color = (0, 0, 0)
        else:
            color = (255, 255, 255)
        text = f'LIVES'
        surface = self.font.render(text, True, color)
        rect = surface.get_rect()
        rect.x = 12
        rect.y = 45
        self.screen.blit(surface, rect)

    def draw_clouds(self):
        for cloud in self.clouds:
            self.screen.blit(CLOUD, (cloud[0], cloud[1]))

    def update_clouds(self):
        cloud_speed = -10
        if len(self.clouds) < 12 and randint(0, 100) < 2:
            new_cloud = [SCREEN_WIDTH, randint(0, SCREEN_HEIGHT//2)]
            self.clouds.append(new_cloud)
        for cloud in self.clouds:
            cloud[0] += cloud_speed 
            if cloud[0] < -CLOUD.get_width():
                self.clouds.remove(cloud)

    def game_over(self):
        self.playing = False
        pygame.mixer.music.stop()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        pygame.mixer.music.stop()
                        game = Game()
                        game.run()
                        print("Code is starting once again:")
                        return
                    elif event.key == pygame.K_m:
                        pygame.quit()
                        sys.exit()

            self.screen.fill((255, 255, 255))
            text = self.font_gameover.render("GAME OVER", True, (0, 0, 0))
            rect = text.get_rect()
            rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            self.screen.blit(text, rect)

            retry_text = self.font.render("Presiona r para reiniciar", True, (0, 0, 0))
            retry_rect = retry_text.get_rect()
            retry_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            self.screen.blit(retry_text, retry_rect)

            exit_text = self.font.render("Presiona m para salir", True, (0, 0, 0))
            exit_rect = exit_text.get_rect()
            exit_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
            self.screen.blit(exit_text, exit_rect)

            pygame.display.update()
            self.clock.tick(60)