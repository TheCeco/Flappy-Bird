import random
import pygame
import os

WIDTH, HEIGHT = 500, 700
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

FPS = 60

BACKGROUND = pygame.image.load(os.path.join('Assets', 'background.png'))
BACKGROUND = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))

NORMAL_PIPE = pygame.image.load(os.path.join('Assets', 'pipe.png'))
NORMAL_PIPE = pygame.transform.scale(NORMAL_PIPE, (85, 500))
UPSIDE_DOWN_PIPE = pygame.image.load(os.path.join('Assets', 'pipe.png'))
UPSIDE_DOWN_PIPE = pygame.transform.rotate(
    pygame.transform.scale(UPSIDE_DOWN_PIPE, (85, 500)) ,180)
SPACE_BETWEEN_PIPES = 150

GAME_OVER = pygame.image.load(os.path.join('Assets', 'gameover.png'))
GAME_OVER = pygame.transform.scale(GAME_OVER, (200, 100))

GROUND = pygame.image.load(os.path.join('Assets', 'ground.jpg'))
GROUND = pygame.transform.scale(GROUND, (WIDTH, 100))
GROUND1 = pygame.image.load(os.path.join('Assets', 'ground.jpg'))
GROUND1 = pygame.transform.scale(GROUND1, (WIDTH, 100))

BIRD = pygame.image.load(os.path.join('Assets', 'bird.png'))
BIRD_WIDTH, BIRD_HEIGHT = 50, 35
BIRD = pygame.transform.scale(BIRD, (BIRD_WIDTH,BIRD_HEIGHT))

FALL_Y_VEL = 3
SPACE_Y_VEL = 120

def window_handler(bird, ground, ground1, pipes):
    WINDOW.blit(BACKGROUND, (0, 0))
    for normal_pipe, upside_down_pipe in pipes:
        WINDOW.blit(UPSIDE_DOWN_PIPE, (upside_down_pipe.x, upside_down_pipe.y))
        WINDOW.blit(NORMAL_PIPE, (normal_pipe.x, normal_pipe.y))
    WINDOW.blit(GROUND, (ground.x, ground.y))
    WINDOW.blit(GROUND1, (ground1.x, ground1.y))
    WINDOW.blit(BIRD, (bird.x, bird.y))
    pygame.display.update()

def move(bird, ground, ground1, pipes):
    bird.y += FALL_Y_VEL
    ground.x -= FALL_Y_VEL
    ground1.x -= FALL_Y_VEL
    if ground.x <= -WIDTH:
        ground.x = ground1.x + WIDTH
    if ground1.x <= -WIDTH:
        ground1.x = ground.x + WIDTH

    for normal_pipe, upside_down_pipe in pipes:
        upside_down_pipe.x -= FALL_Y_VEL
        normal_pipe.x -= FALL_Y_VEL
        if upside_down_pipe.x < -NORMAL_PIPE.get_width():
            pipes.pop(0)
            temp = random.randint(0, 400)
            normal_pipe = pygame.Rect(1150, temp + SPACE_BETWEEN_PIPES, 85, 500)
            upside_down_pipe = pygame.Rect(1150, temp - UPSIDE_DOWN_PIPE.get_height(), 85, 500)
            pipes.append((normal_pipe, upside_down_pipe))

def collide_ground(bird, ground, ground1):
    if bird.colliderect(ground) or bird.colliderect(ground1):
        WINDOW.blit(GAME_OVER, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
        pygame.display.update()
        pygame.time.delay(3000)
        return False
    return True

def collide_pipes(bird, pipes):
    for normal_pipe, upside_down_pipe in pipes:
        if bird.colliderect(normal_pipe) or bird.colliderect(upside_down_pipe):
            WINDOW.blit(GAME_OVER, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
            pygame.display.update()
            pygame.time.delay(3000)
            return False
    return True

def main():
    pipes = []
    temp = random.randint(0, 400)
    normal_pipe = pygame.Rect(WIDTH, temp + SPACE_BETWEEN_PIPES, 85, 500)
    upside_down_pipe = pygame.Rect(WIDTH, temp - UPSIDE_DOWN_PIPE.get_height(), 85, 500)
    pipes.append((normal_pipe, upside_down_pipe))

    bonus = 0
    for i in range(1, 4):
        bonus += 300
        temp = random.randint(0, 400)
        normal_pipe = pygame.Rect(WIDTH + bonus, temp + SPACE_BETWEEN_PIPES, 85, 500)
        upside_down_pipe = pygame.Rect(WIDTH + bonus, temp - UPSIDE_DOWN_PIPE.get_height(), 85, 500)
        pipes.append((normal_pipe, upside_down_pipe))

    bird = pygame.Rect(WIDTH//2 - BIRD_WIDTH, HEIGHT//2 - BIRD_HEIGHT//2, BIRD_WIDTH, BIRD_HEIGHT)
    ground = pygame.Rect(0 , 600, WIDTH, 100)
    ground1 = pygame.Rect(WIDTH ,600, WIDTH, 100)
    run = True
    clock = pygame.time.Clock()
    i = 0
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.y -= 8
                    i = 1
        if i > 0:
            if i == 11:
                i = 0
            else:
                bird.y -= 8
                i += 1

        #TODO: Collide into the pipes

        move(bird, ground, ground1, pipes)
        if not collide_ground(bird, ground, ground1):
            break
        if not collide_pipes(bird, pipes):
            break
        window_handler(bird, ground, ground1, pipes)
    main()

if __name__ == '__main__':
    main()