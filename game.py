import pygame
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
        self.game_state = "title_screen"
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
            # Check for key presses on title screen
            if self.game_state == "title_screen":
                if event.type == pygame.KEYDOWN:
                    self.game_state = "playing"  # Change state to playing
            
            # Check for key presses on game over screen
            elif self.game_state == "game_over":
                if event.type == pygame.KEYDOWN: # It does nothing if any other key is pressed
                    if event.key == pygame.K_r:
                        # Reset game state and objects for a new game
                        self.reset_game()
                        self.game_state = "playing"  # Go directly to playing
                    elif event.key == pygame.K_q:
                        return False  # Quit the game
                    
                    # Without the pygame.KEYDOWN check, pressing anything other than R or Q in the game over screen crashes
                       
            else: # When the game is in the 'playing' state. Might change if I add more game states
                pass

        # Ensures the game keeps running unless QUIT event is triggered
        return True
    
    def draw_title_screen(self):
        # Clear the screen
        self.screen.fill((0, 0, 0))  # Black background
        
        # Render title
        title_font = pygame.font.Font(None, 74)
        title_text = title_font.render("ASTEROIDS", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
        
        # Render "Press any key" message
        prompt_font = pygame.font.Font(None, 36)
        prompt_text = prompt_font.render("Press Any Key to Start", True, (200, 200, 200))
        prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH//2, 2*SCREEN_HEIGHT//3))
        
        # Draw texts
        self.screen.blit(title_text, title_rect)
        self.screen.blit(prompt_text, prompt_rect)
        
        # Update the display
        pygame.display.flip()
    
    def draw_game_over(self):
        self.screen.fill((0, 0, 0))  # Black background
        
        # Render "Game Over" message
        font = pygame.font.Font(None, 74)
        text = font.render("GAME OVER", True, (255, 0, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
        
        # Render score
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(f"Final Score: {self.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        
        # Render "Press R to restart" message
        prompt_font = pygame.font.Font(None, 36)
        prompt_text = prompt_font.render("Press R to Restart or Q to Quit", True, (200, 200, 200))
        prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH//2, 2*SCREEN_HEIGHT//3))
    
        # Draw texts
        self.screen.blit(text, text_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(prompt_text, prompt_rect)
        
        # Update the display
        pygame.display.flip()
    
    def reset_game(self):
        # Reset score
        self.score = 0
        
        # Clear all sprite groups
        self.updatable.empty()
        self.drawable.empty()
        self.asteroids.empty()
        self.shots.empty()
        
        # Recreate player and asteroid field
        self.player = Player(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        self.asteroid_field = AsteroidField()

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
                self.game_state = "game_over"
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
            
            if self.game_state == "title_screen":
                self.draw_title_screen()

            elif self.game_state == "game_over":
                self.draw_game_over()

            else: #game_state == "playing"
                # Update game state
                self.update()
                # Draw everything
                self.draw()
            
            # Manage frame rate
            self.dt = self.game_clock.tick(60) / 1000