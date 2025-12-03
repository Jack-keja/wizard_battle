"""
Wizards Battle - A 2D arcade game built with Pygame Zero

A wizard must defend against approaching enemies by casting fireballs.
Features real-time combat, enemy AI, animations, and scoring system.

Author: [Your Name]
Date: [Current Date]
Python Version: 3.6+
Dependencies: pgzero, time, random
"""

import pgzrun
import time
from random import randint
import random

# ============================================================================
# GAME CONFIGURATION AND CONSTANTS
# ============================================================================

# Screen dimensions - defines the game window size
WIDTH = 500
HEIGHT = 550

# ============================================================================
# GAME ACTORS AND SPRITES
# ============================================================================

# Main player character - wizard sprite
wizard = Actor("wizard")
wizard.pos = (WIDTH/2, HEIGHT/2)  # Center of screen

# Projectile that wizard shoots
fire_ball = Actor("fire_ball")
fire_ball.pos = (wizard.x + 50, wizard.y)  # Start near wizard

# Enemy character with random spawn position
enemy = Actor("enemy_stand")
# Spawn enemy on left or right side, avoiding center area
enemy.x = random.choice([
    randint(10, (WIDTH/2)-200),           # Left side spawn
    randint((WIDTH/2)+200, WIDTH-10)      # Right side spawn
])
enemy.y = randint(50, HEIGHT-50)          # Random vertical position

# Animation frames for enemy death sequence
enemy_frames = ['enemy_running', 'enemy_die']  # Ensure these image files exist

# UI and background elements
gameover_img = Actor("gameover")
background = Actor("background")

# ============================================================================
# GAME STATE VARIABLES
# ============================================================================

# Scoring and timing
score = 0                    # Player's current score
start_time = 0              # Game start timestamp
total_time = 5              # Total time per round (seconds)
time_left = total_time      # Remaining time in current round
time_passed = 0             # Elapsed time since round start

# Game state flags
attack = False              # Whether fireball is currently being shot
game_over = False          # Whether game has ended
flip = False               # Whether wizard is facing left (True) or right (False)
dead = False               # Legacy variable (consider removing)

# Animation control variables
death_animation_timer = 0           # Counter for death animation frames
death_animation_playing = False     # Whether death animation is active
DEATH_FRAME_DURATION = 10          # Update cycles per animation frame

# ============================================================================
# MAIN GAME FUNCTIONS
# ============================================================================

def draw():
    """
    Render all game elements to the screen.
    
    This function is called automatically by Pygame Zero every frame.
    Handles both game-over screen and main gameplay rendering.
    """
    global game_over, time_left, score
    
    if game_over:
        # Game over screen rendering
        screen.fill("white")
        screen.draw.text(f"Score: {score}", color="black", topleft=(250, 25))
        screen.draw.text("press n to start again", color="black", topleft=(180, 50))
        gameover_img.draw()
    else:
        # Main gameplay screen rendering
        background.draw()
        
        # HUD elements
        screen.draw.text(f"Score: {score}", color="white", topleft=(10, 10))
        screen.draw.text(f"time: {round(time_left, 1)}", color="pink", topleft=(10, 30))
        
        # Debug information (remove in production)
        if death_animation_playing:
            screen.draw.text("DEATH ANIMATION PLAYING", color="red", topleft=(10, 50))
            screen.draw.text(f"Timer: {death_animation_timer}", color="red", topleft=(10, 70))
        
        # Draw all game actors
        wizard.draw()
        enemy.draw()
        fire_ball.draw()

def update():
    """
    Update game logic and handle all game mechanics.
    
    Called automatically by Pygame Zero every frame.
    Manages timing, movement, collisions, and game state transitions.
    """
    global game_over, score, start_time, time_left, time_passed, attack, fire_ball, flip
    global death_animation_playing, death_animation_timer
    
    # Update game timer
    time_passed = time.time() - start_time
    time_left = total_time - time_passed
    
    if not game_over:
        # Handle death animation sequence
        if death_animation_playing:
            update_death_animation()
        else:
            # Normal enemy AI movement (only when not dying)
            handle_enemy_movement()
        
        # Fireball mechanics
        handle_fireball_logic()
        
        # Collision detection
        handle_collisions()
        
        # Check for time expiration
        if time_left <= 0:
            print(f"Game over! Final score: {score}")
            game_over = True
    else:
        # Game over state - check for restart
        if keyboard.n:
            restart_game()

def handle_enemy_movement():
    """
    Control enemy AI movement and collision detection.
    
    Enemy intelligently tracks the wizard's position and moves toward them.
    Uses mathematical slope calculation for smooth diagonal movement.
    """
    global game_over
    
    # Check if enemy has reached wizard (game over condition)
    if abs(wizard.x - enemy.x) <= 30:  # Within collision distance
        game_over = True
        return
    
    # Calculate movement direction and update enemy position
    if wizard.x > enemy.x:
        # Wizard is to the right - move right and face right
        enemy.image = "enemy_running_flip"
        enemy.x += 1
        # Calculate vertical movement using slope
        if wizard.x != enemy.x:  # Avoid division by zero
            enemy.y += (wizard.y - enemy.y) / (wizard.x - enemy.x + 0.001)
    else:
        # Wizard is to the left - move left and face left
        enemy.image = "enemy_running"
        enemy.x -= 1
        # Calculate vertical movement using slope
        if wizard.x != enemy.x:  # Avoid division by zero
            enemy.y -= (wizard.y - enemy.y) / (wizard.x - enemy.x + 0.001)

