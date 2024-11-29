import pygame

GRID_SIZE = 20

class TaxiStop:
    def __init__(self, stop_id, position, color):
        self.stop_id = stop_id
        self.position = position
        self.color = color
        self.dropped_passengers = []

    def draw(self, surface):
        pygame.draw.rect(
            surface,
            self.color,
            (self.position.x * GRID_SIZE, self.position.y * GRID_SIZE, GRID_SIZE * 2, GRID_SIZE * 2)
        )