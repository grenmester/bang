import pygame
import socket

from entities.world import World
from entities.entity import Entity
from entities.player import Player
from entities.platform import Platform
from entities.bullet import Bullet

SPEED = 2

def main():
    # socket stuff end
    width, height = 700, 500
    world = World(width,height)
    # answer = world.clientsocket.recv(4096)
    # print(answer)
    ground = Platform(0,height - 100,0,0,width,100,world,False,False)
    platform1 = Platform(100,height - 200,2,0,200,20,world, True, True, 0, world.width//2)
    platform2 = Platform(world.width//2 + 100 ,height - 200,2,0,200,20,world, True, True, world.width//2, world.width)
    platform3 = Platform(world.width//2 - 250, height - 300, 0, 0, 500, 20, world, True, True)
    platform4 = Platform(100,height - 400,2,0,200,20,world, True, True, 0, world.width//2)
    platform5 = Platform(world.width//2 + 100 ,height - 400,2,0,200,20,world, True, True, world.width//2, world.width)
    world.add_platforms([ground,platform1, platform2, platform3, platform4, platform5])
    pygame.init()
    pygame.display.set_caption('Bang!')

    clock = pygame.time.Clock()

    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            answer = []
            try:
                answer = world.clientsocket.recv(4096).decode("utf-8")
                command = answer.split(' ' )
                print(answer)
            except Exception as e:
                pass
            if answer:
                if command[0] == "player" and command[1][0] not in world.playerIds:
                    print(world.playerIds.keys())
                    player = Player(width//2, height//2,SPEED,0,32,32,world, playerId =  command[1][0])
                    world.add_players([player])
                    world.clientsocket.send(("player " + str(player.id)).encode("utf-8"))
                    print("new player added")


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
                    player.restore_ammo()
                # if event.key == pygame.K_a:
                #     player2.move_left()
                # if event.key == pygame.K_d:
                #     player2.move_right()
                # if event.key == pygame.K_w:
                #     player2.jump()
                # if event.key == pygame.K_s:
                #     player2.drop()
                # if event.key == pygame.K_q:
                #     player2.shoot()
                #     player2.attempt_respawn()
                # if event.key == pygame.K_r:
                #     player2.restore_ammo()

        world.update()
        world.draw()
        clock.tick(40)
        pygame.display.flip()

if __name__ == '__main__':
    main()
