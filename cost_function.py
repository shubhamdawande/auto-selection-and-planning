## Cost function
## Based upon ergonomic, functional and visual needs defined by interior design guidelines  
def calculate_cost(layout, room_dim):

    total_cost = 0
    layout_assets = layout.items()[0][1]
    
    cost_clearance = calculate_clearance_term(layout_assets)
    #cost_proportion = calculate_proportion_term(layout_assets, room_dim)

    # calculate final cost
    wt_clearance = 1
    #wt_proportion = 1.3
    total_cost = wt_clearance * cost_clearance #+ wt_proportion * cost_proportion

    return total_cost


## Clearance constraint
def calculate_clearance_term(layout_assets):

    padding = 1
    total_iou = 0 # intersection over union
    
    for i in range(0, len(layout_assets)-1):
        
        for j in range(i + 1, len(layout_assets)):
            asset1 = layout_assets[i]
            asset2 = layout_assets[j]
            iou = calculate_iou(asset1, asset2, padding)

            #print layout_id, i, j, overlap, "...",
            #print asset1[1], [asset1[0]._dimension['depth'], asset1[0]._dimension['width']], asset2[1], [asset2[0]._dimension['depth'], asset2[0]._dimension['width']] 
            
            total_iou += iou

    #return total_iou
    return total_iou/(len(layout_assets) * (len(layout_assets)-1))


## Area proportions constraint
def calculate_proportion_term(layout_assets, room_dim):
    
    room_area = room_dim['width'] * room_dim['depth']
    req_coverage_ratio = 0.35

    covered_area = 0
    for asset in layout_assets:
        covered_area += asset[0]._dimension['width'] * asset[0]._dimension['depth']

    return max(req_coverage_ratio - covered_area/room_area, 0)/req_coverage_ratio  

### Utility functions

## intersection over union
def calculate_iou(asset1, asset2, padding):

    intersection = calculate_overlap(asset1, asset2, padding)

    area_asset1 = (asset1[0]._dimension['depth'] + 2 * padding) * (asset1[0]._dimension['width'] + 2 * padding)
    area_asset2 = (asset2[0]._dimension['depth'] + 2 * padding) * (asset2[0]._dimension['width'] + 2 * padding)
    union = area_asset1 + area_asset2 - intersection

    return intersection/union


## calculate overlap of two axis aligned rectangular bounding boxes
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
        return dx * dz
    else:
        return 0
