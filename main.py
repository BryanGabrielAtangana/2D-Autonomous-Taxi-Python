"""main.py """
import pygame
import random
from collections import namedtuple

from taxi import Taxi
from passenger import Passenger
from taxi_stop import TaxiStop
from charging_station import ChargingStation
from obstacle import Obstacle

pygame.init()

# Constantes
SCREEN_WIDTH, SCREEN_HEIGHT = 1400, 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (230, 230, 230)
TAXI_COLOR = (232, 139, 0)
MAX_PASSENGERS = 14

# Cellule de la grille
Point = namedtuple('Point', 'x, y')

# Initialisation de l'écran
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simulation Agent autonome - IA 2024")

# Police
font = pygame.font.SysFont(None, 24)

# Genère les passager
def generate_passengers(taxi_stops):
    passengers = []
    for i in range(MAX_PASSENGERS):
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        destination = random.choice(taxi_stops)
        passenger = Passenger(passenger_id=i+1, position=Point(x, y), destination=destination)
        passengers.append(passenger)
    return passengers

# Intialise les station d'arrêt
taxi_stops = [
    TaxiStop(stop_id=1, position=Point(10, 5), color=(16, 196, 61)), 
    TaxiStop(stop_id=2, position=Point(55, 10), color=(16, 187, 196)),   
    TaxiStop(stop_id=3, position=Point(20, 20), color=(196, 16, 70)),   
]

charging_stations = [
    ChargingStation(station_id=1, position=Point(5, 25)), 
    ChargingStation(station_id=2, position=Point(25, 5)),   
]

# Ajout d'obstacles sur la grille
grid_obstacles = [
    # Block 1
    Obstacle(obstacle_id=1, position=Point(8, 8)),
    Obstacle(obstacle_id=2, position=Point(8, 9)),
    Obstacle(obstacle_id=3, position=Point(7, 8)),
    Obstacle(obstacle_id=4, position=Point(7, 9)),

    # Block 2
    Obstacle(obstacle_id=5, position=Point(12, 12)),
    Obstacle(obstacle_id=6, position=Point(12, 13)),
    Obstacle(obstacle_id=7, position=Point(12, 14)),
    Obstacle(obstacle_id=8, position=Point(12, 15)),
    Obstacle(obstacle_id=9, position=Point(12, 16)),

    # Block 3
    Obstacle(obstacle_id=10, position=Point(30, 18)),
    Obstacle(obstacle_id=11, position=Point(31, 18)),
    Obstacle(obstacle_id=12, position=Point(30, 19)),
    Obstacle(obstacle_id=13, position=Point(31, 19)),
    Obstacle(obstacle_id=14, position=Point(30, 20)),
    Obstacle(obstacle_id=15, position=Point(31, 20)),

    # Block 4
    Obstacle(obstacle_id=16, position=Point(50, 13)),
    Obstacle(obstacle_id=17, position=Point(50, 14)),
    Obstacle(obstacle_id=18, position=Point(50, 15)),
    Obstacle(obstacle_id=19, position=Point(51, 15)),
    Obstacle(obstacle_id=20, position=Point(52, 15)),

    # Block 5
    Obstacle(obstacle_id=21, position=Point(20, 25)),
    Obstacle(obstacle_id=22, position=Point(21, 25)),
    Obstacle(obstacle_id=23, position=Point(22, 25)),
    Obstacle(obstacle_id=24, position=Point(23, 25)),
    Obstacle(obstacle_id=25, position=Point(24, 25)),

    # Block 6
    Obstacle(obstacle_id=26, position=Point(40, 10)),
    Obstacle(obstacle_id=27, position=Point(41, 11)),
    Obstacle(obstacle_id=28, position=Point(42, 10)),
    Obstacle(obstacle_id=29, position=Point(43, 11)),
    Obstacle(obstacle_id=30, position=Point(44, 10)),
    
    # Block 7
    *[
        Obstacle(obstacle_id=31 + i * 5 + j, position=Point(60 + i, 20 + j))
        for i in range(3)  # Rows
        for j in range(3)  # Columns
    ]
]

# Initialisation des passager
passengers = generate_passengers(taxi_stops)

# Intialisation de l'agent
taxi = Taxi(taxi_id=1, start_point=Point(5, 5), color=TAXI_COLOR, capacity=3)

# Dessine la grille
def draw_grid(surface):
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(surface, BLACK, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(surface, BLACK, (0, y), (SCREEN_WIDTH, y))

# Dessine les passager
def draw_passengers(surface, passengers):
    for passenger in passengers:
        passenger.draw(surface)

# Boucle principale
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Logic de recharge lorsque le taxi est décharger
    if taxi.battery_life <= 20 and not taxi.is_charging:
        obstacles = [obs.position for obs in grid_obstacles]
        charging_station = taxi.navigate_to_charging_station(charging_stations, obstacles)
        if taxi.position == charging_station.position:
            taxi.is_charging = True  # En charge

    # Le taxi s'arrête si la batterie est à 0
    if taxi.battery_life <= 0:
        print("Taxi battery is depleted. Simulation halted.")  

    # Logic pour trouver le chemin
    if not taxi.path:
        # regarde si il faut déposer les passager
        if taxi.passengers:
            for passenger in taxi.passengers[:]: 
                destination = passenger.destination
                obstacles = [stop.position for stop in taxi_stops if stop != destination]
                taxi.path = taxi.a_star_pathfinding(destination.position, obstacles + [obs.position for obs in grid_obstacles])

                # dépose chaque passager à sa destination
                if taxi.position == destination.position:
                    destination.dropped_passengers.append(passenger)
                    taxi.passengers.remove(passenger)

        # Prend le passager si il y a de l'espace
        if len(taxi.passengers) < taxi.capacity and passengers:
            # Trouve le passager le plus proche
            capacity_left = taxi.capacity - len(taxi.passengers)
            nearest_passengers = sorted(passengers, key=lambda p: abs(p.position.x - taxi.position.x) + abs(p.position.y - taxi.position.y))
            
            for passenger in nearest_passengers[:capacity_left]:
                obstacles = [p.position for p in taxi.passengers] + [stop.position for stop in taxi_stops]
                taxi.path = taxi.a_star_pathfinding(passenger.position, obstacles + [obs.position for obs in grid_obstacles])
                
                # récupère le passager
                if taxi.position == passenger.position:
                    taxi.passengers.append(passenger)
                    passengers.remove(passenger)

        #Regénère de nouveaux passager à la fin de chaque cycle
        if not passengers and not taxi.passengers:
            passengers = generate_passengers(taxi_stops)

    # movement du taxi
    taxi.move_along_path()

    screen.fill(WHITE)

    # Dessine la grille, les passengers, les arrêts, les station de recharge, et le taxi
    draw_grid(screen)
    draw_passengers(screen, passengers)
    for stop in taxi_stops:
        stop.draw(screen)
    for station in charging_stations:
        station.draw(screen)
    for obstacle in grid_obstacles:
        obstacle.draw(screen)
    taxi.draw(screen)

    # Actualise la fenêtre d'affichage
    pygame.display.flip()
    clock.tick(10)

pygame.quit()