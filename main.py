from pplay import window, sprite, gameimage
import pygame
import math
from classes import Player

win = window.Window(0,0)
win.set_title("Ad Abyssum")
win.set_fullscreen()



player = Player("Capturar.PNG")
player.set_position(400, 500)


speed = 200 #later put this inside each entity's class




def darkness_setup() -> None:
  
  darkness = pygame.Surface((3000, 3000), pygame.SRCALPHA)

  # where the light "spawns" from
  px = player.x + player.width/2 
  py = player.y + player.height/2 - 50



  angle = player.last_looked  # direction the flashlight is pointing. Ex:. 0 = right, pi/2 = up, etc.
  beam_len = 320
  beam_half_angle = math.radians(30)  # angle from the light coming out of the flashlight


  # every corner of the light beam
  p1 = (px, py)
  p2 = (int(px + math.cos(angle - beam_half_angle) * beam_len),
      int(py + math.sin(angle - beam_half_angle) * beam_len))
  p3 = (int(px + math.cos(angle + beam_half_angle) * beam_len),
      int(py + math.sin(angle + beam_half_angle) * beam_len))



  darkness.fill((0, 0, 0, 220)) # creates the darkness


  pygame.draw.circle(darkness, (0, 0, 0, 0), (px, py), 120) # creates light circle
  pygame.draw.polygon(darkness, (0, 0, 0, 0), [p1, p2, p3]) # creates light beam


  win.get_screen().blit(darkness, (0, 0))# draws all




def get_input(dt) -> None:
   
  kb = win.get_keyboard()

  if kb.key_pressed("A"):
        player.move_left(dt)

  if kb.key_pressed("D"):
        player.move_right(dt)





def main() -> None:

  while True:

    win.set_background_color((100,0,0))


    player.draw()


    dt = win.delta_time() #time passed between current and last frame
    get_input(dt)


    darkness_setup()


    win.update()





if __name__ == "__main__":
   
   main()
