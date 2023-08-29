import pygame
import math
import random

class Particle():

    def __init__(self):

        self.position = pygame.Vector2()
        self.texture = pygame.Surface([0,0])
        self.angle = 0
        self.speed = 1
        self.life_time = 1
    
    def update(self, dt):

        self.life_time -= dt
        self.position += pygame.Vector2(math.cos(self.angle), math.sin(self.angle)) * self.speed * dt
    
    def draw(self, dest : pygame.Surface):

        dest.blit(self.texture, self.position)

def generate_ball_particle_surfaces() -> list[pygame.Surface]:

    surfaces = []

    big_circle = pygame.Surface([9, 9], pygame.SRCALPHA)
    pygame.draw.circle(big_circle, "gray", [5, 5], 4)

    small_circle = pygame.Surface([5, 5], pygame.SRCALPHA)
    pygame.draw.circle(small_circle, "orange", [3, 3], 2)

    surfaces.append(big_circle)
    surfaces.append(small_circle)

    return surfaces

ball_particle_surfaces = generate_ball_particle_surfaces()

def generate_ball_particles(particles : list[Particle], ball_rect : pygame.FRect):
    
    for _ in range(2):
        
        particle = Particle()
        
        particle.texture = random.choice(ball_particle_surfaces)
        particle.position = ball_rect.center + pygame.Vector2(random.uniform(-3, 3), random.uniform(-3, 3)) - 0.5 * pygame.Vector2(particle.texture.get_size())
        particle.angle = random.uniform(0, 2 * math.pi)
        particle.speed = 5
        particle.life_time = random.uniform(0.2, 0.4)

        particles.append(particle)