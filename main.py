# import sys module
import pygame
import sys
from enum import Enum

pygame.init()
clock = pygame.time.Clock()
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
TILE_SIZE = (WIDTH + HEIGHT) / 14
base_font = pygame.font.Font(None, int(TILE_SIZE + TILE_SIZE / 2))

margin_left = WIDTH / 8

inputs = [[], [], [], [], []]
active_inputs = [[], [], [], [], []]
text = [[], [], [], [], []]
input_color = [[], [], [], [], []]
guess = 0
answer = "Henry"


class Screen(Enum):
    START = "start"
    GAME = "game"
    END = "end"


active_screen = Screen.START
COLOR_ACTIVE = pygame.Color('lightskyblue3')
COLOR_PASSIVE = pygame.Color('chartreuse4')


def init_structures():
    for row in range(5):
        for col in range(5):
            inputs[row].append(
                pygame.Rect(margin_left + (TILE_SIZE * col) + (25 * col), 25 + (TILE_SIZE * row) + (12.5 * row),
                            TILE_SIZE,
                            TILE_SIZE))
            active_inputs[row].append(False)
            text[row].append("")
            input_color[row].append(None)
    active_inputs[guess][0] = True


def render_input_fields():
    for row in range(5):
        for input, active, color in zip(inputs[row], active_inputs[row], input_color[row]):
            if row >= guess:
                pygame.draw.rect(screen, COLOR_ACTIVE if active else COLOR_PASSIVE, input)
            else:
                pygame.draw.rect(screen, color, input)


def render_input_text(input_texts):
    for row in range(5):
        for col in range(5):
            input_texts[row].append(base_font.render(text[row][col], True, (255, 255, 255)))
            screen.blit(input_texts[row][col], (inputs[row][col].x + 15, inputs[row][col].y + 5))


init_structures()
run = True
while run:
    text_surface = [[], [], [], [], []]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, input_field in enumerate(inputs[guess]):
                if input_field.collidepoint(event.pos):
                    active_inputs[guess][i] = True
                else:
                    active_inputs[guess][i] = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                for i, active in enumerate(active_inputs[guess]):
                    if active:
                        text[guess][i] = ""
            elif event.key == pygame.K_RETURN:
                if guess < 4:
                    active_inputs[guess] = [False] * 5

                    if "".join(text[guess]) == answer.upper():
                        print(f"U r correct. you guessed in {guess + 1} tries! :)")
                        run = False

                    for i, letter in enumerate(text[guess]):
                        if letter == answer[i].upper():
                            input_color[guess][i] = pygame.Color('green')
                        elif letter in answer.upper():
                            input_color[guess][i] = pygame.Color('red')
                        else:
                            input_color[guess][i] = pygame.Color('black')
                    guess += 1
                    active_inputs[guess][0] = True
                else:
                    print("Game Over")
                    run = False
            else:
                for i, active in enumerate(active_inputs[guess]):
                    if active:
                        text[guess][i] = event.unicode.upper()
                        if i < 4:
                            active_inputs[guess][i + 1] = True
                            active_inputs[guess][i] = False
                        else:
                            active_inputs[guess][i] = False
                        break

    screen.fill((255, 255, 255))
    render_input_fields()
    render_input_text(text_surface)

    pygame.display.flip()
    clock.tick(60)
