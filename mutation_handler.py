import random
from globals import *
from cost_function import calculate_overlap

## Hyperparameters
prob_tran = 0.3 # probability of translation for each asset
prob_rot = 0.3   # probability of rotation for each asset

## Include a random change in the design layout structure
# 1. change position of randomly chosen assets
# 2. change rotation of randomly chosen assets
def mutate_design(layout):

    layout_id = layout.items()[0][0]
    assets = layout.items()[0][1]

    # 1. Randomly change positions
    obj_indices = random.sample(xrange(len(assets)), int(len(assets) * prob_tran))
    
    for i in obj_indices:
        asset = assets[i]
        count = 20
        old_position = asset[1]

        while count >= 0:
            #print "\n", count 
            asset[1] = old_position
            rotation = asset[2]
            if rotation == 0 or rotation == 180:
                x_position = random.uniform(0 + asset[0]._dimension['depth']/2, room_dimensions['width'] - asset[0]._dimension['depth']/2)
                z_position = random.uniform(0 + asset[0]._dimension['width']/2, room_dimensions['depth'] - asset[0]._dimension['width']/2)
            else:
                x_position = random.uniform(0 + asset[0]._dimension['width']/2, room_dimensions['width'] - asset[0]._dimension['width']/2)
                z_position = random.uniform(0 + asset[0]._dimension['depth']/2, room_dimensions['depth'] - asset[0]._dimension['depth']/2)

            new_position = {'x' : x_position, 'z' : z_position}
            asset[1] = new_position

            # check if new position does not intersect with other assets
            flag = True
            for a in assets:
                if a[0] != old_position:
                    if calculate_overlap(a, asset, 0) > 0:
                        flag = False
                        #print "Overlap....", count
                        break
            
            if flag:
                #print "flag = True, count: ", count
                assets[i] = asset
                break
            count -= 1

    '''
    # 2. Randomly change rotations
    obj_indices = random.sample(xrange(len(assets)), int(len(assets) * prob_rot))
    
    for i in obj_indices:
        asset = assets[i]
        count = 10
        old_rotation = asset[2]

        while count >= 0:
            asset[2] = old_rotation
            new_rotation = random.choice([(old_rotation-90)%360, (old_rotation+90)%360])
            asset[2] = new_rotation

            # check if new orientation does not intersect with other assets
            flag = True
            for a in assets:
                if a[1] != asset[1]:
                    if calculate_overlap(a, asset, 1) > 0:
                        flag = False
                        break
            
            if flag:
                assets[i] = asset
                break
            count -= 1
    '''

    # return modified design
    layout[layout_id] = assets
    return layout
