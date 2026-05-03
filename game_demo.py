from tracemalloc import start
import pygame
import sys
import math
import random
import time

class Vector2D:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y
    def __add__(self, other): return Vector2D(self.x + other.x, self.y + other.y)
    def __sub__(self, other): return Vector2D(self.x - other.x, self.y - other.y)
    def __mul__(self, scalar): return Vector2D(self.x * scalar, self.y * scalar)
    def magnitude(self): return math.sqrt(self.x**2 + self.y**2)
    def normalize(self):
        mag = self.magnitude()
        return Vector2D(self.x/mag, self.y/mag) if mag != 0 else Vector2D()

class RigidBody:
    def __init__(self, mass=1.0, position=None, velocity=None, radius=20, controllable=False, enemy=False):
        self.mass = mass
        self.position = position if position else Vector2D()
        self.velocity = velocity if velocity else Vector2D()
        self.radius = radius
        self.controllable = controllable
        self.enemy = enemy
    def update(self, dt):
        self.position = self.position + self.velocity * dt


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

    def draw(self, screen):
        for p in self.particles:
            pygame.draw.circle(screen, self.color, (int(p["pos"].x), int(p["pos"].y)), 3)
        for explosion in explosions:
            explosion.update()
            explosion.draw(screen)
    def update(self, dt):
        self.position = self.position + self.velocity * dt

class PhysicsWorld:
    def __init__(self):
        self.bodies = []
    def add_body(self, body): self.bodies.append(body)
    def step(self, dt):
        for body in self.bodies:
            body.update(dt)
        return self.handle_collisions()
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
        
        return None

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

world = PhysicsWorld()

player = RigidBody(mass=2.0, position=Vector2D(400, 300), radius=25, controllable=True)
enemy1 = RigidBody(mass=2.0, position=Vector2D(200, 200), velocity=Vector2D(200, 150), radius=20, enemy=True)
enemy2 = RigidBody(mass=2.0, position=Vector2D(600, 400), velocity=Vector2D(-280, -140), radius=20, enemy=True)

world.add_body(player)
world.add_body(enemy1)
world.add_body(enemy2)

speed = 550  
game_over = False
explosions = []
start_time = time.time()
last_increase = time.time()
world.display_time = time.time()
font = pygame.font.SysFont(None, 36)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over:
            world.bodies = [player]
            player.position = Vector2D(400, 300)
            player.velocity = Vector2D()
            explosions.clear()
            game_over = False
            start_time = time.time()
            world.display_time = time.time()
            last_increase = time.time()
    elapased = time.time() - world.display_time
    if elapased > 10:
        world.display_time = time.time()
        new_enemy = RigidBody(mass=2.0, 
                              position=Vector2D(random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50)),
                              velocity=Vector2D(random.uniform(-300, 300), random.uniform(-300, 300)), 
                              radius=20, enemy=True)
        world.add_body(new_enemy)
    if game_over == True:
        world.add_body(new_enemy=False)

    if not game_over:
        keys = pygame.key.get_pressed()
        player.velocity = Vector2D()
        if keys[pygame.K_LEFT]:
            player.velocity.x = -speed
        if keys[pygame.K_RIGHT]:
            player.velocity.x = speed
        if keys[pygame.K_UP]:
            player.velocity.y = -speed
        if keys[pygame.K_DOWN]:
            player.velocity.y = speed

        result = world.step(1/60.0)
        if result == "explosion":
            game_over = True
            explosions.append(Explosion(player.position))

    
        for body in world.bodies:
            if body.position.x - body.radius < 0 or body.position.x + body.radius > WIDTH:
                body.velocity.x *= -1
            if body.position.y - body.radius < 0 or body.position.y + body.radius > HEIGHT:
                body.velocity.y *= -1

    
    screen.fill((30, 30, 30))
    for body in world.bodies:
        if body.controllable:
            color = (50, 200, 50)
        elif body.enemy:
            color = (200, 50, 50)
        else:
            color = (100, 100, 200)
        pygame.draw.circle(screen, color,
                           (int(body.position.x), 
                            int(body.position.y)),
                            int(body.radius))

    if not game_over:
        elapsed = time.time() - start_time
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        time_text = f"Time: {minutes:02d}:{seconds:02d}"
        text_surface = font.render(time_text, True, (255, 255, 255))
        screen.blit(text_surface, (10, 10)) 
        if time.time() - last_increase > 120:
             for body in world.bodies:
                if body.enemy:
                    body.velocity.x *= 1.5  
                    body.velocity.y *= 1.15
                    last_increase = time.time() 
 
        
    else:
        game_over = True
        elapsed = elapsed
        font = pygame.font.SysFont(None, 72)
        text = font.render("!!!GAME OVER!!!", True, (255, 155, 0))
        screen.blit(text, (215, HEIGHT//2 - 150))
        timer = font.render(f"Time: {minutes:02d}:{seconds:02d}", True, (255, 255, 255))
        screen.blit(timer, (215, HEIGHT//2 - 200))

    pygame.display.flip()
    clock.tick(60)