from pplay import sprite
from math import pi

gravity = 1000 #pix/s^2



class Entity(sprite.Sprite):

  def __init__(self, image_file, frames=1):
        

    super(Entity, self).__init__(image_file, frames)


    self.is_grounded = True

    self.vel_y = 0



  def fall(self, dt: float) -> None:

    if not self.is_grounded:

      self.vel_y += gravity * dt

      self.y += self.vel_y * dt



  def check_if_grounded(self, ground) -> None:

    if self.y >= ground:

      self.is_grounded = True
      self.vel_y = 0

    else:

      self.is_grounded = False





class Player(Entity):

  def __init__(self, image_file, frames=1):
        

    super(Player, self).__init__(image_file, frames)


    self.speed = 200

    self.hearts = 3

    self.last_looked = 0.0 #right

    self.last_looked_x = 'right'

    self.jump_strength = -400

    self.is_visible = True

    self.invisibilty_timer = 0

  

  def move_right(self, dt: float) -> None:
    
    
    self.x += self.speed * dt

    self.last_looked = 0.0 #right

    self.last_looked_x = 'right'


  
  def move_left(self, dt: float) -> None:
    

    self.x -= self.speed * dt

    self.last_looked = pi #left

    self.last_looked_x = 'left'



  def jump(self, dt: float) -> None:


    self.vel_y = self.jump_strength
    self.is_grounded = False

  

  def check_invisibility(self, dt: float) -> None:


    if not self.is_visible:

      self.invisibilty_timer -= dt


    if self.invisibilty_timer < 0:

      self.invisibilty_timer = 0

      self.is_visible = True






class Enemy(Entity):

  _instances = [] 

  def __init__(self, image_file, frames=1):


    super(Enemy, self).__init__(image_file, frames)


    self.speed = 100

    self.direction = 1 #1 == right, -1 == left

    self.detection_radius = 400

    Enemy._instances.append(self) #every object created is added to the _instances list



  
  def update(self, dt: float, player: Player) -> None:


    if self.x + self.width/2 > player.x + player.width/2:

      self.direction = -1
    
    elif self.x + self.width/2 < player.x + player.width/2:

      self.direction = 1
    


    if self.detection_radius >= abs(self.x - player.x) and player.is_visible:

      self.move_x(self.speed * self.direction * dt)

  
  @classmethod
  def update_all(cls, dt, player):

    for object in cls._instances:

      object.update(dt, player)



  @classmethod
  def draw_all(cls):

    for object in cls._instances:

      object.draw()
    
















