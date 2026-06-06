





# STEP FUNCTION 

def step(predator, prey, grid, predator_algo, prey_algo):

    # predator đi trước
    new_predator = predator_algo(grid, predator, prey)

    # prey chạy
    new_prey = prey_algo(grid, prey, new_predator)

    return new_predator, new_prey

