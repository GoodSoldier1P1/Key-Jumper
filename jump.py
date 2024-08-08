import pygame
import random
import os
import sys

pygame.init()
infoObject = pygame.display.Info()
WIDTH = infoObject.current_w
HEIGHT = infoObject.current_h
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)  # Setting game display size to fullscreen


character_spacing_x = 40 # Adjust horizontal spacing
character_spacing_y = 10 # Adjust vertical spacing

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

background = pygame.image.load(resource_path('./images/castle.jpg'))
background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Scaling image

font = pygame.font.Font(resource_path('./fonts/comic.ttf'), 40)

# Variables
word_speed = 0.2
score = 0
game_over = False
character = None

# Load character images
character_images = [resource_path(os.path.join("images", f)) for f in os.listdir(resource_path("images")) if f.endswith(('.png', '.jpg', '.jpeg'))]

def load_random_character():
    character_path = random.choice(character_images)
    character = pygame.image.load(character_path)
    character = pygame.transform.scale(character, (int(WIDTH * 0.05), int(HEIGHT * 0.05)))
    return character

def new_word():
    global displayword, yourword, x_cor, y_cor, text, word_speed, character
    x_cor = random.randint(300, WIDTH - 100)
    y_cor = 200
    word_speed += 0.03
    yourword = ''
    words = open(resource_path("words.txt")).read().split(', ')
    displayword = random.choice(words)
    character = load_random_character()  # Load a new random character image when a new word is generated
    
    if x_cor + 100 > WIDTH:
        x_cor = WIDTH - 100
    if y_cor + 50 > HEIGHT:
        y_cor = HEIGHT - 50


font_name = pygame.font.match_font(resource_path('./fonts/comic.ttf'))
font_color = (255, 255, 0)  # Yellow color for text

def draw_text(display, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, font_color)  # Use font_color here
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    gameDisplay.blit(text_surface, text_rect)

def draw_button(display, text, color, x, y, width, height):
    pygame.draw.rect(display, color, (x, y, width, height))
    draw_text(display, text, 40, x + width // 2, y + height // 4)

def game_front_screen():
    gameDisplay.blit(background, (0, 0))
    if game_over:
        draw_text(gameDisplay, "GAME OVER!", 90, WIDTH / 2, HEIGHT / 4)
        draw_text(gameDisplay, "Score: " + str(score), 70, WIDTH / 2, HEIGHT / 2)
        draw_button(gameDisplay, "Restart Game", green, WIDTH / 4, HEIGHT * 3 / 4, 200, 50)
        draw_button(gameDisplay, "Quit Game", red, WIDTH * 3 / 4 - 200, HEIGHT * 3 / 4, 200, 50)
    else:
        draw_text(gameDisplay, "Press any key to begin!", 54, WIDTH / 2, 500)

    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP and not game_over:
                waiting = False
            if event.type == pygame.MOUSEBUTTONDOWN and game_over:
                mouse_x, mouse_y = event.pos
                if WIDTH / 4 <= mouse_x <= WIDTH / 4 + 200 and HEIGHT * 3 / 4 <= mouse_y <= HEIGHT * 3 / 4 + 50:
                    waiting = False  # Restart game
                elif WIDTH * 3 / 4 - 200 <= mouse_x <= WIDTH * 3 / 4 and HEIGHT * 3 / 4 <= mouse_y <= HEIGHT * 3 / 4 + 50:
                    pygame.quit()
                    sys.exit()

# Main Loop
game_start = True
while True:
    if game_start or game_over:
        game_front_screen()
        new_word()
        score = 0
        word_speed = 0.5
        game_over = False
        game_start = False

    gameDisplay.blit(background, (0, 0))
    wood = pygame.image.load(resource_path('./images/wood-.png'))
    wood = pygame.transform.scale(wood, (90, 50))
    gameDisplay.blit(wood, (x_cor-50, y_cor+15))
    gameDisplay.blit(character, (x_cor-100, y_cor))  # Use the character image here
    draw_text(gameDisplay, str(displayword), 40, x_cor + character_spacing_x, y_cor + character_spacing_y)
    draw_text(gameDisplay, 'Score: ' + str(score), 40, WIDTH / 2, 5)

    y_cor += word_speed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            yourword += pygame.key.name(event.key)

            if displayword.startswith(yourword):
                if displayword == yourword:
                    score += len(displayword)
                    new_word()  # Update character image with new word
                    word_speed += 0.05
            else:
                game_over = True
                game_front_screen()
                break

    if y_cor < HEIGHT - 5 and not game_over:
        pygame.display.update()
    else:
        game_over = True
        game_front_screen()