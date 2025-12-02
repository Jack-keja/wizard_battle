import pgzrun
import time
from random import randint
import random

# screen settings
WIDTH = 500
HEIGHT = 550

# character setting
wizard = Actor("wizard")
wizard.pos = (WIDTH/2, HEIGHT/2)
fire_ball = Actor("fire_ball")
fire_ball.pos = (wizard.x + 50 , wizard.y)
enemy = Actor("enemy_stand")
enemy.x = random.choice([randint(10 , (WIDTH/2)-200),randint((WIDTH/2)+200,WIDTH-10)])
enemy.y = randint(50 , HEIGHT-50)
enemy_frames = ['enemy_running', 'enemy_die']
gameover_img = Actor("gameover")
background = Actor("background")



# Game variables
score = 0
start_time = 0
total_time = 5
time_left = total_time
time_passed = 0
attack = False
game_over = False
flip = False
dead = False
death_index = 0

death_animation_playing = False  # New flag to track animation state

# draw everything on screen
def draw():
    global game_over,time_left,score,velocity
    if game_over: # end screen
        screen.fill("white")
        screen.draw.text("Score: " + str(score), color = "black", topleft=(250, 25))
        screen.draw.text("press n to start again", color = "black", topleft=(180, 50))
        gameover_img.draw()
    else:
        #screen.fill("white")
        background.draw()
        screen.draw.text("Score: " + str(score), color = "white", topleft=(10, 10))
        screen.draw.text("time: " + str(round(time_left,1)), color = "pink", topleft=(10, 30))
        wizard.draw()
        enemy.draw()
        fire_ball.draw()

def update():#control all games introductions.
    global game_over,score, start_time, time_left, time_passed,attack, fire_ball,Flip
    global death_animation_playing #including this flag

    time_passed = time.time() - start_time
    time_left = total_time - time_passed

    #check if it's gaming
    if game_over == False:
        # Don't move enemy if death animation is playing
        if not death_animation_playing:
            #enermy touch wizard, gameover
            if wizard.x == enemy.x - 30 or wizard.x == enemy.x + 30: 
                game_over = True
            # if wizard is at right of enermy, enermy move to right
            elif wizard.x > enemy.x - 30 :
                enemy.image="enemy_running_flip"
                enemy.x = enemy.x + 1
                enemy.y = enemy.y + (wizard.y - enemy.y)/(wizard.x - enemy.x+0.001)
            # if wizard is at left of enermy, enermy move to left
            else:
                enemy.image="enemy_running"
                enemy.x = enemy.x - 1
                enemy.y = enemy.y - (wizard.y - enemy.y)/(wizard.x - enemy.x+0.001)
        
        if attack:# fireball moving when attack
            if flip == True:
                fire_ball.x = fire_ball.x - 9
                
            else:
                fire_ball.x = fire_ball.x + 9
                
            if fire_ball.x >= WIDTH or fire_ball.x <= 0:
                attack = False
            movement(2)

        #movement of character and fireballs
        else:
            movement(10)
            attack = False        
            fire_ball.y = wizard.y
            if flip == True:
                fire_ball.x = wizard.x - 20
            else:
                fire_ball.x = wizard.x + 20
            wizard.y = max(20, min(HEIGHT-20, wizard.y))
            if keyboard.space:
                sounds.lasergun.play()
                #music.play_once("lasergun")
                attack = True

        # fire ball attack enemy
        if fire_ball.colliderect(enemy) and attack == True and not death_animation_playing:
            #enemy.image="enemy_die"
            trigger_death()#here, this doesnt wait for the enemy animation
            enemy_regeneration()
            score = score + 10
            fire_ball.y = wizard.y
            fire_ball.x = wizard.x
            attack = False
            reset_time()

        #no time, gameover
        if time_left <= 0:
            print("score is " , score)
            game_over = True
    else:
        if keyboard.n :# restart game
            game_over = False
            enemy_regeneration()
            reset_time()
            

# Reset time
def reset_time():
    global time_left, start_time, total_time
    start_time = time.time()
    time_left = total_time

def enemy_regeneration(): # random enemy position
    #you didnt have these variables being accessible here
    global death_animation_playing, dead,death_index
    #enemy.x = wizard.x + randint(100, 250)
    enemy.image= "enemy_stand"
    enemy.x = random.choice([randint(10 , (WIDTH/2)-200),randint((WIDTH/2)+200,WIDTH-10)])
    enemy.y = randint(50 , HEIGHT-50)
    # Reset animation flags
    death_animation_playing = False
    death_index = 0
    dead = False

def movement(velocity): # wizard movement
    global flip, attack
    if keyboard.down:
        wizard.y = wizard.y + velocity
    if keyboard.up:
        wizard.y = wizard.y - velocity
    if attack == False:
        if keyboard.left:
            flip = True
            wizard.image="wizard_flip"
            fire_ball.image="fire_ball_flip"
            
        if keyboard.right:
            flip = False
            wizard.image="wizard"
            fire_ball.image="fire_ball"

def trigger_death():
    global dead, death_index, death_animation_playing
    if not dead:
        dead = True
        death_index = 0
        death_animation_playing = True
        show_next_enemy_frame()
    
def show_next_enemy_frame():
    global death_index, death_animation_playing
    if death_index < len(enemy_frames):
        enemy.image = enemy_frames[death_index]
        death_index += 1
         # Schedule next frame in 0.5 seconds (adjust timing as needed)

        clock.schedule(show_next_enemy_frame, 0.5)  # time between frames
    else:
        # Animation finished; you can respawn, remove, or end game
        death_animation_playing = False
        enemy_regeneration()


reset_time()
pgzrun.go()