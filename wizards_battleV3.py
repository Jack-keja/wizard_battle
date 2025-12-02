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
enemy_frames = ['enemy_running', 'enemy_die']  # Make sure these files exist!
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
death_animation_timer = 0  # Changed from death_index
death_animation_playing = False
DEATH_FRAME_DURATION = 10  # How many update cycles per frame (adjust for speed)

def draw():
    global game_over,time_left,score
    if game_over:
        screen.fill("white")
        screen.draw.text("Score: " + str(score), color = "black", topleft=(250, 25))
        screen.draw.text("press n to start again", color = "black", topleft=(180, 50))
        gameover_img.draw()
    else:
        background.draw()
        screen.draw.text("Score: " + str(score), color = "white", topleft=(10, 10))
        screen.draw.text("time: " + str(round(time_left,1)), color = "pink", topleft=(10, 30))
        
        # Debug: Show animation state
        if death_animation_playing:
            screen.draw.text("DEATH ANIMATION PLAYING", color = "red", topleft=(10, 50))
            screen.draw.text(f"Timer: {death_animation_timer}", color = "red", topleft=(10, 70))
        
        wizard.draw()
        enemy.draw()
        fire_ball.draw()

def update():
    global game_over, score, start_time, time_left, time_passed, attack, fire_ball, flip
    global death_animation_playing, death_animation_timer
    
    time_passed = time.time() - start_time
    time_left = total_time - time_passed
    
    if game_over == False:
        # Handle death animation
        if death_animation_playing:
            update_death_animation()
        else:
            # Normal enemy movement (only when not dying)
            if wizard.x == enemy.x - 30 or wizard.x == enemy.x + 30: 
                game_over = True
            elif wizard.x > enemy.x - 30:
                enemy.image = "enemy_running_flip"
                enemy.x = enemy.x + 1
                enemy.y = enemy.y + (wizard.y - enemy.y)/(wizard.x - enemy.x+0.001)
            else:
                enemy.image = "enemy_running"
                enemy.x = enemy.x - 1
                enemy.y = enemy.y - (wizard.y - enemy.y)/(wizard.x - enemy.x+0.001)
        
        # Fireball logic
        if attack:
            if flip == True:
                fire_ball.x = fire_ball.x - 9
            else:
                fire_ball.x = fire_ball.x + 9
                
            if fire_ball.x >= WIDTH or fire_ball.x <= 0:
                attack = False
            movement(2)
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
                attack = True

        # Fire ball hits enemy
        if fire_ball.colliderect(enemy) and attack == True and not death_animation_playing:
            print("Enemy hit! Starting death animation...")  # Debug
            trigger_death()
            score = score + 10
            fire_ball.y = wizard.y
            fire_ball.x = wizard.x
            attack = False
            reset_time()

        if time_left <= 0:
            print("score is", score)
            game_over = True
    else:
        if keyboard.n:
            game_over = False
            enemy_regeneration()
            reset_time()

def update_death_animation():
    global death_animation_timer, death_animation_playing
    
    death_animation_timer += 1
    
    # Calculate which frame we should be on
    frame_index = death_animation_timer // DEATH_FRAME_DURATION
    
    print(f"Animation timer: {death_animation_timer}, Frame index: {frame_index}")  # Debug
    
    if frame_index < len(enemy_frames):
        enemy.image = enemy_frames[frame_index]
        print(f"Changed enemy image to: {enemy_frames[frame_index]}")  # Debug
    else:
        # Animation finished
        print("Death animation complete!")  # Debug
        death_animation_playing = False
        death_animation_timer = 0
        enemy_regeneration()

def trigger_death():
    global death_animation_playing, death_animation_timer
    print("Triggering death animation...")  # Debug
    death_animation_playing = True
    death_animation_timer = 0

def reset_time():
    global time_left, start_time, total_time
    start_time = time.time()
    time_left = total_time

def enemy_regeneration():
    global death_animation_playing, death_animation_timer
    print("Regenerating enemy...")  # Debug
    enemy.image = "enemy_stand"
    enemy.x = random.choice([randint(10, (WIDTH/2)-200), randint((WIDTH/2)+200, WIDTH-10)])
    enemy.y = randint(50, HEIGHT-50)
    death_animation_playing = False
    death_animation_timer = 0

def movement(velocity):
    global flip, attack
    if keyboard.down:
        wizard.y = wizard.y + velocity
    if keyboard.up:
        wizard.y = wizard.y - velocity
    if attack == False:
        if keyboard.left:
            flip = True
            wizard.image = "wizard_flip"
            fire_ball.image = "fire_ball_flip"
        if keyboard.right:
            flip = False
            wizard.image = "wizard"
            fire_ball.image = "fire_ball"

reset_time()
pgzrun.go()