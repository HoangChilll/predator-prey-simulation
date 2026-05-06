from ui.grid import grid50x50,grid10x10,grid40,grid20x20_2


# GRID

grid = grid20x20_2




# STEP FUNCTION 

def step(prey, predator, grid, prey_algo, predator_algo):

    # prey đi trước
    new_prey = prey_algo(grid, prey, predator)

    # predator đuổi theo prey mới
    new_predator = predator_algo(grid, predator, new_prey)

    return new_prey, new_predator



# INIT STATE (ROW, COL)

prey = (0, 0)
predator = (25, 25)
