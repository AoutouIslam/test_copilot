import pygame
from game import Game
from scoring import ScoreManager
from sound_manager import SoundManager
from particle_manager import ParticleManager

def main():
    pygame.init()

    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Home Invader Game")

    game = Game(screen)
    clock = pygame.time.Clock()

    running = True
    while running:
        delta_time = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game.update()

        screen.fill((0, 0, 0))
        game.draw()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()