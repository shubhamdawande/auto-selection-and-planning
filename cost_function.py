## Cost function
## Based upon ergonomic, functional and visual needs defined by interior design guidelines  
def calculate_cost(layout):

    total_cost = 0
    layout_id = layout.items()[0][0]
    layout = layout.items()[0][1]
    
    cost_clearance = calculate_clearance_term(layout_id, layout)
    
    # calculate final cost
    total_cost = cost_clearance

    return total_cost


## Clearance constraint
def calculate_clearance_term(layout_id, layout):

    cost = 0
    padding = 1
    total_overlap = 0
    for i in range(0, len(layout)-1):
        
        for j in range(i + 1, len(layout)):
            asset1 = layout[i]
            asset2 = layout[j]
            iou = calculate_iou(asset1, asset2, padding)

            #print layout_id, i, j, overlap, "...",
            #print asset1[1], [asset1[0]._dimension['depth'], asset1[0]._dimension['width']], asset2[1], [asset2[0]._dimension['depth'], asset2[0]._dimension['width']] 
            
            total_overlap += iou

    cost += total_overlap
    return cost


## intersection over union
def calculate_iou(asset1, asset2, padding):

    intersection = calculate_overlap(asset1, asset2, padding)

    area_asset1 = (asset1[0]._dimension['depth'] + 2 * padding) * (asset1[0]._dimension['width'] + 2 * padding)
    area_asset2 = (asset2[0]._dimension['depth'] + 2 * padding) * (asset2[0]._dimension['width'] + 2 * padding)
    union = area_asset1 + area_asset2 - intersection

    return intersection/union


## Utility function: calculate overlap of two axis aligned rectangular bounding boxes
def calculate_overlap(asset1, asset2, padding):

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
            dx = min(asset1[1]['x'] + asset1_width/2, asset2[1]['x'] + asset2_depth/2) - max(asset1[1]['x'] - asset1_width/2, asset2[1]['x'] - asset2_depth/2)
            dz = min(asset1[1]['z'] + asset1_depth/2, asset2[1]['z'] + asset2_width/2) - max(asset1[1]['z'] - asset1_depth/2, asset2[1]['z'] - asset2_width/2)
            #print dx, dz, 3

    if dx >= 0 and dz >= 0:
        intersection = dx * dz
    else:
        intersection = 0

    return intersection
