import pygame
import math
import random
from game import *


class Mob(pygame.sprite.Sprite):
    def __init__(self, pos, player, game, groups,score = 100, scale=(32, 32)):
        super().__init__(groups)
        self.player = player
        self.game = game
        self.health = 1
        self.max_health = 1
        self.speed = 1
        self.score = score

        # Randomly choose an image from mob_1 to mob_3
        mob_image = f"assets/mob_{random.randint(1,3)}.png"
        self.original_image = pygame.image.load(mob_image).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, scale)
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        # Always move towards the player
        direction = pygame.Vector2(
            self.player.rect.centerx - self.rect.centerx,
            self.player.rect.centery - self.rect.centery,
        )
        if direction.length() > 0:  # Avoid normalizing zero vectors
            direction = direction.normalize()

        # Adjust the mob position
        self.rect.centerx += direction.x * self.speed  # Example speed
        self.rect.centery += direction.y * self.speed

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.destroy()

    def destroy(self):
            blood_frames = [
                pygame.image.load(f"assets/blood{i}.png").convert_alpha()
                for i in range(1, 6)
            ]

            # Define a scaling factor for the blood splash (e.g., 1.5 to make it 1.5 times larger)
            scale_factor = 0.5

            # Function to animate the blood splash
            def play_blood_splash():
                for frame in blood_frames:
                    # Scale the frame by the scaling factor
                    new_width = int(frame.get_width() * scale_factor)
                    new_height = int(frame.get_height() * scale_factor)
                    scaled_frame = pygame.transform.scale(frame, (new_width, new_height))

                    # Position the splash frame centered on the mob's position
                    splash_rect = scaled_frame.get_rect(center=self.rect.center)

                    # Draw the scaled blood splash frame
                    self.game.screen.blit(scaled_frame, splash_rect.topleft)
                    pygame.display.update()

            # Play the blood splash animation
            play_blood_splash()

            # Update score
            self.game.update_score(self.score)

            # Kill the mob
            self.kill()

    def draw_health_bar(self, screen):
        """Draw the health bar above the mob sprite."""
        health_bar_width = 40
        health_bar_height = 5
        health_percentage = self.health / self.max_health
        health_bar_rect = pygame.Rect(self.rect.centerx - health_bar_width // 2, self.rect.top - 10, health_bar_width, health_bar_height)

        # Background (empty) health bar
        pygame.draw.rect(screen, (0, 0, 0), health_bar_rect)

        # Filled health bar
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(health_bar_rect.x, health_bar_rect.y, health_bar_width * health_percentage, health_bar_height))

class Mob_right(pygame.sprite.Sprite):
    def __init__(self, pos, player, game, groups,score = 200, scale=(32, 32)):
        super().__init__(groups)
        self.player = player
        self.game = game
        self.health = 2
        self.max_health = 2
        self.speed = 1
        self.score = score

        # Randomly choose an image from mobr_1 to mobr_3
        mobr_image = f"assets/mobr_{random.randint(1,4)}.png"
        self.original_image = pygame.image.load(mobr_image).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, scale)
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        # Move towards the player
        direction = pygame.Vector2(
            self.player.rect.centerx - self.rect.centerx,
            self.player.rect.centery - self.rect.centery,
        )
        if direction.length() > 0:  # Avoid normalizing zero vectors
            direction = direction.normalize()

        # Flip the image if moving left
        if direction.x < 0:
            flipped_image = pygame.transform.flip(self.original_image, True, False)
            if flipped_image.get_size() != self.image.get_size():  # Avoid redundant scaling
                self.image = pygame.transform.scale(flipped_image, self.rect.size)
        else:
            if self.image.get_size() != self.rect.size:
                self.image = pygame.transform.scale(self.original_image, self.rect.size)

        # Adjust the mob position
        self.rect.centerx += direction.x * self.speed 
        self.rect.centery += direction.y * self.speed
    
    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.destroy()

    def destroy(self):
            blood_frames = [
                pygame.image.load(f"assets/blood{i}.png").convert_alpha()
                for i in range(1, 6)
            ]

            # Define a scaling factor for the blood splash (e.g., 1.5 to make it 1.5 times larger)
            scale_factor = 0.5

            # Function to animate the blood splash
            def play_blood_splash():
                for frame in blood_frames:
                    # Scale the frame by the scaling factor
                    new_width = int(frame.get_width() * scale_factor)
                    new_height = int(frame.get_height() * scale_factor)
                    scaled_frame = pygame.transform.scale(frame, (new_width, new_height))

                    # Position the splash frame centered on the mob's position
                    splash_rect = scaled_frame.get_rect(center=self.rect.center)

                    # Draw the scaled blood splash frame
                    self.game.screen.blit(scaled_frame, splash_rect.topleft)
                    pygame.display.update()

            # Play the blood splash animation
            play_blood_splash()

            # Update score
            self.game.update_score(self.score)

            # Kill the mob
            self.kill()

    def draw_health_bar(self, screen):
        """Draw the health bar above the mob sprite."""
        health_bar_width = 40
        health_bar_height = 5
        health_percentage = self.health / self.max_health
        health_bar_rect = pygame.Rect(self.rect.centerx - health_bar_width // 2, self.rect.top - 10, health_bar_width, health_bar_height)

        # Background (empty) health bar
        pygame.draw.rect(screen, (0, 0, 0), health_bar_rect)

        # Filled health bar
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(health_bar_rect.x, health_bar_rect.y, health_bar_width * health_percentage, health_bar_height))

