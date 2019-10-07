
print('hello....')

import socket
import asyncore
import select
import random
import pickle
import time
import unit
import player
import threading

print('started importing....')

BUFFERSIZE = 512

players = []
mapDct = {"name": "Montreal"}

def removePlayer(playerId):
  removeIndex = -1
  for i, p in enumerate(players):
    if p.playerId == playerId:
      removeIndex = i
  if removeIndex >= 0:
    print ('removePlayer '+str(removeIndex))
    players.pop(removeIndex)
  if len(players) <= 0:
    raise asyncore.ExitNow('Server is quitting!')

def sendPositions():
  update = ['player locations']
  for p in players:
    update.append([p.playerId, p.x, p.y])
  for p in players:
    try:
      p.connection.send(pickle.dumps(update))
    except Exception:
      print ('Sould Remove this one')

def readData(message):
  arr = pickle.loads(message)
  messageType = arr[0]
  if messageType == "quit":
    removePlayer(arr[1]) 

class MainServer(asyncore.dispatcher):
  def __init__(self, port):
    asyncore.dispatcher.__init__(self)
    self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
    self.bind(('', port))
    self.listen(10)
  def handle_accept(self):
    conn, addr = self.accept()
    print ('Connection address:' + addr[0] + " " + str(addr[1]))
    playerId = len(players)
    newplayer = player.Player(playerId,conn)
    players.append(newplayer)
    SecondaryServer(conn)
    print(mapDct)
    print(pickle.dumps(['init update', playerId, mapDct]))
    conn.send(pickle.dumps(['init update', playerId, mapDct]))

class SecondaryServer(asyncore.dispatcher_with_send):
  def handle_read(self):
    recievedData = self.recv(BUFFERSIZE)
    if recievedData:
      readData(recievedData)
    else: self.close()

print('started')
MainServer(4321)
asyncore.loop()



#----------------------------------------------------------------------

WAIT_SECONDS = 0.5
def updateEverything():
  print("Updating Everything!")
  updateAllUnits()
  threading.Timer(WAIT_SECONDS, updateEverything).start()

def updateAllUnits():
  for player in players:
    for unit in player.units:
      unit.update()
updateEverything()