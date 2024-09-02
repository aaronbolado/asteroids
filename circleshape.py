import pygame

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def collision_check(self, other_circle):
        distance = pygame.Vector2(self.position).distance_to(pygame.Vector2(other_circle.position))
        if distance <= (self.radius + other_circle.radius):
            return True
        return False

    def draw(self, screen):
        pass
    
    def update(self, dt):
        pass
