import mesa

class GrassAgent(mesa.Agent):
  def __init__(self, unique_id, pos, model):
    super().__init__(pos, model)
    self.pos = pos
    self.state = self.random.choice([0, 1, 2])
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
  def __init__(self, pos, model, direction, gridHeight, gridWidth):
    super().__init__(pos, model)
    self.direction = direction
    self.gridHeight = gridHeight
    self.gridWidth = gridWidth

  def move(self):
    new_position = self.pos

    if (self.direction == 0 and self.pos[0] == self.gridWidth-1): #"reaparecer" auto 1
      new_position = (0, int(self.gridWidth/2))
      if (self.model.grid.is_cell_empty(new_position) == True):
        self.model.grid.move_agent(self, new_position)
    
    elif (self.direction == 0 and self.pos[0]+1 < self.gridWidth): #derecha
      new_position = (self.pos[0]+1, self.pos[1])
      if (self.model.grid.is_cell_empty(new_position) == True):
        self.model.grid.move_agent(self, new_position)

    elif (self.direction == 1 and self.pos[1] == 0): #"reaparecer" auto 2
      new_position = (int(self.gridWidth/2-1), self.gridHeight-1)
      if (self.model.grid.is_cell_empty(new_position) == True):
        self.model.grid.move_agent(self, new_position)
    
    elif (self.direction == 1 and self.pos[1]-1 >= 0): #abajo
      new_position = (self.pos[0], self.pos[1]-1)
      if (self.model.grid.is_cell_empty(new_position) == True):
        self.model.grid.move_agent(self, new_position)

  def getArea(self):
    area = self.model.grid.get_neighborhood(
      self.pos, moore=True, include_center=False
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
    if self.getArea() == "green":
      self.move()

class LightAgent(mesa.Agent):
  state = None
  def __init__(self, unique_id, pos, model, state=None):
    super().__init__(pos, model)
    self.pos = pos
    self.state = state
    self.countdown = 8
    self.id = unique_id

  def readArea(self):

    if (self.id == 1 and self.state == "yellow"):
      for obj in self.model.grid.get_cell_list_contents([(9, 13)]):
        if isinstance(obj, CarAgent):
          self.state = "green"
          for obj in self.model.grid.get_cell_list_contents([(7, 9)]):
            obj.state = "red"

    elif (self.id == 2 and self.state == "yellow"):
      for obj in self.model.grid.get_cell_list_contents([(6, 10)]):
        if isinstance(obj, CarAgent):
          self.state = "green"
          for obj in self.model.grid.get_cell_list_contents([(8, 12)]):
            obj.state = "red"

    if self.state == "green" or self.state == "red":
      self.countdown -= 1
    
    if self.countdown == 0:
      self.state = "yellow"
      self.countdown = 8
  
  def step(self):
    self.readArea()