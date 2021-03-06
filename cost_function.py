from globals import *
from math import sqrt
from asset import Asset
import numpy as np
import copy

## Globals
# Add 4 wall objects to be used as parent
wall_obj1 = Asset('Wall', 'Wall', 'Wall', 0, {'width': room_dimensions['depth'], 'depth': 0})
wall_obj2 = Asset('Wall', 'Wall', 'Wall', 0, {'width': room_dimensions['width'], 'depth': 0})
[w1, w2, w3, w4] = [[wall_obj1, {'x': 0, 'z': room_dimensions['depth'] / 2}, 0],
                        [wall_obj2, {'x': room_dimensions['width'] / 2, 'z': 0}, 270],
                        [wall_obj1, {'x': room_dimensions['width'], 'z': room_dimensions['depth'] / 2}, 180],
                        [wall_obj2, {'x': room_dimensions['width'] / 2, 'z': room_dimensions['depth']}, 90]]

## Cost function
## Based upon ergonomic, functional and visual needs defined by interior design guidelines
def calculate_cost(layout, room_dim):

    total_cost = 0
    layout_assets = layout.items()[0][1]
    cost_clearance = 0
    cost_grp_relations = 0

    cost_clearance = calculate_clearance_term(layout_assets)
    cost_grp_relations = check_pairwise_relationship(layout_assets)
    cost_proportion = calculate_proportion_term(layout_assets, room_dim)
    cost_functional_req = check_functional_req(layout_assets)

    # weight parameters
    wt_clearance = 1
    wt_proportion = 1
    wt_grp_relations = 1
    wt_functional_req = 1

    # calculate final cost
    total_cost += wt_clearance * cost_clearance
    total_cost += wt_grp_relations * cost_grp_relations
    total_cost += wt_proportion * cost_proportion
    total_cost += wt_functional_req * cost_functional_req

    # individual layout cost structure: [total, cost associated for each feature]
    # features: clearance, circulation, proportion, functional, group relations, alignement
    return [total_cost, cost_clearance, cost_grp_relations, cost_proportion, cost_functional_req]


## Clearance constraint: objects in a design should have some empty space around them
def calculate_clearance_term(layout_assets):

    padding = 1
    total_iou = 0 # intersection over union
    
    for i in range(0, len(layout_assets)-1):
        
        for j in range(i + 1, len(layout_assets)):

            asset1 = layout_assets[i]
            asset2 = layout_assets[j]
            iou = calculate_iou(asset1, asset2, padding)
            total_iou += iou

    if len(layout_assets) > 1:
        return total_iou / (len(layout_assets) * (len(layout_assets) - 1))
    else:
        return 0

## Consist of asset compatibility w.r.t. room and customer type
def check_functional_req(layout_assets):

    cost = check_room_requirement(layout_assets)
    return cost

## Importance and desired quantity of each asset for a room as per its category
def check_room_requirement(layout_assets):
    
    current_qty = copy.deepcopy(desired_qty)
    cost1 = 0
    cost2 = 0

    for asset in layout_assets:
        if asset != None and asset[0]._subcategory != '':

            current_qty[asset[0]._subcategory] -= 1
            imp = calculate_importance(asset)
            cost2 += (1-imp)

    # check desired qty of assets met
    for _, v in current_qty.items():
            cost1 += abs(v)
    cost1 /= (2 * len(current_qty.items()))
    
    # check asset importance per room
    cost2 /= (2 * len(layout_assets))

    return cost1 + cost2


## Check parent child (pairwise) heirarchy is followed
def check_pairwise_relationship(layout_assets):

    layout_assets.append(w1)
    layout_assets.append(w2)
    layout_assets.append(w3)
    layout_assets.append(w4)
    
    cost = 0
    dist = 0
    distx = 0
    distz = 0

    for index1 in range(0, len(layout_assets) - 1):
        asset1 = layout_assets[index1]

        if asset1 != None and asset1[0]._subcategory != '':
            
            for index2 in range(index1 + 1, len(layout_assets)):
                asset2 = layout_assets[index2]

                if asset2 != None:
                    
                        # if in parent
                        if asset2[0]._subcategory in pairwise_rel[asset1[0]._subcategory][0]:
                            
                            # dist should be min
                            distx = asset1[1]['x'] - asset2[1]['x']
                            distz = asset1[1]['z'] - asset2[1]['z']

                            # angle should be 0/180
                            if abs(asset1[2] - asset2[2]) == 90 or abs(asset1[2] - asset2[2]) == 270:
                                dist += (distx * distx + distz * distz)*(3/2)
                            else:
                                dist += (distx * distx + distz * distz)

                        # if in child
                        elif asset2[0]._subcategory in pairwise_rel[asset1[0]._subcategory][1]:

                            # dist should be min
                            distx = asset1[1]['x'] - asset2[1]['x']
                            distz = asset1[1]['z'] - asset2[1]['z']

                            # angle should be 0/180
                            if abs(asset1[2] - asset2[2]) == 90 or abs(asset1[2] - asset2[2]) == 270:
                                dist += (distx * distx + distz * distz)*(3/2)
                            else:
                                dist += (distx * distx + distz * distz)

    cost = dist/(len(layout_assets) * (len(layout_assets)-1) * sqrt(room_dimensions['width']*room_dimensions['depth']))
    
    layout_assets.pop()
    layout_assets.pop()
    layout_assets.pop()
    layout_assets.pop()

    return cost


