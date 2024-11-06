import pygame
import random
import time
import math
import datetime
import json

pygame.init()

pygame.display.set_caption('Snake v2.0')

with open("data.json", "r", encoding="utf8") as data:
    content = json.load(data)
    settings = content["settings"]
    playerdata = content["player"]
data.close()

# screen size
framerate = settings["game-speed"]
game_size = settings["resolution"]
window_surface = pygame.display.set_mode((60 * game_size[0], 60 * game_size[1])) # 50px x 50px snake + 5px margin on each side of each axis

# background setup
background = pygame.Surface((game_size[0] * 60, game_size[1] * 60))
background.fill(pygame.Color('#000000'))

is_running = True
moving = True
paused = False
won = False
now = datetime.datetime.now()

# add two arrays as vectors
def vector_sum(vector1, vector2):
    res = []
    for i in range(len(vector1)):
        res.append(vector1[i] + vector2[i])

    return res

icons = [pygame.image.load(f"icon/icon-{i}.png") for i in range(1,9)]
icn = 0

win = pygame.image.load("win.png")

class pause:
    sprite = pygame.image.load("pause.png")
    coords = [random.randint(0,game_size[0]*60 - sprite.get_width()), random.randint(0,game_size[1]*60 - sprite.get_height())]
    direction = [random.choice([-1,1]), random.choice([-1,1])]
    def render_other_sprites():
        window_surface.blit(apple.sprite, (apple.coords[0]*60 + 5, 60 * game_size[1] - apple.coords[1]*60 + 5))
        for i in range(1, player.size+1):
            window_surface.blit(player.body, (player.coords[i][0]*60 + 5, 60 * game_size[1] - player.coords[i][1]*60 + 5))
        window_surface.blit(player.head, (player.coords[0][0]*60 + 5, 60 * game_size[1] - player.coords[0][1]*60 + 5))

class player:
    body = pygame.image.load("body.png")
    original_head = pygame.transform.rotate(pygame.image.load("head-1.png"), 90)
    head = original_head
    coords = [[int(game_size[0]/2) + 1, int(game_size[1]/2)],[int(game_size[0]/2), int(game_size[1]/2)],[int(game_size[0]/2) - 1, int(game_size[1]/2)]]
    direction = [1,0]
    size = 2
    turns = []
    def move():
        if moving:
            for i in range(player.size, 0, -1):  
                player.coords[i] = player.coords[i - 1][:]  

            player.coords[0] = vector_sum(player.coords[0], player.direction)
    def turn():
        if player.turns != []:
            if player.direction[0] != -player.turns[0][0] and player.direction[1] != -player.turns[0][1]: 
                player.direction = player.turns[0]
            player.turns.pop(0)

class apple:
    sprite = pygame.image.load("apple.png")
    coords = [int(2/3 * game_size[0]), int(game_size[1]/2)]
    def new_apple():
        while True:
            apple.coords = [random.randint(1, game_size[0]-1), random.randint(1, game_size[1]-1)]
            if apple.coords not in player.coords or won:
                break

