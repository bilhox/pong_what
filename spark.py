import pygame
import math
import random

class Spark:

    def __init__(self):
        
        self.position = pygame.Vector2()
        self.color = pygame.Color(0,0,0)

        self.speed = 1
        self.scale = 1
        self.speed_scale = 2
        self.angle = -math.pi / 2

        self._points = [pygame.Vector2() for _ in range(4)]
    
    def update(self, dt):

        self.position += pygame.Vector2(math.cos(self.angle), math.sin(self.angle)) * self.speed * dt
        
        self._points[0] = self.position - pygame.Vector2(math.cos(self.angle),math.sin(self.angle)) * self.speed_scale * self.scale * 2.5
        self._points[1] = self.position + pygame.Vector2(math.cos(self.angle + math.pi/2),math.sin(self.angle + math.pi/2)) * self.speed_scale * self.scale * 0.3
        self._points[2] = self.position + pygame.Vector2(math.cos(self.angle),math.sin(self.angle)) * self.speed_scale * self.scale
        self._points[3] = self.position + pygame.Vector2(math.cos(self.angle - math.pi/2),math.sin(self.angle - math.pi/2)) * self.speed_scale * self.scale * 0.3

    def draw(self, dest : pygame.Surface):
        
        pygame.draw.polygon(dest, self.color, self._points)

def generate_sparks(sparks : list[Spark], position : pygame.Vector2, normal : pygame.Vector2):

    normal_angle = math.atan2(normal.y, normal.x)

    for _ in range(5):
        spark = Spark()

        spark.position = position.copy()
        spark.speed = random.uniform(250, 300)
        spark.speed_scale = spark.speed / 100
        spark.scale = random.uniform(3.0, 3.75)
        spark.angle = random.uniform(normal_angle - 2*math.pi/6, normal_angle + 2*math.pi/6)
        spark.color = pygame.Color(255, 255, 255)

        sparks.append(spark)


if __name__ == "__main__":

    screen = pygame.display.set_mode([500, 500])

    running = True

    clock = pygame.Clock()

    sparks : list[Spark] = []

    GENERATE_SPARK = pygame.USEREVENT + 1
    pygame.time.set_timer(GENERATE_SPARK, 200)

    while running:

        screen.fill(0x000000)

        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == GENERATE_SPARK:
                for _ in range(5):
                    spark = Spark()

                    spark.position = pygame.Vector2([250, 250])
                    spark.speed = random.uniform(300, 350)
                    spark.speed_scale = spark.speed / 100
                    spark.scale = random.uniform(5.5, 9.5)
                    spark.angle = random.uniform(0, 2 * math.pi)
                    spark.color = pygame.Color(255, 255, 255)

                    sparks.append(spark)
        
        for spark in sparks:

            spark.update(dt)
            spark.speed_scale -= 5 * dt
            spark.speed -= 15.5 * dt

            if spark.speed_scale < 0:
                sparks.remove(spark)
            else:
                spark.draw(screen)
        

        pygame.display.flip()

    pygame.quit()