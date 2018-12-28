import pickle
import random
import operator
import numpy as np
import sys
from cost_function import calculate_cost, calculate_overlap
import tkinter
import time

## Load asset data
with open('data/asset_list', 'rb') as fp:
    asset_data = pickle.load(fp)

## Customer inputs
budget = 2000  # in dollars
room_dimensions = {'depth':30, 'width':30, 'height':20} # {depth, width, height} in feet
room_type = "LivingRoom"  # room type

## hyperparameters
n_generations = 10     # no of generations to iterate over
population_size = 500   # initial number of layouts
tournament_size = int(population_size*0.3)
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


## Returns sorted population as per fitness/cost function
def evaluate_population(current_population):

    population_cost = {}
    
    for i in range(0, population_size):
        
        # layout structure: {id : asset_layouts_list}
        # asset_layouts_list: list of [asset object, position, rotation]
        individual_layout = current_population[i] 
        population_cost[individual_layout.items()[0][0]] = calculate_cost(individual_layout, room_dimensions)

    return population_cost
    #return sorted(sorted_population.items(), key = operator.itemgetter(1), reverse=False)


## Cross over from two parents
def create_child(parent1, parent2):

    global _id
    p1_asset_list = parent1.items()[0][1]
    p2_asset_list = parent1.items()[0][1]
    
    count = len(p1_asset_list)/2

    while count >= 0:
        p1_asset_ind = random.randint(0, len(p1_asset_list)-1)
        p2_asset_ind = random.randint(0, len(p2_asset_list)-1)
        
        # check if parent 1 asset does not conflict with any asset from parent 2
        flag = True
        for asset in p2_asset_list:
            if calculate_overlap(p1_asset_list[p1_asset_ind], asset, 0) > 0:
                flag = False
                break

        if flag:
            p2_asset_list[p2_asset_ind] = p1_asset_list[p1_asset_ind]
        
        count -= 1

    child = {_id: p2_asset_list}
    _id += 1
    return child


## Create a child layout from best parents from next generation
def create_child_layouts(best_parent_layouts):

    child_layout_list = []
    temp = np.arange(len(best_parent_layouts))

    for i in range(0, int(population_size * 0.3)):

        #print "Children number created: ", i
        [parent1, parent2] = random.sample(temp, 2)
        child_layout_list.append(create_child(best_parent_layouts[parent1], best_parent_layouts[parent2]))

    return child_layout_list


## Tournament selection for current population
def create_next_generation(current_population, population_cost):

    next_best_breeders = []

    # select 70% best layouts from current population
    # tournament size
    arr = np.arange(population_size)
    
    while len(next_best_breeders) < population_size*0.7:

        # select tournament_size random layouts
        
        sample_indices = random.sample(xrange(len(arr)), tournament_size)
        winner_cost = sys.maxint
        winner_index = 0

        #print "arr:", arr
        #print "Sample indices:", sample_indices
        
        for ind in sample_indices:
            #print "ind:", ind
            i = arr[ind]
            #print "i:", i
            layout = current_population[i]
            cost = population_cost[layout.items()[0][0]]
            if cost < winner_cost:
                winner_cost = cost
                winner_index = ind

        #print "winner_index:", winner_index
        #print "arr[winner_index]:", arr[winner_index]
        next_best_breeders.append(current_population[arr[winner_index]])
        arr = np.delete(arr, winner_index)

    '''
    # debug
    print "\n\nPrinting 70 percent next best layouts:"
    for l in next_best_breeders:
        print "layout id:", l.items()[0][0]
        for a in l.items()[0][1]:
            print a[0]._category, a[0]._subcategory, a[0]._vertical
    '''

    # create new layouts from crossover of parents
    random.shuffle(next_best_breeders)
    print "Finding Child layouts from 70 percent best ones....."
    child_layouts = create_child_layouts(next_best_breeders)
    
    print "Created 30 percent child layouts....."
    g = next_best_breeders + child_layouts
    random.shuffle(g)

    return g 