while is_running:
    window_surface.fill("black")
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            is_running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_UP, pygame.K_w] and player.direction != [0, -1]:
                #player.direction = [0,1]
                player.turns.append([0,1])
                player.head = pygame.transform.rotate(player.original_head, 90)
            if event.key in [pygame.K_DOWN, pygame.K_s] and player.direction != [0, 1]:
                #player.direction = [0,-1]
                player.turns.append([0,-1])
                player.head = pygame.transform.rotate(player.original_head, 270)
            if event.key in [pygame.K_RIGHT, pygame.K_d] and player.direction != [-1, 0]:
                #player.direction = [1,0]
                player.turns.append([1,0])
                player.head = player.original_head
            if event.key in [pygame.K_LEFT, pygame.K_a] and player.direction != [1, 0]:
                #player.direction = [-1,0]
                player.turns.append([-1,0])
                player.head = pygame.transform.rotate(player.original_head, 180)
            if event.key == pygame.K_r:
                player.coords = [[int(game_size[0]/2) + 1, int(game_size[1]/2)],[int(game_size[0]/2), int(game_size[1]/2)],[int(game_size[0]/2) - 1, int(game_size[1]/2)]]
                player.direction = [1,0]
                player.size = 2
                moving = True
                paused = False
                won = False
                apple.coords = [int(2/3 * game_size[0]), int(game_size[1]/2)]
                player.head = player.original_head
            if event.key == pygame.K_p and not (min(max(-1, player.coords[0][0]), game_size[0]) in [-1, game_size[0]] or min(max(0, player.coords[0][1]), game_size[1]+1) in [0, game_size[1]+1] or player.coords[0] in player.coords[1:len(player.coords)]):
                paused = not paused
                moving = not moving

    window_surface.blit(apple.sprite, (apple.coords[0]*60 + 5, 60 * game_size[1] - apple.coords[1]*60 + 5))
    for i in range(1, player.size+1):
        window_surface.blit(player.body, (player.coords[i][0]*60 + 5, 60 * game_size[1] - player.coords[i][1]*60 + 5))
    window_surface.blit(player.head, (player.coords[0][0]*60 + 5, 60 * game_size[1] - player.coords[0][1]*60 + 5))
    if not paused: pygame.display.update()
    if (datetime.datetime.now() - now).total_seconds() < 1/framerate and not paused and not won: continue

    if player.coords[0] == apple.coords:
        player.coords.append(player.coords[player.size])
        player.size += 1
        apple.new_apple()

    if min(max(-1, player.coords[0][0]), game_size[0]) in [-1, game_size[0]] or min(max(0, player.coords[0][1]), game_size[1]+1) in [0, game_size[1]+1]:
        moving = False
        player.coords[0] = player.coords[1]
        player.coords.append(vector_sum(player.coords[player.size], [-player.direction[0], -player.direction[1]]))
        if player.size - 2 > playerdata["highscore"]:
            with open("data.json", "w", encoding="utf8") as data:
                playerdata["highscore"] = player.size - 2
                new_data = {
                    "settings" : settings,
                    "player" : playerdata
                }
                data.write(str(new_data).replace("'", "\""))
            data.close()
        player.size += 1

    if player.coords[0] in player.coords[1:len(player.coords)]:
        moving = False
        if player.size - 2 > playerdata["highscore"]:
            with open("data.json", "w", encoding="utf8") as data:
                playerdata["highscore"] = player.size - 2
                new_data = {
                    "settings" : settings,
                    "player" : playerdata
                }
                data.write(str(new_data).replace("'", "\""))
            data.close()

    if paused:
        if min(max(0, pause.coords[0]), game_size[0]*60-pause.sprite.get_width()) in [0, game_size[0]*60-pause.sprite.get_width()]:
            pause.direction[0] = - pause.direction[0]
        if min(max(0, pause.coords[1]), game_size[1]*60-pause.sprite.get_height()) in [0, game_size[1]*60-pause.sprite.get_height()]:
            pause.direction[1] = - pause.direction[1]

        window_surface.fill("black")
        pause.render_other_sprites()
        window_surface.blit(pause.sprite, (pause.coords[0], pause.coords[1]))
        time.sleep(0.1/60)
        pygame.display.update()
        pause.coords = vector_sum(pause.coords, pause.direction)


    if player.size + 1 >= game_size[0] * game_size[1] and not won:
        moving = False
        for x in range(0, win.get_width(), 2):
            win_copy = pygame.transform.scale(win, (x, int(win.get_height()/2)))
            
            window_surface.fill("black")
            pause.render_other_sprites()
            window_surface.blit(win_copy, (int(30*game_size[0] - win_copy.get_width()/2), int(30*game_size[1] - win_copy.get_height()/2)))

            pygame.display.update()
        for y in range(int(win.get_height()/2), win.get_height(), 2):
            win_copy = pygame.transform.scale(win, (win.get_width(), y))

            window_surface.fill("black")
            pause.render_other_sprites()
            window_surface.blit(win_copy, (int(30*game_size[0] - win_copy.get_width()/2), int(30*game_size[1] - win_copy.get_height()/2)))

            pygame.display.update()
        window_surface.blit(win_copy, (int(30*game_size[0] - win_copy.get_width()/2), int(30*game_size[1] - win_copy.get_height()/2)))
        won = True

    if won:
        window_surface.blit(win_copy, (int(30*game_size[0] - win_copy.get_width()/2), int(30*game_size[1] - win_copy.get_height()/2)))
    # finish the frame
    now = datetime.datetime.now()
    pygame.display.set_icon(icons[icn])
    if icn < 7: icn += 1
    else: icn = 0
    pygame.display.set_caption(f'Snake v2.0 --- score: {player.size - 2} --- highscore: {playerdata["highscore"]}')
    player.turn()
    player.move()