import pygame, sys
from pygame.locals import *
import pickle
import select
import socket

import unit
import camera

WIDTH = 1000
HEIGHT = 600
BUFFERSIZE = 2048

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Game')

clock = pygame.time.Clock()

serverAddr = '127.0.0.1'
if len(sys.argv) == 2:
  serverAddr = sys.argv[1]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((serverAddr, 4321))

playerId = 0

camera = camera.Camera()
cc = unit.Minion(50, 50, 0)

minions = []

playing = True

def getNetworkCalls():
  global playerId
  ins, outs, ex = select.select([s], [], [], 0)
  for inm in ins: 
    gameEvent = pickle.loads(inm.recv(BUFFERSIZE))
    if gameEvent[0] == 'id update':
      playerId = gameEvent[1]
      print(playerId)
    if gameEvent[0] == 'player locations':
      gameEvent.pop(0)
      minions = []
      for minion in gameEvent:
        if minion[0] != playerId:
          minions.append(unit.Minion(minion[1], minion[2], minion[0]))

def getKeyboardAndMouseInputs():
  global playing
  for event in pygame.event.get():
    if event.type == QUIT:
      playing = False
    if event.type == KEYDOWN:
      if event.key == K_a: camera.vx = -3
      if event.key == K_d: camera.vx = 3
      if event.key == K_w: camera.vy = -3
      if event.key == K_s: camera.vy = 3
    if event.type == KEYUP:
      if event.key == K_a and camera.vx == -3: camera.vx = 0
      if event.key == K_d and camera.vx == 3: camera.vx = 0
      if event.key == K_w and camera.vy == -3: camera.vy = 0
      if event.key == K_s and camera.vy == 3: camera.vy = 0
    if event.type == MOUSEBUTTONDOWN:
      pos = pygame.mouse.get_pos()
      print('mouse down')
    if event.type == MOUSEBUTTONUP:
      pos = pygame.mouse.get_pos()
      print('mouse up')

def drawEverything():
  clock.tick(60)
  screen.fill((255,255,255))
  for m in minions:
    m.render(screen,camera)
  cc.render(screen,camera)
  pygame.display.flip()

def updateEverything():
  camera.update()
  cc.update()

def sendNetworkCalls():
  ge = ['position update', playerId, cc.x, cc.y]
  s.send(pickle.dumps(ge))

while playing:
  getNetworkCalls()
  drawEverything()
  updateEverything()
  sendNetworkCalls()
  getKeyboardAndMouseInputs()

ge = ['quit', playerId]
s.send(pickle.dumps(ge))
pygame.quit()
s.close()