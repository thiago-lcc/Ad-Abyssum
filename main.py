from pplay import window, sprite, gameimage
import pygame
import math


win = window.Window(0,0)
win.set_title("Ad Abyssum")
win.set_fullscreen()


darkness = pygame.Surface((3000, 3000), pygame.SRCALPHA)


player = sprite.Sprite("Capturar.PNG")
player.set_position(400, 500)


speed = 200 #later put this inside each entity's class




def darkness_setup() -> None:
   
  darkness.fill((0, 0, 0, 220)) #creates the darkness

  pygame.draw.circle(darkness, (0, 0, 0, 0), (player.x + player.width/2, player.y + player.height/2), 120) #creates the "light"

  win.get_screen().blit(darkness, (0, 0))#draws both




def get_input(dt) -> None:
   
  kb = win.get_keyboard()

  if kb.key_pressed("A"):
        player.x -= speed * dt

  if kb.key_pressed("D"):
        player.x += speed * dt





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
