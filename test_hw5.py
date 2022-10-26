import pytest

from codebreaker import *
from seamcarve import *


'''
Dodebreaker tests:
General protocol: we test all possible functionality
 + various edge cases, in each case ensuring that both
the fill_similarities array and the cost are as expected.
 Each described function is some
unique behavior that we want to ensure our functionality encompasses.
'''
def test_full_overlap():
  '''
  full overlap of words between second and first
  (lap is a subset of slap) 
  '''
  cb = CodeBreaker('slap','lap')
  assert cb.find_score() == 1
  assert cb.similarity_array == \
    [[1, 2, 3, 4],
     [0, 1, 2, 3],
      [1, 0, 1, 2],
       [2, 1, 0, 1],
        [3, 2, 1, 0]]
  
def test_minor_overlap():
  '''
  some overlap of words between second and first
  (second word is NOT a subset of the first but
   there is a non-empty
  subset of the second word that is also a subset
   of the first)
  '''
  cb = CodeBreaker('slap','trlap')
  assert cb.find_score() == 2
  assert cb.similarity_array == \
    [[2, 1, 1, 2, 3, 4],
     [2, 1, 0, 1, 2, 3],
      [3, 2, 1, 0, 1, 2],
       [4, 3, 2, 1, 0, 1],
        [5, 4, 3, 2, 1, 0]]

def test_repeated_letters():
  '''
  letters repeated in the first word. This specific behavior
  ensures that we aren't using the same letter twice in our
  example words
  '''
  cb = CodeBreaker('apple', 'aple')
  assert cb.find_score() == 1
  assert cb.similarity_array == \
    [[1, 2, 3, 4, 5],
     [1, 1, 2, 3, 4],
      [1, 0, 1, 2, 3],
       [2, 1, 0, 1, 2],
        [3, 2, 1, 0, 1],
         [4, 3, 2, 1, 0]]
def test_repeated_letters_other_order():
  '''
  Since the above test is so critical, we test
   it again with differing
  first and second words
  '''
  cb = CodeBreaker('aple', 'apple')
  assert cb.find_score() == 1
  assert cb.similarity_array == \
    [[1, 1, 1, 2, 3, 4],
     [2, 1, 0, 1, 2, 3],
      [3, 2, 1, 0, 1, 2],
       [4, 3, 2, 1, 0, 1],
        [5, 4, 3, 2, 1, 0]]

def test_non_adj_repeats():
  '''
  letters repeated but seperated by a different letter
  '''
  cb = CodeBreaker('aplple', 'apple')
  assert cb.find_score() == 1
  assert cb.similarity_array == \
    [[1, 2, 3, 4, 5, 6],
     [2, 1, 2, 3, 4, 5],
      [2, 1, 1, 2, 3, 4],
       [2, 1, 0, 1, 2, 3],
        [3, 2, 1, 0, 1, 2],
         [4, 3, 2, 1, 0, 1],
          [5, 4, 3, 2, 1, 0]]


def test_caps():
  '''
  differentiation of capitalization between 
  the same words. (Since DoG and dog contain
  the same characters we would expect)
  them to evaluate to 0
  '''
  cb = CodeBreaker('DoG', 'dog')
  assert cb.find_score() == 0
  assert cb.similarity_array == \
    [[0, 1, 2, 3],
     [1, 0, 1, 2],
      [2, 1, 0, 1],
        [3, 2, 1, 0]]
def test_1_len():
  '''
  special case of input word of length 1
  '''
  cb = CodeBreaker('d', 'dog')
  assert cb.find_score() == 2
  assert cb.similarity_array == \
    [[2, 2, 1, 1],
     [3, 2, 1, 0]]
def test_0_len():
  '''
  other major special case of word of len 0
  '''
  cb = CodeBreaker('', 'dog')
  assert cb.find_score() == 3
  assert cb.similarity_array == \
    [[3, 2, 1, 0]]