class Boss(pygame.sprite.Sprite):
    def __init__(self, pos, player, game, groups, score = 500, scale=(64, 64)):
        super().__init__(groups)
        self.player = player
        self.game = game
        self.health = 5
        self.max_health = 5
        self.speed = 1
        self.score = score

        # Load boss images
        self.images = {
            "walk": [
                pygame.image.load("assets/boss_1.png").convert_alpha(),
                pygame.image.load("assets/boss_2.png").convert_alpha(),
            ],
            "attack": pygame.image.load("assets/boss_atk.png").convert_alpha(),
        }

        # Set initial image and animation variables
        self.current_state = "walk"  # Default state is walking
        self.current_frame = 0
        self.animation_speed = 100  # Milliseconds per frame
        self.last_update = pygame.time.get_ticks()

        # Set the initial image and scale
        self.original_image = self.images["walk"][self.current_frame]
        self.image = pygame.transform.scale(self.original_image, scale)
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        # Handle animation updates
        self.animate()

        # Determine state based on distance to the player
        distance = pygame.Vector2(self.rect.center).distance_to(self.player.rect.center)
        if distance < 50:
            self.current_state = "attack"
        else:
            self.current_state = "walk"

        # Update the image based on the current state
        if self.current_state == "attack":
            self.original_image = self.images["attack"]
        else:
            self.original_image = self.images["walk"][int(self.current_frame)]

        self.image = pygame.transform.scale(self.original_image, (64, 64))

        # Move towards the player if not attacking
        if self.current_state == "walk":
            direction = pygame.Vector2(
                self.player.rect.centerx - self.rect.centerx,
                self.player.rect.centery - self.rect.centery,
            )
            if direction.length() > 0:  # Avoid normalizing zero vectors
                direction = direction.normalize()
            self.rect.centerx += direction.x * self.speed  # Boss speed
            self.rect.centery += direction.y * self.speed

    def animate(self):
        """Handles the boss walking animation."""
        if self.current_state == "walk":
            now = pygame.time.get_ticks()
            if now - self.last_update > self.animation_speed:
                self.last_update = now
                self.current_frame += 1
                if self.current_frame >= len(self.images["walk"]):
                    self.current_frame = 0  # Loop back to the first frame

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.destroy()

    def destroy(self):
            blood_frames = [
                pygame.image.load(f"assets/blood{i}.png").convert_alpha()
                for i in range(1, 6)
            ]

            # Define a scaling factor for the blood splash (e.g., 1.5 to make it 1.5 times larger)
            scale_factor = 1

            # Function to animate the blood splash
            def play_blood_splash():
                for frame in blood_frames:
                    # Scale the frame by the scaling factor
                    new_width = int(frame.get_width() * scale_factor)
                    new_height = int(frame.get_height() * scale_factor)
                    scaled_frame = pygame.transform.scale(frame, (new_width, new_height))

                    # Position the splash frame centered on the mob's position
                    splash_rect = scaled_frame.get_rect(center=self.rect.center)

                    # Draw the scaled blood splash frame
                    self.game.screen.blit(scaled_frame, splash_rect.topleft)
                    pygame.display.update()

            # Play the blood splash animation
            play_blood_splash()

            # Update score
            self.game.update_score(self.score)

            # Kill the mob
            self.kill()
        
    def draw_health_bar(self, screen):
        """Draw the health bar above the mob sprite."""
        health_bar_width = 40
        health_bar_height = 5
        health_percentage = self.health / self.max_health
        health_bar_rect = pygame.Rect(self.rect.centerx - health_bar_width // 2, self.rect.top - 10, health_bar_width, health_bar_height)

        # Background (empty) health bar
        pygame.draw.rect(screen, (0, 0, 0), health_bar_rect)

        # Filled health bar
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(health_bar_rect.x, health_bar_rect.y, health_bar_width * health_percentage, health_bar_height))
