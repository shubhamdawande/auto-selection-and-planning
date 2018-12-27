padding = 0

## Cost function
## Based upon ergonomic, functional and visual needs defined by interior design guidelines  
def calculate_cost(layout):

    cost = 0
    layout_id = layout.items()[0][0]
    layout = layout.items()[0][1]
    total_overlap = 0
    
    # clearance constraint
    for i in range(0, len(layout)-1):
        
        for j in range(i + 1, len(layout)):
            asset1 = layout[i]
            asset2 = layout[j]
            overlap = calculate_overlap(asset1, asset2)

            #if overlap == 0:
            print i, j, layout_id, asset1[2], asset2[2], overlap
            print asset1[1], [asset1[0]._dimension['depth'], asset1[0]._dimension['width']], asset2[1], [asset2[0]._dimension['depth'], asset2[0]._dimension['width']] 
            
            total_overlap += overlap

    cost += total_overlap
    return cost


## Utility function
def calculate_overlap(asset1, asset2):

    # calculate padded dimentions
    asset1_depth = asset1[0]._dimension['depth'] + 2 * padding
    asset1_width = asset1[0]._dimension['width'] + 2 * padding
    asset2_depth = asset2[0]._dimension['depth'] + 2 * padding
    asset2_width = asset2[0]._dimension['width'] + 2 * padding

    x1 = 0
    x2 = 0
    z1 = 0
    z2 = 0
        
    # compute overlap between axis aligned rectangles
    # if assets parallel to each other
    if abs(asset1[2] - asset2[2]) == 0 or abs(asset1[2] - asset2[2]) == 180:

        # if both parallel to z axis 
        if asset1[2] == 0 or asset1[2] == 180:
            x1 = max(asset1[1]['x'] - asset1_width / 2, asset2[1]['x'] - asset2_width / 2)
            z1 = min(asset1[1]['z'] + asset1_depth / 2, asset2[1]['z'] + asset2_depth / 2)
            x2 = min(asset1[1]['x'] + asset1_width / 2, asset2[1]['x'] + asset2_width / 2)
            z2 = max(asset1[1]['z'] - asset1_depth / 2, asset2[1]['z'] - asset2_depth / 2)
            print x1,x2,z1,z2, 0
        # if both parallel to x axis 
        elif asset1[2] == 90 or asset1[2] == 270: 
            x1 = max(asset1[1]['x'] - asset1_depth / 2, asset2[1]['x'] - asset2_depth / 2)
            z1 = min(asset1[1]['z'] + asset1_width / 2, asset2[1]['z'] + asset2_width / 2)
            x2 = min(asset1[1]['x'] + asset1_depth / 2, asset2[1]['x'] + asset2_depth / 2)
            z2 = max(asset1[1]['z'] - asset1_width / 2, asset2[1]['z'] - asset2_width / 2)
            print x1, x2, z1, z2, 1
            
    # if both 90 degrees angle to each other
    else:
 
        if asset1[2] == 0 or asset1[2] == 180:
            x1 = max(asset1[1]['x'] - asset1_width/2, asset2[1]['x'] - asset2_depth/2)
            z1 = min(asset1[1]['z'] + asset1_depth/2, asset2[1]['z'] + asset2_width/2)
            x2 = min(asset1[1]['x'] + asset1_width/2, asset2[1]['x'] + asset2_depth/2)
            z2 = max(asset1[1]['z'] - asset1_depth/2, asset2[1]['z'] - asset2_width/2)
            print x1,x2,z1,z2, 2
        elif asset1[2] == 90 or asset1[2] == 270: 
            x1 = max(asset1[1]['x'] - asset1_depth/2, asset2[1]['x'] - asset2_width/2)
            z1 = min(asset1[1]['z'] + asset1_width/2, asset2[1]['z'] + asset2_depth/2)
            x2 = min(asset1[1]['x'] + asset1_depth/2, asset2[1]['x'] + asset2_width/2)
            z2 = max(asset1[1]['z'] - asset1_width/2, asset2[1]['z'] - asset2_depth/2)
            print x1, x2, z1, z2, 3

    intersection = abs((x2 - x1) * (z1 - z2))

    return intersection
