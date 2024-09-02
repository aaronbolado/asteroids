import pygame
from constants import *
from circleshape import CircleShape

class Shield(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, BUFF_RADIUS)

    def draw(self, screen):
        pygame.draw.circle(screen, "blue", self.position, self.radius, 2)
    
    def update(self, dt):
        self.position += self.velocity * dt