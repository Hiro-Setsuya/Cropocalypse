import pygame
import math

class Bow(pygame.sprite.Sprite):
    def __init__(self, player, groups, scale=(25, 25)):
        # Player connection
        self.player = player
        self.distance = 15  # Adjust the distance to player

        # Sprite setup
        super().__init__(groups)
        self.original_img = pygame.image.load(r"assets/bow.png").convert_alpha()
        self.original_img = pygame.transform.scale(self.original_img, scale)
        self.image = self.original_img
        self.rect = self.image.get_rect(center=self.player.rect.center)

    def update(self):
        # Update player direction based on mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Calculate relative position
        rel_x, rel_y = mouse_x - self.player.rect.centerx, mouse_y - self.player.rect.centery

        # Calculate the angle in degrees
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)

        # Rotate the bow image
        rotated_image = pygame.transform.rotate(self.original_img, angle)

        # Normalize the direction to maintain the bow's position at the correct distance
        distance_factor = self.distance / math.hypot(rel_x, rel_y)

        # Calculate the position to center the bow relative to the player
        bow_x = self.player.rect.centerx + rel_x * distance_factor
        bow_y = self.player.rect.centery + rel_y * distance_factor

        # Update the image and rect for the bow
        self.image = rotated_image
        self.rect = self.image.get_rect(center=(bow_x, bow_y))

class Arrow(pygame.sprite.Sprite):
    def __init__(self, pos, direction, speed, groups, scale=(15, 15)):
        super().__init__(groups)
        self.original_image = pygame.image.load(r"assets/arrow.png").convert_alpha()

        # Scale the image
        self.original_image = pygame.transform.scale(self.original_image, scale)

        # Normalize direction
        self.direction = direction.normalize()  # Normalize direction to prevent very fast arrows at larger distances
        self.speed = speed

        # Calculate the angle using atan2
        angle = math.atan2(direction.y, direction.x)

        # Rotate the image to face the direction of the shot
        self.image = pygame.transform.rotate(self.original_image, -math.degrees(angle))  # Convert radians to degrees
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        # Move the arrow based on its direction
        self.rect.centerx += self.direction.x * self.speed
        self.rect.centery += self.direction.y * self.speed

        # Get the screen's and map's boundaries
        screen_width, screen_height = pygame.display.get_surface().get_size()
        
        # Assuming you have a method or variable for map size, you can access the map boundaries
        map_width = 800  # Replace with actual map width if it's dynamic
        map_height = screen_height  # Use full screen height as map height

        # Get the position of the map (centered on the screen)
        map_x = (screen_width - map_width) // 2
        map_y = 0

        # Check if the arrow is within the map boundaries
        if not self.rect.colliderect(pygame.Rect(map_x, map_y, map_width, map_height)):
            self.kill()


class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups):
        super().__init__(groups)
        self.image = pygame.Surface(size)
        self.image.fill("blue")
        # Unfinish

