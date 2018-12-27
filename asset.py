# Class for furniture Assets

class Asset:

    # Product features
    __slots__ = ('_category', '_subcategory', '_vertical', '_price', '_dimension')
    
    def __init__(self, asset_category, asset_subcategory, asset_vertical, asset_price, asset_dimension):
        self._category = asset_category
        self._subcategory = asset_subcategory
        self._vertical = asset_vertical
        self._price = asset_price
        self._dimension = asset_dimension