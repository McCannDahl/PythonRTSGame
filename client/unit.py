import pygame
BLUE = (0, 0, 255)

class Unit:
  def __init__(self, x, y, unitId, playerId):
    self.x = x
    self.y = y
    self.vx = 0
    self.vy = 0
    self.unitId = unitId
    self.playerId = playerId

  def render(self, screen, camera):
    pygame.draw.circle(screen, BLUE, (self.x+camera.x, self.y+camera.y), 20)
