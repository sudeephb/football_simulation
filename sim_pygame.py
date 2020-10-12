import pygame
from sys import exit 
import random


pygame.init()
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Football match simulation')
bg = pygame.image.load('football_field.jpg').convert()


# (x,y) positions of all the players
gk_pos = (200, 520)
lb_pos = (50, 400)
lcb_pos = (125, 450)
rcb_pos = (275, 450)
rb_pos = (350, 400)

lm_pos = (75, 300)
cm_pos = (200, 350)
rm_pos = (325, 300)

lw_pos = (75, 150)
st_pos = (200, 170)
rw_pos = (325, 150)

barca_kit_nums = [1, 18, 15, 3, 20, 8, 5, 21, 11, 7, 10]
city_kit_nums = [31, 22, 14, 5, 2, 16, 25, 17, 20, 10, 7]


player_positions = [gk_pos, lb_pos, lcb_pos, rcb_pos, rb_pos, lm_pos, cm_pos, rm_pos, lw_pos, st_pos, rw_pos]


player_positions_1 = [list(x) for x in player_positions]


player_positions_2 = [[WIDTH - position[0], HEIGHT - position[1]] for position in player_positions_1]

print(player_positions_2)

pitch_top_left = (23,42)
pitch_bottom_right = (377,558)

d_box_y = (475, 125)

# don't let them get too far from initial position?
def move_player_random(position):
    pos_x, pos_y = position
    pos_x = pos_x + (random.random()-0.5)*2
    pos_y = pos_y + (random.random()-0.5)*2

    if pos_x < pitch_top_left[0]:
        pos_x = pitch_top_left[0]+4
    if pos_x > pitch_bottom_right[0]:
        pos_x = pitch_bottom_right[0]-4

    if pos_y < d_box_y[1]:
        pos_y = d_box_y[1]
    if pos_y > d_box_y[0]:
        pos_y = d_box_y[0]

    return [pos_x, pos_y]
        
font = pygame.font.SysFont('Arial', 25)


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill((255,0,0))
    screen.blit(bg, [0, 0])
    pygame.display.flip()



    # if kit num len == 1, player_pos - 15/3

    #team1
    pygame.draw.circle(screen, (0,0,0), (player_positions_1[0][0], player_positions_1[0][1]), 15)
    screen.blit(font.render(str(barca_kit_nums[0]), True, (255,255,255)), (player_positions_1[0][0] - 15/3, player_positions_1[0][1] - 15/3))
    for i, position in enumerate(player_positions_1[1:]):
        pygame.draw.circle(screen, (255,0,0), (position[0], position[1]), 15)
        screen.blit(font.render(str(barca_kit_nums[i+1]), True, (255,255,255)), (position[0] - 15/2, position[1] - 15/2))
    player_positions_1[1:] = [move_player_random(position) for position in player_positions_1[1:]]

    #team2
    pygame.draw.circle(screen, (255,255,255), (player_positions_2[0][0], player_positions_2[0][1]), 15)
    screen.blit(font.render(str(city_kit_nums[0]), True, (0,0,0)), (player_positions_2[0][0] - 15/2, player_positions_2[0][1] - 15/2))
    for i, position in enumerate(player_positions_2[1:]):
        pygame.draw.circle(screen, (0,0,255), (position[0], position[1]), 15)
        screen.blit(font.render(str(city_kit_nums[i+1]), True, (255,255,255)), (position[0] - 15/2, position[1] - 15/2))

    player_positions_2[1:] = [move_player_random(position) for position in player_positions_2[1:]]



    pygame.display.update()
pygame.quit()
exit()