import pygame
import math
from classes import Player
from pplay.window import Window
from pplay.gameimage import GameImage

darkness = pygame.Surface((3000, 3000), pygame.SRCALPHA)




def load_flashlight(player: Player) -> None:
  

    # where the light "spawns" from
    px = player.x + player.width/2 
    py = player.y + player.height/2 - 10



    angle = player.last_looked  # direction the flashlight is pointing. Ex:. 0 = right, pi/2 = up, etc.
    beam_len = 320
    beam_half_angle = math.radians(30)  # angle from the light coming out of the flashlight



    # every corner of the light beam
    p1 = (px, py)
    p2 = (int(px + math.cos(angle - beam_half_angle) * beam_len),
      int(py + math.sin(angle - beam_half_angle) * beam_len))
    p3 = (int(px + math.cos(angle + beam_half_angle) * beam_len),
      int(py + math.sin(angle + beam_half_angle) * beam_len))
    



    pygame.draw.circle(darkness, (0, 0, 0, 0), (px, py), 50) # creates light circle
    pygame.draw.polygon(darkness, (0, 0, 0, 0), [p1, p2, p3]) # creates light beam






def load_background(win: Window, background: GameImage) -> None:
   

    win.set_background_color((0,0,0))

    background.draw()







def environment_setup(win: Window, player: Player, background: GameImage) -> None:
  


    darkness.fill((0, 0, 0, 254)) # creates the darkness


    load_flashlight(player)

    load_background(win, background)


    win.get_screen().blit(darkness, (0, 0))# draws all




def get_input(dt: float, win: Window, player: Player) -> None:
   

  kb = win.get_keyboard()


  if kb.key_pressed("S"):

    player.last_looked = math.pi / 2
  
  
  if kb.key_pressed("W"):

    player.last_looked = 3 * math.pi / 2
  
  
  if kb.key_pressed("A"):

    player.move_left(dt)


  if kb.key_pressed("D"):

    player.move_right(dt)

  
  if kb.key_pressed("SPACE") and player.is_grounded:

    player.jump(dt)




