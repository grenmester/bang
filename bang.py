import pygame
#import socket

from entities.world import World
from entities.player import Player
from entities.platform import Platform
from entities.healthbar import Healthbar
# import cProfile as profile
commands = ["jump", "bang", "drop", "turn"]


SPEED = 10

def main():



    # socket stuff end
    width, height = 1200, 600
    world = World(width,height)
    ground = Platform(0,height - 100,0,0,width,100,world,False,False)
    platform1 = Platform(100,height - 200,2,0,200,20,world, True, True, 0, world.width//2)
    platform2 = Platform(world.width//2 + 100 ,height - 200,2,0,200,20,world, True, True, world.width//2, world.width)
    platform3 = Platform(world.width//2 - 250, height - 300, 0, 0, 500, 20, world, True, True)
    platform4 = Platform(100,height - 400,2,0,200,20,world, True, True, 0, world.width//2)
    platform5 = Platform(world.width//2 + 100 ,height - 400,2,0,200,20,world, True, True, world.width//2, world.width)
    world.add_platforms([ground,platform1, platform2, platform3, platform4, platform5])

    player = Player(width//2, height//2,SPEED,0,32,32,world,playerId=1, weapon='bazooka', image_file='assets/char1.png')
    player2 = Player(width//2, height//2,SPEED,0,32,32,world,playerId=2, weapon='laser', image_file='assets/char2.png')
    healthbar = Healthbar(width//2, height//2, 0, 0, 80, 16, world, player)
    healthbar2 = Healthbar(width//2, height//2, 0, 0, 80, 16, world, player2)
    world.add_players([player, player2])
    world.add_healthbars([healthbar, healthbar2])

    pygame.init()
    pygame.display.set_caption('Bang!')

    clock = pygame.time.Clock()

    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            answer = []
            #try:
            #    answer = world.clientsocket.recv(4096).decode("utf-8")
            #    command = answer.split(',')
            #    print(command)
            #except Exception as e:
            #    pass
            #if answer:
            #    command[0] == "player" and command[1][0] not in world.playerIds:
            #        print(world.playerIds.keys())
            #        player = Player(width//2, height//2,SPEED,0,32,32,world, playerId =  command[1][0])
            #        world.add_players([player])
            #        #world.clientsocket.send(("player " + str(player.id)).encode("utf-8"))
            #        print("new player added")
            #    if command[0] == "command" and command[1] in world.playerIds:
            #        print(command)
            #        for word in command[2:]:
            #            if word in commands:

            #                playerId = command[1]
            #                player = world.playerIds[playerId]
            #                if word == "jump":
            #                    player.jump()
            #                if word == "bang":
            #                    player.shoot()
            #                if word == "drop":
            #                    player.drop()
            #                if word == "turn":
            #                    if player.direction == 1:
            #                        player.move_left()
            #                    else:
            #                        player.move_right()

                            #world.playerIds[command[1][0]].jump()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move_left()
                if event.key == pygame.K_RIGHT:
                    player.move_right()
                if event.key == pygame.K_UP:
                    player.jump()
                if event.key == pygame.K_SPACE:
                    player.shoot()
                    player.attempt_respawn()
                if event.key == pygame.K_DOWN:
                    player.drop()
                if event.key == pygame.K_RSHIFT:
                    player.reload()
                if event.key == pygame.K_a:
                    player2.move_left()
                if event.key == pygame.K_d:
                    player2.move_right()
                if event.key == pygame.K_w:
                    player2.jump()
                if event.key == pygame.K_s:
                    player2.drop()
                if event.key == pygame.K_q:
                    player2.shoot()
                    player2.attempt_respawn()
                if event.key == pygame.K_r:
                    player2.reload()

        world.update()
        world.draw()
        clock.tick(45)
        pygame.display.flip()

if __name__ == '__main__':
    main()
