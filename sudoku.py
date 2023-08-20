rows = 'ABCDEFGHI'
columns = '123456789'
first_grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'   
second_grid = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'     

def grid_unit_creator (row, column): #Concatenates all possible combinations of the given parameters and creates the grid labels
    return [i + j for i in row for j in column]
            
boxes = grid_unit_creator(rows, columns) #Returns all the boxes of the sudoku grid
row_units = [grid_unit_creator(row, columns) for row in rows] #Returns all the rows of the sudoku grid
col_units = [grid_unit_creator(rows, column) for column in columns] #Returns all the columns of the sudoku grid
square_units = [grid_unit_creator(square_row, square_column) for square_row in ('ABC', 'DEF', 'GHI') for square_column in ('123', '456', '789')] #Returns all the boxes of the sudoku grid
unit_list = row_units + col_units + square_units  #Contains every row, column, and 3x3 square to apply the only choice strategy
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

    assert len(values) == 81
    grid_dictionary = dict(zip(boxes, values))
    return grid_dictionary

def eliminate(grid):

    grid_values = grid.keys()
    solved_values = [box for box in grid_values if len(grid[box]) == 1] #Returns the boxes that have solved values based on the prompted grid

    for box in solved_values: #Loop through every box in the grid
        digit = grid[box] #Digit equals the values of the solved boxes
        peers_of_solved_boxes = peers[box] #Equals the peers of the solved box

        for peer in peers_of_solved_boxes: #Systematically loop through all the peers of the solved boxes, and if the digit of the solved box is in the digit string of one of its peers, it is removed. This is done repeatedly
            grid[peer] = grid[peer].replace(digit,'')
    
    return grid #Returns a grid that has only solved boxes and a smaller list of possible numbers for the unsolved boxes

def only_choice(values): #This function loops through every unit, either a row, column, or 3x3 square, and sees that if there is a digit that only appears once, hence, the only choice, to assign the box that value

    all_digits = '123456789'
    
    for unit in unit_list: 
        for digit in all_digits: 
            boxes_with_digit = [box for box in unit if digit in values[box]] #This variable stores the peer boxes that contain the certain digit 
            if len(boxes_with_digit) == 1: #If only one box from the peer boxes contains the certain digit, it means it is the only possible place where it can fit, it is the only choice
                values[boxes_with_digit[0]] = digit

    return values

def reduce_puzzle(values):
    
    stalled = False
    while not stalled:

        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1]) #Checks how many boxes have a determined value, meaning they have been solved
        values = eliminate(values) #Use the Eliminate Strategy
        values = only_choice(values) #Use the Only Choice Strategy
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1]) #Checks how many boxes have a determined value, to compare
        stalled = solved_values_before == solved_values_after  #If no new values were added, stop the loop. This means it cannot further reduce the sudoku grid through merely these two constraints

        if len([box for box in values.keys() if len(values[box]) == 0]): #Sanity check, return False if there is a box with zero available values:
            return False
        
    return values

def search(values):

    if values is False: #Sanity check for if it fails earlier. A false value would mean the grid is unsolvable
        return False 
    
    if all(len(values[chosen_box]) == 1 for chosen_box in boxes): #Checks if it has been solved
        return values 
    
    fewest_possibilities, chosen_box = min((len(values[chosen_box]), chosen_box) for chosen_box in boxes if len(values[chosen_box]) > 1) #Chooses one of the unfilled squares with the minimal possibilities
   
    for value in values[chosen_box]:  #Recursively creates a new sudoku and attempts at solving it
        new_sudoku = values.copy()
        new_sudoku[chosen_box] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def display(values):

    width = 1 + max(len(values[box]) for box in boxes)
    line = '+'.join(['-' * (width *3 )] * 3)
    for row in rows:
        print(''.join(values[row + column].center(width)+('|' if column in '36' else '')
                      for column in columns))
        if row in 'CF': print(line)
    print()

#print(search(reduce_puzzle(only_choice(eliminate(grid_values(second_grid))))))
display(search(reduce_puzzle(only_choice(eliminate(grid_values(second_grid))))))
