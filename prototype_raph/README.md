# SSC_hackathon

*main.py* the main program to run the code in

*array_map.py* file that contains the map variables for easy changeability
- ARRAY_WIDTH, ARRAY_HEIGHT: variables that keeps the number of rows and columns in the map
- DEST_X, DEST_Y: Destination point
- START_X, START_Y: starting point
There are currently two methods of finding the obstacles: set and 2D array
- obstacles: list of blocks that are obstacles. Easier to navigate whether the fish has hit an obstacle or not
- ARRAY: array of 0s and 1s used to generate the map, 1s being obstacles.

*submission.py* file for students to edit in, where they submit their algorithm
- move(pos_x, pos_y, dest_x, dest_y): move function that gives current position and destination position