# obstacle.py
import pygame

GRID_SIZE = 20

pygame.init()
font = pygame.font.Font('arial.ttf', 25)

class Obstacle:
    def __init__(self, obstacle_id, position):
        self.obstacle_id = obstacle_id
        self.position = position

    def draw(self, surface):
        pygame.draw.rect(
            surface,
            (230, 230, 230),
            (self.position.x * GRID_SIZE, self.position.y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        )

