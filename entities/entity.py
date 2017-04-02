import pygame

class Entity(pygame.sprite.Sprite):
    """
    Generic object entity class
    """
    def __init__(self,x,y,dx,dy,width,height,world,color=(0,255,0),image_file=None):
        super().__init__()
        self.dx = dx
        self.dy = dy
        self.world = world
        self.type = None

        if image_file:
            self.image = pygame.image.load(image_file)
        else:
            self.image = pygame.Surface([width, height])
            self.image.fill(color)
        # generate the hitbox
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
