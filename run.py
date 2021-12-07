
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood
from nnf import true, false

# Encoding that will store all of your constraints
E = Encoding()

#board constraints
size_x = 5
size_y = 4


#represents a single piece on the board and stores it's coordinates and which way it faces
class Piece:
    
    #initializes piece, gives coordinates and direction
    def __init__(self, x, y, d):
        
        #d for direction
        self.x = x
        self.y = y
        self.d = d
        
        #array of booleans that holds true when the piece is in a spot
        self.x_val = []
        self.y_val = []
        self.d_val = []
    
        #initialize all fields with arrays containing the bauhaus 'false' node
        for i in range(4):
            self.x_val.append(false)
            self.y_val.append(false)
            self.d_val.append(false)
        self.x_val.append(false)
        
        #the element in each array corresponding to its position/direction is set to true, so e.g. x_val=[F, F, T, F, F],
        #y_val=[F, T, F, F], d_val = [F, F, F, T] denotes a piece at (3, 2) with mirrored side facing NW.
        self.x_val[x] = true
        self.y_val[y] = true
        self.d_val[d] = true
        
    #variables for modifying position and orientation of pieces, to be used in constraint code
    
    # inc_x increases the value of x by 1 moving the piece to the right by 1 on the board
    def inc_x(self):
        for i in range(5):
            if (self.x_val[i] == true) and (i < 4):
                c = i
        
        #basic error handling; increment the x position unless it as at the max x position, or if some other error has occured.
        if (c != None):
            self.x_val[c] = false
            self.x_val[c+1] = true
            return 1
        return 0
    
    # dec_x decreases the value of x by 1 which moves it to the left by 1 on the board
    def dec_x(self):
        for i in range(5):
            if (self.x_val[i] == true):
                c = i
        
        if (c != None):
            self.x_val[c] = false
            self.x_val[c-1] = true
            return 1
        return 0
    
    # inc_y increases the value of y by 1 which moves the piece up by 1 on the board
    def inc_y(self):
        for i in range(4):
            if (self.y_val[i] == true) and (i < 3):
                c = i
        
        if (c != None):
            self.y_val[c] = false
            self.y_val[c+1] = true
            return 1
        return 0
    
    # dec_y decreases the value of y by 1 which moves the piece down by 1 on the board
    def dec_y(self):
        for i in range(4):
            if (self.y_val[i] == true):
                c = i
        
        if (c != None):
            self.y_val[c] = false
            self.y_val[c-1] = true
            return 1
        return 0
    
    #rotates the piece right by 90 degrees
    def rotr(self):
        for i in range(4):
            if (self.d_val[i] == true):
                c = i
        
        if (c != None):
            if (c < 3):
                self.d_val[c] = false
                self.d_val[c+1] = true
            else:
                self.d_val = [true, false, false, false]
            return 1
        return 0
    
    #rotates the piece left by 90 degrees
    def rotl(self):
        for i in range(4):
            if (self.d_val[i] == true):
                c = i
        if (c != None):
                self.d_val[c] = false
                self.d_val[c-1] = true
                return 1
        return 0
    
    #allows other functions to get x, y coordinates and d direction
    def get_x(self):
        x_current = -1
        for i in range(5):
            if (self.x_val[i] == true):
                x_current = i
        return x_current
    
    def get_y(self):
        y_current = -1
        for i in range(5):
            if (self.y_val[i] == true):
                y_current = i
        return y_current
    
    def get_d(self):
        d_current = -1
        for i in range(4):
            if (self.d_val[i] == true):
                d_current = i
        return d_current


#sits on the last col of the grid, can be initialized along this line
class King:
    
    #only has a y value because x stays the same
    def __init__(self):
        self.y = 3
        self.x = 4
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
            
#d means something different for laser vs piece
#0 = N
#1 = E
#2 = S
#3 = W

#d for Piece represents the ordinal direction of the mirrored side
#0 = NE
#1 = SE
#2 = SW
#3 = NW

