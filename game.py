import pygame
import sys
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shots import Shot

class Game:
    def __init__(self):
        print("Starting Asteroids!")
        print(f"Screen width: {SCREEN_WIDTH}")
        print(f"Screen height: {SCREEN_HEIGHT}")
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.game_clock = pygame.time.Clock()
        self.dt = 0
        self.score = 0
        
        self.setup_sprite_groups()
        self.create_game_objects()
        
    def setup_sprite_groups(self):
        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()
        
        Player.containers = (self.updatable, self.drawable)
        Asteroid.containers = (self.asteroids, self.updatable, self.drawable)
        AsteroidField.containers = (self.updatable)
        Shot.containers = (self.shots, self.updatable, self.drawable)
    
    def create_game_objects(self):
        self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.asteroid_field = AsteroidField()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True
    
    def calculate_asteroid_points(self, asteroid):
        if asteroid.radius <= ASTEROID_MIN_RADIUS:
            return 50  # Small asteroids
        elif asteroid.radius < ASTEROID_MAX_RADIUS:
            return 100  # Medium asteroids
        else:
            return 200  # Large asteroids

    def update(self):
        self.updatable.update(self.dt)
        
        # Check collisions
        for asteroid in self.asteroids:
            if asteroid.collide(self.player):
                print("Game over!")
                sys.exit()
            for shot in self.shots:
                if shot.collide(asteroid):
                    self.score += self.calculate_asteroid_points(asteroid)                    
                    shot.kill()
                    asteroid.split()
    
    def draw(self):
        self.screen.fill("black")
        
        # Draw all game objects
        for d in self.drawable:
               d.draw(self.screen)
               
        # Draw score
        self.draw_score()
        
        # Update display
        pygame.display.flip()

    def draw_score(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def run(self):
        while True:
            # Handle events
            if not self.handle_events():
                return
            
            # Update game state
            self.update()
            
            # Draw everything
            self.draw()
            
            # Manage frame rate
            self.dt = self.game_clock.tick(60) / 1000