





# STEP FUNCTION 

def step(prey, grey, grid, prey_algo, grey_algo):

    # prey đi trước
    new_prey = prey_algo(grid, prey, grey)

    # grey đuổi theo prey mới
    new_grey = grey_algo(grid, grey, new_prey)

    return new_prey, new_grey

