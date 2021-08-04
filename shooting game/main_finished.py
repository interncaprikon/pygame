# Import the pygame module
import pygame

# Import random for random numbers
import random
import math

pygame.init()
# Define constants for the screen width and height
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

background_image = pygame.image.load('assets/BG_Grass.png')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
aim = pygame.image.load('assets/aim.png')
width = SCREEN_WIDTH / 10
height = width * aim.get_height() / aim.get_width()
aim = pygame.transform.scale(aim, (int(width), int(height)))
target = pygame.image.load('assets/target.png')
target = pygame.transform.scale(target, (int(width), int(height)))
reset_button = pygame.image.load("assets/BtnReset.png")
reset_button_rect = reset_button.get_rect()
reset_button_rect.center = (int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2) + 150)
start_button = pygame.image.load("assets/BtnStart.png")
start_button_rect = start_button.get_rect()
start_button_rect.center = (int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2))
aim_rect = aim.get_rect()
aim_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
target_rect = target.get_rect()
target_rect.center = (random.randint(width / 2, SCREEN_WIDTH - width / 2),
                      random.randint(height / 2, SCREEN_HEIGHT - height / 2))


def startGame():
    global score
    global time_left
    global state
    state ='InGame'
    score = 0
    time_left = 20
    pygame.mouse.set_visible(False)
    pygame.time.set_timer(pygame.USEREVENT + 1, 1000, True)
def update():
    screen.blit(background_image, (0, 0))
    if state == 'InGame':
        aim_rect.center = pygame.mouse.get_pos()
        screen.blit(target, target_rect)
        screen.blit(aim, aim_rect)
        score_text = pygame.font.SysFont("default", 30).render("Score: " + str(score), True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        time_text = pygame.font.SysFont("default", 30).render("Time: " + str(time_left), True, (0, 0, 0))
        screen.blit(time_text,(SCREEN_WIDTH - time_text.get_width()- 10, 10))
    elif state == 'MainMenu':

        screen.blit(start_button, start_button_rect)
    elif state == 'GameOver':
        end_text = pygame.font.SysFont("default", 90).render("Game Over", True, (0, 0, 0))
        end_text_rect = end_text.get_rect()
        end_text_rect.center = (int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2) - 150)
        screen.blit(end_text, end_text_rect)
        score_text = pygame.font.SysFont("default", 90).render("Score: " + str(score), True, (0, 0, 0))
        score_text_rect = score_text.get_rect()
        score_text_rect.center = (int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2))
        screen.blit(score_text, score_text_rect)


        screen.blit(reset_button, reset_button_rect)
def updateTimer():
    global time_left
    global state
    time_left -= 1
    if time_left <= 0:
        pygame.mouse.set_visible(True)
        state='GameOver'
    else:
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000, True)
def moveTarget():
    target_rect.center = (random.randint(width / 2, SCREEN_WIDTH - width / 2),
                         random.randint(height / 2, SCREEN_HEIGHT - height / 2))
    pygame.time.set_timer(pygame.USEREVENT + 2, 1000, True)
def shoot():
    global score
    pygame.mixer.Sound('assets/shot.aiff').play(maxtime=300)
    distance = math.sqrt((aim_rect.centerx - target_rect.centerx) ** 2 + (aim_rect.centery - target_rect.centery) ** 2)
    if distance <= width / 2:
        score_added = round(10 - 10 * distance / (width / 2))
        score += score_added
        moveTarget()






pygame.display.set_caption("Shooting Game")
pygame.display.set_icon(pygame.image.load('assets/icon.png'))
state='MainMenu'
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        if state == 'InGame':
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                shoot()
            elif event.type == pygame.USEREVENT+1:
                updateTimer()
            elif event.type == pygame.USEREVENT+2:
                moveTarget()

        elif state == 'MainMenu':
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_position = pygame.mouse.get_pos()
                if start_button_rect.collidepoint(mouse_position):
                    startGame()

        elif state == 'GameOver':
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_position = pygame.mouse.get_pos()
                if reset_button_rect.collidepoint(mouse_position):
                    state= 'MainMenu'
    update()
    pygame.display.flip()
