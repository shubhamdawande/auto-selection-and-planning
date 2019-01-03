import pickle

## Customer inputs
budget = 2000  # in dollars
room_dimensions = {'depth': 15, 'width':15, 'height':20} # {depth, width, height} in feet
room_type = "LivingRoom"  # room type

## Load asset data
with open('data/asset_list', 'rb') as fp:
    asset_data = pickle.load(fp)

## hyperparameters
n_generations = 50      # no of generations to iterate over
population_size = 400   # initial number of layouts
tournament_size = int(population_size*0.3) # select as per population size
max_assets_per_room = 10

## flags
visualizer_on = True

## group relationship dictionary => asset_subcategory: [parent_subcategories, child_subcategories]
grp_rel = {
            'Wall':      [['dummy'], ['Display Units', 'TV Units', 'Shoe Racks', 'Tables', 'Wardrobes', 'Beds', 'Prayer Units', 'Dressers', 'Bar Units']],
            'Sofas':     [['Wall'], ['dummy']],
            'Chairs':    [['Tables', 'Bar Units', 'Dining'], ['dummy']],
            'Tables':    [['dummy'], ['Chairs']],
            'Dining':    [['dummy'], ['Chairs']],
            'Shoe Racks':[['Wall'], ['dummy']],
            'TV Units':  [['Wall'], ['dummy']],
            'Drawers':   [['Wardrobes', 'Dressers'], ['dummy']],
            'Display Units': [['Wall'], ['dummy']],
            'Wardrobes': [['Wall'], ['Drawers']],
            'Beds':      [['Wall'], ['Dressers']], 
            'Prayer Units': [['Wall'], ['dummy']],
            'Dressers':  [['Wall'], ['Drawers']],
            'Bar Units': [['Wall'], ['Chairs']],
            'Partitions':[['dummy'], ['dummy']]
        }
    