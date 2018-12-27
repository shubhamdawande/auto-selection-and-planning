import pickle
import random
import operator
from cost_function import calculate_cost

## Load asset data
with open('data/asset_list', 'rb') as fp:
    asset_data = pickle.load(fp)

## Customer inputs
budget = 1000  # in dollars
room_dimensions = {'depth':10, 'width':10, 'height':10} # {depth, width, height} in feet
room_type = "LivingRoom"  # room type

## hyperparameters
n_generations = 2      # no of generations to iterate over
population_size = 100  # initial number of layouts
_id = 0                # unique id of each layout


## Create a layout
def generate_random_layout():
    
    current_price = 0
    asset_layouts_list = []
    random_asset = random.choice(asset_data)
    rotations_possible = [0,180,90,270]
    asset_layout_dict = {}
    global _id

    while len(asset_layouts_list) < 10:
        
        # randomly choose asset from database
        random_asset = random.choice(asset_data)
        
        # if budget not exceeded
        if current_price + random_asset._price < budget:

            # random rotation of asset, currently either 0/90/180/270 degrees
            rotation = random.choice(rotations_possible)

            # choose random location of asset
            # consider room is in 1st quadrant in x-z coordinates, asset location < room bounds
            if rotation == 0 or rotation == 180:
                x_location = random.uniform(0 + random_asset._dimension['depth']/2, room_dimensions['width'] - random_asset._dimension['depth']/2)
                z_location = random.uniform(0 + random_asset._dimension['width']/2, room_dimensions['depth'] - random_asset._dimension['width']/2)
            else:
                x_location = random.uniform(0 + random_asset._dimension['width']/2, room_dimensions['width'] - random_asset._dimension['width']/2)
                z_location = random.uniform(0 + random_asset._dimension['depth']/2, room_dimensions['depth'] - random_asset._dimension['depth']/2)
            
            position = {'x' : x_location, 'z' : z_location}

            # add asset info to current layout
            # asset info: [ asset obj, asset position, asset rotation ]
            asset_layouts_list.append([random_asset, position, rotation])

            current_price += random_asset._price

    asset_layout_dict[_id] = asset_layouts_list
    _id += 1
    
    return asset_layout_dict


## Create initial population
def generate_first_population():
    
    initial_population = []
    for i in range(0, population_size):
        initial_population.append(generate_random_layout())
    
    return initial_population


## sort population as per fitness/cost function
def evaluate_population(current_population):

    sorted_population = {}
    
    for i in range(0, population_size):
        individual_layout = current_population[i]
        sorted_population[individual_layout.items()[0][0]] = calculate_cost(individual_layout)

    return sorted(sorted_population.items(), key = operator.itemgetter(1), reverse=False)


## Generate next generation from current population
def next_generation(current_population):
    
    # sort population as per cost function
    sorted_population = evaluate_population(current_population)

    # selection, mutation to be done

    return []


## Traverse over multiple generations
def multiple_generations():

    historic = []
    historic.append(generate_first_population())

    for i in range(0, n_generations-1):
        historic.append(next_generation(historic[i]))

    return historic


if __name__ == "__main__":
    generations = multiple_generations()