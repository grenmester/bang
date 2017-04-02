import pygame
from socketIO_client import SocketIO, LoggingNamespace
from entities.player import Player
from socketClientThread import SocketClientThread, ClientCommand, ClientReply

SPEED = 2

class World():
    """
    World class
    """

    # socketIO.emit('hi-event', {1:1}, on_bye_response)

    # socketIO.on('aaa', on_aaa_response)
    # # socketIO.emit('aaa')
    # # socketIO.wait(seconds=1)

    def __init__(self,width,height,players=[],bullets=[],platforms=[], healthbars=[]):
        self.width = width
        self.height = height
        self.players = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.healthbars = pygame.sprite.Group()
        self.screen = pygame.display.set_mode([width,height])
        self.players.add(*players)
        self.bullets.add(*bullets)
        self.platforms.add(*platforms)
        self.healthbars.add(*healthbars)
        #self.clientsocket = SocketIO('localhost', 5001, LoggingNamespace)
        #self.clientsocket.emit("connected", {"data": "Python socket connected"})
        self.clientsocket = SocketClientThread()
        self.clientsocket.start()
        self.clientsocket.cmd_q.put(ClientCommand(ClientCommand.CONNECT, ('localhost', 5001)))
        reply = self.clientsocket.reply_q.get(True)
        # self.clientsocket = SocketIO('localhost', 5001, LoggingNamespace)
        # self.clientsocket.emit("connected", {"data": "Python socket connected"})
        self.playerIds = {" ":True}
        # self.clientsocket.on('sent word', self.command_response)
        # self.clientsocket.on("add-player", self.add_players_wrapper)

    #TODO
    # def endGame(self):
    #     msg = 'end'
    #     self.clientsocket.emit(msg.encode('utf-8'))

    def command_response(self, *args):
        print(args)
        legal_commands = {"jump": Player.jump, "bang":Player.shoot, "drop":Player.drop, "turn":Player.turn}
        data = args[0]
        playerId = data["id"]
        command_words = data["commands"]
        for command in command_words:
            if command in legal_commands:
                print("Player " + playerId + "is trying to " + command)
                self.playerIds[playerId].legal_commands[command]()

    def add_players_wrapper(self, *args):
        player = player = Player(self.width//2, self.height//2,SPEED,0,32,32,self, playerId =  args[0]["id"])
        self.add_players([player])

    def add_players(self,players):
        """
        Expects a list of players
        """
        self.players.add(*players)
        for player in players:
            self.playerIds[player.id] = player

    def add_bullets(self,bullets):
        self.bullets.add(*bullets)

    def add_platforms(self,platforms):
        self.platforms.add(*platforms)

    def add_healthbars(self,healthbars):
        self.healthbars.add(*healthbars)

    def update(self):
        self.platforms.update()
        self.players.update()
        self.bullets.update()
        self.healthbars.update()

    def draw(self):
        """
        Draw all entities
        """
        self.screen.fill((102,178,255))
        self.platforms.draw(self.screen)
        self.players.draw(self.screen)
        self.bullets.draw(self.screen)
        self.healthbars.draw(self.screen)

#        healthbar = pygame.image.load("assets/char2.png")
#        laser = pygame.image.load("assets/laser.png")
#        self.screen.blit(healthbar, (5,5))
#        for health1 in range(5):
#            self.screen.blit(laser, (health1+8,8))
#        #update the screen
#        pygame.display.flip()