class Laser():
    
    #initisalizes the laser board, giving it one spot that is true
    def __init__(self, x, y, d):
        
        self.x = x
        self.y = y
        self.d = d
        
        self.x_val = []
        self.y_val = []
        self.d_val = []
        
        for i in range(size_y):
            self.x_val.append(false)
            self.y_val.append(false)
            self.d_val.append(false)
        self.x_val.append(false
        
        self.x_val[x] = true
        self.y_val[y] = true
        self.d_val[d] = true
    
     #moves the laser by 1, x increases
     def inc_x(self):
        
        for i in range(size_x):
            if (self.x_val[i] == true) and (i < size_x):
                c = i
            
            if (c != None):
                self.x_val[c] = false
                self.x_val[c+1] = true
        
     #moves the laser along x axis, x decreases
     def dec_x(self):
        
        for i in range(size_x):
            if (self.x_val[i] == true) and (i > 0):
                c = i
            
            if (c != None):
                self.x_val[c] = false
                self.x_val[c-1] = true 
                
    def inc_y(self):
        
        for i in range(size_y):
            if (self.y_val[i] == true) and (i < size_y):
                c = i
            
            if (c != None):
                          if (c < 3):
                            self.y_val[c] = false
                            self.y_val[c+1] = true
                          elif (c == 3):
                              self.y_val = [true, false, false, false]
                        
     def dec_y(self):
        
        for i in range(size_y):
            if (self.y_val[i] == true) and (i > 0):
                c = i
            
            if (c != None):
                self.y_val[c] = false
                self.y_val[c-1] = true
                
    def rotr(self):
          for i in range(4):
                          if (self.d_val[i] == true):
                              c = i
                          
        if (c != None):
                          if (c < 3):
                              self.d_val[c] = false
                              self.d_val[c+1] = true
                          else:
                              self.d_val = [true, false, false, false]
          
                    
    def rotl(self):
        
        for i in range(4):
            if self.dval[i] == true):
                c = i
                
        if (c != None):
            self.d_val[c] = false
            self.d_val[c-1] = true
            
    #allows other functions to get x, y coordinates and d direction
    def get_x(self):
        x_current = -1
        for i in range(5):
            if (self.x_val[i] == true):
                x_current = i
        return x_current
    
    def get_y(self):
        y_current = -1
        for i in range(5):
            if (self.y_val[i] == true):
                y_current = i
        return y_current
    
    def get_d(self):
        d_current = -1
        for i in range(4):
            if (self.d_val[i] == true):
                d_current = i
        return d_current
            
#makes instances
king = King()
p1 = Piece()
p2 = Piece()
p3 = Piece()
p4 = Piece()
l = Laser()

all_pieces = [p1, p2, p3, p4]

def check_valid(obj, x_change, y_change):
    #tells you whether the inputted object (either a piece or a laser) can move to the desired position.
    #x_change and y_change can both have values -1, 0 or 1 (i.e. (0, -1) represents moving one position downwards)
    
    #calculate desired x, y position
    x_desired = obj.get_x() + x_change
    y_desired = obj.get_y()  + y_change
    
    #check that space is not already occupied
    for piece in all_pieces:
        if (piece.get_x() == x_desired and piece.get_y() == y_desired):
            return false
    
    #check that space is on the board
    if (0 < x_desired or x_desired > 4 or 0 < y_desired or y_desired > 3):
        return false
    
    #check that the space is not occupied by the king(his position is hardcoded)
    if (x_desired == 4 and y_desired == 3):
        return false
    
    #if space is empty and on board, can me moved to
    return true

