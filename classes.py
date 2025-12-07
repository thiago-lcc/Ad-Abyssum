from pplay import sprite, window
from math import pi
import pygame


gravity = 1000 #pix/s^2



pygame.mixer.init()

player_walk_sound = pygame.mixer.Sound("assets/sounds/step.mp3")
player_walk_sound.set_volume(0.3)

monster_scream_sound = pygame.mixer.Sound("assets/sounds/monster_scream.wav")
monster_scream_sound.set_volume(0.3)



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





class Death(sprite.Sprite):
  
  _instances = []

  def __init__(self, image_file, frames=1):


    super(Death, self).__init__(image_file, frames)

    self.played_music = False
    
    Death._instances.append(self)
    
  @classmethod
  def draw_game_over(cls) -> None:

    for image in cls._instances:

      image.draw()   

class Start(sprite.Sprite):
  
  _instances = []
  
  def __init__(self, image_file, frames=1):
    
    super(Start, self).__init__(image_file, frames)    
    
    self.first = False
    
    Start._instances.append(self)
  
  @classmethod
  def draw_start(cls) -> None:
    
    for screen in cls._instances:
      
      screen.draw()  


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


  def get_hitbox(self):

      return (
        self.x + self.hitbox_offset_x,
        self.y + self.hitbox_offset_y,
        self.x + self.hitbox_offset_x + self.hitbox_width,
        self.y + self.hitbox_offset_y + self.hitbox_height
    )
  

  def hitbox_collided(self, block):

    left, top, right, bottom = self.get_hitbox()

    b_left   = block.x
    b_top    = block.y
    b_right  = block.x + block.width
    b_bottom = block.y + block.height

    return not (
        right <= b_left or
        left >= b_right or
        bottom <= b_top or
        top >= b_bottom
    )




  def check_block_collisions(self):

    prev_x = getattr(self, "prev_x", self.x)
    prev_y = getattr(self, "prev_y", self.y)

    dx = self.x - prev_x
    dy = self.y - prev_y

    cur_x, cur_y = self.x, self.y

    # Extract hitbox parameters for easy use
    hx = self.hitbox_offset_x
    hy = self.hitbox_offset_y
    hw = self.hitbox_width
    hh = self.hitbox_height

    # ---------- HORIZONTAL ----------
    if dx != 0:
        self.y = prev_y
        collided = None

        for block in Block._instances:
            if self.hitbox_collided(block):
                collided = block
                break

        if collided:
            if dx > 0:
                # align hitbox.right = block.left
                self.x = collided.x - (hx + hw)
            else:
                # align hitbox.left = block.right
                self.x = collided.x + block.width - hx

    self.y = cur_y

    # ---------- VERTICAL ----------
    self.is_grounded = False

    if dy != 0:
        collided = None

        for block in Block._instances:
            if self.hitbox_collided(block):
                collided = block
                break

        if collided:
            if dy > 0:
                # landing
                self.y = collided.y - (hy + hh)
                self.vel_y = 0
                self.is_grounded = True
            else:
                # head bump
                self.y = collided.y + block.height - hy
                self.vel_y = 0

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
    self.time_frame = 0.08
    self.time_counter = 0
    self.actual_frame = 0
    self.torch_collision = 0
    self.last_frame = 13

    self.hitbox_offset_x = 0
    
    self.hitbox_offset_y = 0

    self.hitbox_width  = self.width

    self.hitbox_height = self.height



  def check_hits(self, win: window.Window) -> None:

    for enemy in Putris._instances[:]:

      if self.collided(enemy) and not self.hit_target and self.was_thrown:

        self.speed_x = 0
        self.hit_target = True
        Putris._instances.remove(enemy)
        enemy.scream_sound_channel.play(monster_scream_sound)
      
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


          if self.direction == "right":
            self.actual_frame += 1
        

            if self.actual_frame > self.last_frame:
              self.actual_frame = 0
          

          if self.direction == "left":
                self.actual_frame -= 1


                if self.actual_frame < 0:
                  self.actual_frame = self.last_frame

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


    self.speed = 160

    self.hearts = 3

    self.heart_sprites = [sprite.Sprite("assets/sprites/heart_spritesheet.png",2), sprite.Sprite("assets/sprites/heart_spritesheet.png",2), sprite.Sprite("assets/sprites/heart_spritesheet.png",2)]

    self.last_looked = 0.0 #right

    self.last_looked_x = 'right'

    self.jump_strength = -500

    self.is_visible = True

    self.invisibilty_timer = 0

    self.safety_timer = 0
  
    self.knockback_timer = 0

    self.damage_effect_timer = 0

    self.knockback_direction = 0

    self.is_moving = False

    self.frame_right = 0
    
    self.frame_left = 13
    
    self.counter = 0

    self.walk_channel = pygame.mixer.Channel(1)

    self.hitbox_offset_x = 30
    
    self.hitbox_offset_y = 4

    self.hitbox_width  = self.width - 60

    self.hitbox_height = self.height - 8
    
    self.cooldown = 0





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
    

    if self.invisibilty_timer > 0:

      self.invisibilty_timer -= dt
      


    if self.invisibilty_timer < 0:

      self.invisibilty_timer = 0

      self.is_visible = True
      
      self.cooldown = 30
    
    if self.cooldown > 0:
      
      self.cooldown -= dt  
    
    if self.cooldown <= 0:
      
      self.cooldown = 0
  




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
      
      self.damage_effect_timer += dt


      if self.damage_effect_timer > 0.05:

        self.is_visible = not self.is_visible

        self.damage_effect_timer = 0

    
    elif self.safety_timer < 0:

      self.safety_timer = 0

      self.is_visible = True

      self.damage_effect_timer = 0



  
  def check_knockback(self, dt: float) -> None:

    if self.knockback_timer > 0:

      self.knockback_timer -= dt

      self.x += self.knockback_direction * 200 * dt
      self.y -= 220 * dt

    if self.knockback_timer < 0:

      self.knockback_timer = 0




  def animation_right(self, dt):
      
    self.counter += dt
    
    if self.counter >= 0.25:
        self.frame_right += 1
        self.counter = 0
        if self.frame_right > 4:
              self.frame_right = 0
      
    self.set_curr_frame(self.frame_right)    




  def animation_left(self, dt):
          
    self.counter += dt
    
    if self.counter >= 0.25:
        self.frame_left -= 1
        self.counter = 0
        if self.frame_left < 9:
              self.frame_left = 13
      
    self.set_curr_frame(self.frame_left) 



  def check_void(self, win):
     
    if self.y > win.height:

      f = lambda: Door._instances[0] if Door._instances[0].side == "left" else Door._instances[1]

      door = f()

      self.set_position(door.x, door.y)

      self.safety_timer += 1.5
      
      self.hearts -= 1

      self.heart_sprites[self.hearts].set_curr_frame(1)
      
      


  
  def update(self, dt: float, win: window.Window) -> None:
    
    self.fall(dt)
    self.check_invisibility(dt)

    if self.is_visible:

      self.draw()
    
    self.check_safety(dt)
    self.check_knockback(dt)
    self.draw_hearts()

    self.check_block_collisions()
    self.check_void(win)


    # manages walking sounds

    if self.is_moving and not self.walk_channel.get_busy() and self.is_grounded:

      self.walk_channel.play(player_walk_sound, loops=-1)
    
    elif (not self.is_moving and self.walk_channel.get_busy()):

      self.walk_channel.stop()




