from pplay import sprite
from math import pi


class Player(sprite.Sprite):

  def __init__(self, image_file, frames=1):
        

    super(Player, self).__init__(image_file, frames)


    self.speed = 200

    self.hearts = 3

    self.last_looked = 0.0 #right

  

  def move_right(self, dt) -> None:

    self.x += self.speed * dt

    self.last_looked = 0.0 #right


  
  def move_left(self, dt) -> None:

    self.x -= self.speed * dt

    self.last_looked = pi #left




