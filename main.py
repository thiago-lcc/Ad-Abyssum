from pplay import window, sprite, gameimage
from classes import Player, Enemy, Torch, Block, Menu_Button
from setup import darkness_setup, get_input, create_blocks
import pygame




win = window.Window(0,0)
win.set_title("Ad Abyssum")
win.set_fullscreen()
win.mode = "game"


background = gameimage.GameImage("assets/sprites/cave_bg_tiled.png")



player = Player("assets/sprites/player_sprites.png", 6)
player.set_position(400, 500)
player.set_curr_frame(1)
player.heart_sprites[1].set_position(player.heart_sprites[0].width, 0)
player.heart_sprites[2].set_position(player.heart_sprites[0].width * 2, 0)


enemy = Enemy("assets/sprites/enemy.png")
enemy.set_position(800, 500)


torch = Torch("assets/sprites/torch_sprites_5.png", 7)
torch.set_position(player.x, player.y)


resume = Menu_Button("assets/sprites/resume.png")
exit = Menu_Button("assets/sprites/exit.png")

resume.set_position(win.width/2 - resume.width/2, win.height/2 - resume.height/2 - 200)
exit.set_position(win.width/2 - resume.width/2, win.height/2 - resume.height/2 + 200)


create_blocks([(600,win.height-140)], win)



pygame.mixer.init()

background_music = pygame.mixer.Sound("assets/sounds/background_music.mp3")
background_music.set_volume(0.4)



def main() -> None:




    dt = win.delta_time() #time passed between current and last frame
    get_input(dt, win, player, torch)
    

    background.draw()


    Enemy.update_all(dt, player)

    Block.draw_all()



    darkness_setup(win, player, torch)
    

    player.update(dt)

 
    torch.update(dt, win, player)





def menu() -> None:
   
    ms = win.get_mouse()
    kb = win.get_keyboard()


    if resume.was_pressed(ms):
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
        

  
