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
max_initial_assets = 5

## flags
visualizer_on = False

## group relationship dictionary => asset_subcategory: [parent_subcategories, child_subcategories]
pairwise_rel = {
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

## Desired count of each item subcategory
desired_qty = {
            'Sofas':1,
            'Chairs':1,
            'Tables':1,
            'Dining':1,
            'Shoe Racks':1,
            'TV Units':1,
            'Drawers':1,
            'Display Units':1,
            'Wardrobes':1,
            'Beds':1,
            'Prayer Units':1,
            'Dressers':1,
            'Bar Units':1,
            'Partitions':1
        }

## primary , secondary functionality
asset_subcategory_functions = {
            'Sofas':['Sit','Sleep'],
            'Chairs':['Sit', 'dummy'],
            'Tables':['Sit', 'dummy'],
            'Dining':['Sit', 'dummy'],
            'Shoe Racks':['Storage', 'dummy'],
            'TV Units':['Watch', 'dummy'],
            'Drawers':['Storage', 'dummy'],
            'Display Units':['Display', 'dummy'],
            'Wardrobes':['Storage', 'dummy'],
            'Beds':['Sleep', 'dummy'],
            'Prayer Units': ['Display', 'dummy'],
            'Dressers':['Storage', 'dummy'],
            'Bar Units':['Sit', 'Display'],
            'Partitions': ['Display', 'dummy']
}

room_necessary_functions = {
   'LivingRoom': ['Sit', 'Watch', 'Display', 'Light']
}
