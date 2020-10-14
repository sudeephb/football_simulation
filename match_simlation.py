import pandas as pd
import numpy as np
import random
import math

fifa21 = pd.read_csv('FIFA21_official_data.csv')

relavent_fields = ['ID', 'Name', 'Overall', 'Club', 'Jersey Number',
                   'Finishing', 'ShortPassing', 'LongPassing',
                   'Best Position', 'Best Overall Rating']

players = fifa21[relavent_fields]
players = players[players['Overall'] >= 60]

barcelona_players = players[players['Club'] == 'FC Barcelona']
city_players = players[players['Club'] == 'Manchester City']

# Barcelona Starters
barcelona_players = barcelona_players.sort_values('Jersey Number')
barcelona_starters_id = [192448, 152729, 189511, 194765, 180206, 158023, 231443, 220440, 189332, 199564, 228702]
barcelona_starters = barcelona_players[barcelona_players['ID'].isin(barcelona_starters_id)]

# Man city starters
city_players = city_players.sort_values('Jersey Number')
city_starters_id = [188377, 202652, 153079, 212218, 192985, 218667, 135507, 210257, 204884, 203574, 231866]
city_starters = city_players[city_players['ID'].isin(city_starters_id)]


barcelona_starters['scoring likelihood'] = barcelona_starters.apply(lambda row: row.Finishing, axis=1)

def adjust_likelihood(jersey_num, initial_likelihood):
    if jersey_num in gk:
        return initial_likelihood/100
    if jersey_num in defense:
        return initial_likelihood
    if jersey_num in mid:
        return initial_likelihood * 2
    if jersey_num in forwards:
        return initial_likelihood * 4 

#likelihood of each barcelona player scoring
gk = [1]
defense = [3,15,18,20]
mid = [5,8,21]
forwards = [7,10,11]
weights = list(barcelona_starters['Finishing'])
barcelona_starters['scoring likelihood'] = barcelona_starters.apply(
                                                                lambda row: adjust_likelihood(row['Jersey Number'], row['scoring likelihood']), 
                                                                axis = 1)


#likelihood of each city player scoring
city_starters['scoring likelihood'] = city_starters.apply(lambda row: row.Finishing, axis=1)

gk = [31]
defense = [2, 5, 14, 22]
mid = [17, 25, 16]
forwards = [7, 10, 20]

weights = list(city_starters['Finishing'])

city_starters['scoring likelihood'] = city_starters.apply(
                                                    lambda row: adjust_likelihood(row['Jersey Number'], row['scoring likelihood']), 
                                                    axis = 1)


# assigning numnber of passes 
barca_total_passes = 650 + (random.random() - 0.5)*2*100
city_total_passes = 650 + (random.random() - 0.5)*2*100

barca_starters_numbers = [int(x) for x in list(barcelona_starters['Jersey Number'])]
city_starters_numbers = [int(x) for x in list(city_starters['Jersey Number'])]

def get_passes():
    barca_passes_byPlayers = {(p1,p2): [0, []] for p1 in barca_starters_numbers for p2 in barca_starters_numbers if p1 != p2}
    city_passes_byPlayers = {(p1,p2): [0, []] for p1 in city_starters_numbers for p2 in city_starters_numbers if p1 != p2}

    for i in range(90):
        #for this minute
        barca_passes = 7 + (random.random() - 0.5)*2*5
        city_passes = 7 + (random.random() - 0.5)*2*5
        
        #for barca
        for k in range(int(barca_passes)):
            curr_pair_choice = random.choice(list(barca_passes_byPlayers.keys()))
            barca_passes_byPlayers[curr_pair_choice][0] += 1
            barca_passes_byPlayers[curr_pair_choice][1].append(i)
        
        #for city
        for k in range(int(city_passes)):
            curr_pair_choice = random.choice(list(city_passes_byPlayers.keys()))
            city_passes_byPlayers[curr_pair_choice][0] += 1
            city_passes_byPlayers[curr_pair_choice][1].append(i)

    return [barca_passes_byPlayers, city_passes_byPlayers]


barca_passes_byPlayers, city_passes_byPlayers = get_passes()


#the game
def game():
    population = [0,1]
    weights = [29/30, 1/30]
    
    team1_score = 0
    team2_score = 0
    team1_scorers = []
    team1_score_time = []
    team2_scorers = []
    team2_score_time = []

    for i in range(90):
        team_1 = random.choices(population, weights)[0]
        team_2 = random.choices(population, weights)[0]
        
        if team_1 == 1:   #team1 scores
            scorer_population = list(barcelona_starters['Name'])
            scorer_weights = list(barcelona_starters['scoring likelihood'])
            curr_choice = random.choices([x for x in range(0,11)], scorer_weights)[0]
            curr_scorer = scorer_population[curr_choice]
            team1_scorers.append(curr_scorer)
            team1_score_time.append(i)
            # print("Goal Barcelona {}' - {}".format(i, curr_scorer))
            team1_score+=1
            
        if team_2 == 1:    #team2 scores
            scorer_population = list(city_starters['Name'])
            scorer_weights = list(city_starters['scoring likelihood'])
            curr_choice = random.choices([x for x in range(0,11)], scorer_weights)[0]
            curr_scorer = scorer_population[curr_choice]
            team2_scorers.append(curr_scorer)
            team2_score_time.append(i)
            # print("Goal Manchester City {}' - {}' ".format(i, curr_scorer))
            team2_score+=1

        
    # return 'Final Score: {} - {}'.format(team1_score, team2_score)
    return [(team1_score, team2_score), team1_score_time, team2_score_time, team1_scorers, team2_scorers]


