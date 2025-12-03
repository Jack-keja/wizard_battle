# wizard_battle
# 🧙‍♂️ Wizards Battle

A thrilling 2D arcade-style game built with Python and Pygame Zero where you play as a wizard defending against approaching enemies using magical fireballs!

![Game Screenshot](screenshot.png) <!-- Add a screenshot of your game -->

## 🎮 Game Features

- **Real-time Combat**: Cast fireballs to defeat approaching enemies
- **Dynamic Enemy AI**: Enemies intelligently track and chase the wizard
- **Smooth Animations**: Death animations and character movement
- **Score System**: Earn points for each enemy defeated
- **Time-based Gameplay**: Survive waves of enemies within time limits
- **Directional Controls**: Move in all directions and face enemies
- **Sound Effects**: Immersive audio feedback for actions

## 🎯 Target Audience

This game is designed for:
- Beginner to intermediate computer science students
- Anyone learning Python game development
- Students showcasing programming skills for university applications
- Pygame Zero enthusiasts

## 🛠️ Dependencies

- **Python 3.6+**
- **Pygame Zero** (`pgzrun`)
- **Standard Libraries**: `time`, `random`

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/wizards_battle.git
   cd wizards_battle
2. **Install Pygame Zero**:
   ```bash
   pip install pgzero
3. **Ensure you have the required assets**:
   
   Create an images folder and add these `image` files:
   - `wizard.png`
   - `wizard_flip.png`
   - `fire_ball.png`
   - `fire_ball_flip.png`
   - `enemy_stand.png`
   - `enemy_running.png`
   - `enemy_running_flip.png`
   - `enemy_die.png`
   - `gameover.png`
   - `background.png`
4. **Add sound effects**:

   Create a `sounds` folder and add:
   - `lasergun.wav`
     
**🎮 Controls**

- **Arrow Keys**: Move the wizard (Up, Down, Left, Right)
- **Spacebar**: Cast fireball
- **N**: Restart game (when game over)

**🎯 Gameplay**

1. Use arrow keys to move your wizard around the screen
2. Enemies will spawn and chase you intelligently
3. Press spacebar to cast fireballs at enemies
4. Earn 10 points for each enemy defeated
5. Survive as long as possible within the time limit
6. Avoid letting enemies reach you!

**🏗️ Project Structure**

wizards_battle/
│
├── wizards_battleV4.py      # Main game file
├── README.md              # This file
├── images/                # Game sprites
│   ├── wizard.png
│   ├── wizard_flip.png
│   ├── fire_ball.png
│   ├── fire_ball_flip.png
│   ├── enemy_stand.png
│   ├── enemy_running.png
│   ├── enemy_running_flip.png
│   ├── enemy_die.png
│   ├── gameover.png
│   └── background.png
├── sounds/                # Audio files
│   └── lasergun.wav
└── game_screenshot.png         # Game screenshot
