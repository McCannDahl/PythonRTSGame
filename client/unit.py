import pygame
BLUE = (0, 0, 255)

class Minion:
  def __init__(self, x, y, id):
    self.x = x
    self.y = y
    self.vx = 0
    self.vy = 0
    self.id = id

  def update(self):
    self.x += self.vx
    self.y += self.vy

  def render(self, screen, camera):
    pygame.draw.circle(screen, BLUE, (self.x+camera.x, self.y+camera.y), 20)
