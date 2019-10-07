import unit

class Player:
  def __init__(self, playerId, connection):
    self.playerId = playerId
    self.connection = connection
    self.units = []