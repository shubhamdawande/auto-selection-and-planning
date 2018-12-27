import json
import pprint
from asset import Asset
import pickle

#pprint.pprint([[json.dumps(data_categorys['data']['asset_categorys'][i]['subcategories'][j]['name'], indent=4)
#                    for j in range(0, len(data_categorys['data']['asset_categorys'][i]['subcategories']))]
#                    for i in range(0, len(data_categorys['data']['asset_categorys']))])

## load asset categories
with open("categorys.json", "r") as read_file:
   asset_categorys_json = json.loads(read_file.read())

asset_type = {} # type id : type name
for category in asset_categorys_json['data']['asset_categorys']:
    asset_type[category['_id']] = category['name']
    
    for subcategory in category['subcategories']:
        asset_type[subcategory['_id']] = subcategory['name']

        for vertical in subcategory['verticals']:
            asset_type[vertical['_id']] = vertical['name']

#pprint.pprint(asset_type)

## load asset database
with open("assets.json", "r") as read_file:
    assets_json = json.loads(read_file.read())

asset_data = {} # asset info list
asset_count = assets_json['data']['count']
i = 0

for asset in assets_json['data']['assets']:

    # categories 
    asset_category = asset_type[asset['category']]

    # price
    if 'customer' in asset['price']:
        asset_price = asset['price']['customer']
    else:
        asset_price = 0

    if asset_category == 'Furniture' and asset_price != None:

        # dimension
        if 'dimension' in asset:
            d = asset['dimension']
            asset_dimension = { 'depth' : d['depth'], 'width' : d['width'], 'height' : d['height']}
        
        # subcategories
        if asset['subcategory'] != '':
            asset_subcategory = asset_type[asset['subcategory']]
        else:
            asset_subcategory = ''
        
        # verticals
        if asset['vertical'] != '':
            asset_vertical = asset_type[asset['vertical']]
        else:
            asset_vertical = ''

        asset_data[i] = Asset(asset_category, asset_subcategory, asset_vertical, asset_price, asset_dimension)
        
        print [asset_category, asset_subcategory, asset_vertical, asset_price, asset_dimension]
        
        i += 1

## dump asset data to pickle file
#with open('data/asset_list', 'wb') as fp:
#    pickle.dump(asset_data, fp)