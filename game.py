import random
import pygame

pygame.init()

width = 1920
height = 1080
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("Conway's Game of Life")
clock = pygame.time.Clock()

white = (255, 255, 255)
black = (0, 0, 0)
lime = (0, 255, 0)

running = True
started = False
show_grid = False
state_history = []
current = 0


def number_of_cells(state):
    count = 0
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == 1:
                count += 1
    return count


def next_state(state):
    global state_history, current
    state_history.append(state)
    current = len(state_history) - 1
    print(f"Generation {current}: {number_of_cells(state)} cells")
    new_state = []
    for i in range(len(state)):
        new_state.append([])
        for j in range(len(state[i])):
            new_state[i].append(0)
    for i in range(len(state)):
        for j in range(len(state[i])):
            count = 0
            for k in range(-1, 2):
                for l in range(-1, 2):
                    if i + k >= 0 and i + k < len(state) and j + l >= 0 and j + l < len(state[i]):
                        if k == 0 and l == 0:
                            continue
                        if state[i + k][j + l] == 1:
                            count += 1
            if state[i][j] == 1:
                if count < 2 or count > 3:
                    new_state[i][j] = 0
                else:
                    new_state[i][j] = 1
            else:
                if count == 3:
                    new_state[i][j] = 1
    return new_state


state = []
# fill state with 0
for i in range(width//20):
    state.append([])
    for j in range(height//20):
        state[i].append(0)


def setPaused(paused):
    global started
    started = not paused
    if(paused):
        pygame.display.set_caption("Conway's Game of Life [Paused]")
    else:
        pygame.display.set_caption("Conway's Game of Life [Running]")


setPaused(True)

while running:
    screen.fill(black)
    if show_grid:
        for i in range(0, width, 20):
            pygame.draw.line(screen, white, (i, 0), (i, height))
        for i in range(0, height, 20):
            pygame.draw.line(screen, white, (0, i), (width, i))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # clear state when escape is clicked
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                show_grid = not show_grid
            if event.key == pygame.K_ESCAPE:
                setPaused(True)
                state = []
                for i in range(width//20):
                    state.append([])
                    for j in range(height//20):
                        state[i].append(0)
        # if enter is clicked set started to true
        if event.type == pygame.KEYDOWN and not started:
            if event.key == pygame.K_RETURN:
                setPaused(False)
            # if r is pressed randomize state
            if event.key == pygame.K_r:
                for i in range(width//20):
                    for j in range(height//20):
                        state[i][j] = random.randint(0, 1)
            # if right arrow is pressed move to next state
            if event.key == pygame.K_RIGHT:
                state = next_state(state)
            # if left arrow is pressed move to previous state
            if event.key == pygame.K_LEFT:
                if current > 0:
                    current -= 1
                    state = state_history[current]
        # if space is clicked set started to false
        if event.type == pygame.KEYDOWN and started:
            if event.key == pygame.K_SPACE:
                setPaused(True)

    if pygame.mouse.get_pressed()[0] and not started:
        x, y = pygame.mouse.get_pos()
        x = x // 20
        y = y // 20
        state[x][y] = 1

    if pygame.mouse.get_pressed()[2] and not started:
        x, y = pygame.mouse.get_pos()
        x = x // 20
        y = y // 20
        state[x][y] = 0

    # draw state
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == 1:
                pygame.draw.rect(screen, lime, (i * 20, j * 20, 20, 20))

    if started:
        state = next_state(state)

    pygame.display.update()

    # if game is started run at 10 fps else run at 60 fps
    clock.tick(started and 10 or 60)
