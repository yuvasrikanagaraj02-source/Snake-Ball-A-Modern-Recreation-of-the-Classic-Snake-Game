# Snake-Ball-A-Modern-Recreation-of-the-Classic-Snake-Game
🎮 Snake Ball

Snake Ball is a modern arcade-style game developed using Python, OpenCV, and NumPy. The game reimagines the classic Snake experience with smooth mouse-based controls, dynamic visual effects, progressive difficulty, and engaging gameplay mechanics.

Players control a chain of connected ball segments that follows the mouse cursor in real time. The objective is to collect glowing energy orbs to increase the score and grow the snake while avoiding collisions with both moving obstacles and the snake's own tail. As the snake grows longer, the challenge intensifies, requiring greater precision and strategic movement.

Key Features

✔ Smooth mouse-based controls

✔ Dynamic snake growth system

✔ Glowing collectible energy orbs

✔ Real-time score and level tracking

✔ Progressive difficulty scaling

✔ Moving obstacle balls with collision detection

✔ Self-collision detection mechanism

✔ Particle effects and animations

✔ High-score tracking

Gameplay
Objective

Collect energy orbs to increase your score and grow the snake while avoiding collisions.

How It Works
The snake head follows the mouse cursor.
Collect glowing orbs to earn points.
Each orb collected increases the snake's length.
Longer snakes earn more points per orb.
Avoid colliding with your own tail.
Avoid hitting moving obstacle balls.
Survive as long as possible to achieve the highest score.

| Key/Input      | Action                  |
| -------------- | ----------------------- |
| Mouse Movement | Control Snake Direction |
| R              | Restart Game            |
| Q              | Quit Game               |

Scoring System

The scoring mechanism is based on the current length of the snake.

Points Earned = Current Snake Length

This rewards players who successfully manage longer snakes and survive for extended periods.

Level Progression

The game includes an automatic level progression system.

Levels increase as the score grows.
Snake movement speed gradually increases.
Higher levels create a more challenging gameplay experience.
Maximum level is capped to maintain balanced gameplay.

| Technology    | Purpose                                 |
| ------------- | --------------------------------------- |
| Python        | Core game development                   |
| OpenCV        | Graphics rendering and user interaction |
| NumPy         | Frame and array processing              |
| Math Module   | Distance and movement calculations      |
| Random Module | Orb and obstacle generation             |

Installation
1. Clone the Repository
   git clone https://github.com/yuvasrikanagaraj02-source/Snake-Ball-A-Modern-Recreation-of-the-Classic-Snake-Game
   cd snake-ball
2. Install Dependencies
   pip install opencv-python numpy
3. Run the Game
   python snake_ball.py



