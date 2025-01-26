import pygame
import sys
import os
import random
from player import Player
from sprites import *
from mobs import *


class Game:
    def __init__(self):
        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'  # This centers the window if it's windowed


        # Adjust the screen size to a smaller windowed mode
        self.game_width = 800  # Smaller width for windowed mode
        self.game_height = 600  # Smaller height for windowed mode
        self.fullscreen = False  # Set fullscreen to False initially


        # Initialize screen in windowed mode with the smaller size
        self.screen = pygame.display.set_mode((self.game_width, self.game_height), pygame.RESIZABLE)


        pygame.display.set_caption("Cropocalypse")
        pygame.display.set_icon(pygame.image.load(r"assets/icon.jpg"))
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0


        # Cursor
        self.cursor = pygame.image.load(r"assets/cursor.png").convert_alpha()
        pygame.mouse.set_visible(False)


        # Load images
        self.load_images()


        # Groups to hold sprites
        self.all_sprites = pygame.sprite.Group()
        self.arrow_sprites = pygame.sprite.Group()
        self.mob_sprites = pygame.sprite.Group()


        # Play button (centered dynamically based on the screen mode)
        self.update_play_button_position()


        # Game State
        self.game_state = "menu"  # Can be "menu" or "game"


        # Sprites
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()


        # Load and scale the map image
        self.map_image = pygame.image.load(r"assets/mapril.png").convert_alpha()
        self.map_image = pygame.transform.scale(self.map_image, (self.game_width, self.screen_height))
        self.map_width, self.map_height = self.map_image.get_size()


        # Center of the map
        self.map_center_x = self.map_width // 2
        self.map_center_y = self.map_height // 2


        # Initialize player at the center of the map
        self.player = Player((self.screen_width / 2, self.screen_height / 2), self.all_sprites)
        self.center_player()  # Center the player on the screen


        # Reload Arrow
        self.can_shoot = True
        self.shoot_time = 0
        self.bow_cooldown = 300  # Cooldown in milliseconds


        # Enemy spawn timer
        self.enemy_spawn_time = 0
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_counter = 0


        self.pause_button = None  # To store the pause button
        self.is_paused = False    # Game pause state
        self.pause_bg = pygame.image.load(r"assets/pause_bg.png").convert_alpha()  # Load pause background
        self.pause_bg = pygame.transform.scale(self.pause_bg, (self.game_width, self.game_height))  # Scale it


        self.quit_button_image = pygame.image.load(r"assets/quit_button.png").convert_alpha()
       
        # Delay
        self.game_started = False
        self.start_time = None
        self.spawn_delay = 5000
        # Set up initial game objects


        # Inside __init__ method
        self.show_endless_text = False  # To control the "ENDLESS APOCALYPSE" text display
        self.text_display_time = 0  # To track the time for displaying the text


        self.show_intro_text = True


        self.setup()
       
    def center_player(self):
        """Reposition the player in the center of the screen."""
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        self.player.rect.center = (self.screen_width / 2, self.screen_height / 2)


    def load_images(self):
        """Load all the images for the game."""
        self.arrow_surf = pygame.image.load(r"assets/arrow.png").convert_alpha()
        self.background_image = pygame.image.load(r"assets/cover_2.jpg").convert_alpha()  # Menu background
        self.game_background_image = pygame.image.load(r"assets/bg_image.png").convert_alpha()  # Game background
        self.map_image = pygame.image.load(r"assets/mapril.png").convert_alpha()  # Original map
        self.border_map_image = pygame.image.load(r"assets/border.jpg").convert_alpha()  # New border map image
        self.chars_image = pygame.image.load(r"assets/player.png").convert_alpha()
        self.resume_button_image = pygame.image.load(r"assets/resume_button.png").convert_alpha()  # Load resume button


    def spawn_chars(self):
        """Spawn the chars.png sprite in the middle of the mapril.png."""
        # Calculate the center position of mapril.png
        map_center_x = self.center_x + self.game_width // 2
        map_center_y = self.center_y + self.screen_height // 2


        # Create the sprite
        chars_sprite = pygame.sprite.Sprite()
        chars_sprite.image = pygame.transform.scale(self.chars_image, (50, 50))  # Resize if necessary
        chars_sprite.rect = chars_sprite.image.get_rect(center=(map_center_x, map_center_y))


        # Add to sprite group
        self.all_sprites.add(chars_sprite)


    def input(self):
        """Handle shooting of arrows."""
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            # Get the position and direction for the arrow
            mouse_x, mouse_y = pygame.mouse.get_pos()
            rel_x, rel_y = mouse_x - self.player.rect.centerx, mouse_y - self.player.rect.centery
            direction = pygame.Vector2(rel_x, rel_y).normalize()


            # Create the arrow object
            Arrow(self.player.rect.center, direction, 10, self.all_sprites)


            # Reset shoot cooldown
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    self.toggle_fullscreen()
            if self.pause_button and self.pause_button.is_hovered() and pygame.mouse.get_pressed()[0]:
                self.is_paused = not self.is_paused  # Toggle pause state


            # Handle quit button click while paused
            if self.is_paused:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                quit_button_width, quit_button_height = 250, 300
                quit_button_x = (self.screen_width - quit_button_width) // 2
                quit_button_y = self.screen_height // 2 + 100  # Place it below the pause background
                quit_button_rect = pygame.Rect(quit_button_x, quit_button_y, quit_button_width, quit_button_height)
               
                if quit_button_rect.collidepoint(mouse_x, mouse_y) and pygame.mouse.get_pressed()[0]:
                    self.running = False  # Exit the game when quit button is clicked

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                        # Check if any mob is clicked
                    for mob in self.mob_sprites:
                        if mob.rect.collidepoint(mouse_x, mouse_y):
                            mob.take_damage()
                            break
                    
    def draw_pause_screen(self):
        """Draw a pause background image and show the cursor when hovered over it."""
        screen_width, screen_height = pygame.display.get_surface().get_size()


        # Scale the pause background to 40% of screen width and 99% of screen height
        scaled_width = int(screen_width * 0.3)
        scaled_height = int(screen_height * 0.89)
        scaled_pause_bg = pygame.transform.scale(self.pause_bg, (scaled_width, scaled_height))


        # Calculate the position to center the scaled pause background and move it slightly downward
        pause_x = (screen_width - scaled_width) // 2
        pause_y = ((screen_height - scaled_height) // 2) + int(screen_height * 0.05)


        # Draw the scaled pause background image
        self.screen.blit(scaled_pause_bg, (pause_x, pause_y))


        # Get the mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()


        # Check if the mouse is over the pause background
        pause_bg_rect = pygame.Rect(pause_x, pause_y, scaled_width, scaled_height)
        if pause_bg_rect.collidepoint(mouse_x, mouse_y):
            pygame.mouse.set_visible(True)  # Show the cursor
        else:
            pygame.mouse.set_visible(False)  # Hide the cursor when not hovering


        # Draw the quit button when the game is paused
        quit_button_width, quit_button_height = 225, 200  # Increased height from 100 to 150
        quit_button_x = (screen_width - quit_button_width) // 2
        quit_button_y = screen_height // 2 + 50  # Place it below the pause background
        quit_button_rect = pygame.Rect(quit_button_x, quit_button_y, quit_button_width, quit_button_height)


        # Load and draw the quit button image
        quit_button_image = pygame.image.load(r"assets/quit_button.png").convert_alpha()
        quit_button_image = pygame.transform.scale(quit_button_image, (quit_button_width, quit_button_height))
        self.screen.blit(quit_button_image, quit_button_rect)


        # Check if the quit button is clicked
        if quit_button_rect.collidepoint(mouse_x, mouse_y) and pygame.mouse.get_pressed()[0]:
            game = Game()
            game.run()


        # Draw the resume button when the game is paused
        resume_button_width, resume_button_height = 300, 150  # Increased width to 500
        resume_button_x = (screen_width - resume_button_width) // 2 + 50  # Moved 50 pixels to the right
        resume_button_y = screen_height // 2 - 100  # Moved it slightly lower (adjusted from -200 to -150)
        resume_button_rect = pygame.Rect(resume_button_x, resume_button_y, resume_button_width, resume_button_height)


        # Draw the resume button image
        self.screen.blit(self.resume_button_image, resume_button_rect)


        # Check if the resume button is clicked
        if resume_button_rect.collidepoint(mouse_x, mouse_y) and pygame.mouse.get_pressed()[0]:
            self.is_paused = False  # Unpause the game when resume button is clicked


    def go_to_home_screen(self):
        """Reset the game state and display the home screen."""
        self.is_paused = False  # Unpause the game if paused
        # Add any other reset logic here, like resetting game variables, scores, etc.
        self.show_home_screen()  # Call a method that shows the home screen  


    def show_home_screen(self):
        """Display the home screen."""
        # Here, you can implement the logic to display your home screen (e.g., buttons, titles, etc.)
        self.screen.fill((0, 0, 0))  # Clear the screen with a black color (optional)
       
        # Show the home screen background or other UI elements
        home_screen_text = pygame.font.SysFont('Arial', 50).render('Home Screen', True, (255, 255, 255))
        self.screen.blit(home_screen_text, (self.screen_width // 2 - home_screen_text.get_width() // 2, self.screen_height // 2))
       
        pygame.display.flip()  # Update the screen  


    def toggle_fullscreen(self):
        """Toggle between windowed and fullscreen mode."""
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.SCALED)
        else:
            self.screen = pygame.display.set_mode((self.game_width, self.game_height), pygame.RESIZABLE)


        # Update the screen dimensions dynamically
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()


        # Recenter the player in the new screen size
        self.center_player()


        # Update the play button position based on the new screen size
        self.update_play_button_position()


    def update_play_button_position(self):
        """Update the play button position based on the screen size."""
        if self.fullscreen:
            self.button_x = self.screen.get_width() / 2 - 100  # Centered horizontally
            self.button_y = self.screen.get_height() / 2 + 100  # Centered vertically (a bit lower)
        else:
            self.button_x = self.game_width / 2 - 100  # Centered horizontally
            self.button_y = self.game_height / 2 + 100  # Centered vertically (a bit lower)


        self.play_button = Button(self.button_x, self.button_y, "assets/play_button.png")
        self.quit_button = Button(self.button_x, self.button_y, "assets/quit_button.png")


    def bow_timer(self):
            """Handles the cooldown timer for shooting arrows."""
            if not self.can_shoot:
                now = pygame.time.get_ticks()
                if now - self.shoot_time >= self.bow_cooldown:
                    self.can_shoot = True


    def handle_pause_button_position(self):
        """Update the pause button position dynamically."""
        pause_x = self.screen_width - 1160  # Move it to the right side of the screen
        pause_y = 7  # Keep it near the top
        button_width = 75  # New width for the button
        button_height = 75  # New height for the button


        # Scale the image to the new dimensions
        self.pause_button = Button(pause_x, pause_y, "assets/pause_button.png", button_width, button_height)


    def update(self):
        """Update game objects."""
        if self.game_state == "game":
            self.input()
            self.bow_timer()
            self.all_sprites.update()
            self.spawn_enemies()


            # Border collision for the player
            self.check_player_border_collision()

            # Border collision for mobs
            self.check_mob_border_collision()

            self.player_mob_collision()

    
    def player_mob_collision(self):
        """Check for collisions between the player and mobs."""
        for mob in self.mob_sprites:
            if pygame.sprite.collide_rect(self.player, mob):
                self.player.take_damage(1)
                mob.kill()
                if self.player.health <= 0:
                    self.is_paused = True           # Game Over Interface

    def check_player_border_collision(self):
        """Prevent the player from going outside the border area defined by the border.jpg."""
        # Calculate the position and size of the border (from previous code)
        border_width_factor = 0.43  # 70% width of the screen
        border_height_factor = 0.75  # 65% height of the screen


        border_width = int(self.screen_width * border_width_factor)  # 70% of the screen width
        border_height = int(self.screen_height * border_height_factor)  # 65% of the screen height


        # Position of the border
        border_x = (self.screen_width - border_width) // 2  # Centered horizontally
        border_y = (self.screen_height - border_height) // 2  # Centered vertically
        # Get the player's current position and size
        player_rect = self.player.rect


        # Prevent player from going outside the border
        if player_rect.left < border_x:
            player_rect.left = border_x
        if player_rect.right > border_x + border_width:
            player_rect.right = border_x + border_width
        if player_rect.top < border_y:
            player_rect.top = border_y
        if player_rect.bottom > border_y + border_height:
            player_rect.bottom = border_y + border_height


    def check_mob_border_collision(self):
        """Prevent mobs from going outside the map borders."""
        # Get the map's boundaries based on the scaled map
        map_x = (self.screen_width - self.game_width) // 2  # Horizontal center of the map
        map_y = 0  # The map starts at the top edge
        map_width = self.game_width  # Map width stays the same as the game width
        map_height = self.screen_height  # Map height is the full screen height


        # Check for border collision with the mobs
        for mob in self.mob_sprites:
            if mob.rect.left < map_x:
                mob.rect.left = map_x
            if mob.rect.right > map_x + map_width:
                mob.rect.right = map_x + map_width
            if mob.rect.top < map_y:
                mob.rect.top = map_y
            if mob.rect.bottom > map_y + map_height:
                mob.rect.bottom = map_y + map_height


    def draw(self):
        """Draw all game objects on the screen."""
        self.fill_excess_area()


        if self.game_state == "menu":
            self.play_button.draw(self.screen)
            self.quit_button.draw(self.screen)


        elif self.game_state == "game":
            self.all_sprites.draw(self.screen)
            if self.pause_button:  # Draw the pause button in the game
                self.pause_button.draw(self.screen)

            for mob in self.mob_sprites:
                mob.update()  # Update the mob logic
                mob.draw_health_bar(self.screen)  # Draw the health bar
            
            # Draw the player's health bar
            self.player.update()
            self.player.draw_health_bar(self.screen)

            self.display_score()
            
        self.screen.blit(self.cursor, pygame.mouse.get_pos())

    def fill_excess_area(self):
        """Fill the excess space around the gameplay area and stretch the map vertically."""
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        self.center_x = (self.screen_width - self.game_width) // 2
        self.center_y = (self.screen_height - self.game_height) // 2


        # Fill the entire screen with the appropriate background image
        if self.game_state == "menu":
            scaled_background = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))
        else:
            scaled_background = pygame.transform.scale(self.game_background_image, (self.screen_width, self.screen_height))


        self.screen.blit(scaled_background, (0, 0))


        # Only draw the map if the game state is "game"
        if self.game_state == "game":
            # Scale the original map to fit the game width and stretch its height
            scaled_map = pygame.transform.scale(self.map_image, (self.game_width, self.screen_height))


            # Calculate position to center the masp horizontally
            map_x = (self.screen_width - self.game_width) // 2  # Center horizontally
            map_y = 0  # Align the map to the top edge


            # Draw the black border first
            border_thickness = 30  # Thickness of the border
            border_rect = pygame.Rect(
                map_x - border_thickness,
                map_y - border_thickness,
                self.game_width + 2 * border_thickness,
                self.screen_height + 2 * border_thickness
            )
            pygame.draw.rect(self.screen, (0, 0, 0), border_rect)  # Draw the black border


            # Draw the map on top of the border
            self.screen.blit(scaled_map, (map_x, map_y))


    def setup(self):
        """Set up initial game objects."""
        self.bow = Bow(self.player, self.all_sprites)
       
    def spawn_enemies(self):
        if not self.game_started:
            return
       
        now = pygame.time.get_ticks()
        if now - self.start_time < self.spawn_delay:
            return
       
        spawn_locations = ['middle_left', 'middle_right', 'middle_bottom']
        self.spawn_counter = self.spawn_counter % len(spawn_locations)


        # Check if it's time to spawn AN enemy (regardless of location)
        if now - self.last_spawn_time >= self.enemy_spawn_time:
            spawn_edge = spawn_locations[self.spawn_counter]
            self.enemy_spawn_time = random.randint(1000, 3000) #Still random interval
            mob_type = random.choice([Mob, Mob_right, Boss])
            spawn_x, spawn_y = self.get_spawn_position(spawn_edge)
            enemy = mob_type((spawn_x, spawn_y), self.player, game, self.all_sprites)
            self.all_sprites.add(enemy)
            self.mob_sprites.add(enemy)
            self.last_spawn_time = now
            self.spawn_counter += 1

    def get_spawn_position(self, edge):
        """Get the spawn position for enemies based on specific edges of the map image."""
        # Calculate the map's position and size
        map_x = (self.screen_width - self.game_width) // 2  # Center the map horizontally
        map_y = 0  # Align the map to the top edge
        map_width = self.game_width  # Map width matches the game width
        map_height = self.screen_height  # Map height matches the screen height

        # Determine spawn positions based on the selected edge
        if edge == 'middle_left':
            spawn_x = map_x  # Left edge of the map
            spawn_y = map_y + map_height // 2  # Vertical center of the map
        elif edge == 'middle_right':
            spawn_x = map_x + map_width  # Right edge of the map
            spawn_y = map_y + map_height // 2  # Vertical center of the map
        elif edge == 'middle_bottom':
            spawn_x = map_x + map_width // 2  # Horizontal center of the map
            spawn_y = map_y + map_height  # Bottom edge of the map
        else:
            raise ValueError("Invalid edge specified for mob spawning.")


        return spawn_x, spawn_y
   
    def update_play_button_position(self):
        """Update the play button position based on the screen size."""
        if self.fullscreen:
            # Center the play button on the fullscreen window
            self.button_x = self.screen.get_width() / 2 - 100  # Centered horizontally
            self.button_y = self.screen.get_height() / 2 + 100  # Centered vertically (a bit lower)
        else:
            # In windowed mode, center the button relative to the game window, but shift it even more to the right
            self.button_x = self.game_width / 2 - 100 + 600  # Move it much more to the right by adding 600 pixels
            self.button_y = self.game_height / 2 + 100  # Centered vertically (a bit lower)
            self.quit_button_x = self.game_width / 2 - 110 + 600  # Move it much more to the right by adding 600 pixels
            self.quit_button_y = self.game_height / 2 + 150  # Centered vertically (a bit lower)


        # Create or update the button with the new position
        self.play_button = Button(self.button_x, self.button_y, "assets/play_button.png", width=220, height=80)
        self.quit_button = Button(self.quit_button_x, self.quit_button_y, "assets/quit_button.png", width=220, height=160)


    def run(self):
        pygame.mixer.init()
        # Load the home screen music
        pygame.mixer.music.load(r"sfx/homescreenogg.mp3")
        pygame.mixer.music.play(-1, 0.0)  # Play the music looped indefinitely (-1)"""Main game loop."""
        while self.running:
            self.handle_events()
            if self.game_state == "menu":
                if self.play_button.is_hovered() and pygame.mouse.get_pressed()[0]:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(r"sfx/battle_ost.ogg")  # Load the battle OST
                    pygame.mixer.music.play(-1, 0.0)
                    self.game_started = True
                    self.start_time = pygame.time.get_ticks()            
                    self.game_state = "game"
                    self.center_player()
                    self.handle_pause_button_position()

                if self.quit_button.is_hovered() and pygame.mouse.get_pressed()[0]:
                    sys.exit()
                    pygame.quit()

            elif self.game_state == "game":
                if self.show_intro_text:
                    self.display_endless_apocalypse()
                    self.show_intro_text = False  # Set this to False after showing the text
                if not self.is_paused:
                    self.update()
                else:
                    self.draw_pause_screen()  # Draw pause background when paused


            if not self.is_paused:
                self.draw()  # Draw game objects when not paused
           
            self.all_sprites.update()
            pygame.display.update()
            self.clock.tick(60)


        pygame.quit()
        sys.exit()


    def display_endless_apocalypse(self):
        """Display 'ENDLESS APOCALYPSE' text on the screen briefly."""
        # Create the font object
        font = pygame.font.Font(r"font/apo.ttf", 45)
        text_surface = font.render('ENDLESS APOCALYPSE', True, (255, 0, 0))  # Red text color
        text_rect = text_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))


        # Draw the text on the screen
        self.screen.blit(text_surface, text_rect)
        pygame.display.update()  # Update the display


        # Wait for a few seconds before starting the game
        pygame.time.delay(2000)  # Delay for 2 seconds (adjust as necessary)
       
        # After the delay, switch to the game state
        self.game_state = "game"

    def update_score(self, score):
        """Update the game score."""
        self.score += score

    def display_score(self):
        """Display the current score on the screen."""
        font = pygame.font.Font(None, 36)
        score_surface = font.render(f"Score: {self.score}", True, (255, 0, 0))
        self.screen.blit(score_surface, (10, 10))


# Button class with image support
class Button:
    def __init__(self, x, y, image_path, width=200, height=50):
        self.rect = pygame.Rect(x, y, width, height)  # Use dynamic size
        self.image = pygame.image.load(image_path).convert_alpha()  # Load image
        self.image = pygame.transform.scale(self.image, (width, height))  # Scale the image to the given size


    def draw(self, screen):
        # Draw the button using the image
        screen.blit(self.image, self.rect)


    def is_hovered(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_x, mouse_y)


# Run the game
if __name__ == "__main__":
    game = Game()
    game.run()
    
