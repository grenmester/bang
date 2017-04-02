import pygame

from entities.world import World
from entities.entity import Entity
from entities.player import Player
from entities.platform import Platform
from entities.bullet import Bullet

SPEED = 2

def main():
    width, height = 700, 500
    world = World(width,height)
    ground = Platform(0,height - 100,0,0,width,100,world,False,False)
    platform1 = Platform(100,height - 200,2,0,200,20,world, True, True, 0, world.width//2)
    platform2 = Platform(world.width//2 + 100 ,height - 200,2,0,200,20,world, True, True, world.width//2, world.width)
    platform3 = Platform(world.width//2 - 250, height - 300, 0, 0, 500, 20, world, True, True)
    platform4 = Platform(100,height - 400,2,0,200,20,world, True, True, 0, world.width//2)
    platform5 = Platform(world.width//2 + 100 ,height - 400,2,0,200,20,world, True, True, world.width//2, world.width)
    world.add_platforms([ground,platform1, platform2, platform3, platform4, platform5])
    player = Player(width//2, height//2,SPEED,0,32,32,world)
    player2 = Player(0,0,SPEED,0,32,32,world)
    world.add_players([player, player2])
    pygame.init()
    pygame.display.set_caption('Bang!')

    clock = pygame.time.Clock()

    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

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
                    player2.restore_ammo()

        world.update()
        world.draw()
        clock.tick(40)
        pygame.display.flip()

if __name__ == '__main__':
    main()
