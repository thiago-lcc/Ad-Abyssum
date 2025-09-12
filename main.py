from pplay import window, sprite, gameimage
import pygame
import math
from classes import Player, Enemy, Torch
from setup import darkness_setup, get_input, load_background




win = window.Window(0,0)
win.set_title("Ad Abyssum")
win.set_fullscreen()


background = gameimage.GameImage("assets/cave_bg_tiled.png")



ground = 600


player = Player("assets/player_sprites.png", 6)
player.set_position(400, 500)
player.set_curr_frame(1)


enemy = Enemy("assets/enemy.png")
enemy.set_position(600, 500)


torch = Torch("assets/torch.png")
torch.set_position(player.x, player.y)



def main() -> None:
  
  while True:


    dt = win.delta_time() #time passed between current and last frame
    get_input(dt, win, player, torch)
    


    player.fall(dt)
    player.check_if_grounded(ground)


    enemy.fall(dt)
    enemy.check_if_grounded(ground)


    load_background(win, background)



    Enemy.update_all(dt, player)



    darkness_setup(win, player, torch)
    


    player.check_invisibility(dt)
    

    if player.is_visible:

      player.draw()
    


    if torch.was_thrown:

      torch.draw()
    
    if torch.was_thrown and torch.hit_target and torch.collided(player):

      torch.was_thrown = False
      torch.hit_target = False
    
    torch.update(dt, win)




    win.update()





if __name__ == "__main__":
   
   main()
