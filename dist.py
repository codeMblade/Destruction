import pygame
import random
pygame.init()

# window
WIDTH, HEIGHT = 1300, 730
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Distruction")

# fps
FPS = 60


# player 
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_SPEED = 7
player = pygame.Rect(200, 300, PLAYER_WIDTH, PLAYER_HEIGHT)


# blocks 
BLOCKS = []
for x in range(10):
    block = pygame.Rect(random.randint(400, 1000), random.randint(100, 650), 90, 90)
    BLOCKS.append(block)


# particals 
particals = []


# colours
colours = {
    "black": (0, 0, 0),
    "gey": (20, 20, 20),
    "orange": (200, 100, 0)
}


def draw_Window(shake_x, shake_y):
    WINDOW.fill((30, 30, 30))

    for partical in particals:
        pygame.draw.circle(WINDOW, partical["colour"], (partical["x"] + shake_x, partical["y"] + shake_y), partical["size"])

    for block in BLOCKS:
        pygame.draw.rect(WINDOW, (20, 20, 20), (block.x, block.y + shake_x, block.width + shake_y, block.height))
        pygame.draw.rect(WINDOW, (0, 0, 0), (block.x + shake_x, block.y + shake_y, block.width, block.height), 3)

    pygame.draw.circle(WINDOW, (255, 255, 255), (player.centerx + shake_x, player.centery + shake_y), PLAYER_HEIGHT // 2)

    pygame.display.update()


# player moveemnt function
def player_movement():
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        player.x -= PLAYER_SPEED

    if keys[pygame.K_d]:
        player.x += PLAYER_SPEED

    if keys[pygame.K_w]:
        player.y -= PLAYER_SPEED

    if keys[pygame.K_s]:
        player.y += PLAYER_SPEED

    # player window collision
    if player.left < 0:
        player.left = 0

    if player.right > WIDTH:
        player.right = WIDTH

    if player.top < 0:
        player.top = 0

    if player.bottom > HEIGHT:
        player.bottom = HEIGHT


# spawn particals
def spawn_particals(pos):
    spawn_num = 10

    for x in range(spawn_num):
        partical = {
            "x": pos[0],
            "y": pos[1],
            "size": random.randint(5, 20),
            "speed x": random.randint(-7, 7),
            "speed y": random.randint(-7, 7),
            "life": random.randint(10, 20),
            "colour": random.choice(list(colours.values()))
        }
        particals.append(partical)


# main function
def main():
    clock = pygame.time.Clock()

    Game_running = True

    SHAKE = 15
    shake_timer = 0

    while Game_running:
        clock.tick(FPS)

        # event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Game_running = False


        # block window collision
        for block in BLOCKS:
            if block.left < 0:
                block.left =  0

            if block.right > WIDTH:
                block.right = WIDTH

            if block.top < 0:
                block.top =  0

            if block.bottom > HEIGHT:
                block.bottom = HEIGHT


        # pushing blocks
        for block in BLOCKS:
            if player.colliderect(block):
                if player.centerx < block.centerx:
                    pos = player.center
                    spawn_particals(pos)
                    shake_timer = 20
                    block.centerx += PLAYER_SPEED

                if player.centerx > block.centerx:
                    pos = player.center
                    spawn_particals(pos)                    
                    shake_timer = 20
                    block.centerx -= PLAYER_SPEED

                if player.centery > block.centery:
                    pos = player.center
                    spawn_particals(pos)                    
                    shake_timer = 20
                    block.centery -= PLAYER_SPEED

                if player.centery < block.centery:
                    pos = player.center
                    spawn_particals(pos)           
                    shake_timer = 20
                    block.centery += PLAYER_SPEED


        shake_y = 0
        shake_x = 0

        if shake_timer > 0:
            shake_x = random.randint(-SHAKE, SHAKE)
            shake_x = random.randint(-SHAKE, SHAKE)
            shake_timer -= 1


        # moving particals
        for partical in particals[:]:
            partical["x"] += partical["speed x"]
            partical["y"] += partical["speed y"]
            partical["life"] -= 1
            if partical["life"] < 0:
                particals.remove(partical)


        # player system
        player_movement()

        
        # display system
        draw_Window(shake_x, shake_y)


    pygame.quit()


# calling the main function
if __name__ == "__main__":
    main()