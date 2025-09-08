from pplay import window, sprite, gameimage
import pygame
import math
from classes import Player, Enemy
from setup import darkness_setup, get_input, load_background, load_flashlight




win = window.Window(0,0)
win.set_title("Ad Abyssum")
win.set_fullscreen()


background = gameimage.GameImage("assets/cave_bg_tiled.png")



ground = 600


player = Player("assets/player_spritesheet_2frames.png", 2)
player.set_position(400, 500)

enemy = Enemy("assets/enemy.png")
enemy.set_position(600, 500)



def main() -> None:
  
  while True:


    dt = win.delta_time() #time passed between current and last frame
    get_input(dt, win, player)

    


    player.fall(dt)
    player.check_if_grounded(ground)


    enemy.fall(dt)
    enemy.check_if_grounded(ground)


    load_background(win, background)



    Enemy.draw_all()
    Enemy.update_all(dt, player)



    darkness_setup(win, player)
    


    player.check_invisibility(dt)
    

    if player.is_visible:

      player.draw()
    


    win.update()





if __name__ == "__main__":
   
   main()
