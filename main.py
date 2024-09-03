import pygame
import pygame_menu
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from bufffield import BuffField
from shot import Shot
from constants import *
from buffs import *

# Initialize pygame
pygame.init()
pygame.font.get_init()


# Screen display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
game_clock = pygame.time.Clock()
score = 0

font_name = pygame.font.match_font('arial')
TEXT_FONT = pygame.font.Font(font_name, 32)

def main():
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    
    menu = pygame_menu.Menu('Welcome', 400, 300,
                       theme=pygame_menu.themes.THEME_BLUE)

    menu.add.button('Play', game_state)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(screen)

def game_state():
    in_game = True
    while True:
        if in_game:
            # Game loop
            in_game = game_loop()
        else:
            # Menu loop
            in_game = menu_loop()

        if not in_game:
            break

    pygame.quit()
    
def display_ui(score):
    # Render the text with the font
    score_text = TEXT_FONT.render(f'Score: {score}', True, (255, 255, 255))
    
    # Position the text at the center top of the screen
    text_rect = score_text.get_rect(center=(screen.get_width() / 2, 50))
    
    # Blit the text onto the window at the specified position
    screen.blit(score_text, text_rect)

def game_loop():
    dt = 0
    score = 0
    
    # Groups for objects
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    buffs = pygame.sprite.Group()

    # Must use containers on the class itself before creating object
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, updatable, drawable)
    Shield.containers = (buffs, updatable, drawable)
    BuffField.containers = updatable

    # Create player object
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    asteroid_field = AsteroidField()
    buff_field = BuffField()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False


        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            return menu_loop()

        screen.fill("black")
        display_ui(score)

        for thing in updatable:
            thing.update(dt)

        for asteroid in asteroids:
            if asteroid.collision_check(player) == True and player.immune_timer > 0:
                score += asteroid.split()

            elif asteroid.collision_check(player) == True and player.immune_timer <= 0:
                main()

            for bullet in shots:
                if asteroid.collision_check(bullet) == True:
                    score += asteroid.split()
                    bullet.kill()

        for buff in buffs:
            if buff.collision_check(player) == True:
                buff.kill()
                player.apply_buff(buff)
            
        for thing in drawable:
            thing.draw(screen)

        pygame.display.flip()

        # Limit framerate to 60 FPS
        dt = game_clock.tick(60) / 1000
        
    return True

def menu_loop():
    menu = pygame_menu.Menu('Welcome', 400, 300,
                            theme=pygame_menu.themes.THEME_BLUE)

    menu.add.button('Restart', game_loop)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    menu_active = True
    while menu_active:
        menu.update(pygame.event.get())
        menu.draw(screen)
        pygame.display.flip()
        
    return True

if __name__ == "__main__":
    main()