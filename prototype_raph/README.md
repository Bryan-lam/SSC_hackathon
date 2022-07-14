# SSC_hackathon

**main.py** 
the main program to run the code in

**array_map.py** 
file that contains the map variables for easy changeability
- ARRAY_WIDTH, ARRAY_HEIGHT: variables that keeps the number of rows and columns in the map
- DEST_X, DEST_Y: Destination point
- START_X, START_Y: starting point
- 4 types of blocks: empty, deadEnds, obstacles, and energyBlocks
  - you cannot pass through deadEnds
  - passing through obstacles takes 2 stepCounters
  - passing through energyBlocks only takes 0.5 stepCounters (can be modified if necessary)

There are currently two methods of finding the obstacles: set and 2D array
- set: list of blocks that are obstacles. Easier to navigate whether the fish has hit an obstacle or not
- array: array of 0s and 1s used to generate the map, 1s being obstacles.

**submission.py** 
file for students to edit in, where they submit their algorithm shortest_path(grid, start, deadEnds, dest, energyBlocks, obs)
- function to be filled by students, they can also make their own functions (e.g. building an empty 2D array)
- it must return an array of tuples/array representing the coordinates of the fish path in order
  - therefore, it's up to the students to avoid deadEnds, obstacles, and get energyBlocks