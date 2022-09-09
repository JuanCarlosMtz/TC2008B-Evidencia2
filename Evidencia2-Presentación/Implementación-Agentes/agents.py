import mesa

class GrassAgent(mesa.Agent):
  def __init__(self, unique_id, pos, model):
    super().__init__(pos, model)
    self.id = unique_id
    self.state = self.random.choice([0, 1, 2])
    self.countdown = 12
    self.change = 0

  def step(self):
    if self.change > 2:
      self.state = self.random.choice([0, 1, 2])
      self.change = 0
    else:
      self.change += 1

class CarAgent(mesa.Agent):
  def __init__(self, pos, model, direction, gridHeight, gridWidth, turn):
    super().__init__(pos, model)
    self.direction = direction
    self.originalDirection = direction
    self.gridHeight = gridHeight
    self.gridWidth = gridWidth
    self.turn = turn
    self.passedLight = False

  def keep_direction(self):
    if (self.direction == "right"): #derecha
      new_position = (self.pos[0]+1, self.pos[1])
      if (self.model.grid.is_cell_empty(new_position) == True):
        self.model.grid.move_agent(self, new_position)

    elif (self.direction == "down"): #abajo
      new_position = (self.pos[0], self.pos[1]-1)
      if (self.model.grid.is_cell_empty(new_position) == True):
        self.model.grid.move_agent(self, new_position)

    elif (self.direction == "left"): #izquierda
      new_position = (self.pos[0]-1, self.pos[1])
      if (self.model.grid.is_cell_empty(new_position) == True):
        self.model.grid.move_agent(self, new_position)
      
    elif (self.direction == "up"): #arriba
      new_position = (self.pos[0], self.pos[1]+1)
      if (self.model.grid.is_cell_empty(new_position) == True):
        self.model.grid.move_agent(self, new_position)

  def move_to_right(self):
    if (self.direction == "right"): #derecha hacia abajo
      if (self.pos[0] == int(self.gridWidth/2) - 1):
        self.direction = "down"
        self.turn = 0
      else: 
        new_position = (self.pos[0]+1, self.pos[1])
        if (self.model.grid.is_cell_empty(new_position) == True):
          self.model.grid.move_agent(self, new_position)
            
    elif (self.direction == "down"): #abajo hacia izquierda
      if (self.pos[1] == int(self.gridHeight/2)):
        self.direction = "left"
        self.turn = 0
      else: 
        new_position = (self.pos[0], self.pos[1]-1)
        if (self.model.grid.is_cell_empty(new_position) == True):
          self.model.grid.move_agent(self, new_position)

    elif (self.direction == "left"): #izquierda hacia arriba
      if (self.pos[0] == int(self.gridWidth/2)):
        self.direction = "up"
        self.turn = 0
      else:
        new_position = (self.pos[0]-1, self.pos[1])
        if (self.model.grid.is_cell_empty(new_position) == True):
          self.model.grid.move_agent(self, new_position)
      
    elif (self.direction == "up"): #arriba hacia derecha
      if (self.pos[1] == int(self.gridHeight/2) - 1):
        self.direction = "right"
        self.turn = 0
      else:
        new_position = (self.pos[0], self.pos[1]+1)
        if (self.model.grid.is_cell_empty(new_position) == True):
          self.model.grid.move_agent(self, new_position)
          
  def move_to_left(self):
    if (self.direction == "right"): #derecha hacia arriba
      if (self.pos[0] == int(self.gridWidth/2)):
        self.direction = "up"
        self.turn = 0
      else: 
        new_position = (self.pos[0]+1, self.pos[1])
        if (self.model.grid.is_cell_empty(new_position) == True):
          self.model.grid.move_agent(self, new_position)
            
    elif (self.direction == "down"): #abajo hacia derecha
      if (self.pos[1] == int(self.gridHeight/2) - 1):
        self.direction = "right"
        self.turn = 0
      else: 
        new_position = (self.pos[0], self.pos[1]-1)
        if (self.model.grid.is_cell_empty(new_position) == True):
          self.model.grid.move_agent(self, new_position)

    elif (self.direction == "left"): #izquierda hacia arriba
      if (self.pos[0] == int(self.gridWidth/2)):
        self.direction = "up"
        self.turn = 0
      else:
        new_position = (self.pos[0]-1, self.pos[1])
        if (self.model.grid.is_cell_empty(new_position) == True):
          self.model.grid.move_agent(self, new_position)
      
    elif (self.direction == "up"): #arriba hacia derecha
      if (self.pos[1] == int(self.gridHeight/2) - 1):
        self.direction = "right"
        self.turn = 0
      else:
        new_position = (self.pos[0], self.pos[1]+1)
        if (self.model.grid.is_cell_empty(new_position) == True):
          self.model.grid.move_agent(self, new_position)
      
  def move(self):
    if(self.turn == 0):
      self.keep_direction()
    elif(self.turn == 1):
      self.move_to_left()
    elif(self.turn == 2):
      self.move_to_right()
      
  def getArea(self):
    if (self.passedLight == False):
      for obj in self.model.grid.iter_neighbors(self.pos, moore=True, include_center=False):
        if isinstance(obj, LightAgent):
          if obj.state == "red":
            return "red"
          elif obj.state == "green":
            self.passedLight = True
            return "green"
          elif obj.state == "yellow":
            return "yellow"
    return "green"

  def killAgent(self):
    if self.pos == ((self.gridWidth-1, int(self.gridHeight/2-1))):
      self.model.kill_agents.append(self)
      return True
    
    elif self.pos == ((int((self.gridWidth/2)-1), 0)):
      self.model.kill_agents.append(self)
      return True

    elif self.pos == ((int((self.gridWidth/2)), self.gridHeight-1)):
      self.model.kill_agents.append(self)
      return True

    elif self.pos == ((0, int(self.gridHeight/2))):
      self.model.kill_agents.append(self)
      return True
      
    return False  
  
  def step(self):
    if self.killAgent() == False:
      if self.getArea() == "green":
        self.move()

