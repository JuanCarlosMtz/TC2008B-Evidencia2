import sys
import mesa
import json
import numpy as np
from agents import LightAgent, CarAgent, GrassAgent

class TrafficModel(mesa.Model):
  def __init__(self, height=14, width=14):
      super().__init__()
      self.height = height
      self.width = width
      self.spawned_agents = 3
      self.spawn_direction = 0
      self.iteration = 0
      self.dicc = []
      
      self.schedule = mesa.time.SimultaneousActivation(self)
      self.grid = mesa.space.SingleGrid(self.width, self.height, torus=True)
      
      self.spawnLights()
      self.spawnGrass()

  def spawnLights(self):
    state = "yellow"
      
    x = int(self.width/2-2)
    y = int(self.height/2-2)
    light = LightAgent(0, (x, y), self, state)
    self.grid.place_agent(light, (x, y))
    self.schedule.add(light)
      
    x = int(self.width/2-2)
    y = int(self.height/2+1)
    light = LightAgent(1, (x, y), self, state)
    self.grid.place_agent(light, (x, y))
    self.schedule.add(light)
      
    x = int(self.width/2+1)
    y = int(self.height/2+1)
    light = LightAgent(2, (x, y), self, state)
    self.grid.place_agent(light, (x, y))
    self.schedule.add(light)
      
    x = int(self.width/2+1)
    y = int(self.height/2-2)
    light = LightAgent(3, (x, y), self, state)
    self.grid.place_agent(light, (x, y))
    self.schedule.add(light)
      
  def spawnGrass(self):
    for (content, x, y) in self.grid.coord_iter():
      if (x > int(self.width/2) or x < int(self.width/2-1)) and (y > int(self.height/2) or y < int(self.height/2-1)):
        if self.grid.is_cell_empty((x, y)):
          a = GrassAgent((x, y), (x, y), self)
          self.grid.place_agent(a, (x, y))
          self.schedule.add(a)
  
  def spawnCars(self):
    spawn = 5
    spawn_ = self.random.choice([0, 1, 0, 0])
    turn = self.random.choice([0, 1, 2])
    if spawn_ == 1:
      spawn = self.random.choice([0, 1, 2, 3])
      self.spawn_direction = 4

    if (spawn == 0):
      if (self.grid.is_cell_empty((0, int(self.height/2-1))) == True):
        self.spawn_direction = 0
        x = 0
        y = int(self.height/2-1)
        direction = "right"
        car = CarAgent(self.spawned_agents, self, direction, self.height, self.width, turn)
        self.schedule.add(car)
        self.grid.place_agent(car, (x, y))
        self.spawned_agents += 1
    elif (spawn == 1):
      if (self.grid.is_cell_empty((int(self.width/2-1), self.height-1)) == True):
        self.spawn_direction = 1
        x = int(self.width/2-1)
        y = self.height-1
        direction = "down"
        car = CarAgent(self.spawned_agents, self, direction, self.height, self.width, turn)
        self.grid.place_agent(car, (x, y))
        self.schedule.add(car)
        self.spawned_agents += 1
    elif (spawn == 2):
      self.spawn_direction = 2
      if (self.grid.is_cell_empty((self.width-1, int(self.height/2))) == True):
        x = self.width-1
        y = int(self.height/2)
        direction = "left"
        car = CarAgent(self.spawned_agents, self, direction, self.height, self.width, turn)
        self.schedule.add(car)
        self.grid.place_agent(car, (x, y))
        self.spawned_agents += 1
    elif (spawn == 3):
      self.spawn_direction = 3
      if (self.grid.is_cell_empty((int(self.width/2), 0)) == True):
        x = int(self.width/2)
        y = 0
        direction = "up"
        car = CarAgent(self.spawned_agents, self, direction, self.height, self.width, turn)
        self.grid.place_agent(car, (x, y))
        self.schedule.add(car)
        self.spawned_agents += 1
  
  def killAgents(self):
    self.kill_agents = []
    self.schedule.step()
    for x in self.kill_agents:
      self.grid.remove_agent(x)
      self.schedule.remove(x)
      self.kill_agents.remove(x)
  
  def getJson(self):
    self.iteration += 1
    if self.iteration < 100:
      self.trafficLightStatus = ["", "", "", ""]
      
      self.killAgents()
      self.spawnCars()
      
      self.dicc.append(
        {self.iteration: [
        {"Spawer": str(self.spawn_direction)},
        {"TLight0": self.trafficLightStatus[0]}, 
        {"TLight1": self.trafficLightStatus[1]},
        {"TLight2": self.trafficLightStatus[2]},
        {"TLight3": self.trafficLightStatus[3]}]}
      )
      
    if self.iteration == 100:
      counter = 0
      if output_dir:
        with open(output_dir, "w") as archivo:
          archivo.write("[")
          for i in self.dicc:
            json.dump(i, archivo)
            if counter < self.iteration - 1:
              archivo.write(",\n")
            else:
              archivo.write("\n")
            counter += 1
          archivo.write("]")
      else:
        with open("simulation.json", "w") as archivo:
          archivo.write("[")
          for i in self.dicc:
            json.dump(i, archivo)
            if counter < self.iteration - 1:
              archivo.write(",\n")
            else:
              archivo.write("\n")
            counter += 1
          archivo.write("]")

  
  def step(self):
    self.getJson()

width = 14
height = 14
steps = 100

program, output_dir = sys.argv 

model = TrafficModel(width, height)

for i in range(steps):
  model.step()
