class Unit:
  def __init__(self, x, y, unitId, playerId):
    self.x = x
    self.y = y
    self.vx = 0
    self.vy = 0
    self.unitId = unitId
    self.playerId = playerId

  def update(self):
    self.x += self.vx
    self.y += self.vy