import random
from globals import *
from cost_function import calculate_overlap, calculate_cost

## Hyperparameters
prob_tran = 0.3 # probability of translation for each asset
prob_rot = 0.0   # probability of rotation for each asset

## Include a random change in the design layout structure
# 1. change position of randomly chosen assets
# 2. change rotation of randomly chosen assets
def mutate_design(layout, g_cost):

    layout_id = layout.items()[0][0]
    assets = layout.items()[0][1]

    if len(assets) == 0:
        return [layout, g_cost]

    if layout_id in g_cost:
        prior_cost = g_cost[layout_id]
    else:
        prior_cost = calculate_cost(layout, room_dimensions)
        g_cost[layout_id] = prior_cost

    # 1. Randomly change positions
    obj_indices = random.sample(xrange(len(assets)), int(len(assets) * prob_tran))
    
    for i in obj_indices:

        asset = assets[i]
        count = 50
        old_position = asset[1]

        while count >= 0:

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
            
            assets[i] = asset
            #print "calculating cost..."
            new_cost = calculate_cost({layout_id:assets}, room_dimensions)
            #print "calculating cost done"

            if new_cost[0] < prior_cost[0]:
                prior_cost = new_cost
                #print "found"
                break
            else:
                #print "count:", count
                asset[1] = old_position
                assets[i] = asset
            
            count -= 1

    # 2. Randomly change orientations
    obj_indices = random.sample(xrange(len(assets)), int(len(assets) * prob_rot))
    prior_cost = calculate_cost({layout_id: assets}, room_dimensions)

    for i in obj_indices:
        asset = assets[i]
        count = 50
        old_rotation = asset[2]

        while count >= 0:
            asset[2] = old_rotation
            new_rotation = random.choice([(old_rotation-90)%360, (old_rotation+90)%360])
            asset[2] = new_rotation
            
            assets[i] = asset
            new_cost = calculate_cost({layout_id:assets}, room_dimensions)
            
            if new_cost[0] < prior_cost[0]:
                prior_cost = new_cost
                break
            else:
                asset[1] = old_rotation
                assets[i] = asset
            
            count -= 1

    # Remove random existing asset
    #print "Removing asset...."
    prior_cost = calculate_cost({layout_id: assets}, room_dimensions)
    count = 50

    while count >= 0:
        
        asset_ind = random.randint(0, len(assets)-1)
        a = assets[asset_ind]
        assets[asset_ind] = None
        new_cost = calculate_cost({layout_id: assets}, room_dimensions)

        if new_cost[0] < prior_cost[0]:
            assets.pop(asset_ind)
            prior_cost = new_cost
            break
        else:
            assets[asset_ind] = a

        count -= 1

    # Add new object: exploration step
    #print "Adding asset...."
    prior_cost = calculate_cost({layout_id: assets}, room_dimensions)
    current_price = 0
    
    for asset in assets:
        current_price += asset[0]._price

    count1 = 50
    while count1 >= 0:
        new_asset_obj = random.choice(asset_data)
        
        if new_asset_obj._price + current_price < budget:
            count = 10

            while count >= 0:
                rotation = random.choice([0, 90, 180, 270])
                if rotation == 0 or rotation == 180:
                    x_position = random.uniform(0 + new_asset_obj._dimension['depth'] / 2, room_dimensions['width'] - new_asset_obj._dimension['depth'] / 2)
                    z_position = random.uniform(0 + new_asset_obj._dimension['width'] / 2, room_dimensions['depth'] - new_asset_obj._dimension['width'] / 2)
                else:
                    x_position = random.uniform(0 + new_asset_obj._dimension['width'] / 2, room_dimensions['width'] - new_asset_obj._dimension['width'] / 2)
                    z_position = random.uniform(0 + new_asset_obj._dimension['depth'] / 2, room_dimensions['depth'] - new_asset_obj._dimension['depth'] / 2)
                
                assets.append([new_asset_obj, {'x': x_position, 'z':z_position}, rotation])
                new_cost = calculate_cost({layout_id: assets}, room_dimensions)

                if new_cost[0] < prior_cost[0]:
                    prior_cost = new_cost
                    break
                else:
                    assets.pop()
                    count -= 1
            break
        else:
            count1 -= 1

    final_cost = calculate_cost({layout_id: assets}, room_dimensions)
    g_cost[layout_id] = final_cost

    return [{layout_id: assets}, g_cost]
