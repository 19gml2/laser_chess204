
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood

# Encoding that will store all of your constraints
E = Encoding()



size_x = 5
size_y = 4
board = [size_x][size_y]

#sits on the last col of the grid, can be initialized along this line
class King():
    y_val = [4]
    def __init__(self, y):
        
        for i in range(size_y):
            self.y_val[i] = False
        
        self.y_val[y] = True;
        
    def inc_y():
        
        for i in range(size_y):
            if (y_val[i] == True) and (i < 4):
                c = i
            
            if (c != None):
                y_val[c] = False
                y_val[c+y] = True
                
     def dec_y():
        
        for i in range(size_y):
            if (y_val[i] == True) and (i < 0):
                c = i
            
            if (c != None):
                y_val[c] = False
                y_val[c+y] = True
            

king = King()
#d for Piece represents the ordinal direction of the mirrored side
#0 = NE
#1 = SE
#2 = SW
#3 = NW


p1 = Piece()
p2 = Piece()
p3 = Piece()
p4 = Piece()
#d means something different for laser vs piece
#0 = N
#1 = E
#2 = S
#3 = W
Class Laser():
    
    def __init__(self, x, y, d):
        
        for i in range(size_y):
            self.x_val[i] = False
            self.y_val[i] = False
            self.d_val[i] = False
        self.x_val[4] = False
        
        self.x_val[x] = True
        self.y_val[y] = True
        self.d_val[d] = True
    
     def inc_x():
        
        for i in range(size_x):
            if (x_val[i] == True) and (i < size_x):
                c = i
            
            if (c != None):
                x_val[c] = False
                x_val[c+1] = True
                
     def dec_x():
        
        for i in range(size_x):
            if (x_val[i] == True) and (i > 0):
                c = i
            
            if (c != None):
                x_val[c] = False
                x_val[c+1] = True 
                
    def inc_y():
        
        for i in range(size_y):
            if (y_val[i] == True) and (i < size_y):
                c = i
            
            if (c != None):
                y_val[c] = False
                y_val[c+1] = True
                
     def dec_y():
        
        for i in range(size_y):
            if (y_val[i] == True) and (i > 0):
                c = i
            
            if (c != None):
                y_val[c] = False
                y_val[c+1] = True
                
    def rotr():
        
        for i in range(4):
            if (d_val[i] == True):
                if (i == 3):
                    d_val[i] = False
                    d_val[0] = True
                else:
                    d_val[i] = False
                    d_val[i+1] = True
                    
    def rotl():
        
        for i in range(4):
            if (d_val[i] == True):
                d_val[i] = False
                d_val[i-1] = True
            
                
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
                            E.add_constraint(~((i.x_val[k]) & (i.y_val[p] & j.y_val[p]))

         
        
    return E
                
l = Laser()
# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.

def ():
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

