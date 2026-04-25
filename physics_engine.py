import math

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
        self.radius = radius  # for collision

    def apply_force(self, force):
        self.force = self.force + force

    def update(self, dt):
        # Newton's 2nd Law: F = m*a → a = F/m
        acceleration = Vector2D(self.force.x / self.mass, self.force.y / self.mass)
        self.velocity = self.velocity + acceleration * dt
        self.position = self.position + self.velocity * dt
        self.force = Vector2D()  # reset force after update

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
                    # Simple elastic collision response
                    self.resolve_collision(a, b)

    def resolve_collision(self, a, b):
        normal = (a.position - b.position).normalize()
        relative_velocity = a.velocity - b.velocity
        vel_along_normal = relative_velocity.x * normal.x + relative_velocity.y * normal.y

        if vel_along_normal > 0:
            return  # already separating

        # Elastic collision impulse
        restitution = 1.0  # perfectly elastic
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
