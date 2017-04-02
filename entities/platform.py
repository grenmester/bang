import pygame
from entities.entity import Entity

class Platform(Entity):
    # if you want moving platforms, specify here minimum and maximum x and y values
    def __init__(self,x,y,dx,dy,width,height,world,passthrough=True,dropdown=True, min_x = 0, max_x = 700,image_file=None):
        super().__init__(x,y,dx,dy,width,height,world,color=(102,51,0),image_file=image_file)
        self.type = 'platform'
        self.passthrough = passthrough
        self.dropdown = dropdown
        self.min_x = min_x
        self.max_x = max_x

    def update(self):
        self.rect.x += self.dx
        if self.rect.x < self.min_x:
            self.dx *= -1
            self.rect.x = self.min_x + 1
        if self.rect.x + self.rect.width > self.max_x:
            self.dx *= -1
        self.rect.x %= self.world.width
        self.rect.y += self.dy
        if self.rect.y > self.world.height:
                self.rect.y%= self.world.height
