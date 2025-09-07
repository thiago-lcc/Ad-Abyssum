from pplay import sprite
from math import pi

gravity = 600 #pix/s^2



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

    self.jump_strength = -300

  

  def move_right(self, dt: float) -> None:
    
    
    self.x += self.speed * dt

    self.last_looked = 0.0 #right


  
  def move_left(self, dt: float) -> None:
    

    self.x -= self.speed * dt

    self.last_looked = pi #left



  def jump(self, dt: float) -> None:


    self.vel_y = self.jump_strength
    self.is_grounded = False




