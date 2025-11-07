import pygame
import math
from classes import Player, Torch, Block, Enemy, Door
from pplay.window import Window
from pplay.gameimage import GameImage
import json

darkness = pygame.Surface((3000, 3000), pygame.SRCALPHA)



def read_json(path: str) -> dict:
   
  with open(path, "r") as file:
     
    dictionary = json.load(file)
  
  return dictionary





def create_blocks(blocks: list, win: Window) -> None:
   
  for block in blocks:
     
    x,y = block

    if x < 0:
      x = win.width + x

    if y < 0:
      y = win.height + y


    b = Block("assets/sprites/block.png")
    b.set_position(x, y)
    

  for x in range(0, win.width, 70):
     
     b_top = Block("assets/sprites/block.png")
     b_bottom = Block("assets/sprites/block.png")

     b_top.set_position(x, 0)
     b_bottom.set_position(x, win.height - 70)
  
  for y in range(0, win.height, 70):
     
     b_left = Block("assets/sprites/block.png")
     b_right = Block("assets/sprites/block.png")

     b_left.set_position(0, y)
     b_right.set_position(win.width - 70, y)




def create_enemies(enemies) -> None:
  pass


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
  create_enemies(enemies)
  create_doors(doors, win)

  for door in Door._instances:

    if door.side == player_spawn:

      player.set_position(door.x + 70, door.y)




def change_levels(levels: dict, win: Window, door_side: str, player: Player) -> None:
  
  Door._instances.clear()
  Enemy._instances.clear()
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
    px = player.x + player.width/2 - 5
    py = player.y + player.height/2 - 10



    angle = player.last_looked  # direction the flashlight is pointing. Ex:. 0 = right, pi/2 = up, etc.
    beam_len = 280
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



  
