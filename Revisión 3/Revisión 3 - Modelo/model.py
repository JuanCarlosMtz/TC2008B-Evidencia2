import mesa
import json
import numpy as np
from agents import LightAgent, CarAgent, GrassAgent

class TrafficModel(mesa.Model):

  height = 14
  width = 14
  num_agents = 5
  
  def __init__(
    self,
    height=14,
    width=14,
    num_agents=10):
      super().__init__()
      self.height = height
      self.width = width
      self.num_agents = num_agents
      self.spawned_agents = 3
      self.spawn_direction = 0
      self.iteration = 0
      self.dicc = []
      
      self.schedule = mesa.time.SimultaneousActivation(self)
      self.grid = mesa.space.SingleGrid(self.width, self.height, torus=True)
      
      self.datacollector = mesa.DataCollector()
      """
        {
          "Lights": lambda m: m.schedule.get_type_count(LightAgent),
          "Cars": lambda m: m.schedule.get_type_count(CarAgent)
        }
      )
      """

      

      for (content, x, y) in self.grid.coord_iter():
				
        if (y != int(self.height/2-1) and x != int(self.width/2-1) and y != int(self.height/2) and x != int(self.width/2)):
          
          if (y == int(self.height/2-2) and x == int(self.width/2-3)):
            state = "yellow"
            light = LightAgent(0, (x, y), self, state)
            self.grid.place_agent(light, (x, y))
            self.schedule.add(light)
          elif (y == int(self.height/2+2) and x == int(self.width/2-2)):
            state = "yellow"
            light = LightAgent(1, (x, y), self, state)
            self.grid.place_agent(light, (x, y))
            self.schedule.add(light)
          elif (y == int(self.height/2+1) and x == int(self.width/2+2)):
            state = "yellow"
            light = LightAgent(2, (x, y), self, state)
            self.grid.place_agent(light, (x, y))
            self.schedule.add(light)
          elif (y == int(self.height/2-3) and x == int(self.width/2+1)):
            state = "yellow"
            light = LightAgent(3, (x, y), self, state)
            self.grid.place_agent(light, (x, y))
            self.schedule.add(light)

          elif (y == int(self.height/2+3) and x == int(self.width/2-2) or
          y == int(self.height/2+1) and x == int(self.width/2-2) or
          y == int(self.height/2-2) and x == int(self.width/2-2) or
          y == int(self.height/2-2) and x == int(self.width/2-4) or
          y == int(self.height/2+1) and x == int(self.width/2+1) or
          y == int(self.height/2+1) and x == int(self.width/2+3) or
          y == int(self.height/2-2) and x == int(self.width/2+1) or
          y == int(self.height/2-4) and x == int(self.width/2+1)):
            continue
          else:
            a = GrassAgent((x, y), (x, y), self)
            self.grid.place_agent(a, (x, y))
            self.schedule.add(a)


      self.running = True
      self.datacollector.collect(self)

  
  def step(self):
    if self.iteration < 10000:
      self.trafficLightStatus = ["", "", "", ""]

      self.kill_agents = []
      self.schedule.step()
      for x in self.kill_agents:
        self.grid.remove_agent(x)
        self.schedule.remove(x)
        self.kill_agents.remove(x)

      self.datacollector.collect(self)

      
      spawn = self.random.choice([0, 1])
      turn = self.random.choice([0, 1])
      if spawn == 0:
        spawn = self.random.choice([0, 1, 2, 3])
        self.spawn_direction = 4

      if (spawn == 0):
        if (self.grid.is_cell_empty((0, int(self.height/2-1))) == True):
          self.spawn_direction = 0
          x = 0
          y = int(self.height/2-1)
          direction = 0
          car = CarAgent(self.spawned_agents, self, direction, self.height, self.width, turn)
          self.schedule.add(car)
          self.grid.place_agent(car, (x, y))
          self.spawned_agents += 1
      elif (spawn == 1):
        if (self.grid.is_cell_empty((int(self.width/2-1), self.height-1)) == True):
          self.spawn_direction = 1
          x = int(self.width/2-1)
          y = self.height-1
          direction = 1
          car = CarAgent(self.spawned_agents, self, direction, self.height, self.width, turn)
          self.grid.place_agent(car, (x, y))
          self.schedule.add(car)
          self.spawned_agents += 1
      elif (spawn == 2):
        self.spawn_direction = 2
        if (self.grid.is_cell_empty((self.width-1, int(self.height/2))) == True):
          x = self.width-1
          y = int(self.height/2)
          direction = 2
          car = CarAgent(self.spawned_agents, self, direction, self.height, self.width, turn)
          self.schedule.add(car)
          self.grid.place_agent(car, (x, y))
          self.spawned_agents += 1
      elif (spawn == 3):
        self.spawn_direction = 3
        if (self.grid.is_cell_empty((int(self.width/2), 0)) == True):
          x = int(self.width/2)
          y = 0
          direction = 3
          car = CarAgent(self.spawned_agents, self, direction, self.height, self.width, turn)
          self.grid.place_agent(car, (x, y))
          self.schedule.add(car)
          self.spawned_agents += 1


      self.dicc.append({self.iteration: [
        {"Spawer": str(self.spawn_direction)},
        {"TLight0": self.trafficLightStatus[0]}, 
        {"TLight1": self.trafficLightStatus[1]},
        {"TLight2": self.trafficLightStatus[2]},
        {"TLight3": self.trafficLightStatus[3]}]}
      )
      
      self.iteration += 1
    
    

    elif self.iteration == 100:
      counter = 0
      with open("json_file3.json", "w") as archivo:
        archivo.write("[")
        for i in self.dicc:
          json.dump(i, archivo)
          if counter < self.iteration - 1:
            archivo.write(",\n")
          else:
            archivo.write("\n")
          counter += 1
        archivo.write("]")

    

  def get_grid(model):
    grid = np.zeros((model.grid.width, model.grid.height))

    for cell in model.grid.coord_iter():
      agent, x, y = cell

      if isinstance(agent, CarAgent):
        grid[x][y] = 5

      elif isinstance(agent, LightAgent):
        if agent.state == "yellow":
          grid[x][y] = 1
        if agent.state == "red":
          grid[x][y] = 2
        if agent.state == "green":
          grid[x][y] = 3

      else:
        grid[x][y] = 0

    return grid

  def read_agents(model):
    agents_list = []
    agent_dict = {}
    for cell in model.grid.coord_iter():
      agent, x, y = cell

      if isinstance(agent, CarAgent):
        agent_dict = {
          'type': 'car',
          'positionX': agent.pos[0],
          'positionY': 0,
          'positionZ': agent.pos[1]
        }
      elif isinstance(agent, LightAgent):
        agent_dict = {
          'id': agent.unique_id,
          'kind': 'trafficLight',
          'positionX': agent.pos[0],
          'positionY': 0,
          'positionZ': agent.pos[1],
          'state': agent.state
        }

      agents_list.append(agent_dict)

    return agents_list
    