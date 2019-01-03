## Libraries
import pickle
import random
import operator
import numpy as np
import sys
import pdb

## Custom imports
from cost_function import calculate_cost, calculate_overlap
from visualizer import render_layouts, render_one
from mutation_handler import mutate_design
from globals import *

# unique id for each design
_id = 0

## Create a layout
def generate_random_layout():
    
    current_price = 0
    asset_layouts_list = []
    random_asset = random.choice(asset_data)
    rotations_possible = [0,180,90,270]
    asset_layout_dict = {}
    global _id

    while len(asset_layouts_list) < max_assets_per_room:
        
        # randomly choose asset from database
        random_asset = random.choice(asset_data)
        
        # if budget not exceeded
        if current_price + random_asset._price < budget:

            # random rotation of asset, currently either 0/90/180/270 degrees
            rotation = random.choice(rotations_possible)

            # choose random location of asset
            # consider room is in 1st quadrant in x-z coordinates, asset location < room bounds
            if rotation == 0 or rotation == 180:
                x_position = random.uniform(0 + random_asset._dimension['depth']/2, room_dimensions['width'] - random_asset._dimension['depth']/2)
                z_position = random.uniform(0 + random_asset._dimension['width']/2, room_dimensions['depth'] - random_asset._dimension['width']/2)
            else:
                x_position = random.uniform(0 + random_asset._dimension['width']/2, room_dimensions['width'] - random_asset._dimension['width']/2)
                z_position = random.uniform(0 + random_asset._dimension['depth']/2, room_dimensions['depth'] - random_asset._dimension['depth']/2)
            
            position = {'x' : x_position, 'z' : z_position}

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


## Returns population cost as per fitness function
def evaluate_population(current_population, g_cost):

    population_cost = {}
    
    for i in range(0, population_size):
        
        # layout structure: {id : asset_layouts_list}
        # asset_layouts_list: list of [asset object, position, rotation]
        individual_layout = current_population[i]

        # check if cost already calculated
        key_id = individual_layout.items()[0][0]
        if key_id not in g_cost:
            cl = calculate_cost(individual_layout, room_dimensions)
            population_cost[key_id] = cl
            g_cost[key_id] = cl
        else:
            population_cost[key_id] = g_cost[key_id]

    return [population_cost, g_cost]
    #return sorted(sorted_population.items(), key = operator.itemgetter(1), reverse=False)


## Cross over from two parents
def create_child(parent1, parent2):

    global _id
    p1_asset_list = parent1.items()[0][1]
    p2_asset_list = parent2.items()[0][1]
    
    new_asset_list = []
    l = p1_asset_list  + p2_asset_list
    random.shuffle(l)

    # child layout size
    count = len(l)/2
    
    for asset in l:
        if len(new_asset_list) >= count:
            break
        
        # if empty list add directly
        if len(new_asset_list) == 0:
            new_asset_list.append(asset)
        
        else:  # else check overlap is null and then add
            flag = True
            for a in new_asset_list:
                if calculate_overlap(asset, a, 1) > 0:
                    flag = False
                    break
            if flag:
                new_asset_list.append(asset)

    child = {_id: new_asset_list}
    _id += 1
    return child


## Crossover: create child layouts from best parents of current generation
def create_child_layouts(best_parent_layouts):

    child_layout_list = []
    temp = np.arange(len(best_parent_layouts))

    for i in range(0, int(population_size * 0.3)):

        [parent1, parent2] = random.sample(temp, 2)
        cc = create_child(best_parent_layouts[parent1], best_parent_layouts[parent2])
        #render_one(cc, room_dimensions, gen_count)
        child_layout_list.append(cc)

    return child_layout_list


## Tournament selection for current population + crossover from best ones
def select_and_crossover(current_population, population_cost):

    next_best_breeders = []
    arr = np.arange(population_size)
    
    # select 70% best layouts from current population
    while len(next_best_breeders) < population_size*0.7:

        # select random layouts of size tournament_size
        sample_indices = random.sample(xrange(len(arr)), tournament_size)
        winner_cost = sys.maxint
        winner_index = 0
        
        for ind in sample_indices:
            i = arr[ind]
            layout = current_population[i]
            cost = population_cost[layout.items()[0][0]]
            if cost < winner_cost:
                winner_cost = cost
                winner_index = ind

        next_best_breeders.append(current_population[arr[winner_index]])
        arr = np.delete(arr, winner_index)

    # create 30 percent new layouts from crossover of parents
    random.shuffle(next_best_breeders)
    print "Finding Child layouts from 70 percent best ones....."
    child_layouts = create_child_layouts(next_best_breeders)

    print "Created 30 percent child layouts....."
    g = next_best_breeders + child_layouts
    random.shuffle(g)
    return g


## Generate next generation from current population
def create_next_generation(current_population, g_cost):
     
    # find cost of individuals in population
    [current_population_cost, g_cost] = evaluate_population(current_population, g_cost)
    print "Calculated population cost...."

    # 1. selection + crossover stage
    next_breeders = select_and_crossover(current_population, current_population_cost)
    print "Calculated next generation...."
    
    # 2. mutation stage
    if 1:
        print "Mutating 50 percent of layouts...."
        random.shuffle(next_breeders)
        
        for i in range(0, int(len(next_breeders)/2)):
            [layout_new, g_cost] = mutate_design(next_breeders[i], g_cost)
            next_breeders[i] = layout_new

    return [next_breeders, current_population_cost, g_cost]


## Traverse over multiple generations
def generate_multiple_generations():

    # store asset layout data for all generations
    historic = []

    # store cost for layouts in all generations
    generation_costs = []
    historic.append(generate_first_population())
    
    # global hashmap for storing all costs
    g_cost = {}

    for i in range(0, n_generations - 1):
        
        print "Generation: ", i
        [gen0, gen1, g_cost] = create_next_generation(historic[i], g_cost)

        historic.append(gen0)
        generation_costs.append(gen1)

    # get cost for last generation
    p_cost = evaluate_population(gen0, g_cost)
    generation_costs.append(p_cost)

    # print costs for all generations
    for g in range(n_generations-1):
        print "\n\ngeneration number:  ", g
        for k, v in generation_costs[g].items():
            print k, ":", v[0], ",",

    '''
    # print design assets of all generations
    for g in range(0, n_generations-1):
        print "\nGeneration designs: ", g
        for l in historic[g]:
            print "layout id:", l.items()[0][0]
            for a in l.items()[0][1]:
                print a[0]._category, a[0]._subcategory, a[0]._vertical
    '''

    # python data visualizer
    if visualizer_on:
        render_layouts(generation_costs, historic)

if __name__ == "__main__":
    
    print "Population Size: ", population_size, ", No of Generations: ", n_generations
    generate_multiple_generations()