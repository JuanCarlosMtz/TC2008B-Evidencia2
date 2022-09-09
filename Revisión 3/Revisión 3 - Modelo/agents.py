import mesa

class GrassAgent(mesa.Agent):
  def __init__(self, unique_id, pos, model):
    super().__init__(pos, model)
    #self.pos = pos
    self.state = self.random.choice([0, 1, 2])
    self.countdown = 12
    self.id = unique_id
    self.change = 0

  def step(self):
    if self.change > 2:
      self.state = self.random.choice([0, 1, 2])
      self.change = 0
    else:
      self.change += 1

class CarAgent(mesa.Agent):
  direction = None
  def __init__(self, pos, model, direction, gridHeight, gridWidth, turn):
    super().__init__(pos, model)
    self.direction = direction
    self.gridHeight = gridHeight
    self.gridWidth = gridWidth
    self.turn = turn

  def move(self):


    if(self.turn == 0):    
      if (self.direction == 0): #derecha
        new_position = (self.pos[0]+1, self.pos[1])
        if (self.model.grid.is_cell_empty(new_position) == True):
          self.model.grid.move_agent(self, new_position)

      if (self.direction == 1): #abajo
        new_position = (self.pos[0], self.pos[1]-1)
        if (self.model.grid.is_cell_empty(new_position) == True):
          self.model.grid.move_agent(self, new_position)

      if (self.direction == 2): #izquierda
        new_position = (self.pos[0]-1, self.pos[1])
        if (self.model.grid.is_cell_empty(new_position) == True):
          self.model.grid.move_agent(self, new_position)
      
      if (self.direction == 3): #arriba
        new_position = (self.pos[0], self.pos[1]+1)
        if (self.model.grid.is_cell_empty(new_position) == True):
          self.model.grid.move_agent(self, new_position)

    if(self.turn == 1): 
      if (self.direction == 0): #derecha
        if (self.pos[0] == int(self.gridWidth/2) - 1):
          self.direction = 1
          self.turn = 0
        else: 
          new_position = (self.pos[0]+1, self.pos[1])
          if (self.model.grid.is_cell_empty(new_position) == True):
            self.model.grid.move_agent(self, new_position)

      if (self.direction == 1): #abajo
        if (self.pos[1] == int(self.gridHeight/2)):
          self.direction = 2
          self.turn = 0
        else: 
          new_position = (self.pos[0], self.pos[1]-1)
          if (self.model.grid.is_cell_empty(new_position) == True):
            self.model.grid.move_agent(self, new_position)

      if (self.direction == 2): #izquierda
        if (self.pos[0] == int(self.gridWidth/2)):
          self.direction = 3
          self.turn = 0
        else:
          new_position = (self.pos[0]-1, self.pos[1])
          if (self.model.grid.is_cell_empty(new_position) == True):
            self.model.grid.move_agent(self, new_position)
      
      if (self.direction == 3): #arriba
        if (self.pos[1] == int(self.gridHeight/2) - 1):
          self.direction = 0
          self.turn = 0
        else:
          new_position = (self.pos[0], self.pos[1]+1)
          if (self.model.grid.is_cell_empty(new_position) == True):
            self.model.grid.move_agent(self, new_position)

  def getArea(self):
    area = self.model.grid.get_neighborhood(
      self.pos, moore=False, include_center=False
    )

    for obj in self.model.grid.get_cell_list_contents(area):
      if isinstance(obj, LightAgent):
        if obj.state == "red":
          return "red"
        elif obj.state == "green":
          return "green"
        elif obj.state == "yellow":
          return "yellow"
    return "green"
  
  def step(self):
    if self.pos == ((self.gridWidth-1, int(self.gridHeight/2-1))):
      self.model.kill_agents.append(self)
    
    elif self.pos == ((int((self.gridWidth/2)-1), 0)):
      self.model.kill_agents.append(self)

    elif self.pos == ((int((self.gridWidth/2)), self.gridHeight-1)):
      self.model.kill_agents.append(self)

    elif self.pos == ((0, int(self.gridHeight/2))):
      self.model.kill_agents.append(self)

    elif self.getArea() == "green":
      self.move()

class LightAgent(mesa.Agent):
  state = None
  def __init__(self, unique_id, pos, model, state=None):
    super().__init__(pos, model)
    #self.pos = pos
    self.state = state
    self.countdown = 9
    self.id = unique_id
    self.greenLimit = 0

  def readArea(self):
    #self.countdown -= 1

    if (self.state == "yellow" and self.greenLimit < 2):
      for obj in self.model.grid.get_neighbors(self.pos, moore=True, include_center = False):
        if isinstance(obj, CarAgent):
          self.state = "green"
          self.greenLimit += 1
          for objLight in self.model.grid.get_neighbors(self.pos, moore=True, include_center = False, radius = 5):
            if isinstance(objLight, LightAgent):
              objLight.state = "red"
              objLight.greenLimit = 0

    if self.state == "green" or self.state == "red":
      self.countdown -= 1
    
    if self.countdown == 0:
      self.state = "yellow"
      self.countdown = 9
      
    #if self.state == "green":
    #  self.state = "yellow"
    #  self.countdown = 5
  
  def step(self):
    self.readArea()
    if self.state != "yellow":
      self.model.trafficLightStatus[self.id] = self.state
    else:
      self.model.trafficLightStatus[self.id] = "red"