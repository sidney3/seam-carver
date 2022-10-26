'''
Seamcarve Homework

The code in this file does the following:
1. It takes in an image (filename in the same directory),
2. Reads it into a 3D array,
3. Processes the 3D array to extract the RGB colors, 
4. Computes the cell costs (color deltas) to produce a 2D array of importance values, and
4. Uses Dynamic Programming to produce the lowest-cost seam as an array of column ids to cut. 
'''
from importance_calculator import ImportanceCalculator
from PIL import Image
import numpy as np
import argparse
import copy

class SeamCarve:
    '''
    This is a class that contains code for finding the "least important" seams,
    and apply it to image resizing.
    '''

    def __init__(self, image_path: str):
        '''
        Initialization method for the SeamCarve class.
        DO NOT EDIT this method.
        '''
        # Convert an input image to a 3D array (row (height), column (width), color value (RGBA))
        self.image_array = np.array(Image.open(image_path)) # image file path has to be in the same directory
        self.image_height = len(self.image_array) # get the number of rows (height dimension)
        self.image_width = len(self.image_array[0]) # get the number of columns (width dimension)
        self.costs = None
        self.dirs = None

    def argmin(self, array: list) -> int:
        '''
        Returns the minimum element's "index"
        of a given row (not the element itself)

        Parameters: 
        array -- a 1-D array representing a
         single row of the image.

        Returns: 
        a number -- the minimum element's INDEX
         in the given row
        '''
        index = 0
        min_index = index
        #this will implicitly tiebreak - we go from left to right
        #  so we already favor leftmost minimum values
        for arg in array:
            if arg < array[min_index]:
                min_index = index
            index += 1
        return min_index


    def find_least_important_seam(self, vals): # Our input, "vals"
        # is a 2D array containing the image's "importance values".
        '''
        Given a 2D array of importance values, this method
         finds the "least important seam" using the
        seamcarve algorithm and dynamic programming.

        Parameters:
        vals -- a 2D array storing "importance values", where
         an importance value indicates
        how much color contrast a pixel has with its neighbors.

        Returns: 
        A least-important seam in the image that is most unlikely
        to cause change in the original image when taken out.
        '''
        self.fill_costs_dirs(vals)
        curr_index = self.argmin(self.costs[0])
        curr_row = 0
        seam = []
        while(curr_row < self.image_height-1):
            seam.append(curr_index)
            #our dir array entry at the current
            #  position tells us what to do to
            #  our index to remain on the ideal
            # path note that this will never take
            #  us to an illegal entry as our dir's
            #  edges can only map down and inward
            curr_index += self.dirs[curr_row][curr_index]
            curr_row += 1
        seam.append(curr_index) #last row
        return seam
            

  
    def fill_costs_dirs(self, vals :list):
        '''
        Takes in empty 2d arrays for "costs" (cost to vertically
         reach a specific position in image) and "dirs" 
        (directions leading in most efficient path up tree) and
         fills them in. This is done in one method as these
        two tables can be filled in concurrently (as dirs depends
         directly upon cost). We don't "need" to pass these in,
        but doing so in such a way ensures that empty arrays
         are never inputted.

        Returns none as the purpose of this method just to
         fill in costs, dirs
        '''
        self.costs = \
            [[None for ignored in range(self.image_width)]\
             for ignored in range(self.image_height)]
        self.dirs = \
            [[None for ignored in range(self.image_width)]\
             for ignored in range(self.image_height-1)]
        self.init_bottom_costs_row(self.costs, vals)


        #we work from the bottom of our table (note that the "row"
        #  index var refers to both costs and dirs tables, as they are of
        # the same dimension). 
        for row in range(self.image_height - 2, -1, -1):
            for col in range(self.image_width):
                #far left edge, thus we consider only bottom and
                #  bottom-right cells as origin points
                if col == 0:
                    considered_vals = [self.costs[row+1][col],\
                         self.costs[row+1][col+1]]
                    index = self.argmin(considered_vals)
                    self.costs[row][col] = considered_vals[index]\
                         + vals[row][col]
                    #when travelling down the array, if we arrive upon
                    #  this cell, we will clearly go to the cheapest route downward,
                    #and thus we can just assign these values (note that
                    #  here we are working with 0,1 which are equiv, directionwise,
                    # to 0,1, whereas in below instances we are working
                    #  with 0,1,2 which apython3 seamcarve.pyre equiv to
                    #  -1,0,1 directionally)
                    self.dirs[row][col] = index
                # far right edge and we only need to consider below and
                #  left cells as origin points
                elif col == self.image_width-1:
                    considered_vals = \
                        [self.costs[row+1][col-1],\
                         self.costs[row+1][col]]
                    index = \
                        self.argmin(considered_vals)
                    self.costs[row][col] = considered_vals[index]\
                         + vals[row][col]
                    self.dirs[row][col] = index - 1
                #normal middle case
                else:
                    considered_vals = \
                        [self.costs[row+1][col-1],\
                         self.costs[row+1][col], self.costs[row+1][col+1]]
                    index = self.argmin(considered_vals)
                    self.costs[row][col] = considered_vals[index]\
                         + vals[row][col]
                    self.dirs[row][col] = index - 1

    def init_bottom_costs_row(self, costs:list, vals:list):
        '''
        As the "base case" (not depending on any algorithm)
         of our costs value is given simply by the 
        respective 'val' at that cell (or, rather, image_array[
            that cell's index]), we fill this in here
        '''

        #in each column, the (image-height)'th element is equivalent
        #  to that corresponding cell value in self.image_array
        for col in range(self.image_width):
            costs[self.image_height-1][col]\
                 = vals[self.image_height-1][col]

    def calculate_importance_values(self):
        '''
        Uses the ImportanceCalculator class
         to calculate the importance values for 
        each pixel in the image

        Returns: 
        the 2D array of calculated importance values for each pixel

        DO NOT EDIT this method.
        '''
        importance_calc = ImportanceCalculator(self.image_array)
        return importance_calc.calculate_importance_values()

    def check_bounds(self, new_row: int, new_col: int) -> bool:
        '''
        Helper method to check if the given coordinate is out of bounds. 

        Returns:
        A boolean -- True if the passed in coordinate is within the image's bounds, else return False.

        DO NOT EDIT this method.
        '''
        if new_row < 0 or new_row >= self.image_height or new_col < 0 or new_col >= self.image_width:
            return False # out of bounds
        return True # else, this coordinate is within bounds.



