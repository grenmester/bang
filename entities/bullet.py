import pygame
from entities.entity import Entity

class Bullet(Entity):
    def __init__(self,x,y,dx,dy,width,height,world,damage,player):
        super().__init__(x,y,dx,dy,width,height,world,color=(0,0,0))
        self.type = 'bullet'
        self.damage = damage
        # player who fired the bullet
        self.player = player

    def update(self):
        self.rect.x += self.dx
        # first check for collisions in platforms
        platforms_hit = pygame.sprite.spritecollide(self, self.world.platforms, False)
        if platforms_hit:
            # kill the sprite if we collide with a platform
            self.kill()
        # check for player collisions
        players_hit = pygame.sprite.spritecollide(self, self.world.players, False)
        if players_hit:
            self.kill()
            # damage all players if you intersect instead of undefined behavior
            for player in players_hit:
                if player != self.player:
                    player.damage(self.damage)
        # check for bullet collisions
        bullets_hit = pygame.sprite.spritecollide(self, self.world.bullets, False)
        if bullets_hit:
            for bullet in bullets_hit:
                # if the bullet is owned by another player
                if self.player != bullet.player:
                    # destroy both
                    self.kill()
                    bullet.kill()
        # destroy the bullet if it gets out of bounds
        if self.rect.x > self.world.width or self.rect.y < 0:
            self.kill()
