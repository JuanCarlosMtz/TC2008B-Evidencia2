import mesa
import numpy as np
from agents import LightAgent, CarAgent, GrassAgent

class TrafficModel(mesa.Model):

  height = 20
  width = 20
  num_agents = 5
  
  def __init__(
    self,
    height=20,
    width=20,
    num_agents=10):
      super().__init__()
      self.height = height
      self.width = width
      self.num_agents = num_agents
      
      self.schedule = mesa.time.SimultaneousActivation(self)
      self.grid = mesa.space.SingleGrid(self.width, self.height, torus=True)
      
      self.datacollector = mesa.DataCollector()

			# Primer auto eje x
      x = 0
      y = int(self.height/2)
      direction = 0
      car = CarAgent((x, y), self, direction, height, width)
      self.schedule.add(car)
      self.grid.place_agent(car, (x, y))

			# Segundo auto eje x
      x = 3
      y = int(self.height/2)
      direction = 0
      car = CarAgent((x, y), self, direction, height, width)
      self.schedule.add(car)
      self.grid.place_agent(car, (x, y))

      # Primer auto eje y
      x = int(self.width/2-1)
      y = height-1
      direction = 1
      car = CarAgent((x, y), self, direction, height, width)
      self.grid.place_agent(car, (x, y))
      self.schedule.add(car)

			# Segundo auto eje y
      x = int(self.width/2-1)
      y = height-3
      direction = 1
      car = CarAgent((x, y), self, direction, height, width)
      self.grid.place_agent(car, (x, y))
      self.schedule.add(car)

      for (content, x, y) in self.grid.coord_iter():
				
        if (y != int(self.height/2) and x != int(self.width/2-1)):
          if (y == int(self.height/2+2) and x == int(self.width/2-2)):
            state = "yellow"
            light = LightAgent(1, (x, y), self, state)
            self.grid.place_agent(light, (x, y))
            self.schedule.add(light)
          elif (y == int(self.height/2-1) and x == int(self.width/2-3)):
            state = "yellow"
            light = LightAgent(2, (x, y), self, state)
            self.grid.place_agent(light, (x, y))
            self.schedule.add(light)
          elif (y == int(self.height/2+3) and x == int(self.width/2-2) or
          y == int(self.height/2+1) and x == int(self.width/2-2) or
          y == int(self.height/2-1) and x == int(self.width/2-2) or
          y == int(self.height/2-1) and x == int(self.width/2-4)):
            continue
          else:
            a = GrassAgent((x, y), (x, y), self)
            self.grid.place_agent(a, (x, y))
            self.schedule.add(a)


      self.running = True
      self.datacollector.collect(self)

  def step(self):
    self.schedule.step()
    self.datacollector.collect(self)

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
    