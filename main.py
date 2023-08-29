import pygame
import random
import math

from particle_system import *
from spark import *

SCREEN_SIZE = pygame.Vector2(960, 540)

pygame.init()

sparks = []
particles = []

class Ball:

    def __init__(self, position : pygame.Vector2):

        self.rect = pygame.FRect(position, [15, 15])

        self.surface = pygame.Surface([15, 15], pygame.SRCALPHA)
        pygame.draw.circle(self.surface, [233, 245, 249], [8, 8], 7)

        random_angle = random.uniform(3*math.pi/4, 5*math.pi/4) - math.pi * (1 - random.randint(0, 1))

        self.direction = pygame.Vector2(math.cos(random_angle), math.sin(random_angle))

        deviation_angle = random_angle + random.uniform(-3*math.pi/6, 3*math.pi/6)
        self.deviation = pygame.Vector2(math.cos(deviation_angle), math.sin(deviation_angle))

        self.movement = pygame.Vector2(0,0)

        self.deviation_timer = 0
        self.deviation_time = 3

        self.speed = 400
    
    def random_deviation(self):

        self.deviation_timer = 0

        angle = math.atan2(self.direction.y, self.direction.x)

        deviation_angle = angle + random.uniform(-3*math.pi/6, 3*math.pi/6)
        self.deviation = pygame.Vector2(math.cos(deviation_angle), math.sin(deviation_angle))

# def generate_shadows(objects : list[pygame.FRect, pygame.Surface]) -> list[pygame.Surface, tuple]:

#     shadows = []

#     for rect, surf in objects:
        
#         pos = rect.topleft + pygame.Vector2(5, 5)
#         mask = pygame.mask.from_surface(surf, 0)
#         shadows.append([mask.to_surface(setcolor=(0, 0, 0, 255), unsetcolor=(0, 0, 0, 0)), pos])

#     return shadows

def collisions(rect : pygame.FRect, colliders : list[pygame.FRect]) -> list[pygame.FRect]:

    collided = []

    for collider in colliders:
        if rect.colliderect(collider):
            collided.append(collider)
    
    return collided

def collision_resolution(ball : Ball, colliders : list[pygame.FRect]) -> None:

    ball.rect.x += ball.movement.x

    score_result = -1

    if(ball.rect.left < 0):
        ball.rect.left = 0
        ball.direction.reflect_ip(pygame.Vector2(1, 0))
        score_result = 1
    elif (ball.rect.right > SCREEN_SIZE.x):
        ball.rect.right = SCREEN_SIZE.x
        ball.direction.reflect_ip(pygame.Vector2(-1, 0))
        score_result = 0
    
    for collided in collisions(ball.rect, colliders):
        ball.speed += 20
        if ball.movement.x < 0:
            ball.rect.left = collided.right
            ball.direction.reflect_ip(pygame.Vector2(1, 0))
        elif ball.movement.x > 0:
            ball.rect.right = collided.left
            ball.direction.reflect_ip(pygame.Vector2(-1, 0))
        ball.random_deviation()
    
    ball.rect.y += ball.movement.y

    if(ball.rect.top < 0):
        ball.rect.top = 0
        ball.direction.reflect_ip(pygame.Vector2(0, 1))
        generate_sparks(sparks, pygame.Vector2(ball.rect.midtop), pygame.Vector2(0, 1))
        ball.random_deviation()
    elif (ball.rect.bottom > SCREEN_SIZE.y):
        ball.rect.bottom = SCREEN_SIZE.y
        ball.direction.reflect_ip(pygame.Vector2(0, -1))
        generate_sparks(sparks, pygame.Vector2(ball.rect.midbottom), pygame.Vector2(0, -1))
        ball.random_deviation()
    
    for collided in collisions(ball.rect, colliders):
        if ball.movement.y < 0:
            ball.rect.top = collided.bottom
            ball.direction.reflect_ip(pygame.Vector2(0, 1))
        elif ball.movement.y > 0:
            ball.rect.bottom = collided.top
            ball.direction.reflect_ip(pygame.Vector2(0, -1))
        ball.random_deviation()
    
    return score_result

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Pong what")

player_1 , player_2 = (pygame.FRect([0, 0], [20, 100]) for _ in range(2))

