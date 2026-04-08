import curses # Python library for building terminal-based UIs
from curses import wrapper # Initializes curses safely
import queue # Stores items in FIFO order
import time # time-related functions

maze = [
    ["#", "#", "#", "#", "#", "O", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"]
]

def print_maze(maze, stdscr, path=[]):
    #Pull buckets of paint
    BLUE = curses.color_pair(1)
    RED = curses.color_pair(2)

    for i,row in enumerate(maze):
        for j,value in enumerate(row):
            if (i,j) in path:
                stdscr.addstr(i * 2, j * 2, "X", RED)
            else:
                stdscr.addstr(i * 2, j * 2, value, BLUE)

def find_start(maze):
    for i,row in enumerate(maze):
        for j,value in enumerate(row):
            if value == "O":
                return (i,j)
    return None

def find_neighbors(maze,row,col):
    neighbors = []
    if row > 0: #UP
        neighbors.append((row - 1, col))
    if row < len(maze) - 1: #DOWN
        neighbors.append((row + 1, col))
    if col < len(maze[0]) - 1: #RIGHT
        neighbors.append((row, col + 1))
    if col > 0: #LEFT
        neighbors.append((row, col - 1))
    
    return neighbors
    
def find_path(maze,stdscr):
    q = queue.Queue()
    start_pos = find_start(maze)
    q.put((start_pos,[start_pos])) # [start_position,path]
    
    visited = set() # walkable path that have taken in a maze
    visited.add(start_pos)
    
    # 1. Keep going as long as there are coordinates in the queue
    while not q.empty():
        current_pos, path = q.get()
        row, col = current_pos

        # --- THE ANIMATION HEARTBEAT ---
        stdscr.clear() # 1. Wipe the old frame
        print_maze(maze, stdscr, path) #2 Draw the current state
        stdscr.refresh() # 3. Push the drawing to the monitor
        time.sleep(1) # 4. Wait 0.1 seconds so we can see it

        # 2. CHECK: Did we find the exit?
        if maze[row][col] == "X": # Assuming "X" is your exit
            return path
        
         # 3. Look at neighbors
        neighbors = find_neighbors(maze,row,col) # Find available routes

        for neighbor in neighbors:
            if neighbor in visited:
                continue
            r,c = neighbor
            # 4. Check for walls
            if maze[r][c] == "#":
                continue
            # Note: When it hit 'dead-end' for loops just finished without hitting q.put()
            # Go back to while loops if all neighbor were 'continued'
            # neighbor is 'walkable' path here f.e (1,5)
            new_path = path + [neighbor] # Add accessible plot to the path
            q.put((neighbor,new_path))
            visited.add(neighbor) # Added all places have been visited, so we don't revisit
    return None # Return None if no path exist

def main(stdscr):
    # This prepares colors: ID 1 will be Blue text on Black background
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    # ID 2: Red ink for the path
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    # Call your pathfinder and pass the screen to it
    find_path(maze,stdscr)

    # This keeps the window open at the end until you press a key
    stdscr.getch()

#This starts the whole thing safely
wrapper(main)




        
    