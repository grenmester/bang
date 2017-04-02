import pygame
from entities.entity import Entity

class Healthbar(Entity):
    def __init__(self,x,y,dx,dy,width,height,world,player,image_file="assets/hearts5.png"):
        super().__init__(x,y,dx,dy,width,height,world,image_file=image_file)
        self.type = 'healthbar'
        self.player = player

    def update(self):
        self.rect.x = self.player.rect.x - 40 + 16
        self.rect.y = self.player.rect.y - 16
        if self.player.hp > 0:
            self.image = pygame.image.load("assets/hearts" + str(self.player.hp) + ".png")
        else:
            self.image = pygame.Surface([1, 1])
            self.image.fill((0,0,0))
