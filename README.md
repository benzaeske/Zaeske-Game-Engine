Working repository for a 2D pixel art game a la "[Vampire Survivors](https://store.steampowered.com/app/1794680/Vampire_Survivors/)"

The current state of the game is a very simple proof of concept: The player must survive waves of jellyfish that move 
towards them by utilizing the various powers given to them by the variety of colored fish they encounter. 

The fish are simulated using [Boid's algorithm](https://en.wikipedia.org/wiki/Boids), which is a neat little algorithm 
that was developed by studying the flocking behavior of birds. The simulation is sped up significantly by utilizing 
spatial partitioning (spatial hashing). Entities in the game move by maintaining position/velocity/accleration vectors that are updated each frame.

With some small tweaks as development continues, I believe that the architecture I have laid out here will prove to be 
incredible scalable and efficient at adding features rapidly as I continue to expand the game. If you want to check out 
the code, a few recommended places to start:
<li>For high level architecture check out the Controller</li>
<li>For seeing how the game world is simulated check out the Model</li>
<li>For seeing how I'm drawing things check out the View</li>
<li>To skip past everything and look at how Boid's algorithm was implemented, check out Fish, Boid, and PhysicsEntity</li>

### Setup Instructions:
1. Make sure you have installed the latest version of Python: https://www.python.org/downloads/ 

2. Clone the repository and set up a python virtual environment (I develop using venv): `python -m venv venv`

3. Install the necessary dependencies from the requirements.txt in the project:
   - First you must activate the virtual envionment: `venv\Scripts\activate` (if using the command line from an IDE like Pycharm, it will automatically do this for you)
   - Install the requirements into your virtual environment: `pip install -r requirements.txt`
  
4. The current state of the game can be run by launching main.py
