rows = 'ABCDEFGHI'
columns = '123456789'
first_grid_string = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'

def grid_unit_creator (row, column): #Concatenates all possible combinations of the given parameters
    return [i + j for i in row for j in column]

#Same outcome as the function above except easier to understand 
# def grid_unit_creator (row, column): 
#     grid_array = []
#     for i in row:
#         for j in column:
#             grid_array.append(i+j)
#     return grid_array
            
boxes = grid_unit_creator(rows, columns) #Returns all the boxes of the sudoku grid
row_units = [grid_unit_creator(row, columns) for row in rows] #Returns all the rows of the sudoku grid
col_units = [grid_unit_creator(rows, column) for column in columns] #Returns all the columns of the sudoku grid
square_units = [grid_unit_creator(square_row, square_column) for square_row in ('ABC', 'DEF', 'GHI') for square_column in ('123', '456', '789')] #Returns all the boxes of the sudoku grid
unit_list = row_units + col_units + square_units
units = dict((s, [u for u in unit_list if s in u]) for s in boxes) #Maps the row, column, and 3x3 square that every box belongs to
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes) #Maps all the peers of every box

def grid_values(grid):

    values = []
    all_digits = '123456789'

    for value in grid:
        if value == '.':
            values.append(all_digits)
        elif value in all_digits:
            values.append(value)

    #print(f'The boxes are {boxes}\n The values are {values}\n')
    assert len(values) == 81
    grid_dictionary = dict(zip(boxes, values))
    return grid_dictionary

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1] #Returns the boxes that have solved values based on the prompted grid
    #print(f'Here are the values {values}\n Here are the value keys {values.keys()}')
    for box in solved_values:
        digit = values[box] #Digit equals the values of the solved boxes
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values): #This function goes over every box and sees if there is a unique only choice for a box, then it assigns it
    for unit in unit_list:
        for digit in '123456789':
            possible_digits = [box for box in unit if digit in values[box]]
            if len(possible_digits) == 1:
                values[possible_digits[0]] = digit
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

eliminate(grid_values(first_grid_string))
#print(reduce_puzzle(grid_values(first_grid_string)))





