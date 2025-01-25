import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, scale=(64, 64)):  # Add a scale parameter
        super().__init__(groups)
        self.original_image = pygame.image.load(r"assets/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.original_image, scale)  # Scale the image
        self.rect = self.image.get_rect(center=pos)
    
        # Movement
        self.direction = pygame.Vector2()
        self.speed = 3
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
