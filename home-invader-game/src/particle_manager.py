import pygame
import random


class Particle:
    def __init__(self, position, velocity, lifetime, color):
        self.position = position
        self.velocity = velocity
        self.lifetime = lifetime
        self.color = color
        self.age = 0

    def update(self, delta_time):
        self.position[0] += self.velocity[0] * delta_time
        self.position[1] += self.velocity[1] * delta_time
        self.age += delta_time

    def is_alive(self):
        return self.age < self.lifetime


class ParticleManager:
    def __init__(self):
        self.particles = []

    def create_particle(self, position, velocity, lifetime, color):
        particle = Particle(position, velocity, lifetime, color)
        self.particles.append(particle)

    def create_explosion(self, position, color):
        for _ in range(10):  # Create 10 particles for the explosion
            velocity = [random.uniform(-2, 2), random.uniform(-2, 2)]
            lifetime = random.uniform(0.5, 1.5)
            self.create_particle(position, velocity, lifetime, color)

    def update_particles(self, delta_time):
        for particle in self.particles[:]:
            particle.update(delta_time)
            if not particle.is_alive():
                self.particles.remove(particle)

    def render_particles(self, screen):
        for particle in self.particles:
            pygame.draw.circle(screen, particle.color, (int(particle.position[0]), int(particle.position[1])), 5)  # Draw particles as circles

    def clear_particles(self):
        self.particles.clear()