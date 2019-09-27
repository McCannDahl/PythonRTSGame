Python RTS Game

Buildings
    land builder
    sea builder
    air builder
    land resources depo
    sea resources depo
Units
    land = circle
        dump truck
        pawn
        healer
    sea = rectangle
        canoe
    air = triangle
        fighter
        hellicopter
Resources
    gold
    oil
    space rocks
Tech Tree

Server interactions Sudo Code
    client
        unit
            if unit.velocity changed
                send to server (id, playerId, x, y, type)
            if unit Destroyed
                send to server (id)
        if building Created or Destroyed
            send to server (id, playerId, type)
    server
        pass on changes from clients
    server & client
        periodically check all unit positions. If discrepancy in enemy position, correct by sending all them out (own client holds truth). 

Client side Sudo Code
    update
        unit
            update position according to velocity, collisions
        enemy units
            update position according to velocity
            enemy shoots specific target or closest thing (reduce health of unit or building)
        buildings
            build units/gather resources
    

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