from pplay import sprite, window
from math import pi
import pygame


gravity = 1000 #pix/s^2



pygame.mixer.init()

player_walk_sound = pygame.mixer.Sound("assets/sounds/step.mp3")
player_walk_sound.set_volume(0.3)


class Menu_Button(sprite.Sprite):


  _instances = []

  def __init__(self, image_file, frames=1):


    super(Menu_Button, self).__init__(image_file, frames)

    Menu_Button._instances.append(self)
  


  def was_pressed(self, ms) -> bool:

    return ms.is_over_object(self) and ms.is_button_pressed(1)
  


  @classmethod
  def draw_all(cls) -> None:

    for button in cls._instances:

      button.draw()





class Block(sprite.Sprite):

  _instances = []



  def __init__(self, image_file, frames=1):


    super(Block, self).__init__(image_file, frames)

    Block._instances.append(self)
  



  @classmethod
  def draw_all(cls) -> None:

    for block in cls._instances:

      block.draw()





class Entity(sprite.Sprite):

  def __init__(self, image_file, frames=1):
        

    super(Entity, self).__init__(image_file, frames)


    self.is_grounded = False

    self.vel_y = 0





  def fall(self, dt: float) -> None:

    if not self.is_grounded:

      self.vel_y += gravity * dt

      self.y += self.vel_y * dt





  def check_block_collisions(self) -> None:
    
    
   ### must be called AFTER movement ###


    # previous position fallback (first frame)
    prev_x = getattr(self, "prev_x", self.x)
    prev_y = getattr(self, "prev_y", self.y)

    dx = self.x - prev_x
    dy = self.y - prev_y

    # Save current coords
    cur_x, cur_y = self.x, self.y

    # ---------- HORIZONTAL resolution ----------
    if dx != 0:
      # Temporarily test horizontal movement at previous vertical position
      self.y = prev_y
      collided_block = None
      for block in Block._instances:
        if self.collided(block):
          collided_block = block
          break

      if collided_block:
        if dx > 0:
          # moved right into block -> snap to its left
          self.x = collided_block.x - self.width
        else:
          # moved left into block -> snap to its right
          self.x = collided_block.x + collided_block.width

    # restore vertical position after horizontal resolution
    # but keep the resolved self.x
    self.y = cur_y

    # ---------- VERTICAL resolution ----------
    # reset grounded assumption; we'll set True if we land on something
    self.is_grounded = False

    if dy != 0:
      collided_block = None
      for block in Block._instances:
        if self.collided(block):
          collided_block = block
          break

      if collided_block:
        if dy > 0:
          # moved down -> land on top of block
          self.y = collided_block.y - self.height
          self.vel_y = 0
          self.is_grounded = True
        else:
          # moved up -> hit head on underside
          self.y = collided_block.y + collided_block.height
          self.vel_y = 0

    # store prev position for next frame
    self.prev_x = self.x
    self.prev_y = self.y






class Torch(Entity):

  def __init__(self, image_file, frames=1):

    super(Torch, self).__init__(image_file, frames)


    self.was_thrown = False
    self.hit_target = False
    self.speed_x = 0
    self.speed_y = 0
    self.direction = 'right'
    self.frame_torch = 0
    self.actual_frame = self.frame_torch
    self.set_curr_frame(self.actual_frame)
    self.time_frame = 0.3
    self.time_counter = 0
    self.actual_frame = 0
    self.torch_collision = 0
    self.last_frame = 6



  def check_hits(self, win: window.Window) -> None:

    for enemy in Enemy._instances:

      if self.collided(enemy):

        self.speed_x = 0
        self.hit_target = True
      
    for block in Block._instances:

      if self.collided(block):

        self.speed_x = 0
        self.hit_target = True

  def animation_torch(self, dt):

    if self.hit_target:
        
      self.set_curr_frame(self.torch_collision) 
      return 
    
    if self.was_thrown:
      
      self.time_counter += dt
      
      if self.time_counter >= self.time_frame:

          self.time_counter = 0
          self.actual_frame += 1
        
          if self.was_thrown:

            self.actual_frame += 1

            if self.actual_frame > self.last_frame:
              self.actual_frame = 0

            self.set_curr_frame(self.actual_frame)
    
  def update(self, dt: float, win: window.Window, player) -> None:

    if self.was_thrown:

      self.draw()
    

    if self.was_thrown and self.hit_target and self.collided(player):

      self.was_thrown = False
      self.hit_target = False


    self.check_hits(win)

    if self.was_thrown and not self.hit_target:

      self.speed_x = 400

      if self.direction == 'left':
        self.speed_x *= -1


    self.check_block_collisions()

    if self.hit_target:

      self.fall(dt)

    
    
    self.move_x(self.speed_x * dt)
    self.move_y(self.speed_y * dt)

    self.animation_torch(dt)




