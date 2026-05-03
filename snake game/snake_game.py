import pygame, sys, random, time

pygame.init()
width, height = 400, 400
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

snake = [(100,100)]
direction = (20,0)
food = (random.randint(0, (width-20)//20)*20,
        random.randint(0, (height-20)//20)*20)

speed = 10
game_over = False
start_time = time.time()
last_increase = time.time()
grid_surface = pygame.Surface((width, height), pygame.SRCALPHA)
for x in range(0, width, 20):
    pygame.draw.line(grid_surface, (40, 40, 40, 80), (x, 0), (x, height))
for y in range(0, height, 20):
    pygame.draw.line(grid_surface, (40, 40, 40, 80), (0, y), (width, y))


def reset_game():
    global snake, direction, food, speed, game_over, start_time, last_increase
    snake = [(100,100)]
    direction = (20,0)
    food = (random.randint(0, (width-20)//20)*20,
            random.randint(0, (height-20)//20)*20)
    speed = 8
    game_over = False
    start_time = time.time()
    last_increase = time.time()
    

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0,20): direction = (0,-20)
            elif event.key == pygame.K_DOWN and direction != (0,-20): direction = (0,20)
            elif event.key == pygame.K_LEFT and direction != (20,0): direction = (-20,0)
            elif event.key == pygame.K_RIGHT and direction != (-20,0): direction = (20,0)
            elif event.key == pygame.K_r and game_over: reset_game()

    if not game_over:
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        snake.insert(0, new_head)

        if new_head[0] < 0 or new_head[0] >= width or new_head[1] < 0 or new_head[1] >= height:
            game_over = True

        if new_head in snake[1:]:
            game_over = True

        if new_head == food:
            food = (random.randint(0, (width-20)//20)*20,
                    random.randint(0, (height-20)//20)*20)
        else:
            snake.pop()

        if time.time() - last_increase > 10:
            speed += 2
            last_increase = time.time()

    screen.fill((0,0,0))
    for x in range(0, width, 20):
        pygame.draw.line(screen, (200,200,200), (x,0), (x,height))
    for y in range(0, height, 20):
        pygame.draw.line(screen, (200,200,200), (0,y), (width,y))

    for i, segment in enumerate(snake):
        if i == 0:  # head
            pygame.draw.rect(screen, (0,200,0), (segment[0], segment[1], 20, 20))
            pygame.draw.circle(screen, (255,255,255), (segment[0]+5, segment[1]+5), 3)
            pygame.draw.circle(screen, (255,255,255), (segment[0]+15, segment[1]+5), 3)
        else:       # body
            pygame.draw.rect(screen, (0,255,0), (segment[0], segment[1], 20, 20))

    
    pygame.draw.rect(screen, (255,0,0), (food[0], food[1], 20, 20))

    if game_over:
        text = font.render("Game Over!", True, (255,255,255))
        screen.blit(grid_surface, (0,0))
        screen.blit(text, (width//2 - text.get_width()//2, height//2 - text.get_height()//2))

    pygame.display.flip()
    clock.tick(speed)
