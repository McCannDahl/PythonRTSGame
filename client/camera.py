
class Camera:
  def __init__(self):
    self.x = 0
    self.y = 0
    self.vx = 0
    self.vy = 0
    self.zoom = 0

  def update(self):
    self.x += self.vx
    self.y += self.vy