class LightAgent(mesa.Agent):
  def __init__(self, unique_id, pos, model, state):
    super().__init__(pos, model)
    self.state = state
    self.id = unique_id
    self.countdown = 8

  def readArea(self):
    if self.id == 0 and self.state == "yellow":
      obj = self.model.grid.get_cell_list_contents((self.pos[0]-1, self.pos[1]+1))
      if len(obj) > 0:
        self.state="green"
        for objLight in self.model.grid.get_neighbors(self.pos, moore=True, include_center=False, radius=4):
          if isinstance(objLight, LightAgent):
            objLight.state = "red"
            objLight.countdown = 8
    
    elif self.id == 1 and self.state == "yellow":
      obj = self.model.grid.get_cell_list_contents((self.pos[0]+1, self.pos[1]+1))
      if len(obj) > 0:
        self.state="green"
        for objLight in self.model.grid.get_neighbors(self.pos, moore=True, include_center=False, radius=4):
          if isinstance(objLight, LightAgent):
            objLight.state = "red"
            objLight.countdown = 8
          
    elif self.id == 2 and self.state == "yellow":
      obj = self.model.grid.get_cell_list_contents((self.pos[0]+1, self.pos[1]-1))
      if len(obj) > 0:
        self.state="green"
        for objLight in self.model.grid.get_neighbors(self.pos, moore=True, include_center=False, radius=4):
          if isinstance(objLight, LightAgent):
            objLight.state = "red"
            objLight.countdown = 8
    
    elif self.id == 3 and self.state == "yellow":
      obj = self.model.grid.get_cell_list_contents((self.pos[0]-1, self.pos[1]-1))
      if len(obj) > 0:
        self.state="green"
        for objLight in self.model.grid.get_neighbors(self.pos, moore=True, include_center=False, radius=4):
          if isinstance(objLight, LightAgent):
            objLight.state = "red"
            objLight.countdown = 8
    
    if self.state == "green":
      self.countdown -= 2
      if self.countdown <= 0:
          self.state = "red"
          self.countdown = 8
          
    if self.state == "red":
      self.countdown -= 1
      if self.countdown <= 0:
          self.state = "yellow"
          self.countdown = 8
  
  def step(self):
    self.readArea()
    if self.state != "yellow":
      self.model.trafficLightStatus[self.id] = self.state
    else:
      self.model.trafficLightStatus[self.id] = "red"