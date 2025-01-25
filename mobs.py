import pygame
import math
import random


class Mob(pygame.sprite.Sprite):
    def __init__(self, pos, player, groups, scale=(32, 32)):
        super().__init__(groups)
        self.player = player

        # Randomly choose an image from mob_1 to mob_5
        mob_image = f"assets/mob_2.png"
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
        self.rect.centerx += direction.x * 2  # Example speed
        self.rect.centery += direction.y * 2

    def destroy(self):
        self.kill()


class Mob_right(pygame.sprite.Sprite):
    def __init__(self, pos, player, groups, scale=(32, 32)):
        super().__init__(groups)
        self.player = player

        # Randomly choose an image from mobr_1 to mobr_3
        mobr_image = f"assets/mobr_4.png"
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
        self.rect.centerx += direction.x * 2  # Example speed
        self.rect.centery += direction.y * 2

    def destroy(self):
        self.kill()


class Boss(pygame.sprite.Sprite):
    def __init__(self, pos, player, groups, scale=(64, 64)):
        super().__init__(groups)
        self.player = player

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
            self.rect.centerx += direction.x * 1.5  # Boss speed
            self.rect.centery += direction.y * 1.5

    def animate(self):
        """Handles the boss walking animation."""
        if self.current_state == "walk":
            now = pygame.time.get_ticks()
            if now - self.last_update > self.animation_speed:
                self.last_update = now
                self.current_frame += 1
                if self.current_frame >= len(self.images["walk"]):
                    self.current_frame = 0  # Loop back to the first frame

    def destroy(self):
        self.kill()