## Mutation stage
def mutate_design(layout):

    layout_id = layout.items()[0][0]
    assets = layout.items()[0][1]

    # 1. Randomly change positions
    prob_trans = 0.4 # probability of random translation
    obj_indices = random.sample(xrange(len(assets)), int(len(assets) * prob_trans))
    
    for i in obj_indices:
        asset = assets[i]
        count = 10
    
        while count >= 0:
            rotation = asset[2]
            if rotation == 0 or rotation == 180:
                x_position = random.uniform(0 + asset[0]._dimension['depth']/2, room_dimensions['width'] - asset[0]._dimension['depth']/2)
                z_position = random.uniform(0 + asset[0]._dimension['width']/2, room_dimensions['depth'] - asset[0]._dimension['width']/2)
            else:
                x_position = random.uniform(0 + asset[0]._dimension['width']/2, room_dimensions['width'] - asset[0]._dimension['width']/2)
                z_position = random.uniform(0 + asset[0]._dimension['depth']/2, room_dimensions['depth'] - asset[0]._dimension['depth']/2)

            old_position = asset[1]
            new_position = {'x' : x_position, 'z' : z_position}
            asset[1] = new_position

            # check if new position does not intersect with other assets
            flag = True
            for a in assets:
                if a[1] != old_position:
                    if calculate_overlap(a, asset, 0) > 0:
                        flag == False
                        break
            
            if flag:
                assets[i] = asset
                break
            count -= 1

    # 1. Randomly change rotations
    prob_rot = 0.4 # probability of random rotation
    obj_indices = random.sample(xrange(len(assets)), int(len(assets) * prob_rot))
    
    for i in obj_indices:
        asset = assets[i]
        count = 10
    
        while count >= 0:
            old_rotation = asset[2]
            new_rotation = random.choice([old_rotation-90, old_rotation+90])
            asset[2] = new_rotation

            # check if new orientation does not intersect with other assets
            flag = True
            for a in assets:
                if a[1] != asset[1]:
                    if calculate_overlap(a, asset, 0) > 0:
                        flag == False
                        break
            
            if flag:
                assets[i] = asset
                break
            count -= 1

    # return modified design
    layout[layout_id] = assets
    return layout


## Generate next generation from current population
def next_generation(current_population):
     
    # find cost of individuals in population
    population_cost = evaluate_population(current_population)    
    print "Calculated population cost...."

    # selection stage: tournament selection
    next_breeders = create_next_generation(current_population, population_cost)
    print "Calculated next generation...."
    
    # mutation stage....to be done.....
    print "Mutating 50 percent of assets...."
    random.shuffle(next_breeders)
    
    '''
    for i in range(0, int(len(next_breeders)/2)):
        layout_new = mutate_design(next_breeders[i])
        next_breeders[i] = layout_new
    '''
    return [next_breeders, population_cost]


# python visualizer
scale = 15
root = tkinter.Tk()
root.geometry("500x500")
canvas = tkinter.Canvas(root, bg='green', width=scale*room_dimensions['width'], height=scale*room_dimensions['depth'])
canvas.pack()

def render_layouts(generation_costs, historic):

    for i in range(0, population_size):
        
        layout = historic[n_generations - 2][i]
        print generation_costs[n_generations-2][layout.items()[0][0]]
            
        if generation_costs[n_generations-2][layout.items()[0][0]] <= 0.1:

            print "Plotting layout....."
            asset_list = layout.items()[0][1]
            for asset in asset_list:
                print asset[1]
                print asset[0]._vertical
                if asset[2] == 0 or asset[2] == 180: 
                    canvas.create_rectangle(scale*(asset[1]['x'] - asset[0]._dimension['depth']/2), scale*(asset[1]['z'] - asset[0]._dimension['width']/2), scale*(asset[1]['x'] + asset[0]._dimension['depth']/2), scale*(asset[1]['z'] + asset[0]._dimension['width']/2), fill='red')
                else:
                    canvas.create_rectangle(scale*(asset[1]['x'] - asset[0]._dimension['width']/2), scale*(asset[1]['z'] - asset[0]._dimension['depth']/2), scale*(asset[1]['x'] + asset[0]._dimension['width']/2), scale*(asset[1]['z'] + asset[0]._dimension['depth']/2), fill='red')

            root.update()
            time.sleep(.5)
            canvas.delete("all")
            print "debug:", i
    
    root.mainloop()
    #canvas.after(20, update(i + 1, generation_costs, historic))
    #print "debug:", i+1


## Traverse over multiple generations
def generate_multiple_generations():

    historic = []
    generation_costs = []
    historic.append(generate_first_population())
    
    for i in range(0, n_generations - 1):
        print "Generation: ", i
        temp = next_generation(historic[i])
        historic.append(temp[0])
        generation_costs.append(temp[1])

    '''
    # print costs for all generations
    for g in range(n_generations-1):
        print "\ngeneration number:  ", g
        for k, v in generation_costs[g].items():
            print v,",", 

    # print design assets of all generations
    for gen in range(0, n_generations-1):
        print "\nGeneration designs: ", gen
        for l in historic[gen]:
            print "layout id:", l.items()[0][0]
            for a in l.items()[0][1]:
                print a[0]._category, a[0]._subcategory, a[0]._vertical
    '''

    # python data visualizer
    render_layouts(generation_costs, historic)

if __name__ == "__main__":
    print "Population Size: ", population_size, ", No of Generations: ", n_generations
    generate_multiple_generations()