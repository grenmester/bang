import pygame
import socket

class World():
    """
    World class
    """
    def __init__(self,width,height,players=[],bullets=[],platforms=[]):
        self.width = width
        self.height = height
        self.players = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.screen = pygame.display.set_mode([width,height])
        self.players.add(*players)
        self.bullets.add(*bullets)
        self.platforms.add(*platforms)
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsocket.connect(('localhost', 5000))
        self.clientsocket.settimeout(.05)
        message = 'hi to node from python'
        self.clientsocket.send(message.encode('utf-8'))
        self.playerIds = {" ":True}

    def endGame(self):
        msg = 'end'
        self.clientsocket.send(msg.encode('utf-8'))

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

    def update(self):
        self.platforms.update()
        self.players.update()
        self.bullets.update()

    def draw(self):
        """
        Draw all entities
        """
        self.screen.fill((0,0,255))
        self.platforms.draw(self.screen)
        self.players.draw(self.screen)
        self.bullets.draw(self.screen)