'''
We test full functionality for seamcarve
 (in which there are much fewer edge cases than
codebreaking), and then evaluate the more deep
 edge cases of min_index tiebreaks
'''
def test_5x5_example(): #5x5 sample functionality test on SeamCarve
  '''
  This tests the full breadth of seamcarve functionality,
   dirs, seams, and expected seam
  on complicated functionality. 
  '''
  sc_spreadsheet = SeamCarve("5x5_image.png")
  importance = [[255,168.3333333,125,211.6666667,255],\
    [211.6666667,93.75,190,255,255],
  [213.3333333,97.5,192.5,255,255],[255,192.5,130,192.5,255],\
    [255,255,171.6666667,130,192.5]]

  expected_costs = [[706.25,619.5833333,576.25,759.1666667,962.5],\
    [569.1666667,451.25,547.5,707.5,770],
  [577.5,357.5,452.5,515,577.5],[510,364.1666667,260,322.5,385],\
    [255,255,171.6666667,130,192.5]]

  expected_dirs = [[1,0,-1,-1,-1],[1,0,-1,-1,-1],\
    [1,1,0,-1,-1],[0,1,1,0,-1]]
  expected_seam = [2,1,1,2,3]

  computed_seam = sc_spreadsheet.\
    find_least_important_seam(importance)
  for i in range(0, 5):
    for j in range(0, 5):
        assert sc_spreadsheet.costs[i][j] == \
          pytest.approx(expected_costs[i][j])
  assert sc_spreadsheet.dirs == expected_dirs
  assert computed_seam == expected_seam
def test_5x5_tiebreaks():
  '''
  One other key piece of functionality for
   seamcarve is the tiebreaking mechanics. We want our
  path to prioritize leftmost movement, and
   thus we set up the following test:
  '''
  sc_spreadsheet = SeamCarve("5x5_image.png")
  importance = [[255,255,125,211.6666667,255],\
    [93.75,93.75,190,255,255],
  [213.3333333,97.5,192.5,255,255],[255,192.5,130,130,130],\
    [255,255,171.6666667,130,192.5]]
  #note the several repeated values

  expected_costs = [[706.25, 706.25, 576.25, 759.1666667, 962.5],
   [451.25, 451.25, 547.5, 707.5, 770],\
      [577.5, 357.5, 452.5, 515, 515],
    [510, 364.1666667, 260, 260, 260],\
       [255, 255, 171.6666667, 130, 192.5]]
  expected_seam = [2, 1, 1, 2, 3]
  expected_dirs = [[0, -1, -1, -1, -1],\
     [1, 0, -1, -1, -1],
   [1, 1, 0, -1, -1], [0, 1, 1, 0, -1]]
  computed_seam = sc_spreadsheet.\
    find_least_important_seam(importance)

  for i in range(0, 5):
    for j in range(0, 5):
        assert sc_spreadsheet.costs[i][j]\
           == pytest.approx(expected_costs[i][j])
  
  assert sc_spreadsheet.dirs == expected_dirs
  assert computed_seam == expected_seam
def check_min_index_tiebreaking():
  '''
  We want to tiebreak leftwise, 
  so we ensure this behavior is seen
  '''
  lst = [3,3,3,3]
  sc_spreadsheet = SeamCarve("5x5_image.png")
  assert sc_spreadsheet.min_index(lst) == 0
def check_min_index_base_func():
  '''
  Basic (and general) functionality
  '''
  lst = [3,9,3,0,2,5,3,1]
  sc_spreadsheet = SeamCarve("5x5_image.png")
  assert sc_spreadsheet.min_index(lst) == 3
def check_min_index_smallest_on_end():
  '''
  An error in the for loop used could lead
   to the final value in a list being ignored,
  so we check that this value is correctly 
  configured with check_min_index
  '''
  lst = [3,1,3,2,0]
  sc_spreadsheet = SeamCarve("5x5_image.png")
  assert sc_spreadsheet.min_index(lst) == 4
def check_min_index_smallest_on_start():
  '''
  Since our calculation to find the minimum
   will begin with the starting value, this
  is an easy one to ignore, so we test for 
  a list where min_index(list) == 0
  '''
  lst = [0,3,2,1]
  sc_spreadsheet = SeamCarve("5x5_image.png")
  assert sc_spreadsheet.min_index(lst) == 0
