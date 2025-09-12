from pplay import sprite, window
from math import pi


ground = 600
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






class Torch(sprite.Sprite):

  def __init__(self, image_file, frames=1):

    super(Torch, self).__init__(image_file, frames)


    self.was_thrown = False
    self.hit_target = False
    self.speed_x = 0
    self.speed_y = 0
    self.direction = 'right'
  


  def check_hits(self, win: window.Window) -> None:

    for enemy in Enemy._instances:

      if self.collided(enemy):

        self.speed_x = 0
        self.hit_target = True
      
    if self.x >= win.width or self.x <= 0:

      self.speed_x = 0
      self.hit_target = True

  
  def update(self, dt: float, win: window.Window) -> None:

    self.check_hits(win)

    if self.was_thrown and not self.hit_target:

      self.speed_x = 400

      if self.direction == 'left':
        self.speed_x *= -1


    
    if self.hit_target:

      self.speed_y += gravity

    
    if self.y >= ground - self.height:

      self.y = ground - self.height
      self.speed_y = 0


    
    self.move_x(self.speed_x * dt)
    self.move_y(self.speed_y * dt)





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
  

  def throw_torch(self, torch: Torch):

    torch.was_thrown = True
    torch.set_position(self.x, self.y)
    torch.direction = self.last_looked_x






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
      object.draw()













