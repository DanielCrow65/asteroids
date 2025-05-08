# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
from game import Game

def main():
     pass
     """BEFORE REFACTORING
      print("Starting Asteroids!")
      print(f"Screen width: {SCREEN_WIDTH}")
      print(f"Screen height: {SCREEN_HEIGHT}")
      
      screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
      game_clock = pygame.time.Clock()
      dt = 0
      
      updatable = pygame.sprite.Group()
      drawable = pygame.sprite.Group()
      asteroids = pygame.sprite.Group()
      shots = pygame.sprite.Group()
      Player.containers = (updatable, drawable)
      Asteroid.containers = (asteroids, updatable, drawable)
      AsteroidField.containers = (updatable)
      Shot.containers = (shots, updatable, drawable)

      #this ensures that the player spawns in the middle of the screen
      player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
      asteroid_field = AsteroidField() 

      while True:
          #this ensures that the close button works, because this is otherwise an infinite loop that needs to be terminated
          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    return 
          screen.fill("black")
           
          updatable.update(dt)
           
          #checks if asteroid collides with player
          for asteroid in asteroids:
               if asteroid.collide(player):
                    print("Game over!")
                    sys.exit()
               for shot in shots:
                    if shot.collide(asteroid):
                         shot.kill()
                         asteroid.split()
           
          for d in drawable:
               d.draw(screen)
           
          #this updates the entire display
          pygame.display.flip()
          dt = game_clock.tick(60) / 1000
     """      

if __name__ == "__main__":
    #main() <-- BEFORE REFACTORING
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()
