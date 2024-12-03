"""taxi.py"""

import pygame
import heapq
from collections import namedtuple

pygame.init()
font = pygame.font.Font('arial.ttf', 25)

SCREEN_WIDTH, SCREEN_HEIGHT = 1400, 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

Point = namedtuple('Point', 'x, y')

class Taxi:
    def __init__(self, taxi_id, start_point, color, capacity):
        self.taxi_id = taxi_id
        self.position = start_point
        self.color = color
        self.capacity = capacity
        self.passengers = []
        self.path = []
        self.battery_life = 100
        self.is_charging = False
        self.charge_time = 0

    def draw(self, surface):
        
        pygame.draw.rect(
            surface, 
            self.color, 
            (self.position.x * GRID_SIZE, self.position.y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        )

        # Affichage du nombre de passager
        passenger_text = font.render(str(len(self.passengers)), True, (200,200,200))
        passenger_rect = passenger_text.get_rect(center=(
            self.position.x * GRID_SIZE + GRID_SIZE // 2,
            self.position.y * GRID_SIZE - GRID_SIZE // 2
        ))
        surface.blit(passenger_text, passenger_rect)

        # Affichage de la batterie
        battery_color = (0, 255, 0) if self.battery_life > 50 else (255, 165, 0) if self.battery_life > 20 else (255, 0, 0)
        battery_width = int((self.battery_life / 100) * GRID_SIZE)
        pygame.draw.rect(
            surface, 
            battery_color, 
            (self.position.x * GRID_SIZE, self.position.y * GRID_SIZE + GRID_SIZE, battery_width, 5)
        )

    # Algorithme A* pour trouver le chemin
    def a_star_pathfinding(self, target, obstacles):
        def heuristic(a, b):
            return abs(a.x - b.x) + abs(a.y - b.y)

        def get_neighbors(point):
            neighbors = [
                Point(point.x + 1, point.y), Point(point.x - 1, point.y),
                Point(point.x, point.y + 1), Point(point.x, point.y - 1),
                Point(point.x + 1, point.y + 1), Point(point.x - 1, point.y - 1),
                Point(point.x + 1, point.y - 1), Point(point.x - 1, point.y + 1)
            ]
            # Exclue les points qui ne sont pas dans la grille
            return [
                n for n in neighbors 
                if (0 <= n.x < GRID_WIDTH and 0 <= n.y < GRID_HEIGHT) and 
                n not in obstacles
            ]

        open_set = []
        heapq.heappush(open_set, (0, self.position))
        came_from = {}
        g_score = {self.position: 0}
        f_score = {self.position: heuristic(self.position, target)}

        while open_set:
            current = heapq.heappop(open_set)[1]

            if current == target:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            for neighbor in get_neighbors(current):
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, target)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return []  # Reste statique si aucun chemin n'est trouvé

    
    def navigate_to_charging_station(self, charging_stations, obstacles):
        # Trouve la station la plus proche
        nearest_station = min(
            charging_stations,
            key=lambda station: abs(station.position.x - self.position.x) + abs(station.position.y - self.position.y)
        )
        self.path = self.a_star_pathfinding(nearest_station.position, obstacles)
        return nearest_station

    def move_along_path(self):
        if self.battery_life <= 0:
            print(f"Taxi {self.taxi_id} has stopped due to battery depletion.")
            return 
        
        if self.is_charging:
            self.charge_time += 1
            if self.charge_time >= 5:
                self.battery_life = 100
                self.is_charging = False
                self.charge_time = 0
            return
        elif self.path:
            self.position = self.path.pop(0)
            self.battery_life -= 0.25

