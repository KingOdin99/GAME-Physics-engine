import math
import random
import tracemalloc
import pygame
from tracemalloc import start

class Vector2D:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self):
        mag = self.magnitude()
        return Vector2D(self.x/mag, self.y/mag) if mag != 0 else Vector2D()

    def __repr__(self):
        return f"({self.x:.2f}, {self.y:.2f})"
    
class RigidBody:
    def __init__(self, mass=1.0, position=None, velocity=None, radius=1.0):
        self.mass = mass
        self.position = position if position else Vector2D()
        self.velocity = velocity if velocity else Vector2D()
        self.force = Vector2D()
        self.radius = radius  

    def apply_force(self, force):
        self.force = self.force + force

    def update(self, dt):
        acceleration = Vector2D(self.force.x / self.mass, self.force.y / self.mass)
        self.velocity = self.velocity + acceleration * dt
        self.position = self.position + self.velocity * dt
        self.force = Vector2D()

class PhysicsWorld:
    def __init__(self):
        self.bodies = []

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
world = PhysicsWorld()
player = RigidBody(mass=1.0, position=Vector2D(WIDTH/2, HEIGHT/2), radius=20, controllable=True)
world.bodies.append(player)

speed = 200