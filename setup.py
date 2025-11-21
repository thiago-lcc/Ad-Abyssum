import pygame
import math
from classes import Player, Torch, Block, Putris, Door, Spider
from pplay.window import Window
from pplay.gameimage import GameImage
import json
from pplay import gameimage

darkness = pygame.Surface((3000, 3000), pygame.SRCALPHA)



def read_json(path: str) -> dict:
   
  with open(path, "r") as file:
     
    dictionary = json.load(file)
  
  return dictionary





def create_blocks(blocks: list, win: Window) -> None:
   
  for block in blocks:
     
    if block[1] == "single":

      x,y = block[0]

      if x < 0:
        x = win.width + x

      if y < 0:
        y = win.height + y
      

      b = Block("assets/sprites/block.png")
      b.set_position(x, y)
    
    else: 

      start_x, end_x, y = block[0]

      if start_x < 0:
        start_x = win.width + start_x
      
      if end_x < 0:
        end_x = win.width + end_x

      if y < 0:
        y = win.height + y

      for x in range(start_x, end_x, 50):

        b = Block("assets/sprites/block.png")
        b.set_position(x, y)

    

  for x in range(0, win.width, 50):
     
     b_top = Block("assets/sprites/block.png")
     b_bottom = Block("assets/sprites/block.png")

     b_top.set_position(x, 0)
     b_bottom.set_position(x, win.height - 50)
  
  for y in range(0, win.height, 50):
     
     b_left = Block("assets/sprites/block.png")
     b_right = Block("assets/sprites/block.png")

     b_left.set_position(0, y)
     b_right.set_position(win.width - 50, y)




def create_enemies(enemies: list, win: Window) -> None:
  
  for enemy in enemies:

    x,y = enemy[0]

    if x < 0:
      x = win.width + x

    if y < 0:
      y = win.height + y


    if enemy[1] == "putris":

      e = Putris("assets/sprites/enemy.png", 8)
    
    else:

      e = Spider("assets/sprites/spider.png", 31)


    e.set_position(x,y)




def create_doors(doors: list, win: Window) -> None:
  
  for door in doors:

    x,y = door[0]

    if x < 0:
      x = win.width + x

    if y < 0:
      y = win.height + y


    side = door[1]

    d = Door("assets/sprites/door.png", side)
    d.set_position(x,y)




def load_level(levels: dict, win: Window, player: Player, player_spawn: str) -> None:

  blocks = levels[win.level]["blocks"]
  enemies = levels[win.level]["enemies"]
  doors = levels[win.level]["doors"]

  create_blocks(blocks, win)
  create_enemies(enemies, win)
  create_doors(doors, win)

  for door in Door._instances:

    if door.side == player_spawn:

      player.set_position(door.x + 70, door.y)




def change_levels(levels: dict, win: Window, door_side: str, player: Player) -> None:
  
  Door._instances.clear()
  Putris._instances.clear()
  Spider._instances.clear()
  Block._instances.clear()

  player_spawn = ""

  if door_side == "left":
     
    win.level -= 1
    player_spawn = "right"
  
  elif door_side == "right":
    
    levels[win.level]["enemies"] = []
    win.level += 1
    player_spawn = "left"
  
  load_level(levels, win, player, player_spawn)





def load_flashlight(player: Player) -> None:
  

    # where the light "spawns" from
    px = player.x + player.width/2 - 2
    py = player.y + player.height/2 - 10



    angle = player.last_looked  # direction the flashlight is pointing. Ex:. 0 = right, pi/2 = up, etc.
    beam_len = 200
    beam_half_angle = math.radians(30)  # angle from the light coming out of the flashlight



    # every corner of the light beam
    p1 = (px, py)
    p2 = (int(px + math.cos(angle - beam_half_angle) * beam_len),
      int(py + math.sin(angle - beam_half_angle) * beam_len))
    p3 = (int(px + math.cos(angle + beam_half_angle) * beam_len),
      int(py + math.sin(angle + beam_half_angle) * beam_len))
    



    pygame.draw.circle(darkness, (0, 0, 0, 170), (px, py), 50) # creates light circle
    pygame.draw.polygon(darkness, (0, 0, 0, 60), [p1, p2, p3]) # creates light beam





def load_torch(torch: Torch):
   

   tx = torch.x + torch.width/2
   ty = torch.y + torch.height/2

   pygame.draw.circle(darkness, (255, 191, 0, 40), (tx, ty), 110) # creates yellow light circle







def darkness_setup(win: Window, player: Player, torch: Torch) -> None:
  


    darkness.fill((0, 0, 0, 254)) # creates the darkness

    load_flashlight(player)

    if torch.was_thrown: load_torch(torch)

    win.get_screen().blit(darkness, (0, 0))# draws all




def get_input(dt: float, win: Window, player: Player, torch: Torch) -> None:
   
  player.timer = 0
  kb = win.get_keyboard()
  ms = win.get_mouse()
  player.is_moving = False

  if player.hearts > 0 and player.knockback_timer == 0:

    if kb.key_pressed("S"):

      player.last_looked = math.pi / 2

      if player.last_looked_x == 'right':
        
        player.set_curr_frame(6)
      
      if player.last_looked_x == 'left':
        
        player.set_curr_frame(7)
    
    

    if kb.key_pressed("W"):

      player.last_looked = 3 * math.pi / 2

      if player.last_looked_x == 'right':
        
        player.set_curr_frame(5)
      
      if player.last_looked_x == 'left':
        
        player.set_curr_frame(8)
    
    

    if kb.key_pressed("A"):

      player.move_left(dt)
      player.animation_left(dt)



    if kb.key_pressed("D"):

      player.move_right(dt)
      player.animation_right(dt)

    if kb.key_pressed("SPACE") and player.is_grounded:

      player.jump(dt)



    if kb.key_pressed("E") and player.is_visible:
      
      player.is_visible = False

      player.invisibilty_timer = 5
    


    if kb.key_pressed("Q") and not torch.was_thrown:
      
        player.throw_torch(torch)



  if kb.key_pressed("ESC"):
        
        ms.unhide()
        win.mode = "menu"

def restart(win):
    Putris._instances.clear()
    Block._instances.clear()
    Door._instances.clear()
    Spider._instances.clear()

    player = Player("assets/sprites/player_spritesheet.png", 14)
    player.set_position(140, 70)
    player.heart_sprites[1].set_position(player.heart_sprites[0].width, 0)
    player.heart_sprites[2].set_position(player.heart_sprites[0].width * 2, 0)

    torch = Torch("assets/sprites/torch.png", 14)
    torch.set_position(player.x, player.y)

    levels = {int(key): value for key, value in read_json("assets/test.json").items()}

    win.level = 1
    win.door_cooldown = 0

    load_level(levels, win, player, "left")

    return player, torch


    


  
