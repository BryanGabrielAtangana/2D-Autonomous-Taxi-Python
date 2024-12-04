import time
from collections import namedtuple

class PerformanceTracker:
    def __init__(self, total_ride_requests):
        self.total_ride_requests = total_ride_requests
        self.completed_rides = 0
        self.total_battery_consumption = 0
        self.idle_time = 0
        self.total_ride_time = 0
        self.operational_time = 0
        self.charging_time = 0
        self.total_distance = 0
        
        self.ride_start_time = 0
        self.simulation_start_time = time.time()

    def start_ride(self):
        self.ride_start_time = time.time()

    def end_ride(self):
        ride_duration = time.time() - self.ride_start_time
        self.total_ride_time += ride_duration

    def calculate_metrics(self):
        total_simulation_time = time.time() - self.simulation_start_time
        metrics = {
            'completion_rate': (self.completed_rides / self.total_ride_requests * 100),
            'idle_percentage': (self.idle_time / max(1, total_simulation_time)) * 100,
            'avg_ride_duration': self.total_ride_time / max(1, self.completed_rides),
        }
        return metrics