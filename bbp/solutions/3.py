from collections import Counter 
from itertools import chain

class Annotation:
    '''
    Just a general comment: as I understood the explanation, this class builds just a voxel. Just one. 
    And that voxel is always the (0, 0, 0) voxel. But, data is an N-d array, which maps voxels to values. 
    For instance, data[0][0][0] is the value of voxel (0, 0, 0); data[1][1][1] is the value of voxel (1,1,1).
    
    So, for the 'lookup' method, it looks like I will be always returning the value data[0][0][0], if 
    the coordinates given are within range, which seems a bit weird. 
    '''
    def __init__(self, data, voxel_dimensions, origin):
        self.data = data
        
        # Just to make sure everything is a tuple
        self.voxel_dimensions  = tuple(voxel_dimensions)
        self.lower_corner      = tuple(origin)
        self.upper_corner      = tuple(orig + dimension for orig, dimension in zip(origin, voxel_dimensions))
        
        self.x_low, self.y_low, self.z_low = self.lower_corner
        self.x_high, self.y_high, self.z_high = self.upper_corner

    def lookup(self, coordinate):
        """ Return voxel value corresponding to point `coordinate`.

        Coordinate: x, y, z position in 'real space'
        """
        # Assuming coordinate is a list or tuple
        x, y, z = coordinate

        if (not (self.x_low <= x <= self.x_high 
                and self.y_low <= y <= self.y_high 
                and self.z_low <= z <= self.z_high)):
            
            raise IndexError(f'Coordinate {x}, {y}, {z} is outside this voxel!')

        try:
            # If this voxel always maps to 0, 0, 0!
            value = self.data[0][0][0]

        except KeyError:
            raise IndexError(f'Coordinate {x}, {y}, {z} not contained in data!')

        else:
            return value


    def count(self, values):
        """ Count the number of voxel with value from `values` (could be a scalar or list/tuple/set/numpy array)"""
        value_to_n_voxels = Counter()

        # First, convert to flatten list
        flatten_values = list(chain.from_iterable(self.data))

        # Count
        value_counter = Counter(flatten_values)

        # Assuming values is a subset of the values in self.data, and values is an iterable
        for value in values:
            value_to_n_voxels[value] = value_counter[value]

        return value_to_n_voxels