class Player(Entity):

  def __init__(self, image_file, frames=1):
        

    super(Player, self).__init__(image_file, frames)


    self.speed = 200

    self.hearts = 3

    self.heart_sprites = [sprite.Sprite("assets/sprites/heart_spritesheet.png",2), sprite.Sprite("assets/sprites/heart_spritesheet.png",2), sprite.Sprite("assets/sprites/heart_spritesheet.png",2)]

    self.last_looked = 0.0 #right

    self.last_looked_x = 'right'

    self.jump_strength = -400

    self.is_visible = True

    self.invisibilty_timer = 0

    self.safety_timer = 0
  
    self.knockback_timer = 0

    self.knockback_direction = 0

    self.is_moving = False


    self.walk_channel = pygame.mixer.Channel(1)





  def move_right(self, dt: float) -> None:
    
    
    self.x += self.speed * dt

    self.last_looked = 0.0 #right

    self.last_looked_x = 'right'

    self.is_moving = True




  
  def move_left(self, dt: float) -> None:
    

    self.x -= self.speed * dt

    self.last_looked = pi #left

    self.last_looked_x = 'left'

    self.is_moving = True





  def jump(self, dt: float) -> None:


    self.vel_y = self.jump_strength
    self.is_grounded = False

    self.walk_channel.stop()

  



  def check_invisibility(self, dt: float) -> None:


    if not self.is_visible:

      self.invisibilty_timer -= dt


    if self.invisibilty_timer < 0:

      self.invisibilty_timer = 0

      self.is_visible = True
  




  def throw_torch(self, torch: Torch) -> None:

    torch.was_thrown = True
    torch.set_position(self.x, self.y)
    torch.direction = self.last_looked_x





  def draw_hearts(self) -> None:
    
    for heart in self.heart_sprites:

      heart.draw()





  def check_safety(self, dt: float) -> None:

    if self.safety_timer > 0:

      self.safety_timer -= dt
    
    elif self.safety_timer < 0:

      self.safety_timer = 0




  
  def check_knockback(self, dt: float) -> None:

    if self.knockback_timer > 0:

      self.knockback_timer -= dt

      self.x += self.knockback_direction * 200 * dt
      self.y -= 220 * dt

    if self.knockback_timer < 0:

      self.knockback_timer = 0




  
  def update(self, dt: float) -> None:
    
    self.fall(dt)
    self.check_invisibility(dt)

    if self.is_visible:

      self.draw()
    
    self.check_safety(dt)
    self.check_knockback(dt)
    self.draw_hearts()

    self.check_block_collisions()


    # manages walking sounds

    if self.is_moving and not self.walk_channel.get_busy() and self.is_grounded:

      self.walk_channel.play(player_walk_sound, loops=-1)
    
    elif (not self.is_moving and self.walk_channel.get_busy()):

      self.walk_channel.stop()




class Enemy(Entity):

  _instances = [] 



  def __init__(self, image_file, frames=1):


    super(Enemy, self).__init__(image_file, frames)


    self.speed = 100

    self.direction = 1 #1 == right, -1 == left

    self.detection_radius = 400

    Enemy._instances.append(self) #every object created is added to the _instances list





  def hit_player(self, player: Player) -> None:
    
    player.hearts -= 1

    player.safety_timer += 3

    player.heart_sprites[player.hearts].set_curr_frame(1) # Changes the sprite of the heart, to simulate losing one life

    player.knockback_timer = 0.5

    player.knockback_direction = self.direction





  
  def update(self, dt: float, player: Player) -> None:


    if self.x + self.width/2 > player.x + player.width/2:

      self.direction = -1
    
    elif self.x + self.width/2 < player.x + player.width/2:

      self.direction = 1
    

    if self.detection_radius >= abs(self.x - player.x) and self.detection_radius >= abs(self.y - player.y) and player.is_visible:

      self.move_x(self.speed * self.direction * dt)


    if self.collided(player) and player.safety_timer == 0:
      
      self.hit_player(player)





  @classmethod
  def update_all(cls, dt, player) -> None:

    for enemy in cls._instances:

      enemy.update(dt, player)
      enemy.fall(dt)
      enemy.check_block_collisions()
      enemy.draw()




class Door(sprite.Sprite):

  _instances = []

  def __init__(self, image_file, side, frames=1):


    super(Door, self).__init__(image_file, frames)

    Door._instances.append(self)


    self.side = side

  

  def was_used(self, player: Player, kb, win: window.Window) -> bool:

    if self.collided(player) and kb.key_pressed("UP") and win.door_cooldown == 0:
      win.door_cooldown+=0.2
      return True
    
    return False
  
  
  def manage_cooldown(self, win: window.Window, dt: float):

    if win.door_cooldown > 0:
      win.door_cooldown -= dt
    
    elif win.door_cooldown < 0:
      win.door_cooldown = 0


  @classmethod
  def update_all(cls, player:Player, kb, dt: float, win: window.Window) -> str:
    
    return_statement = ""

    for door in cls._instances:

      door.manage_cooldown(win, dt)

      door.draw()

      if door.was_used(player, kb, win):
        return_statement = door.side
    
    return return_statement




  


      

















