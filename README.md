# 2D-Autonomous-Taxi-Python

## Setup

Download python : https://www.python.org/downloads/

Clone repository

```
git clone https://github.com/BryanGabrielAtangana/2D-Autonomous-Taxi-Python.git
cd 2D-Autonomous-Taxi-Python
```

Install pygame

Windows :
```
pip install pygame
```

MacOS :
```
pip3 install pygame
```
---

## Description

### **Autonomous Taxi System Overview**

#### **Components:**
1. **Taxi:** A self-driving electric vehicle tasked with transporting passengers between designated stops. 
2. **Obstacles:**  
   - **Static:** Fixed objects such as buildings or roadblocks.  
   - **Dynamic:** Other moving vehicles or agents. (not implemented yet)
3. **Passenger:** Individuals with a destination tied to a specific taxi stop.
4. **Stop:** Locations where passengers board and disembark.
5. **Charging Station:** Stations where taxis recharge to maintain operational readiness.

---

#### **Operation and Role of the Agent:**

1. **Assignment:** A centralized system allocates passengers to specific taxis based on location, destination, and taxi availability.
2. **Taxi Mission:** The autonomous taxi picks up its assigned passengers and delivers them to their designated stops while navigating obstacles and adhering to system constraints (e.g., battery levels).
3. **Intelligent Agent:** This is the core AI system that ensures:  
   - Optimal route planning.  
   - Obstacle avoidance.  
   - Battery management.  
   - Efficient passenger handling.

---

#### **Potential Extensions:**

1. **Public Transport Integration:** Merge with bus and train systems to create a seamless urban mobility solution.  
3. **Fleet Management:** Develop systems to oversee vehicle maintenance, scheduling, and optimal taxi allocation.  
4. **AI-Driven Improvements:** Enhance decision-making algorithms for better energy usage, Reingorcement learning could be used.

---
