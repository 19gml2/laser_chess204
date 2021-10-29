
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood
from nnf import true, false

# Encoding that will store all of your constraints
E = Encoding()

size_x = 5
size_y = 4
board = [size_x][size_y]

class Piece:
    
    def __init__(self, x, y, d):
        
        self.x = x
        self.y = y
        self.d = d
        self.x_val = []
        self.y_val = []
        self.d_val = []
    
        #initialize all fields with false arrays
        for i in range(4):
            self.x_val.append(false)
            self.y_val.append(false)
            self.d_val.append(false)
        self.x_val.append(false)
        
        #set one item in each array to true, so e.g. x_val=[F, F, T, F, F], y_val=[F, T, F, F], d_val = [F, F, F, T]
        #denotes a piece at (3, 2) with mirrored side facing NW.
        self.x_val[x] = true
        self.y_val[y] = true
        self.d_val[d] = true
        
    #variables for modifying position and orientation of pieces, to be used in constraint code
    def inc_x(self):
        for i in range(5):
            if (self.x_val[i] == true) and (i < 4):
                c = i
        
        if (c != None):
            self.x_val[c] = false
            self.x_val[c+1] = true
            return 1
        return 0
            
    def dec_x(self):
        for i in range(5):
            if (self.x_val[i] == true):
                c = i
        
        if (c != None):
            self.x_val[c] = false
            self.x_val[c-1] = true
            return 1
        return 0
    
    def inc_y(self):
        for i in range(4):
            if (self.y_val[i] == true) and (i < 3):
                c = i
        
        if (c != None):
            self.y_val[c] = false
            self.y_val[c+1] = true
            return 1
        return 0
    
    def dec_y(self):
        for i in range(4):
            if (self.y_val[i] == true):
                c = i
        
        if (c != None):
            self.y_val[c] = false
            self.y_val[c-1] = true
            return 1
        return 0
    
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
        
    def rotl(self):
        for i in range(4):
            if (self.d_val[i] == true):
                c = i
        if (c != None):
                self.d_val[c] = false
                self.d_val[c-1] = true
                return 1
        return 0


#sits on the last col of the grid, can be initialized along this line
class King:
    
    def __init__(self, y):
        self.y = y
        self.y_val = []
        for i in range(size_y):
            self.y_val.append(false)
        self.y_val[y] = true;
        
    def inc_y(self):
        
        c = self.y
            
        if (c != None):
            if (c < 3):
                self.y_val[c] = false
                self.y_val[c+1] = true
            else:
                self.y_val = [true, false, false, false]
            return 1
        return 0
                
    def dec_y(self):
        
        c = self.y
                    
        if (c != None):
            if (c > 0):
                self.y_val[c] = false
                self.y_val[c-1] = true
            else:
                self.y_val = [false, false, false, true]
            return 1
        return 0
            
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
    
    def __init__(self, x, y, d):
        
        for i in range(size_y):
            self.x_val[i] = false
            self.y_val[i] = false
            self.d_val[i] = false
        self.x_val[4] = false
        
        self.x_val[x] = true
        self.y_val[y] = true
        self.d_val[d] = true
    
     def inc_x():
        
        for i in range(size_x):
            if (x_val[i] == true) and (i < size_x):
                c = i
            
            if (c != None):
                x_val[c] = false
                x_val[c+1] = true
                
     def dec_x():
        
        for i in range(size_x):
            if (x_val[i] == true) and (i > 0):
                c = i
            
            if (c != None):
                x_val[c] = false
                x_val[c+1] = true 
                
    def inc_y():
        
        for i in range(size_y):
            if (y_val[i] == true) and (i < size_y):
                c = i
            
            if (c != None):
                y_val[c] = false
                y_val[c+1] = true
                
     def dec_y():
        
        for i in range(size_y):
            if (y_val[i] == true) and (i > 0):
                c = i
            
            if (c != None):
                y_val[c] = false
                y_val[c+1] = true
                
    def rotr():
        
        for i in range(4):
            if (d_val[i] == true):
                if (i == 3):
                    d_val[i] = false
                    d_val[0] = true
                else:
                    d_val[i] = false
                    d_val[i+1] = true
                    
    def rotl():
        
        for i in range(4):
            if (d_val[i] == true):
                d_val[i] = false
                d_val[i-1] = true
            
#makes instances
king = King()
p1 = Piece()
p2 = Piece()
p3 = Piece()
p4 = Piece()
l = Laser()

def piece_theory():

    all_pieces = [p1, p2, p3, p4]
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
        
    return E
                                             
      
def laser_constraints():

    # Laser cannot be in more than one x or y value at the same time.
    E.add_constraint(l.x_val[0] | l.x_val[1] | l.x_val[2] | l.x_val[3] | l.x_val[4])
    E.add_constraint(l.y_val[0] | l.y_val[1] | l.y_val[2] | l.y_val[3])
    # Laser cannot have more than one direction.
    E.add_constraint(l.d_val[0] | l.d_val[1] | l.d_val[2] | l.d_val[3])

    # Laser continues if it does not make contact with any pieces and does not go out of bounds.
    for i in range(5):
        for j in range(4):
            (l.x_val[i] =! p1.x_val[i] and l.y_val[j] =! p1.y_val[j] and
             l.x_val[i] =! p2.x_val[i] and l.y_val[j] =! p2.y_val[j] and
             l.x_val[i] =! p3.x_val[i] and l.y_val[j] =! p3.y_val[j] and
             l.x_val[i] =! p4.x_val[i] and l.y_val[j] =! p4.y_val[j]):

        # Check if laser goes out of bounds based on x/y value and direction.
        # d.val 0 = N
        if (l.d_val[0] == true and l.y_val[3] == true):
            E.add_constraint((l.y_val[4]).negate())
        # d.val 1 = E
        elif (l.d_val[1] == true and l.x_val[4] == true):
            E.add_constraint((l.x_val[5]).negate())
        # d.val 2 = S
        elif (l.d_val[2] == true and l.y_val[0] == true):
            E.add_constraint(l.y_val[-1]).negate())
        # d.val 3 = W
        elif (l.d_val[3] == true and l.x_val[0] == true):
            E.add_constraint(l.x_val[-1]).negate())

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

    T = example_theory()
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

