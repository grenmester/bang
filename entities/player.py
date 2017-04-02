import pygame, os
from entities.entity import Entity
from entities.bullet import Bullet

GRAVITY = 4
HP = 5
RESPAWN_TICKS = 5
NUM_PLAYERS = 0

WEAPONS = {'revolver':{'damage': 1, 'max_ammo': 6, 'speed': 13, 'file_name': 'assets/revolver.png', 'bullet_file_name': 'assets/bullet.png'},
            'bazooka':{'damage': 2, 'max_ammo': 2, 'speed': 11, 'file_name': 'assets/bazooka.png', 'bullet_file_name': 'assets/rocket.png'},
            'laser':{'damage': 1, 'max_ammo': 3, 'speed': 16, 'file_name': 'assets/laser_rifle.png', 'bullet_file_name': 'assets/laser.png'}}

class Player(Entity):
    """
    Player class
    """
    def __init__(self,x,y,speed,dy,width,height,world,weapon='revolver',hp=HP,gravity=GRAVITY,direction = 1,image_file=None,playerId=1):
        # dx is speed (there is directionality to movement for the player)
        super().__init__(x,y,speed,dy,width,height,world,color=(255,0,0),image_file=image_file)
        global NUM_PLAYERS
        NUM_PLAYERS += 1
        self.start_x,self.start_y = x,y
        self.type = 'player'
        self.hp = hp
        self.weapon = weapon
        self.max_ammo = WEAPONS[weapon]['max_ammo']
        self.ammo_count = self.max_ammo
        self.gravity = gravity
        self.speed = speed
        self.direction = direction
        self.dropping = False
        self.alive = True
        if playerId:
            self.id = playerId
        else:
            self.id = NUM_PLAYERS
        # self.world.clientsocket.send(("player " + str(self.id)).encode("utf-8"))

    def sendColor(self):
        #msg = 'color ' + str(self.id) + ' ' + str(self.color)
        self.world.clientsocket.emit('color', {'id': self.id, 'color': self.color})

    def sendHealth(self):
        #msg = 'health ' + str(self.id) + ' ' + str(max(0, self.hp))
        self.world.clientsocket.emit('health', {'id': self.id, 'health': self.hp})

    def sendAmmo(self):
        #msg = 'ammo ' + str(self.id) + ' ' + str(max(0, self.ammo_count))
        self.world.clientsocket.emit('ammo', {'id': self.id, 'ammo': self.ammo_count})

    def update(self):
        """
        Update the player location
        """
        # # the entities we are allowed to collide with
        # collidable_entities = pygame.sprite.Group()
        # collidable_entities.add(self.world.players)
        # collidable_entities.add(self.world.platforms)
        if self.dropping:
            self.rect.x += self.speed * self.direction
            self.rect.x %= self.world.width
            self.rect.y += self.dy
            self.rect.y += 1
            self.rect.y %= self.world.height
            self.dy += self.gravity

            platforms_hit = pygame.sprite.spritecollide(self, self.world.platforms, False)
            if not platforms_hit:
                self.dropping = False
        else:
            # first check for collisions in moving without wrapping
            platforms_hit = pygame.sprite.spritecollide(self, self.world.platforms, False)
            passthrough_platforms = [x for x in platforms_hit if x.passthrough]
            hard_platforms = [x for x in platforms_hit if not x.passthrough]

            # move in the x direction
            self.rect.y += 1
            entities_hit = pygame.sprite.spritecollide(self, self.world.platforms, False)
            self.rect.x += self.speed * self.direction
            if not self.dropping and entities_hit != [] and self.dy > 0:
                self.rect.x += entities_hit[0].dx * 4
            self.rect.y -= 1

            if hard_platforms and not passthrough_platforms:
                # if we're moving left
                self.resolve_x_platform_collision(hard_platforms)
                # now we try to wrap the player around
            elif passthrough_platforms and not hard_platforms:
                if self.rect.y + self.rect.height < max(map(lambda s: s.rect.height, passthrough_platforms)):
                    self.resolve_x_platform_collision(passthrough_platforms)

            elif passthrough_platforms and hard_platforms:
                if self.rect.y + self.rect.height < max(map(lambda s: s.rect.height, passthrough_platforms)):
                    self.resolve_x_platform_collision(platforms_hit)
                else:
                    self.resolve_x_platform_collision(hard_platforms)


            self.rect.x %= self.world.width

            self.rect.y += self.dy
            # decrement velocity by acceleration
            self.dy += self.gravity

            # check for collisions (this time in the y direction)
            platforms_hit = pygame.sprite.spritecollide(self, self.world.platforms, False)
            passthrough_platforms = [x for x in platforms_hit if x.passthrough]
            hard_platforms = [x for x in platforms_hit if not x.passthrough]
            if hard_platforms and not passthrough_platforms:
                self.resolve_y_platform_collision(hard_platforms)

            elif passthrough_platforms and not hard_platforms:
                if self.rect.y + self.rect.height < max(map(lambda s: s.rect.y, passthrough_platforms)) + self.dy:
                    self.resolve_y_platform_collision(passthrough_platforms)

            elif passthrough_platforms and hard_platforms:
                if self.rect.y + self.rect.height < max(map(lambda s: s.rect.y, passthrough_platforms)) + self.dy:
                    self.resolve_y_platform_collision(platforms_hit)
                else:
                    self.resolve_y_platform_collision(hard_platforms)
            if self.rect.y > self.world.height:
                self.rect.y %= self.world.height


    def resolve_x_platform_collision(self, platforms_list):
        if self.direction < 0:
            self.rect.x = max(map(lambda s: s.rect.right,platforms_list))

        # if we're moving right
        elif self.direction > 0:

            # push the player to the left edge of the leftmost entity
            self.rect.x = min(map(lambda s: s.rect.left,platforms_list))- self.rect.width

    def resolve_y_platform_collision(self, platforms_list):
        if self.dy < 0:
            # push the player to the bottom edge of the rightmost entitiy
            self.rect.y = max(map(lambda s: s.rect.bottom,platforms_list))
            # if you collide, set dy to 0
            self.dy = 0

        # if we're moving down
        elif self.dy > 0:
            # push the player to the top edge of the leftmost entity
            self.rect.y = min(map(lambda s: s.rect.top,platforms_list))-self.rect.height
            # if you collide, set dy to 0
            self.dy = 0
        if self.rect.y + self.rect. height> self.world.height - 100 + 3:
            self.rect.y = self.world.height - 100 + self.rect.height

    def damage(self,damage):
        """
        Damages player; returns True if player killed, False otherwise
        """
        self.hp -= damage
        # self.sendHealth()
        if self.hp <= 0:
            self.kill()
            self.alive = False
            self.ticks_until_respawn = RESPAWN_TICKS
            return True
        return False

    def shoot(self):
        if self.alive and self.ammo_count > 0:
            # create a hardcoded bullet
            x = self.rect.x
            # lead the bullet differently depending on what direction you're facing
            if self.direction < 0:
                x = self.rect.x - 15
            elif self.direction > 0:
                x = self.rect.x + self.rect.width
            # get bullet values
            bullet_speed = WEAPONS[self.weapon]['speed']
            bullet_file_name = WEAPONS[self.weapon]['bullet_file_name']
            bullet_damage = WEAPONS[self.weapon]['damage']
            args = {'x':x, 'y': self.rect.y + round(self.rect.height * .6),
                    'dx':bullet_speed*self.direction, 'dy':0,
                    'width':None, 'height':None, 'world':self.world, 'weapon':self.weapon,
                    'damage':bullet_damage,'player':self, 'image_file':bullet_file_name}
            bullet = Bullet(**args)
            self.world.bullets.add(bullet)
            self.ammo_count -= 1
            # self.sendAmmo()

    def reload(self):
        self.ammo_count = self.max_ammo

    def jump(self):
        """
        Increases y velocity
        """
        self.rect.y +=1
        entities_hit = pygame.sprite.spritecollide(self, self.world.platforms, False)
        # if you are touching at least one platform, jump
        self.rect.y-=1
        if entities_hit:
            self.dy = -28

    def drop(self):
        self.rect.y +=1
        platforms_hit = pygame.sprite.spritecollide(self, self.world.platforms, False)
        # if you are touching at least one platform, jump
        self.rect.y-=1
        if all([x.dropdown for x in platforms_hit]):
            self.dropping = True

    def move_left(self):
        """
        Moves the player left
        """
        oldDirection = self.direction
        self.direction = -1
        if not oldDirection == self.direction:
            self.image = pygame.transform.flip(self.image, True, False)

    def move_right(self):
        """
        Move the player right
        """
        oldDirection = self.direction
        self.direction = 1
        if not oldDirection == self.direction:
            self.image = pygame.transform.flip(self.image, True, False)

    def turn(self):
        """
        Turn the opposite direction
        """
        if self.direction == 1:
            self.move_left()
        else:
            self.move_right()

    def stop(self):
        """
        Stops player movement
        """
        self.direction = 0

    def spawn(self,x,y,hp=HP):
        self.hp = hp
        self.rect.x = x
        self.rect.y = y
        self.alive = True
        self.ammo_count = self.max_ammo
        self.world.add_players([self])

    def attempt_respawn(self):
        if not self.alive:
            self.ticks_until_respawn -= 1
            if self.ticks_until_respawn == 0:
                self.spawn(self.start_x,self.start_y,HP)

    def reload(self,ammo=None):
        # if no argument given, increment by max_ammo
        if not ammo:
            ammo = self.max_ammo
        # add ammo but don't exceed the max
        self.ammo_count += ammo
        if self.ammo_count > self.max_ammo:
            self.ammo_count = self.max_ammo
