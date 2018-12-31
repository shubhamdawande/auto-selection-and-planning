## Customer inputs
budget = 2000  # in dollars
room_dimensions = {'depth': 30, 'width':30, 'height':20} # {depth, width, height} in feet
room_type = "LivingRoom"  # room type

## hyperparameters
n_generations = 10      # no of generations to iterate over
population_size = 100   # initial number of layouts
tournament_size = int(population_size*0.3)

## flags
visualizer_on = False