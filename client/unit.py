import pygame
BLUE = (0, 0, 255)

class Minion:
  def __init__(self, x, y, id):
    self.x = x
    self.y = y
    self.vx = 0
    self.vy = 0
    self.id = id

  def update(self, camera):
    self.x += self.vx
    self.y += self.vy

    self.x += camera.x
    self.y += camera.y

  def render(self, screen):
    pygame.draw.circle(screen, BLUE, (self.x, self.y), 20)
