assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities from the other boxes in their unit
   
    #display(values)
    twins_spotted={}
    donotadd=False
    
    

    for b in boxes:
        for s in peers[b]:
            if (values[s] == values[b]) and (len(values[b])==2):
                #Check if they have been already spotted
                if (b in twins_spotted.values() and s in twins_spotted.keys()):
                    donotadd=True
                
                #adding to twins dictionary
                if (not donotadd): 
                    twins_spotted[b]=s
                    #print "twins_spotted",twins_spotted
                for t in units[b]:
                    #print "t=", t
                    if s in t and b in t:
                        for i in t:
                            if i!=s and i!=b:
                                #for the twins - dont replace
                                #but remove the two values from other members of the unti
                                str_twin = values[b]
                                #print "i value", values[i],str_twin
                                values[i]= values[i].replace(str_twin[0],'')  
                                values[i]= values[i].replace(str_twin[1],'')
     
    #print ('**')*60
    #display(values)                
    return values



       
def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [ s+t for s in A for t in B]


boxes = cross(rows,cols)
row_units = [cross(r,cols) for r in rows]
col_units=[cross(rows,c) for c in cols]
diag_units1=[rows[i]+ cols[i] for i in range(len(cols))]
diag_units2=[rows[i]+ cols[len(cols)-1-i] for i in range(len(cols))]
diag_units = [diag_units1] + [diag_units2]
square_units = [ cross (r,s)  for r in ('ABC','DEF','GHI') for s in ('123','456','789')]
unitlist = row_units + col_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)

peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    assert len(grid) is 81 , " Grid string should have a length of 81 to proceed"
    grid_init= dict(zip(boxes,grid))
    for k , v in grid_init.items():
        #Check if value is '.' , then replace , else skip
        if grid_init[k]=='.':
            grid_init[k]='123456789'
    
    return grid_init

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return
    

def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    boxes_ready=[b for b in values.keys() if len(values[b])==1]
    #from the boxes that are ready get the value and remove it  from the 
    #possibilities of its peers 
    for b in boxes_ready:
        given_value = values[b]#eliminate this value from all its peers
        for m in peers[b]:
            values[m] = values[m].replace(given_value,'')
    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    #Taking only not ready boxes for comparison
    boxes_notready = []
    for b in boxes:
        if len(values[b])> 1:
            boxes_notready.append(b)
        
    #all strings init
    combineallmultipleposs = ''
    current_string=''
    
    for b1 in boxes_notready:
        current_string = values[b1]
        for i in units[b1]:
            combineallmultipleposs=''
            for k in i:
                if k != b1:
                    app = values[k]
                    combineallmultipleposs = combineallmultipleposs + app                    
            #check for each unit combined string against current string    
            for c in current_string:
                if c not in combineallmultipleposs:
                    #make this as the only choice and set the box to 
                    #this value and break
                    values[b1]=c
                    break
    return values

def single_possibility(values):
    """Impose the single possibility rule.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the boxes with only possibility filled in.
    """
    for u in unitlist:
        if (len([t for t in u if len(t)==1])==7):# a unit in unitlist has 7 filled in 
            for t in u:
                if len(t)>1 :
                    single_poss_candidate = t 
           
        #spot the value possible for this candidate
        all_poss='123456789'
        for t in u :
            if len(t)==1:
                values[single_poss_candidate] = all_poss.replace(values[t],'')
         
    return values
        
def reduce_puzzle(values):
    # To solve the puzzle , to recursively keep reducing the puzzle until
    # after before and after elimination and only choice , there is no  
    #tdifference in the number of solved before and after reducing
    
    stalled = False

    while (not stalled):
        solved_before = [b for b in boxes if len(values[b])==1]
        #naked twin elimination
        values = naked_twins(values)
        #Eliminate against the solved /given boxes with only 1 value
        values = eliminate(values)
        #If a box has a choice which is the only one among its peers
        values = only_choice(values)
        #If all boxes in a unit are filled with unique choice, then single possibility applies
        values = single_possibility(values)
        #To check the boxes if any are resolved after the above step, so 
        #it could recursively be applied to all units across the puzzle
        solved_after = [b for b in boxes if len(values[b])==1]
        stalled = solved_after==solved_before
        if len([box for box in boxes if len(values[box]) == 0]):
            return False
    return values

def search(values):
    """Search by DFS for each option of possibilities.

    Start with the unit with the least set of possibilities, assign one value.
    After reducing the puzzle , if no solution found, 
    then repeat , by getting to the next box with min possibilities and so on.
    In this manner,  the entire grid is spanned and if there is no solution, 
    it will go back to the last parent, apply the next possiblity for that 
    parent and so on

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after searching for solution.
    Final solution is the destination to return
    """    
    #reduce puzzle
    values = reduce_puzzle(values)
    
    #if values is false , failure
    if (not values):
        return False
    #Check if solved - by checking if the length of 
    if all (len(values[s])==1  for s in boxes ):
        return values # Resolved
    
    #Finding box with min possibilities
    n,box_min = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)

    #Start the search , by giving one value out of this as the solution to this
    for v in values[box_min]:
        puzzle_temp = values.copy()
        puzzle_temp[box_min]=v
        #continue the search  to reduce the puzzle and check if solved
        check_attempt = search(puzzle_temp)
        if (check_attempt):
            return check_attempt #return with values once resolved


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    #Assigning value to the grid
    init_values={}
    #Replacing all possibilities instead of blanks or "."
    init_values = grid_values(grid)
    values={}

    for b in boxes:
        assign_value(values,b,init_values[b]) 

    return search(values)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
