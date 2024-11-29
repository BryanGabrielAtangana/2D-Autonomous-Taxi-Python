import pygame

GRID_SIZE = 20

class Passenger:
    def __init__(self, passenger_id, position, destination):
        self.passenger_id = passenger_id
        self.position = position
        self.destination = destination
        self.color = destination.color

    def draw(self, surface):
        pygame.draw.rect(
            surface,
            self.color,
            (self.position.x * GRID_SIZE, self.position.y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        )