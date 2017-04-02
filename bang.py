import pygame
from socketIO_client import SocketIO, LoggingNamespace
from socketClientThread import SocketClientThread, ClientCommand, ClientReply
from entities.world import World
from entities.player import Player
from entities.platform import Platform
import Queue
# import cProfile as profile


# def on_bye_response(*args):
#     print(args)

def main():
    # socketIO = SocketIO('localhost', 5001, LoggingNamespace)
    # socketIO.emit('hi-event', {1:1})
    # socketIO.on('bye-event', on_bye_response)
    # socketIO.wait(seconds=1)

    # socket stuff end
    width, height = 700, 500
    world = World(width,height)
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

            if pygame.time.get_ticks() % 5 == 0:
                world.clientsocket.cmd_q.put(ClientCommand(ClientCommand.RECEIVE, (.1, "add-player")))
                world.clientsocket.cmd_q.put(ClientCommand(ClientCommand.RECEIVE, (.1, "sent word")))

            # if answer:
            #     if command[0] == "player" and command[1][0] not in world.playerIds:
            #         print(world.playerIds.keys())
            #         player = Player(width//2, height//2,SPEED,0,32,32,world, playerId =  command[1][0])
            #         world.add_players([player])
            #         world.clientsocket.send(("player " + str(player.id)).encode("utf-8"))
            #         print("new player added")
            #     if command[0] == "command" and command[1] in world.playerIds:
            #         print(command)
            #         for word in command[2:]:
            #             if word in commands:

            #                 playerId = command[1]
            #                 player = world.playerIds[playerId]
            #                 if word == "jump":
            #                     player.jump()
            #                 if word == "bang":
            #                     player.shoot()
            #                 if word == "drop":
            #                     player.drop()
            #                 if word == "turn":
            #                     if player.direction == 1:
            #                         player.move_left()
            #                     else:
            #                         player.move_right()

            #                 #world.playerIds[command[1][0]].jump()

        world.update()
        world.draw()
        clock.tick(20)

        pygame.display.flip()
        if pygame.time.get_ticks() % 5 == 0:
            try:
                playerReply = world.clientsocket.reply_q.get(block=False)
                wordReply = world.clientsocket.reply_q.get(block=False)
                status = "SUCCESS" if reply.type == ClientReply.SUCCESS else "ERROR"
                self.log('Client reply %s: %s' % (status, reply.data))
                print(playerReply.data)
                print(wordReply.data)
            except Queue.Empty:
                print("empty queue")
                pass
        if pygame.time.get_ticks() % 5 == 0:
            try:
                playerReply = world.clientsocket.reply_q.get(True)
                wordReply = world.clientsocket.reply_q.get(True)
                print(playerReply.data)
                print(wordReply.data)
            except Queue.Empty:
                print("empty queue")
                pass



# profile.run('main()')
if __name__ == '__main__':
    main()
