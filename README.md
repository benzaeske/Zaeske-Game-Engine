Working repository for a 2D pixel art game a la "[Vampire Survivors](https://store.steampowered.com/app/1794680/Vampire_Survivors/)"

The current state of the game is an ocean simulation with multiple schools of different colored fish that follow different behaviors for schooling and shoaling.

The underlying code uses Boid's algorithm each frame on entities that move according to a position, velocity and acceleration. The model uses spatial partioning and divides the world space into a grid of smaller cells in order to get increased efficiency when calculating forces between a large amount of entities.

At a glance, Boid's algorithm was developed to simulate the flocking behavior of birds or fish. There is no overarching control or logic that is being applied to every entity at once. Instead each entity decides how to move in each frame following 3 simple rules:
1. Each entity attempts to move towards the average position of its neighbors.  In the code, this is called coherence
2. Each entity attempts to align its velocity with that of its neighbors. In the code, this is called alignment
3. Each entity attempts to avoid neighbors that are very close. In the code, this is called avoidance

### Setup Instructions:
1. Make sure you have installed the latest version of Python: https://www.python.org/downloads/ 

2. Clone the repository and set up a python virtual environment (I develop using venv): `python -m venv venv`

3. Install the necessary dependencies from the requirements.txt in the project:
   - First you must activate the virtual envionment: `venv\Scripts\activate` (if using the command line from an IDE like Pycharm, it will automatically do this for you)
   - Install the requirements into your virtual environment: `pip install -r requirements.txt`
   - Pygame may require you to install certain sdl dependencies in order for it to work... I'm not exactly sure but when I tried setting this up on my mac it had issues. `pip install pygame` in your repository might also fix this.
  
4. The current state of the game can be run by launching main.py
