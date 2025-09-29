from pplay import window, sprite, gameimage
from classes import Player, Enemy, Torch, Block
from setup import darkness_setup, get_input, load_background, create_blocks




win = window.Window(0,0)
win.set_title("Ad Abyssum")
win.set_fullscreen()


background = gameimage.GameImage("assets/sprites/cave_bg_tiled.png")



player = Player("assets/sprites/player_sprites.png", 6)
player.set_position(400, 500)
player.set_curr_frame(1)
player.heart_sprites[1].set_position(player.heart_sprites[0].width, 0)
player.heart_sprites[2].set_position(player.heart_sprites[0].width * 2, 0)


enemy = Enemy("assets/sprites/enemy.png")
enemy.set_position(800, 500)


torch = Torch("assets/sprites/torch.png")
torch.set_position(player.x, player.y)


create_blocks([(600,win.height-140)], win)



def main() -> None:
  
  while True:


    dt = win.delta_time() #time passed between current and last frame
    get_input(dt, win, player, torch)
    

    load_background(win, background)



    Enemy.update_all(dt, player)

    Block.draw_all()



    darkness_setup(win, player, torch)
    

    player.update(dt)

 
    torch.update(dt, win, player)




    win.update()





if __name__ == "__main__":
   
   main()