def handle_fireball_logic():
    """
    Manage fireball shooting, movement, and player controls.
    
    Handles both active fireball movement and player input for new shots.
    """
    global attack, flip
    
    if attack:
        # Move active fireball
        if flip:
            fire_ball.x -= 9  # Move left
        else:
            fire_ball.x += 9  # Move right
        
        # Check if fireball has left screen bounds
        if fire_ball.x >= WIDTH or fire_ball.x <= 0:
            attack = False
        
        # Allow limited movement while shooting
        movement(2)  # Slower movement during attack
    else:
        # Normal movement and fireball positioning
        movement(10)  # Full speed movement
        
        # Position fireball relative to wizard
        fire_ball.y = wizard.y
        fire_ball.x = wizard.x + (-20 if flip else 20)
        
        # Keep wizard within screen bounds
        wizard.y = max(20, min(HEIGHT-20, wizard.y))
        
        # Check for shoot input
        if keyboard.space:
            sounds.lasergun.play()  # Play shooting sound
            attack = True

def handle_collisions():
    """
    Detect and handle collisions between game objects.
    
    Currently handles fireball-enemy collisions, triggering death animation
    and score updates.
    """
    global score, attack
    
    # Check fireball hitting enemy
    if (fire_ball.colliderect(enemy) and attack and not death_animation_playing):
        print("Enemy hit! Starting death animation...")
        trigger_death()
        score += 10  # Award points
        
        # Reset fireball position
        fire_ball.y = wizard.y
        fire_ball.x = wizard.x
        attack = False
        
        # Reset round timer
        reset_time()

def update_death_animation():
    """
    Handle the enemy death animation sequence.
    
    Cycles through animation frames and manages timing.
    When complete, triggers enemy regeneration.
    """
    global death_animation_timer, death_animation_playing
    
    death_animation_timer += 1
    
    # Calculate which animation frame to display
    frame_index = death_animation_timer // DEATH_FRAME_DURATION
    
    print(f"Animation timer: {death_animation_timer}, Frame index: {frame_index}")
    
    if frame_index < len(enemy_frames):
        # Display current animation frame
        enemy.image = enemy_frames[frame_index]
        print(f"Changed enemy image to: {enemy_frames[frame_index]}")
    else:
        # Animation sequence complete
        print("Death animation complete!")
        death_animation_playing = False
        death_animation_timer = 0
        enemy_regeneration()

def trigger_death():
    """
    Initialize the enemy death animation sequence.
    
    Sets flags and resets counters to begin the death animation.
    """
    global death_animation_playing, death_animation_timer
    print("Triggering death animation...")
    death_animation_playing = True
    death_animation_timer = 0

def reset_time():
    """
    Reset the game timer for a new round.
    
    Updates the start time and resets the countdown timer.
    """
    global time_left, start_time, total_time
    start_time = time.time()
    time_left = total_time

def enemy_regeneration():
    """
    Respawn the enemy at a new random location.
    
    Resets enemy state, position, and animation flags.
    Called after death animation completes.
    """
    global death_animation_playing, death_animation_timer
    
    print("Regenerating enemy...")
    
    # Reset enemy appearance and state
    enemy.image = "enemy_stand"
    death_animation_playing = False
    death_animation_timer = 0
    
    # Generate new random position (avoiding center area)
    enemy.x = random.choice([
        randint(10, (WIDTH/2)-200),
        randint((WIDTH/2)+200, WIDTH-10)
    ])
    enemy.y = randint(50, HEIGHT-50)

def movement(velocity):
    """
    Handle player movement and sprite direction changes.
    
    Args:
        velocity (int): Movement speed in pixels per frame
        
    Processes keyboard input for wizard movement and handles sprite flipping
    based on direction faced.
    """
    global flip, attack
    
    # Vertical movement
    if keyboard.down:
        wizard.y += velocity
    if keyboard.up:
        wizard.y -= velocity
    
    # Horizontal movement and sprite direction (only when not attacking)
    if not attack:
        if keyboard.left:
            flip = True  # Facing left
            wizard.image = "wizard_flip"
            fire_ball.image = "fire_ball_flip"
        if keyboard.right:
            flip = False  # Facing right
            wizard.image = "wizard"
            fire_ball.image = "fire_ball"

def restart_game():
    """
    Reset all game variables and restart the game.
    
    Called when player presses 'N' after game over.
    """
    global game_over, score
    
    game_over = False
    score = 0  # Reset score for new game
    enemy_regeneration()
    reset_time()

# ============================================================================
# GAME INITIALIZATION AND STARTUP
# ============================================================================

# Initialize the game timer
reset_time()

# Start the game loop
pgzrun.go()