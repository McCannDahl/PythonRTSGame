
print('hello....')

import socket
import asyncore
import select
import random
import pickle
import time
import unit
import player

print('started importing....')

BUFFERSIZE = 512

players = []

def removePlayer(playerId):
  removeIndex = -1
  for i, p in enumerate(players):
    if p.playerId == playerId:
      removeIndex = i
  if removeIndex >= 0:
    print ('removePlayer '+str(removeIndex))
    players.pop(removeIndex)

def updatePositions(playerId, x, y):
  for p in players:
    if p.playerId == playerId:
      p.x = x
      p.y = y
  sendPositions()

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
  elif messageType == 'position update':
    updatePositions(arr[1],arr[2],arr[3])

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
    conn.send(pickle.dumps(['your id is', playerId]))
    players.append(newplayer)
    SecondaryServer(conn)

class SecondaryServer(asyncore.dispatcher_with_send):
  def handle_read(self):
    recievedData = self.recv(BUFFERSIZE)
    if recievedData:
      readData(recievedData)
    else: self.close()

print('started')
MainServer(4321)
asyncore.loop()
