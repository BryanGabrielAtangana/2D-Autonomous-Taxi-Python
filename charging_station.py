"""charging_station.py"""
import pygame 

CHARGING_STATION_COLOR = (0, 102, 255)
WHITE = (255, 255, 255)
GRID_SIZE = 20

pygame.init()
font = pygame.font.Font('arial.ttf', 25)

class ChargingStation:
    def __init__(self, station_id, position):
        self.station_id = station_id
        self.position = position

    def draw(self, surface):
        # Draw a larger rectangle for charging station
        pygame.draw.rect(
            surface,
            CHARGING_STATION_COLOR,
            (self.position.x * GRID_SIZE, self.position.y * GRID_SIZE, GRID_SIZE * 2, GRID_SIZE * 2)
        )
        # Electric insignia
        text = font.render("C", True, WHITE)
        text_rect = text.get_rect(center=(
            self.position.x * GRID_SIZE + GRID_SIZE,
            self.position.y * GRID_SIZE + GRID_SIZE
        ))
        surface.blit(text, text_rect)