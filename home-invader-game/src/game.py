import pygame
import random

class Game:
    def __init__(self, screen):
        self.screen = screen  # Store the screen for rendering
        self.player_position = [400, 550]  # Near the bottom of the screen
        self.player_size = 50  # Adjusted size for player
        self.enemy_size = 50  # Adjusted size for enemy
        self.player_speed = 5
        self.projectiles = []
        self.enemies = []
        self.last_shot_time = 0  # Track the time of the last shot
        self.player_image = pygame.image.load("./home-invader-game/assets/player.png").convert_alpha()
        self.player_image = pygame.transform.scale(self.player_image, (self.player_size, self.player_size))  # Resize player image
        self.enemy_images = [
            pygame.transform.scale(pygame.image.load("./home-invader-game/assets/enemy1.png"), (self.enemy_size, self.enemy_size)),
            pygame.transform.scale(pygame.image.load("./home-invader-game/assets/enemy2.png"), (self.enemy_size, self.enemy_size)),
            pygame.transform.scale(pygame.image.load("./home-invader-game/assets/enemy3.png"), (self.enemy_size, self.enemy_size))
        ]
        self.state = "running"  # Game state: "running" or "gameover"
        self.score = 0

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if self.state == "running":
            if keys[pygame.K_UP]:
                self.player_position[1] -= self.player_speed
            if keys[pygame.K_DOWN]:
                self.player_position[1] += self.player_speed
            if keys[pygame.K_LEFT]:
                self.player_position[0] -= self.player_speed
            if keys[pygame.K_RIGHT]:
                self.player_position[0] += self.player_speed
            if keys[pygame.K_SPACE]:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_shot_time > 500:  # 0.5 seconds
                    self.shoot_projectile()
                    self.last_shot_time = current_time
        elif self.state == "gameover":
            if keys[pygame.K_SPACE]:
                self.reset()  # Restart the game

    def shoot_projectile(self):
        projectile_rect = pygame.Rect(
            self.player_position[0] + self.player_size // 2 - 2,  # Center of the player
            self.player_position[1] - 10,  # Above the player
            4, 10  # Projectile size
        )
        self.projectiles.append(projectile_rect)

    def update_projectiles(self):
        for projectile in self.projectiles[:]:
            projectile.y -= 10  # Move upward
            if projectile.y < 0:
                self.projectiles.remove(projectile)  # Remove off-screen projectiles

    def spawn_enemy(self):
        enemy_x = random.randint(0, self.screen.get_width() - self.enemy_size)
        enemy_y = -self.enemy_size  # Start above the screen
        enemy_speed = random.randint(2, 5)
        enemy_image = random.choice(self.enemy_images)  # Randomly select an enemy type
        self.enemies.append({'rect': pygame.Rect(enemy_x, enemy_y, self.enemy_size, self.enemy_size), 'speed': enemy_speed, 'image': enemy_image})

    def update_enemies(self):
        # Spawn enemies periodically
        if random.randint(1, 60) == 1:  # Roughly one enemy per second at 60 FPS
            self.spawn_enemy()

        # Move enemies
        for enemy in self.enemies[:]:
            enemy['rect'].y += enemy['speed']
            if enemy['rect'].y > self.screen.get_height():
                self.enemies.remove(enemy)  # Remove enemies that go off-screen

    def check_collisions(self):
        player_rect = pygame.Rect(*self.player_position, self.player_size, self.player_size)
        for enemy in self.enemies[:]:
            if player_rect.colliderect(enemy['rect']):
                self.state = "gameover"  # Set game state to gameover

        for projectile in self.projectiles[:]:
            for enemy in self.enemies[:]:
                if projectile.colliderect(enemy['rect']):
                    self.projectiles.remove(projectile)
                    self.enemies.remove(enemy)
                    self.score += 1  # Increment score for destroyed enemy

    def update(self):
        self.handle_input()
        self.update_projectiles()
        self.update_enemies()
        self.check_collisions()

    def draw(self):
        if self.state == "running":
            self.screen.blit(self.player_image, self.player_position)  # Draw player image

            # Draw enemies
            for enemy in self.enemies:
                self.screen.blit(enemy['image'], enemy['rect'].topleft)  # Draw enemy image

            # Draw projectiles
            for projectile in self.projectiles:
                pygame.draw.rect(self.screen, (255, 255, 0), projectile)  # Yellow projectiles

            # Draw score
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))
        elif self.state == "gameover":
            font = pygame.font.Font(None, 72)
            gameover_text = font.render("Game Over", True, (255, 0, 0))
            self.screen.blit(gameover_text, (self.screen.get_width() // 2 - 150, self.screen.get_height() // 2 - 50))

            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
            self.screen.blit(score_text, (self.screen.get_width() // 2 - 100, self.screen.get_height() // 2 + 50))

            restart_text = font.render("Press SPACE to restart", True, (255, 255, 255))
            self.screen.blit(restart_text, (self.screen.get_width() // 2 - 150, self.screen.get_height() // 2 + 100))

    def reset(self):
        self.player_position = [400, 550]  # Reset player to near the bottom
        self.enemies.clear()
        self.projectiles.clear()
        self.score = 0
        self.state = "running"  # Reset game state