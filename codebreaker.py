'''
This is your CodeBreaker class! You will be responsible for filling in the logic 
of this based on the instructions from the handout and TODO comments below
'''


from os import remove


class CodeBreaker:
    def __init__(self, start_word: str, end_word: str):
        '''
        CodeBreaker constructor. Defines variables and initializes the similarity array

        You are responsible for initializing self.similarity_array in this method
        '''
        # A letter's case does not matter,
        #  we use lower() to make input words all lower-case
        self.start_word = start_word.lower()
        self.end_word = end_word.lower()
        
        #if len(list(self.start_word)) > 0
        #  and len(list(self.end_word)) > 0:
        #    self.trim_words()

        self.similarity_array = self.fill_similarities()
        
    def find_score(self) -> int: 
        '''
        Since our table indexes by intersection of
         words to the point of the cell (vertically 
        or horizontally), and our result, we find our
         desired result at (0,0)
        '''
        return self.similarity_array[0][0]


    def fill_similarities(self):
        '''
        Creates and computes a 2 dimensional array
         where columns represent the letters in a starter word,
        rows represent letters in a target word (that we
         compare to the starter word), and each cell computes
        the difference between (the word given by letters in
         the rows including and below the cell) and
        (the word given by letters in columns including and
         to the right of the cell). 
        '''
   
        similarity_array = \
            [[None for ignored in range(len(self.end_word) + 1)]\
             for ignored in range(len(self.start_word) + 1)]
        #base case
        self.init_list(similarity_array)
        #increasing case
        for row in range(len(self.start_word) - 1, -1, -1):
            self.fill_row(similarity_array, row)
        return similarity_array
    def fill_row(self, fill_list : list, row : int):
        '''
        As we need for each cell we examine to have
         a bottom right, below, and right cell, we can
        iterate through our cells row by row, from bottom
         to top, from right to left (we see that this achieves
        desired sequencing). Thus, this method represents one
         such iteration of a row, and is called iteratively for
          each row
        '''
        start_word_lst = list(self.start_word)
        end_word_lst = list(self.end_word)

        for col in range(len(self.end_word)-1, -1, -1):
            #check if match at target cell
            if (end_word_lst[col] == start_word_lst[row]): 
                fill_list[row][col] = fill_list[row+1][col+1]
            else:
                #Otherwise such a string will require at least one operation
                fill_list[row][col] = min(fill_list[row+1][col],\
                     fill_list[row][col+1],\
                          fill_list[row+1][col+1]) + 1
    def init_list(self, fill_list : list):
        '''
        fills in the base cases (cells for which we 
        do not have a bottom right + below + right cell to compare to,
        as described in fill_similarities algo).
        '''
        #fill in rightmost side of table
        for row in range(len(self.start_word) + 1):
            fill_list[row][len(self.end_word)]\
                 = len(self.start_word) - row
        #fill in bottommost row of table
        for col in range(len(self.end_word) + 1):
            fill_list[len(self.start_word)][col]\
                 = len(self.end_word) - col
                
if __name__ == '__main__':
    cb = CodeBreaker('', 'dog')
    print(cb.similarity_array)