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

playerid = 0

#game events
#['event type', param1, param2]
#
#event types: 
# id update 
# ['id update', id]
#
# player locations
# ['player locations', [id, x, y], [id, x, y] ...]

#user commands
# position update
# ['position update', id, x, y]

camera = camera.Camera()
cc = unit.Minion(50, 50, 0)

minions = []

while True:
  ins, outs, ex = select.select([s], [], [], 0)
  for inm in ins: 
    gameEvent = pickle.loads(inm.recv(BUFFERSIZE))
    if gameEvent[0] == 'id update':
      playerid = gameEvent[1]
      print(playerid)
    if gameEvent[0] == 'player locations':
      gameEvent.pop(0)
      minions = []
      for minion in gameEvent:
        if minion[0] != playerid:
          minions.append(unit.Minion(minion[1], minion[2], minion[0]))
    
  for event in pygame.event.get():
    if event.type == QUIT:
    	pygame.quit()
    	sys.exit()
    if event.type == KEYDOWN:
      if event.key == K_a: camera.vx = -10
      if event.key == K_d: camera.vx = 10
      if event.key == K_w: camera.vy = -10
      if event.key == K_s: camera.vy = 10
    if event.type == KEYUP:
      if event.key == K_a and camera.vx == -10: camera.vx = 0
      if event.key == K_d and camera.vx == 10: camera.vx = 0
      if event.key == K_w and camera.vy == -10: camera.vy = 0
      if event.key == K_s and camera.vy == 10: camera.vy = 0
    if event.type == MOUSEBUTTONDOWN:
      pos = pygame.mouse.get_pos()
      print('mouse down')
    if event.type == MOUSEBUTTONUP:
      pos = pygame.mouse.get_pos()
      print('mouse up')

  clock.tick(60)
  screen.fill((255,255,255))

  cc.update(camera)

  for m in minions:
    m.render(screen)

  cc.render(screen)

  pygame.display.flip()

  ge = ['position update', playerid, cc.x, cc.y]
  s.send(pickle.dumps(ge))
s.close()