####################################################################################
###################### DO NOT MODIFY ANY CODE BELOW THIS LINE ######################
####################################################################################

def parse_args():
    '''
    Parses command line arguments for image file path and number of seams carved
    
    DO NOT EDIT this method.
    '''
    parser = argparse.ArgumentParser(
        description="for running seamcarve on a chosen image!",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '--path',
        default='seamcarve_images/sample1.png',
        help='''The file path of our chosen image'''
    )
    parser.add_argument(
        '--seamcount',
        default=1,
        help='''The number of seams we want to identify'''
    )

    return parser.parse_args()

# stores parsed arguments
ARGS = parse_args()

# This is the main method that runs the program
if __name__ == "__main__":
    # create instance of seamcarve class with given image
    mySeamCarve = SeamCarve(ARGS.path)

    # create copy of image array to crop seam by seam
    carved_array = copy.deepcopy(mySeamCarve.image_array)

    # carve the given number of seams out (default 1)
    for i in range(int(ARGS.seamcount)):
        # Actual production of the least important seam below, using all of the helper methods
        importance_array = mySeamCarve.calculate_importance_values() # calculate importance values using the input image array.
        seam = mySeamCarve.find_least_important_seam(importance_array) # then, we find the lowest-cost (least important) seam, in the form of a 1D array of column ids.
        # get current dimensions
        r, c, k = carved_array.shape

        # make a mask of pixels to remove
        mask = np.ones((r, c), dtype=np.bool)

        # deal with seam not found case
        if seam is None:
            print("seam not found!")
        else:
            # Visualize the seam with a white color (255, 255, 255, 255) (RGBA)
            # For a bright image, you can use black (0, 0, 0, 255) instead
            for row in range(mySeamCarve.image_height): # for every row,
                column_index_to_cut = seam[row] # get column index for that row (column id to cut)
                mySeamCarve.image_array[row][column_index_to_cut][0] = 200 # make it white
                mySeamCarve.image_array[row][column_index_to_cut][1] = 200
                mySeamCarve.image_array[row][column_index_to_cut][2] = 200
                mask[row][column_index_to_cut-i] = False
            # stack the mask to match number of channels in image
            mask = np.stack([mask]*k, axis=2)
            # carve a seam out
            carved_array = carved_array[mask].reshape((r, c -  1, k))

    # show image with seams overlaying it
    img = Image.fromarray(mySeamCarve.image_array)
    img.show()

    # show image with seams carved out
    img = Image.fromarray(carved_array)
    img.show()