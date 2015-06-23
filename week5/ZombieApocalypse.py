"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"

class Zombie(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles, humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)  #must use Base class' clear function, neverethless cause infinite loop
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were added.
        """
        # replace with an actual generator
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for human in self._human_list:
            yield human
        
    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """
        visited = poc_grid.Grid(self.get_grid_height(), self.get_grid_width())
        for row in range(self.get_grid_height()):
            for col in range(self.get_grid_width()):
                if not self.is_empty(row, col):           
                    visited.set_full(row, col)
        distance_field = [[self.get_grid_height() * self.get_grid_width() for dummy_col in range(self.get_grid_width())] 
                          for dummy_row in range(self.get_grid_height())]
        boundary = poc_queue.Queue()
        if entity_type == ZOMBIE:
            for item in self.zombies():
                boundary.enqueue(item)
        else:
            for item in self.humans():
                boundary.enqueue(item)
        for cell in boundary:
            visited.set_full(cell[0], cell[1])
            distance_field[cell[0]][cell[1]] = 0
        while len(boundary) > 0:
            current_cell = boundary.dequeue()
            four_neighbors = visited.four_neighbors(current_cell[0], current_cell[1])
            for neighbor in four_neighbors:
                if visited.is_empty(neighbor[0], neighbor[1]):
                    visited.set_full(neighbor[0], neighbor[1])
                    distance_field[neighbor[0]][neighbor[1]] = distance_field[current_cell[0]][current_cell[1]] + 1
                    boundary.enqueue(neighbor)
        return distance_field
    
    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves are allowed
        Two humans can not move to the same cell
        """
        # omit eaten humans
        self._human_list = filter(lambda p: p not in self._zombie_list, self._human_list)

        new_human_list = []
        for human in self.humans():
            best_step = []
            distance = 0        	
            next_steps = poc_grid.Grid.eight_neighbors(self, human[0], human[1])
            # filter FULL cell
            next_steps = filter(lambda p: poc_grid.Grid.is_empty(self, p[0], p[1]) == True, next_steps)

            for step in next_steps:
                if zombie_distance[step[0]][step[1]] > distance:
                    distance = zombie_distance[step[0]][step[1]]
                    best_step = []
                    best_step.append(step)
                elif zombie_distance[step[0]][step[1]] == distance:
                    best_step.append(step)

            best_step = filter(lambda p: p not in new_human_list, best_step)
            if len(best_step) == 0:
                new_human_list.append(human)
            else:
                new_human_list.append(random.choice(best_step))
        self._human_list = new_human_list                        
        
    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves are allowed
        Human is ate when meets Zombies
        Two zombies can not move to the same cell
        """
        # omit eaten humans
        self._human_list = filter(lambda p: p not in self._zombie_list, self._human_list)

        new_zombie_list = []
        for zombie in self.zombies():
            best_step = []
            distance = self.get_grid_width() * self.get_grid_height()
            next_steps = poc_grid.Grid.four_neighbors(self, zombie[0], zombie[1])
            # filter FULL cell
            next_steps = filter(lambda p: poc_grid.Grid.is_empty(self, p[0], p[1]) == True, next_steps)

            for step in next_steps:
                if human_distance[step[0]][step[1]] < distance:
                    distance = human_distance[step[0]][step[1]]
                    best_step = []
                    best_step.append(step)
                elif human_distance[step[0]][step[1]] == distance:
                    best_step.append(step)

            best_step = filter(lambda p: p not in new_zombie_list, best_step)
            if len(best_step) == 0:
                new_zombie_list.append(zombie)
            else:
                new_zombie_list.append(random.choice(best_step))
        self._zombie_list = new_zombie_list

poc_zombie_gui.run_gui(Zombie(30, 40))

