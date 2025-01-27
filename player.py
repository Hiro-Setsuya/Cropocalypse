import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, scale=(64, 64)):  # Add a scale parameter
        super().__init__(groups)
        self.original_image = pygame.image.load(r"assets/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.original_image, scale)  # Scale the image
        self.rect = self.image.get_rect(center=pos)
        self.health = 5
        self.max_health = 5
    
        # Movement
        self.direction = pygame.Vector2()
        self.speed = 1.5
        self.facing_right = True  # Track the facing direction

    def input(self):
        keys = pygame.key.get_pressed()

        # Horizontal Movement
        if keys[pygame.K_a]:
            self.direction.x = -1
            if self.facing_right:  # Flip the image only if currently facing right
                self.image = pygame.transform.flip(self.image, True, False)
                self.facing_right = False
        elif keys[pygame.K_d]:
            self.direction.x = 1
            if not self.facing_right:  # Flip the image only if currently facing left
                self.image = pygame.transform.flip(self.image, True, False)
                self.facing_right = True
        else:
            self.direction.x = 0 

        # Vertical movement
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0
    
    def move(self):
        self.rect.center += self.direction * self.speed

    def update(self):
        self.input()
        self.move()

    def draw_health_bar(self, screen):
        """Draw the health bar above the mob sprite."""
        health_bar_width = 40
        health_bar_height = 5
        health_percentage = self.health / self.max_health
        health_bar_rect = pygame.Rect(self.rect.centerx - health_bar_width // 2, self.rect.top + 5, health_bar_width, health_bar_height)

        # Background (empty) health bar
        pygame.draw.rect(screen, (0, 0, 0), health_bar_rect)

        # Filled health bar
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(health_bar_rect.x, health_bar_rect.y, health_bar_width * health_percentage, health_bar_height))

    def take_damage(self, amount = 1):
        """Reduces player's health by the given amount."""
        self.health -= amount
        if self.health < 0:
            self.dead()
    
    def dead(self):
        """Returns True if the player's health is zero."""
        return self.health == 0