def piece_constraints():

    for i in all_pieces:
        E.add_constraint(i.x_val[0] | i.x_val[1] | i.x_val[2] | i.x_val[3] | i.x_val[4])
        E.add_constraint(i.y_val[0] | i.y_val[1] | i.y_val[2] | i.y_val[3])
        E.add_constraint(i.d_val[0] | i.d_val[1] | i.d_val[2] | i.d_val[3])

        
        for j in range(5):
            for k in range(5):
                if (k != j):
                    E.add_constraint(~(i.x_val[j] & i.x_val[k]))
        for j in range(4):
            for k in range(4):
                if (k != j):
                    E.add_constraint(~(i.y_val[j] & i.y_val[k]))
                    E.add_constraint(~(i.d_val[j] & i.d_val[k]))
                    
        #cannot take up the same spot as another piece
        for j in all_pieces:
            for k in range(5):
                for p in range(4):
                    if (i != j):
                        E.add_constraint(~((i.x_val[k] & j.x_val[k]) & (i.y_val[p] & j.y_val[p]))

                        #king cannot be in the same spot
                        if (k == 4)
                            E.add_constraint(~((i.x_val[k]) & (i.y_val[p] & king.y_val[p]))
                                                                                        
        if (i.x_val[4] == true):
            E.add_constraint((i.inc_x().negate()))
        if (i.x_val[0] == true):
            E.add_constraint((i.dec_x().negate()))
        if (i.y_val[3] == true):
            E.add_constraint((i.inc_y().negate()))
        if (i.y_val[0] == true):
            E.add_constraint((i.dec_y().negate()))
                                             
                                             
    return E
                                             
      
def laser_constraints():
 
   all_pieces = [p1, p2, p3, p4]
    # Laser cannot be in more than one x or y value at the same time.
    E.add_constraint(l.x_val[0] or l.x_val[1] or l.x_val[2] or l.x_val[3] or l.x_val[4])
    E.add_constraint(l.y_val[0] or l.y_val[1] or l.y_val[2] or l.y_val[3])
    
    # Laser cannot have more than one direction.
    E.add_constraint(l.d_val[0] or l.d_val[1] | l.d_val[2] | l.d_val[3])

    # Laser only continues if it does not make contact with any pieces and does not go out of bounds.
    laser_check = true
    for p in all_pieces:
        for i in range(5):
            for j in range(4):
                if (l.x_val[i] != p.x_val[i] and l.y_val[j] != p.y_val[j]):
                    laser_check = true
                else:
                    laser_check = false

    # If laser does not make contact with any pieces.
    if (laser_check == true):
        # Check if laser goes out of bounds based on x/y value and direction.
        # d.val 0 = N
        if (l.d_val[0] == true and l.y_val[3] == true):
            E.add_constraint((l.inc_y()).negate())
        # d.val 1 = E
        elif (l.d_val[1] == true and l.x_val[4] == true):
            E.add_constraint((l.inc_x()).negate())
        # d.val 2 = S
        elif (l.d_val[2] == true and l.y_val[0] == true):
            E.add_constraint((l.dec_y()).negate())
        # d.val 3 = W
        elif (l.d_val[3] == true and l.x_val[0] == true):
            E.add_constraint((l.dec_x()).negate())

    # If laser has made contact with a piece
    else:
        for k in all_pieces:
            for i in range(5):
                for j in range(4):
                    
                    if ((l.x_val[i] == k.x_val[i] and l.y_val[j] == k.y_val[j]) and
                        (l.d_val[0] and k.d_val[1]) or (l.d_val[1] and k.d_val[2]) or (l.d_val[2] and k.d_val[3]) or (l.d_val[3] and k.d_val[0])):
                        l.rotr()
                        
                    if ((l.x_val[i] == k.x_val[i] and l.y_val[j] == k.y_val[j]) and
                        (l.d_val[0] and k.d_val[2]) or (l.d_val[1] and k.d_val[3]) or (l.d_val[2] and k.d_val[0]) or (l.d_val[3] and k.d_val[1])):
                        l.rotl()
                        
                    # If laser makes contact with piece, but wrong direction.
                    else:
                        E.add_constraint((l.d_val[k]).negate())
                    
    return E

def king_constraints():

    
    E.add_constraint(king.y_val[0] | king.y_val[1] | king.y_val[2] | king.y_val[3])

    for j in range(4):
        for k in range(4):
            if (k != j):
                E.add_constraint(~(king.y_val[j] & king.y_val[k]))

    return E
# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.

def constraint_function():
    # Add custom constraints by creating formulas with the variables you created. 
    for x in range(size_x):
        E.add_constraint(
    
    E.add_constraint((a | b) & ~x)
    # Implication
    E.add_constraint(y >> z)
    # Negate a formula
    E.add_constraint((x & y).negate())
    # You can also add more customized "fancy" constraints. Use case: you don't want to enforce "exactly one"
    # for every instance of BasicPropositions, but you want to enforce it for a, b, and c.:
    constraint.add_exactly_one(E, a, b, c)

    return E


if __name__ == "__main__":

    T = piece_constraints()
    T = laser_constraints()
    # Don't compile until you're finished adding all your constraints!
    T = T.compile()
    # After compilation (and only after), you can check some of the properties
    # of your model:
    print("\nSatisfiable: %s" % T.satisfiable())
    print("# Solutions: %d" % count_solutions(T))
    print("   Solution: %s" % T.solve())

    print("\nVariable likelihoods:")
    for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
        # Ensure that you only send these functions NNF formulas
        # Literals are compiled to NNF here
        print(" %s: %.2f" % (vn, likelihood(T, v)))
    print()

