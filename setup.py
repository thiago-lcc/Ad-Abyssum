import pygame
import math


darkness = pygame.Surface((3000, 3000), pygame.SRCALPHA)


def darkness_setup(win, player) -> None:
  

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