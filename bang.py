import pygame
# constants
GRAVITY = -1
SPEED = 2
HP = 5

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

    def add_players(self,players):
        """
        Expects a list of players
        """
        self.players.add(*players)

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

class Entity(pygame.sprite.Sprite):
    """
    Generic object entity class
    """
    def __init__(self,x,y,dx,dy,width,height,world,color=(0,255,0),image_file=None):
        super().__init__()
        self.dx = dx
        self.dy = dy
        self.width = width
        self.height = height
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

class Player(Entity):
    """
    Player class
    """
    def __init__(self,x,y,speed,dy,width,height,world,hp=HP,gravity=GRAVITY,direction = 1):
        # dx is speed (there is directionality to movement for the player)
        super().__init__(x,y,speed,dy,width,height,world,color=(255,0,0))
        self.type = 'player'
        self.hp = hp
        self.weapon = None
        self.ammo_count = None
        self.gravity = gravity
        self.speed = speed
        self.direction = direction

    def update(self):
        """
        Update the player location
        """
        # # the entities we are allowed to collide with
        # collidable_entities = pygame.sprite.Group()
        # collidable_entities.add(self.world.players)
        # collidable_entities.add(self.world.platforms)
        self.rect.x += self.speed * self.direction
        # first check for collisions in moving without wrapping
        platforms_hit = pygame.sprite.spritecollide(self, self.world.platforms, False)
        if platforms_hit:
            # print(platforms_hit)
            # if we're moving left
            if self.direction < 0:
                print("left")
                # push the player to the right edge of the rightmost entitiy
                self.rect.x = max(map(lambda s: s.rect.right,platforms_hit))
            # if we're moving right
            elif self.direction > 0:
                print("right")
                # push the player to the left edge of the leftmost entity
                self.rect.x = min(map(lambda s: s.rect.left,platforms_hit))- self.rect.width
            # now we try to wrap the player around
        self.rect.x %= self.world.width
            # second check for collisions in moving without wrapping
        # entities_hit = pygame.sprite.spritecollide(self, collidable_entities, False)
        # # do the same logic as before but since we're wrapping around invert collisions
        # # if we're moving right
        # if self.dx > 0:
        #     # push the player to the right edge of the rightmost entitiy
        #     self.rect.x = max(map(lambda s: s.rect.right,entities_hit))
        # # if we're moving left
        # elif self.dx < 0:
        #     # push the player to the left edge of the leftmost entity
        #     self.rect.x = min(map(lambda s: s.rect.left,entities_hit))
        self.rect.y += self.dy
        # decrement velocity by acceleration
        self.dy -= self.gravity
        # final check for collisions (this time in the y direction)
        platforms_hit = pygame.sprite.spritecollide(self, self.world.platforms, False)
        # print(platforms_hit)
        if platforms_hit:
            # print("hit")
            # if we're moving up
            if self.dy < 0:
                print("down")
                # push the player to the bottom edge of the rightmost entitiy
                self.rect.y = max(map(lambda s: s.rect.bottom,platforms_hit))
                # if you collide, set dy to 0
                self.dy = 0
            # if we're moving right
            elif self.dy > 0:
                print("up")
                # push the player to the top edge of the leftmost entity
                self.rect.y = min(map(lambda s: s.rect.top,platforms_hit))-self.rect.height
                # if you collide, set dy to 0
                self.dy = 0

    def damage(self,damage):
        self.hp -= damage
        if self.hp < 0:
            self.kill()

    def shoot(self):
        # create a hardcoded bullet
        x = self.rect.x
        # lead the bullet differently depending on what direction you're facing
        if self.direction < 0:
            x = self.rect.x - 10
        elif self.direction > 0:
            x = self.rect.x + self.rect.width
        bullet = Bullet(x, self.rect.y + round(self.rect.height * .25), 4*self.direction, 0, 8, 3, self.world, 1, self)
        self.world.bullets.add(bullet)

    def jump(self):
        """
        Increases y velocity
        """
        self.rect.y +=1
        entities_hit = pygame.sprite.spritecollide(self, self.world.platforms, False)
        # if you are touching at least one platform, jump
        self.rect.y-=1
        if entities_hit:
            self.dy = -15
            print("can jump")
        else:
            print("can't jump")

    def move_left(self):
        """
        Moves the player left
        """
        self.direction = -1

    def move_right(self):
        """
        Move the player right
        """
        self.direction = 1

    def stop(self):
        """
        Stops player movement
        """
        self.direction = 0

    def dropdown(self):
        """
        Drops through platform -- Unimplemented
        """
        entities_hit = pygame.sprite.spritecollide(self, self.world.platforms, False)

class Platform(Entity):
    # if you want moving platforms, specify here minimum and maximum x and y values
    def __init__(self,x,y,dx,dy,width,height,world,passthrough=True,dropdown=True):
        super().__init__(x,y,dx,dy,width,height,world,color=(255,0,255))
        self.type = 'platform'
        self.passthrough = True
        self.dropdown = True

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



def main():
    width, height = 700, 500
    world = World(width,height)
    ground = Platform(0,height - 100,0,0,width,100,world,False,False)
    platform1 = Platform(100,height - 200,0,0,100,20,world)
    world.add_platforms([ground,platform1])
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
                if event.key == pygame.K_a:
                    player2.move_left()
                if event.key == pygame.K_d:
                    player2.move_right()
                if event.key == pygame.K_w:
                    player2.jump()
                if event.key == pygame.K_s:
                    player2.shoot()

        world.update()
        world.draw()
        clock.tick(40)
        pygame.display.flip()

if __name__ == '__main__':
    main()