class Putris(Entity):

  _instances = [] 



  def __init__(self, image_file, frames=1):


    super(Putris, self).__init__(image_file, frames)


    self.actual_frame_right = 0
    
    self.actual_frame_left = 4
    
    self.set_curr_frame(4)
    
    self.time_frame = 0.3
    
    self.time_counter = 0
    
    self.last_frame_left = 7
    
    self.last_frame_right = 3
    
    self.speed = 100

    self.direction = 1 #1 == right, -1 == left

    self.detection_radius = 400

    self.scream_sound_channel = pygame.mixer.Channel(2)

    self.hitbox_offset_x = 10
    
    self.hitbox_offset_y = 0

    self.hitbox_width  = self.width - 10

    self.hitbox_height = self.height

    Putris._instances.append(self) #every object created is added to the _instances list




  def hit_player(self, player: Player) -> None:
    
    if player.hearts > 0:
      
      player.hearts -= 1

      player.safety_timer += 1.5

      player.heart_sprites[player.hearts].set_curr_frame(1) # Changes the sprite of the heart, to simulate losing one life

      player.knockback_timer = 0.5

      player.knockback_direction = self.direction


  def enemy_animation(self, dt: float, player: Player):
    self.time_counter += dt
        
    if self.direction == -1:
      self.set_curr_frame(self.actual_frame_left)
              
      if self.detection_radius >= abs(self.x - player.x) and self.detection_radius >= abs(self.y - player.y) and player.is_visible:
                
        if self.time_counter >= self.time_frame:
          self.time_counter = 0
          self.actual_frame_left += 1 
                      
          if self.actual_frame_left > self.last_frame_left:
              self.actual_frame_left = 4

              self.set_curr_frame(self.actual_frame_left)

          else:
                self.set_curr_frame(4)
      
    if self.direction == 1:
              
      self.set_curr_frame(self.actual_frame_right)
      if self.detection_radius >= abs(self.x - player.x) and self.detection_radius >= abs(self.y - player.y) and player.is_visible:        

        if self.time_counter >= self.time_frame:
          self.time_counter = 0
          self.actual_frame_right += 1 
                      
                      
          if self.actual_frame_right > self.last_frame_right:
            self.actual_frame_right = 0
                      
            self.set_curr_frame(self.actual_frame_right)
          else:
            self.set_curr_frame(0)
              
              
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
      enemy.enemy_animation(dt, player)
      enemy.draw()




