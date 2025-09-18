import pygame
import math
from classes import Player, Torch
from pplay.window import Window
from pplay.gameimage import GameImage

darkness = pygame.Surface((3000, 3000), pygame.SRCALPHA)




def load_flashlight(player: Player) -> None:
  

    # where the light "spawns" from
    px = player.x + player.width/2 
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








def load_background(win: Window, background: GameImage) -> None:
   

    win.set_background_color((0,0,0))

    background.draw()







def darkness_setup(win: Window, player: Player, torch: Torch) -> None:
  


    darkness.fill((0, 0, 0, 254)) # creates the darkness

    load_flashlight(player)

    if torch.was_thrown: load_torch(torch)

    win.get_screen().blit(darkness, (0, 0))# draws all




def get_input(dt: float, win: Window, player: Player, torch: Torch) -> None:
   

  kb = win.get_keyboard()
  ms = win.get_mouse()

  if player.hearts > 0 and player.knockback_timer == 0:

    if kb.key_pressed("S"):

      player.last_looked = math.pi / 2

      if player.last_looked_x == 'right':
        
        player.set_curr_frame(4)
      
      if player.last_looked_x == 'left':
        
        player.set_curr_frame(5)
    
    

    if kb.key_pressed("W"):

      player.last_looked = 3 * math.pi / 2

      if player.last_looked_x == 'right':
        
        player.set_curr_frame(3)
      
      if player.last_looked_x == 'left':
        
        player.set_curr_frame(2)
    
    

    if kb.key_pressed("A"):

      player.move_left(dt)
      player.set_curr_frame(0)



    if kb.key_pressed("D"):

      player.move_right(dt)
      player.set_curr_frame(1)

    

    if kb.key_pressed("SPACE") and player.is_grounded:

      player.jump(dt)



    if kb.key_pressed("E") and player.is_visible:
      
      player.is_visible = False

      player.invisibilty_timer = 5
    


    if kb.key_pressed("Q") and not torch.was_thrown:
      
        player.throw_torch(torch)



  if kb.key_pressed("ESC"):
     
     win.close()



  