player_1.topleft = pygame.Vector2(20, 20)
player_2.topleft = pygame.Vector2(SCREEN_SIZE.x - player_1.width - 20 , 20)

player_surface = pygame.Surface([20, 100])
player_surface.fill("white")

ball = Ball(pygame.Vector2())
ball.rect.center = SCREEN_SIZE / 2

controls = {"up_1":False, "up_2":False, "down_1":False, "down_2":False}

clock = pygame.Clock()

small_font = pygame.Font("alagard.ttf", 25)
big_font = pygame.Font("alagard.ttf", 40)

score = [0, 0]

particle_timer = 0
particle_spawnrate = 0.05

running = True

while running:

    dt = clock.tick(0) / 1000

    particle_timer += dt

    # event handling

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                controls["up_1"] = True
            elif event.key == pygame.K_DOWN:
                controls["down_1"] = True
            elif event.key == pygame.K_a:
                controls["up_2"] = True
            elif event.key == pygame.K_z:
                controls["down_2"] = True
        
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                controls["up_1"] = False
            elif event.key == pygame.K_DOWN:
                controls["down_1"] = False
            elif event.key == pygame.K_a:
                controls["up_2"] = False
            elif event.key == pygame.K_z:
                controls["down_2"] = False

    # updating

    if controls["up_1"]:
        player_1.y -= 400 * dt
    elif controls["down_1"]:
        player_1.y += 400 * dt

    player_1.y = pygame.math.clamp(player_1.y, 20, SCREEN_SIZE.y - 20 - player_1.height)

    if controls["up_2"]:
        player_2.y -= 400 * dt
    elif controls["down_2"]:
        player_2.y += 400 * dt
    
    player_2.y = pygame.math.clamp(player_2.y, 20, SCREEN_SIZE.y - 20 - player_2.height)

    ball.deviation_timer = max(ball.deviation_timer + dt, ball.deviation_time)
    ball.movement = (ball.direction + (ball.deviation_timer / ball.deviation_time) * ball.deviation).normalize() * ball.speed * dt

    result = collision_resolution(ball, [player_1, player_2])

    if(result != -1):
        if(result):
            score[1] += 1
        else:
            score[0] += 1
        
        random_angle = random.uniform(-math.pi/4, math.pi/4) + math.pi * result
        ball.direction = pygame.Vector2(math.cos(random_angle), math.sin(random_angle))
        ball.rect.center = SCREEN_SIZE / 2
        ball.speed = 400
        ball.deviation_timer = 0

        particles.clear()
    
    if(particle_timer > particle_spawnrate):
        generate_ball_particles(particles, ball.rect)
        particle_timer = 0

    # drawing

    screen.fill(0x130c2b)
    
    # display_surface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)

    # screen.blits(shadows)

    for spark in sparks:

        spark.update(dt)
        spark.speed_scale -= 8 * dt
        spark.speed -= 60.5 * dt

        if spark.speed_scale < 0:
            sparks.remove(spark)
        else:
            spark.draw(screen)
    
    for particle in particles:
        particle.update(dt)

        if(particle.life_time <= 0):
            particles.remove(particle)
        else:
            particle.draw(screen)

    screen.blit(player_surface, player_1.topleft)
    screen.blit(player_surface, player_2.topleft)
    
    pygame.draw.line(screen, [168, 213, 229], (480, 0), (480, 540))

    screen.blit(ball.surface, ball.rect.topleft)

    fps_text = small_font.render(f"FPS : {round(clock.get_fps(), 2)}", True, "white")
    screen.blit(fps_text, [SCREEN_SIZE.x / 2 - 60, SCREEN_SIZE.y - fps_text.get_height() - 20])

    score_text_player_1 = big_font.render(f"{score[0]}", True, "white")
    screen.blit(score_text_player_1, [SCREEN_SIZE.x / 2 - score_text_player_1.get_width() - 40, 20])

    score_text_player_2 = big_font.render(f"{score[1]}", True, "white")
    screen.blit(score_text_player_2, [SCREEN_SIZE.x / 2 + 40, 20])

    # mask = pygame.mask.from_surface(screen, 0)
    # screen.blit(mask.to_surface(setcolor=(0, 0, 0, 255), unsetcolor=(0, 0, 0, 0)), [5, 5])
    # screen.blit(screen, [0,0])
    pygame.display.flip()

pygame.quit()