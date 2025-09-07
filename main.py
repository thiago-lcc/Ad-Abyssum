from pplay import window, sprite, gameimage
import pygame
import math
from classes import Player
from setup import darkness_setup, get_input

win = window.Window(0,0)
win.set_title("Ad Abyssum")
win.set_fullscreen()

ground = 600

player = Player("Capturar.PNG")
player.set_position(400, 500)





def main() -> None:

  while True:

    dt = win.delta_time() #time passed between current and last frame
    get_input(dt, win, player)


    player.fall(dt)
    player.check_if_grounded(ground)

    win.set_background_color((100,0,0))


    player.draw()


    darkness_setup(win, player)


    win.update()





if __name__ == "__main__":
   
   main()
