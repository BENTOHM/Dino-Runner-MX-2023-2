import os
import pygame
from dino_runner.components.game import Game
from dino_runner.components.random_list_check.random_tips import RandomTips
pygame.init()

font = pygame.font.Font('dino_runner/assets/Main_resources/Main_font.ttf', 35)
font_text = pygame.font.Font('dino_runner/assets/Main_resources/Main_font.ttf', 25)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)   

os.environ['SDL_VIDEO_CENTERED'] = '1'
screen = pygame.display.set_mode((900, 600))

gif_frames = []
for i in range(36):
    frame_name = f"dino_runner/assets/Main_resources/backround/Main_image_{i:02d}.gif"
    gif_frames.append(pygame.image.load(frame_name))

frame_duration = 50
start_button_color = (150, 150, 150)
exit_button_color = (150, 150, 150)

start_button = pygame.Rect(150, 470, 200, 50)
exit_button = pygame.Rect(550, 470, 200, 50)

pygame.mixer.music.load("dino_runner/assets/Main_resources/Main_song.wav")
pygame.mixer.music.play(-1)

running = True
frame_index = 0 
frame_timer = 0 
last_tick = pygame.time.get_ticks() 

tips = RandomTips()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                if __name__ == "__main__":
                    pygame.mixer.music.stop()
                    game = Game()
                    game.run()
                    print("Code is starting:")
            elif exit_button.collidepoint(event.pos):
                running = False
        elif event.type == pygame.MOUSEMOTION:
            if start_button.collidepoint(event.pos):
                start_button_color = DARK_GRAY
            else:
                start_button_color = GRAY
            if exit_button.collidepoint(event.pos):
                exit_button_color = DARK_GRAY
            else:
                exit_button_color = GRAY

    screen.blit(gif_frames[frame_index], (0, 0))

    frame_timer += pygame.time.get_ticks() - last_tick
    if frame_timer >= frame_duration:
        frame_timer = 0
        frame_index = (frame_index + 1) % len(gif_frames)

    last_tick = pygame.time.get_ticks()

    if frame_index % 3600 == 0:
        tip = tips.get_tip()
        tips.last_tip_change_time = pygame.time.get_ticks()

    pygame.draw.rect(screen, start_button_color, start_button)
    pygame.draw.rect(screen, exit_button_color,  exit_button)
    start_text = font.render("Start", True, BLACK)
    start_text_rect = start_text.get_rect()
    start_text_rect.x = 165
    start_text_rect.y = 475
    screen.blit(start_text, start_text_rect)
    exit_text = font.render("Exit", True, BLACK)
    exit_text_rect = exit_text.get_rect()
    exit_text_rect.x = 595
    exit_text_rect.y = 475
    screen.blit(exit_text, exit_text_rect)
    main_text = font.render("Dinno Runner", True, BLACK)
    main_text_rect = main_text.get_rect()
    main_text_rect.x = 260
    main_text_rect.y = 10
    screen.blit(main_text, main_text_rect)
    tip_text = font_text.render(tips.get_tip(), True, BLACK)
    tip_text_rect = tip_text.get_rect()
    tip_text_rect.centerx = screen.get_width() // 2
    tip_text_rect.y = 550
    screen.blit(tip_text, tip_text_rect)
    
    pygame.display.flip()
 
pygame.quit