# print(game())




(team1_score, team2_score), team1_score_time, team2_score_time, team1_scorers, team2_scorers = game()

# print('=======', barca_passes_byPlayers)


import pygame
from sys import exit 
import time

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


player_positions_1_dict = dict(zip(barca_kit_nums, player_positions_1))
player_positions_2_dict = dict(zip(city_kit_nums, player_positions_2))


#boundaries
pitch_top_left = (23,42)
pitch_bottom_right = (377,558)
d_box_y = (475, 125)

#todo: don't let them get too far from initial position?
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


def draw_line(p1, p2):
    ''' draw line between player1 and player2. Pass the coordinates as arguments '''
    pygame.draw.line(screen, (0,0,0, 0.5), p1, p2)


list_of_passes = []

initial_time = time.time()

print('-------------------', team1_score_time)
print('-------------------', team2_score_time)

team1_dynamic_score = [0]*94
team2_dynamic_score = [0]*94
for i in range(94):
    if i in team1_score_time:
        team1_dynamic_score[i:] = [x+1 for x in team1_dynamic_score[i:]]
    if i in team2_score_time:
        team2_dynamic_score[i:] = [x+1 for x in team2_dynamic_score[i:]]


game_end = False
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if not game_end:


        screen.fill((255,0,0))
        screen.blit(bg, [0, 0])
        pygame.display.flip()

        curr_time = time.time()
        #length of a real time minute
        elapsed_time = int((curr_time - initial_time)*8)
        if elapsed_time>90:
            game_end = True
        screen.blit(font.render(str(elapsed_time) + "'", True, (255,255,255)), (350, 5))
        # time.sleep(1)
        # if kit num len == 1, player_pos - 15/3


        #showing current score
        if elapsed_time <= 90:
            screen.blit(font.render("Score: {} - {}".format(team1_dynamic_score[elapsed_time], team2_dynamic_score[elapsed_time]), True, (0,0,0)), (10, 20))




        #team1
        pygame.draw.circle(screen, (0,0,0), (player_positions_1[0][0], player_positions_1[0][1]), 15)
        screen.blit(font.render(str(barca_kit_nums[0]), True, (255,255,255)), (player_positions_1[0][0] - 15/3, player_positions_1[0][1] - 15/3))
        for i, position in enumerate(player_positions_1[1:]):
            pygame.draw.circle(screen, (255,0,0), (position[0], position[1]), 15)
            screen.blit(font.render(str(barca_kit_nums[i+1]), True, (255,255,255)), (position[0] - 15/2, position[1] - 15/2))
        player_positions_1[1:] = [move_player_random(position) for position in player_positions_1[1:]]

        #line drawing test
        # draw_line(player_positions_1[0], player_positions_1[1])
        

        #passes
        # for key, value in barca_passes_byPlayers.items():
        #     if elapsed_time in value[1]:
        #         list_of_passes.append([player_positions_1_dict[key[0]], player_positions_1_dict[key[1]]])
        
        # for each in list_of_passes:
        #     draw_line(each[0], each[1])

        #show team1 goals with scorer
        for j in range(5):      #to show for 5 'game minutes'
            if elapsed_time-j in team1_score_time:
                curr_scorer = team1_scorers[team1_score_time.index(elapsed_time-j)]
                screen.blit(font.render('Goal Barcelona - {}'.format(curr_scorer), True, (255,255,255)), (50, 3))

        #show team2 goals with scorer
        for j in range(5):      #to show for 5 'game minutes'
            if elapsed_time-j in team2_score_time:
                curr_scorer = team2_scorers[team2_score_time.index(elapsed_time-j)]
                screen.blit(font.render('Goal Manchester City - {}'.format(curr_scorer), True, (255,255,255)), (50, 580))

        #team2
        pygame.draw.circle(screen, (255,255,255), (player_positions_2[0][0], player_positions_2[0][1]), 15)
        screen.blit(font.render(str(city_kit_nums[0]), True, (0,0,0)), (player_positions_2[0][0] - 15/2, player_positions_2[0][1] - 15/2))
        for i, position in enumerate(player_positions_2[1:]):
            pygame.draw.circle(screen, (0,0,255), (position[0], position[1]), 15)
            screen.blit(font.render(str(city_kit_nums[i+1]), True, (255,255,255)), (position[0] - 15/2, position[1] - 15/2))

        player_positions_2[1:] = [move_player_random(position) for position in player_positions_2[1:]]
    pygame.display.update()

    if game_end:
        screen.fill((0,0,0))
        myfont = pygame.font.SysFont('Comic Sans MS', 30)

        finalScoreText = myfont.render('Final Score: ', False, (255, 255, 255))
        screen.blit(finalScoreText,(WIDTH / 3,HEIGHT/4))

        finalScore = myfont.render("FC Barcelona {} - {} Manchester City".format(team1_score, team2_score), False, (255, 255, 255))
        screen.blit(finalScore,(30,180))



        for i,v in enumerate(team1_score_time):
                screen.blit(font.render("{}' - {}".format(v, team1_scorers[i]), True, (255,255,255)), (15, 210+i*20))

        for i,v in enumerate(team2_score_time):
                screen.blit(font.render("{}' - {}".format(v, team2_scorers[i]), True, (255,255,255)), (220, 210+i*20))        









pygame.quit()



print('='*10)
print('Final score: Barcelona {} - {} Manchester City'.format(team1_score, team2_score))
scorers_all = team1_scorers+team2_scorers
score_time_all = team1_score_time + team2_score_time
for i,v in enumerate(score_time_all):
    print("{}' - {}".format(v, scorers_all[i]))

exit()