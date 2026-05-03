import math
from random import random

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
        # Newton's 2nd Law: F = m*a → a = F/m
        acceleration = Vector2D(self.force.x / self.mass, self.force.y / self.mass)
        self.velocity = self.velocity + acceleration * dt
        self.position = self.position + self.velocity * dt
        self.force = Vector2D()  
class Explosion:
    def __init__(self, position, color=(255, 200, 0)):
        self.particles = []
        for _ in range(30):  
            velocity = Vector2D(random.uniform(-200, 200), random.uniform(-200, 200))
            self.particles.append({
                "pos": Vector2D(position.x, position.y),
                "vel": velocity,
                "life": random.randint(20, 40)
            })
        self.color = color

    def update(self):
        for p in self.particles:
            p["pos"] = p["pos"] + p["vel"] * 0.05
            p["life"] -= 1
        self.particles = [p for p in self.particles if p["life"] > 0]

class PhysicsWorld:
    def __init__(self):
        self.bodies = []

    def add_body(self, body):
        self.bodies.append(body)

    def step(self, dt):
        for body in self.bodies:
            body.update(dt)
        self.handle_collisions()

    def handle_collisions(self):
        for i in range(len(self.bodies)):
            for j in range(i+1, len(self.bodies)):
                a, b = self.bodies[i], self.bodies[j]
                dist = (a.position - b.position).magnitude()
                if dist < a.radius + b.radius:
                    if a.controllable and b.enemy:
                        return "explosion"
                    if b.controllable and a.enemy:
                        return "explosion"
                    self.resolve_collision(a, b)

    def resolve_collision(self, a, b):
        normal = (a.position - b.position).normalize()
        relative_velocity = a.velocity - b.velocity
        vel_along_normal = relative_velocity.x * normal.x + relative_velocity.y * normal.y

        if vel_along_normal > 0:
            return  
        
        restitution = 1.0
        impulse_mag = -(1 + restitution) * vel_along_normal
        impulse_mag /= (1/a.mass + 1/b.mass)

        impulse = normal * impulse_mag
        a.velocity = a.velocity + impulse * (1/a.mass)
        b.velocity = b.velocity - impulse * (1/b.mass)


if __name__ == "__main__":
    world = PhysicsWorld()

    ball1 = RigidBody(mass=2.0, position=Vector2D(0, 0), velocity=Vector2D(5, 0), radius=1.0)
    ball2 = RigidBody(mass=2.0, position=Vector2D(10, 0), velocity=Vector2D(-5, 0), radius=1.0)

    world.add_body(ball1)
    world.add_body(ball2)

    for step in range(10):
        world.step(0.1)
        print(f"Step {step}: Ball1 {ball1.position}, Ball2 {ball2.position}")
