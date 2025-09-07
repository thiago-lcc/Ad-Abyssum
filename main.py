from pplay import window, sprite, gameimage
import pygame
import math
from classes import Player
from setup import environment_setup, get_input




win = window.Window(0,0)
win.set_title("Ad Abyssum")
win.set_fullscreen()


background = gameimage.GameImage("cave_bg_tiled.png")


ground = 600


player = Player("sprite_1.png")
player.set_position(400, 500)





def main() -> None:

  while True:


    dt = win.delta_time() #time passed between current and last frame
    get_input(dt, win, player)


    player.fall(dt)
    player.check_if_grounded(ground)


    environment_setup(win, player, background)


    player.set_curr_frame(0)
    player.draw()


    win.update()





if __name__ == "__main__":
   
   main()