## Desired area occupancy requirement
def calculate_proportion_term(layout_assets, room_dim):
    
    room_area = room_dim['width'] * room_dim['depth']
    req_coverage_ratio = 0.3
    covered_area = 0

    for asset in layout_assets:
        if asset != None:
            covered_area += asset[0]._dimension['width'] * asset[0]._dimension['depth']

    return max(req_coverage_ratio - covered_area/room_area, 0)/req_coverage_ratio


### Utility functions

def calculate_importance(asset):
    
    f1 = asset_subcategory_functions[asset[0]._subcategory][0]
    f2 = asset_subcategory_functions[asset[0]._subcategory][1]
    if f1 in room_necessary_functions[room_type]:
        return 1
    elif f2 in room_necessary_functions[room_type]:
        return 0.75
    else:
        return 0.1


## intersection over union
def calculate_iou(asset1, asset2, padding):

    if asset1 == None or asset2 == None:
        return 0
    
    intersection = calculate_overlap(asset1, asset2, padding)

    area_asset1 = (asset1[0]._dimension['depth'] + 2 * padding) * (asset1[0]._dimension['width'] + 2 * padding)
    area_asset2 = (asset2[0]._dimension['depth'] + 2 * padding) * (asset2[0]._dimension['width'] + 2 * padding)
    union = area_asset1 + area_asset2 - intersection

    return intersection/union


## calculate overlap of two axis aligned rectangular bounding boxes
def calculate_overlap(asset1, asset2, padding):

    if asset1 == None or asset2 == None:
        return 0

    # calculate padded dimentions
    asset1_depth = asset1[0]._dimension['depth'] + 2 * padding
    asset1_width = asset1[0]._dimension['width'] + 2 * padding
    asset2_depth = asset2[0]._dimension['depth'] + 2 * padding
    asset2_width = asset2[0]._dimension['width'] + 2 * padding

    dx = 0
    dz = 0

    # compute overlap between axis aligned rectangles
    # if assets parallel to each other
    if abs(asset1[2] - asset2[2]) == 0 or abs(asset1[2] - asset2[2]) == 180:

        # if both parallel to z axis 
        if asset1[2] == 0 or asset1[2] == 180: 
            dx = min(asset1[1]['x'] + asset1_depth / 2, asset2[1]['x'] + asset2_depth / 2) - max(asset1[1]['x'] - asset1_depth / 2, asset2[1]['x'] - asset2_depth / 2)
            dz = min(asset1[1]['z'] + asset1_width / 2, asset2[1]['z'] + asset2_width / 2) - max(asset1[1]['z'] - asset1_width / 2, asset2[1]['z'] - asset2_width / 2)
            #print dx, dz, 0
        # if both parallel to x axis 
        elif asset1[2] == 90 or asset1[2] == 270: 
            dx = min(asset1[1]['x'] + asset1_width / 2, asset2[1]['x'] + asset2_width / 2) - max(asset1[1]['x'] - asset1_width / 2, asset2[1]['x'] - asset2_width / 2)
            dz = min(asset1[1]['z'] + asset1_depth / 2, asset2[1]['z'] + asset2_depth / 2) - max(asset1[1]['z'] - asset1_depth / 2, asset2[1]['z'] - asset2_depth / 2)
            #print dx, dz, 1
            
    # if both 90 degrees angle to each other
    else:
 
        if asset1[2] == 0 or asset1[2] == 180: 
            dx = min(asset1[1]['x'] + asset1_depth / 2, asset2[1]['x'] + asset2_width / 2) - max(asset1[1]['x'] - asset1_depth / 2, asset2[1]['x'] - asset2_width / 2) 
            dz = min(asset1[1]['z'] + asset1_width / 2, asset2[1]['z'] + asset2_depth / 2) - max(asset1[1]['z'] - asset1_width / 2, asset2[1]['z'] - asset2_depth / 2)
            #print dx, dz, 2
        elif asset1[2] == 90 or asset1[2] == 270: 
            dx = min(asset1[1]['x'] + asset1_width / 2, asset2[1]['x'] + asset2_depth / 2) - max(asset1[1]['x'] - asset1_width / 2, asset2[1]['x'] - asset2_depth / 2)
            dz = min(asset1[1]['z'] + asset1_depth / 2, asset2[1]['z'] + asset2_width / 2) - max(asset1[1]['z'] - asset1_depth / 2, asset2[1]['z'] - asset2_width / 2)
            #print dx, dz, 3

    if dx >= 0 and dz >= 0:
        return dx * dz
    else:
        return 0
