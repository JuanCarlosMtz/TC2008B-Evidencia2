import mesa
from model import TrafficModel
from agents import LightAgent, CarAgent, GrassAgent

def car_and_lights_portrayal(agent):
  if agent is None:
    return

  portrayal = {}

  if type(agent) is CarAgent:
    if agent.originalDirection == "up":
      portrayal["Color"] = ["#00AAAA", "#00AAAA", "#00AAAA"]
    elif agent.originalDirection == "down":
      portrayal["Color"] = ["#000055", "#000055", "#000055"]
    elif agent.originalDirection == "left":
      portrayal["Color"] = ["#AA00EE", "#AA00EE", "#AA00EE"]
    elif agent.originalDirection == "right":
      portrayal["Color"] = ["#0055AA", "#0055AA", "#0055AA"]
    portrayal["Shape"] = "circle"
    portrayal["Filled"] = "true"
    portrayal["Layer"] = 1
    portrayal["r"] = 0.75

  elif type(agent) is LightAgent:
    if agent.state == "yellow":
      portrayal["Color"] = ["#FFFD37", "#FFFD37", "#FFFD37"]
    elif agent.state == "red":
      portrayal["Color"] = ["#AA0000", "#AA0000", "#AA0000"]
    elif agent.state == "green":
      portrayal["Color"] = ["#45f248", "#45f248", "#45f248"]
    portrayal["Shape"] = "circle"
    portrayal["Filled"] = "true"
    portrayal["Layer"] = 1
    portrayal["r"] = 1


  elif type(agent) is GrassAgent:
    if agent.state == 0:
      portrayal["Color"] = ["#00AA00", "#00AA00", "#00AA00"]
    elif agent.state == 1:
      portrayal["Color"] = ["#234f1e", "#234f1e", "#234f1e"]
    elif agent.state == 2:
      portrayal["Color"] = ["#26580f", "#26580f", "#26580f"]
    portrayal["Shape"] = "rect"
    portrayal["Filled"] = "true"
    portrayal["Layer"] = 1
    portrayal["w"] = 1
    portrayal["h"] = 1

  return portrayal

canvas_element = mesa.visualization.CanvasGrid(car_and_lights_portrayal, 14, 14, 500, 500)

server = mesa.visualization.ModularServer(
  TrafficModel, [canvas_element], "Cars And Lights",
)
server.port = 8521