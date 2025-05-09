import pygame
import json
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

        self.player_name = "" # Add this to store the current input
        self.input_active = False # Flag for the input box being active

        # High scores list - will hold tuples of (name, score)
        self.high_scores = []
        self.load_high_scores()  # Load high scores when starting
        
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
                    if event.key == pygame.K_SPACE:                        
                        print(f"New game state: {self.game_state}")
                        if self.check_high_score(self.score):
                            self.game_state = "enter_name"  # Go to name entry instead
                            self.player_name = ""  # Reset player name
                            self.input_active = True
                        else:
                            self.game_state = "high_scores"  # Go straight to high scores
            
            elif self.game_state == "enter_name":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Enter pressed, save the high score and go to high scores
                        self.add_high_score(self.player_name, self.score)
                        self.game_state = "high_scores"
                    elif event.key == pygame.K_BACKSPACE:
                        # Handle backspace - remove last character
                        self.player_name = self.player_name[:-1]
                    else:
                        # Add character to name (limit to reasonable length)
                        if len(self.player_name) < 15:  # Limit name length
                            # Only add printable characters
                            if event.unicode.isprintable():
                                self.player_name += event.unicode

            elif self.game_state == "high_scores":
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
        
        # Prompt to move to High Score screen
        prompt_font = pygame.font.Font(None, 36)
        prompt_text = prompt_font.render("Press SPACE to return", True, (200, 200, 200))
        prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 100))
        self.screen.blit(prompt_text, prompt_rect)
    
        # Draw texts
        self.screen.blit(text, text_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(prompt_text, prompt_rect)
        
        # Update the display
        pygame.display.flip()

    def draw_enter_name(self):
        # Draw the background
        self.screen.fill((0, 0, 0))
        
        # Draw title
        font = pygame.font.Font(None, 74)
        title_text = font.render("New High Score!", True, "white")
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        self.screen.blit(title_text, title_rect)
        
        # Draw score
        score_text = font.render(f"Score: {self.score}", True, "white")
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(score_text, score_rect)
        
        # Draw input box
        input_box = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2, 50)
        pygame.draw.rect(self.screen, "white", input_box, 2)

        # Draw the current input text
        font = pygame.font.Font(None, 32)
        input_text = font.render(self.player_name, True, "white")
        input_rect = input_text.get_rect(center=(input_box.centerx, input_box.centery))
        self.screen.blit(input_text, input_rect)
        
        # Optional: Add instructions
        instruction_font = pygame.font.Font(None, 26)
        instruction_text = instruction_font.render("Type your name and press Enter", True, "white")
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(instruction_text, instruction_rect)

        # Don't forget to update the display
        pygame.display.flip()
    
    def draw_high_scores(self):
        self.screen.fill((0, 0, 0))  # Black background
        
        # Title
        font = pygame.font.Font(None, 74)
        title = font.render("HIGH SCORES", True, (255, 215, 0))  # Gold color
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.screen.blit(title, title_rect)
        
        # Display scores
        score_font = pygame.font.Font(None, 36)
        y_position = 200
        
        for i, (name, score) in enumerate(self.high_scores[:10]):  # Show top 10
            text = score_font.render(f"{i+1}. {name}: {score}", True, (255, 255, 255))
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, y_position))
            self.screen.blit(text, text_rect)
            y_position += 50
        
        # Render "Press R to restart" message
        prompt_font = pygame.font.Font(None, 36)
        prompt_text = prompt_font.render("Press R to Restart or Q to Quit", True, (200, 200, 200))
        prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH//2, 2*SCREEN_HEIGHT//3))

        # Draw texts
        self.screen.blit(text, text_rect)
        self.screen.blit(prompt_text, prompt_rect)

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
        self.create_game_objects()

    def calculate_asteroid_points(self, asteroid):
        if asteroid.radius <= ASTEROID_MIN_RADIUS:
            return 50  # Small asteroids
        elif asteroid.radius < ASTEROID_MAX_RADIUS:
            return 100  # Medium asteroids
        else:
            return 200  # Large asteroids

    def load_high_scores(self):
        try:
            with open("high_scores.json", "r") as file:
                self.high_scores = json.loads(file.read())
        except (FileNotFoundError, json.JSONDecodeError):
            # If file doesn't exist or is invalid, start with empty list
            self.high_scores = []

    def save_high_scores(self):
        with open("high_scores.json", "w") as file:
            json.dump(self.high_scores, file)

    def check_high_score(self, score):
        """Check if current score is a high score"""
        # Don't count 0 as a high score
        if score == 0:
            return False
        
        # If we have fewer than 10 scores, or this score beats the lowest one
        if len(self.high_scores) < 10 or score > self.high_scores[-1][1]:
            return True
        return False

    def add_high_score(self, name, score):
        """Add a new high score to the list"""
        # Don't add a score of 0
        if score == 0:
            return

        self.high_scores.append((name, score))
        # Sort high scores by score value (descending)
        self.high_scores.sort(key=lambda x: x[1], reverse=True)
        # Keep only top 10
        self.high_scores = self.high_scores = self.high_scores[:10]
        self.save_high_scores()
    
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

            elif self.game_state == "enter_name":
                self.draw_enter_name()

            elif self.game_state == "high_scores":
                self.draw_high_scores()

            else: #game_state == "playing"
                # Update game state
                self.update()
                # Draw everything
                self.draw()
            
            # Manage frame rate
            self.dt = self.game_clock.tick(60) / 1000