class Door(sprite.Sprite):

  _instances = []

  def __init__(self, image_file, side, frames=1):


    super(Door, self).__init__(image_file, frames)

    Door._instances.append(self)


    self.side = side

  

  def was_used(self, player: Player, kb, win: window.Window) -> bool:

    if self.collided(player) and kb.key_pressed("UP") and win.door_cooldown == 0:
      win.door_cooldown+=0.7
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




class Spider(Entity):
    _instances = []  
    
    def __init__(self, image_file, frames=1):
      super(Spider, self).__init__(image_file, frames)
        
      self.position = 'ceil'
        
      self.counter = 0.0
        
      self.on_ceil = False
        
      self.speed = 300.0

      self.hitbox_offset_x = 0
    
      self.hitbox_offset_y = 0

      self.hitbox_width  = self.width

      self.hitbox_height = self.height

      self.timer_counter = 0
      
      self.timer_frame = 0.1
      
      self.first_right = 16
      
      self.last_right = 22
        
      Spider._instances.append(self)
      
    def change_position(self, player: Player):

      if abs(player.x - self.x) <= 5:  
          self.on_ceil = True


    def update_ceil(self, dt: float):
        if self.position == 'ceil' and self.on_ceil:
            self.counter += dt
            
            if self.counter >= 0.4:
                
                self.position = 'fall'
        else:
            self.counter = 0

    
    def falling(self, dt, player):
        
        if self.position == 'fall':
            self.y += self.speed * dt
            
            if self.y >= player.y + 75:
              self.position = 'ground'
    
    def back(self, dt, player, win):
        
        if self.position == 'ground' and player.is_visible:
            self.x += 300 * dt    
            if self.x == win.width - 100:
              self.position = 'wall'      
    
    
    def hit_player(self, player: Player) -> None:
        
      player.hearts -= 1

      player.safety_timer += 3

      player.heart_sprites[player.hearts].set_curr_frame(1) 


    def update(self, player):
      
      if self.collided(player) and player.safety_timer == 0:
            
        self.hit_player(player)
    
    def animation_spy(self, dt):
        if self.position == 'ground':

          self.timer_counter += dt

          if self.timer_counter >= self.timer_frame:
            self.timer_counter = 0
            self.first_right += 1

            if self.first_right > self.last_right:
                self.first_right = 16

        self.set_curr_frame(self.first_right)  
        
    @classmethod
    def update_all(cls, dt, player, win):
        
        for spider in cls._instances:
            spider.change_position(player)
            spider.update_ceil(dt)
            spider.falling(dt, player)
            spider.back(dt, player, win)
            spider.update(player)
            spider.animation_spy(dt)
            spider.draw()


        
class Heart(sprite.Sprite):
    _instances = []

    def __init__(self, image_file, frames=1):
      super(Heart, self).__init__(image_file, frames)

      Heart._instances.append(self)
    

    def check_if_used(self, player: Player) -> bool:
       
      if self.collided(player) and player.hearts < 3:
        
        player.heart_sprites[player.hearts].set_curr_frame(0)
        player.hearts += 1
        return True
      
      elif self.collided(player):

        return True

      return False
    

    @classmethod
    def update_all(cls, player: Player, levels: dict, win: window.Window):
       
      for heart in Heart._instances[:]:
         
        heart.draw()

        if heart.check_if_used(player):
          Heart._instances.remove(heart)
          levels[win.level]["heart"] = []

      
        

    
      

















