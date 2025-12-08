from pplay import window, sprite, gameimage
from classes import Player, Putris, Torch, Block, Menu_Button, Door, Spider, Death, Heart, Start, Moving_Block, Breaking_Block
from setup import darkness_setup, get_input, create_blocks, read_json, change_levels, load_level, check_restart, check_start
import pygame




win = window.Window(1440,810)
win.set_title("Ad Abyssum")
win.get_mouse().hide()
win.mode = "game"
win.level = 13
win.door_cooldown = 0
win.levels = {int(key): value for key, value in read_json("assets/test.json").items()}


background = gameimage.GameImage("assets/sprites/cave_bg_tiled.png")


player = Player("assets/sprites/player_spritesheet.png", 14)
player.set_position(140, 70)
player.heart_sprites[1].set_position(player.heart_sprites[0].width, 0)
player.heart_sprites[2].set_position(player.heart_sprites[0].width * 2, 0)


load_level(win.levels, win, player, "left")


torch = Torch("assets/sprites/torch.png", 14)
torch.set_position(player.x, player.y)


resume = Menu_Button("assets/sprites/resume.png")
exit = Menu_Button("assets/sprites/exit.png")

death = Death("assets/sprites/Die.png")
start = Start("assets/sprites/start_screen.png")

resume.set_position(win.width/2 - resume.width/2, win.height/2 - resume.height/2 - 200)
exit.set_position(win.width/2 - resume.width/2, win.height/2 - resume.height/2 + 200)

pygame.mixer.init()

background_music = pygame.mixer.Sound("assets/sounds/background_music.mp3")
background_music.set_volume(0.4)

game_over_sound = pygame.mixer.Sound("assets/sounds/game_over_sound.mp3")
game_over_sound.set_volume(0.1)


def main() -> None:

    global player, torch, levels, background

    kb = win.get_keyboard()
    dt = min(win.delta_time(), 0.032) #time passed between current and last frame
    get_input(dt, win, player, torch)
    

    background.draw()


    
    change_level = door_side = Door.update_all(player, kb, dt, win)

    

    Spider.update_all(dt, player, win)

    Putris.update_all(dt, player)

    Block.draw_all()

    Heart.update_all(player, win.levels, win)
    
    Breaking_Block.update_break(dt, player)

      
    if bool(change_level):
       
       change_levels(win.levels, win, door_side, player)
       
       if torch.x != player.x and torch.y != player.y:
          torch.set_position(player.x, player.y)   




    Moving_Block.update(dt, player)
    

    player.update(dt, win)

    
    
    torch.update(dt, win, player)

           
    if player.hearts <= 0:
      
      if (not(death.played_music)):     
         
         death.game_over_sound_channel.play(game_over_sound)
         death.played_music = True
         
      player, torch, death.played_music = check_restart(kb, player, torch, win)

    if win.level == 1 and not(start.first):
      start.first = check_start(kb, start)
         

def menu() -> None:
   
    ms = win.get_mouse()
    kb = win.get_keyboard()


    if resume.was_pressed(ms):
       ms.hide()
       win.mode = "game"
    
    if exit.was_pressed(ms):
       win.close()
    
    Menu_Button.draw_all()
       
       
    






if __name__ == "__main__":
   

  background_music.play(loops=-1)


  while True:
    

    win.set_background_color((0,0,0))



    match win.mode:
       
      case "game":
        main()
      
      case "menu":
        menu()

        
    
    win.update()
        

  
