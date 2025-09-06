from pplay import window, sprite, gameimage
import pygame
import math
from classes import Player
from setup import darkness_setup

win = window.Window(0,0)
win.set_title("Ad Abyssum")
win.set_fullscreen()

ground = 600

player = Player("Capturar.PNG")
player.set_position(400, 500)



def get_input(dt: float) -> None:
   

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









def main() -> None:

  while True:

    dt = win.delta_time() #time passed between current and last frame
    get_input(dt)


    player.fall(dt)
    player.check_if_grounded(ground)

    win.set_background_color((100,0,0))


    player.draw()


    darkness_setup(win, player)


    win.update()





if __name__ == "__main__":
   
   main()
