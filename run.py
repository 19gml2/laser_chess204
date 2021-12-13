
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood
from nnf import true, false
from tabulate import tabulate
import random

# Encoding that will store all of your constraints
E = Encoding()

#board constraints
size_x = 5
size_y = 4


#represents a single piece on the board and stores it's coordinates and which way it faces
@proposition(E)
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
        for i in range(4):
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
@proposition(E)
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

@proposition(E)
class Laser:
    
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
        self.x_val.append(false)
        
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
            if (self.d_val[i] == true):
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
        for i in range(4):
            if (self.y_val[i] == true):
                y_current = i
        return y_current
    
    def get_d(self):
        d_current = -1
        for i in range(4):
            if (self.d_val[i] == true):
                d_current = i
        return d_current
        
    def reset(self):
        
        for i in range(size_y):
            self.x_val.append(false)
            self.y_val.append(false)
            self.d_val.append(false)
        self.x_val.append(false)
        
        self.x_val[0] = true
        self.y_val[0] = true
        self.d_val[1] = true
            

#runs the laser until out of bounds, hits a piece or hits the king
def run_laser(p1, p2, p3, p4, king, l):
    
    all_pieces = [p1, p2, p3, p4, king, l]
    
    while(true):
        
        #curr direction of l
        direction = l.get_d()
        
        #makes moveset for l
        goin_x = 0
        goin_y = 0
        if (direction == 0):
            goin_x = 0
            goin_y = 1
        if (direction == 1):
            goin_x = 1
            goin_y = 0
        if (direction == 2):
            goin_x = 0
            goin_y = -1
        if (direction == 3):
            goin_x = -1
            goin_y = 0
           
        #checks if move is valid (if there's nothing there then true and it moves the laser, else changes directions or ends)
        can_move = check_valid(l, goin_x, goin_y, p1, p2, p3, p4, king, l)
        if (can_move == true):
            if (direction == 0):
                l.inc_y()
            if (direction == 1):
                l.inc_x()
            if (direction == 2):
                l.dec_y()
            if (direction == 3):
                l.dec_x()
                
        else:
            x_desired = l.get_x() + goin_x
            y_desired = l.get_y()  + goin_y
            
            #hits king
            if (x_desired == 4 and y_desired == 3):
                l.reset()
                print("fuck yea dead king")
                return true
            #never obtainable
            piece_direction = 5
            
            #finds piece at spot
            for piece in all_pieces:
                if (piece.get_x() == x_desired and piece.get_y() == y_desired):
                    piece_direction = piece.get_d()
                    break
            # if no piece is there it ends the path
            if (piece_direction == 5):
                l.reset()
                return false
            
            rotate = 0
            #hits a non-mirrored side
            if ((piece_direction) % 4) != ((direction + 1) % 4) and ((piece_direction)) % 4 != ((direction +2) % 4):
                l.reset()
                return false
                
            #moves into new spot
            if (direction == 0):
                l.inc_y()
            if (direction == 1):
                l.inc_x()
            if (direction == 2):
                l.dec_y()
            if (direction == 3):
                l.dec_x()
            
            #hits a mirror, changes direction accordingly
            if (((piece_direction) % 4) == ((direction + 1) % 4)):
                l.rotr()
            else:
                l.rotl()
    
            
def check_valid(obj, x_change, y_change, p1, p2, p3, p4, king, l):
    #tells you whether the inputted object (either a piece or a laser) can move to the desired position.
    #x_change and y_change can both have values -1, 0 or 1 (i.e. (0, -1) represents moving one position downwards)
    all_pieces = [p1, p2, p3, p4]
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
    
def piece_move(p1, p2, p3, p4, king, l):
    print("here")
    sol_count = 0
    
    all_pieces = [p1, p2, p3, p4]
    
    move1 = [0, 1]
    move2 = [1, 1]
    move3 = [1, 0]
    move4 = [1, -1]
    move5 = [0, -1]
    move6 = [-1, -1]
    move7 = [-1, 0]
    move8 = [-1, 1]
    move9 = [0, 0]
    moves_set = [move1, move2, move3, move4, move5, move6, move7, move8, move9]
    
    solved = run_laser(p1, p2, p3, p4, king, l)
    if (solved == true):
        print("this works")
        
    for p in all_pieces:
        for move in moves_set:
        
            if (move[0] == 1):
                p.inc_x()
            if (move[0] == -1):
                p.dec_x
            if (move[1] == 1):
                p.inc_y()
            if (move[1] == -1):
                p.dec_y()
            solved = run_laser(p1, p2, p3, p4, king, l)
            if (solved == true):
                sol_count = sol_count + 1
                
            if (move[0] == 1):
                p.dec_x()
            if (move[0] == -1):
                p.inc_x
            if (move[1] == 1):
                p.dec_y()
            if (move[1] == -1):
                p.inc_y()
                
        p.rotr()
        solved = run_laser(p1, p2, p3, p4, king, l)
        if (solved == true):
            sol_count = sol_count + 1
            
        p.rotl()
        p.rotl()
        solved = run_laser(p1, p2, p3, p4, king, l)
        if (solved == true):
            sol_count = sol_count + 1
        
        p.rotr()
    
    print(sol_count, "\n")
    
def piece_constraints(p1, p2, p3, p4, king, l):

    all_pieces = [p1, p2, p3, p4]

    for i in all_pieces:
        ixvals = [i.x_val[0], i.x_val[1], i.x_val[2], i.x_val[3], i.x_val[4]]
        iyvals = [i.y_val[0], i.y_val[1], i.y_val[2], i.y_val[3]]
        idvals = [i.d_val[0], i.d_val[1], i.d_val[2], i.d_val[3]]
        kingpos = [i.x_val[4], i.y_val[3]]
        
        constraint.add_exactly_one(E, *(ixvals))
        constraint.add_exactly_one(E, *(iyvals))
        constraint.add_exactly_one(E, *(idvals))
        constraint.add_at_most_one(E, *(kingpos))
        ixval0 = ixvals[0]
        ixval1 = ixvals[1]
        ixval2 = ixvals[2]
        ixval3 = ixvals[3]
        ixval4 = ixvals[4]
        iyval0 = ixvals[0]
        iyval1 = ixvals[1]
        iyval2 = ixvals[2]
        iyval3 = ixvals[3]
        
        x = i.get_x()
        y = i.get_y()
        
        # A piece cannot be out of bounds
        if (x > 4):
            E.add_constraint(i.x_val[x].negate())
        
        if (x < 0):
            E.add_constraint(i.x_val[x].negate())
            
        if (y > 3):
            E.add_constraint(i.y_val[y].negate())
            
        if (y < 0):
            E.add_constraint(i.y_val[y].negate())
                    
        #cannot take up the same spot as another piece
        for j in all_pieces:
            jxvals = [j.x_val[0], j.x_val[1], j.x_val[2], j.x_val[3], j.x_val[4]]
            jyvals = [j.y_val[0], j.y_val[1], j.y_val[2], j.y_val[3]]
            jxval0 = jxvals[0]
            jxval1 = jxvals[1]
            jxval2 = jxvals[2]
            jxval3 = jxvals[3]
            jxval4 = jxvals[4]
            jyval0 = jxvals[0]
            jyval1 = jxvals[1]
            jyval2 = jxvals[2]
            jyval3 = jxvals[3]
            
            
            if (i != j):
                constraint.add_implies_all(E, [ixval0, iyval0], [jxval0.negate(), jyval0.negate()])
                constraint.add_implies_all(E, [ixval0, iyval1], [jxval0.negate(), jyval1.negate()])
                constraint.add_implies_all(E, [ixval0, iyval2], [jxval0.negate(), jyval2.negate()])
                constraint.add_implies_all(E, [ixval0, iyval3], [jxval0.negate(), jyval3.negate()])
                constraint.add_implies_all(E, [ixval1, iyval0], [jxval1.negate(), jyval0.negate()])
                constraint.add_implies_all(E, [ixval1, iyval1], [jxval1.negate(), jyval1.negate()])
                constraint.add_implies_all(E, [ixval1, iyval2], [jxval1.negate(), jyval2.negate()])
                constraint.add_implies_all(E, [ixval1, iyval3], [jxval1.negate(), jyval3.negate()])
                constraint.add_implies_all(E, [ixval2, iyval0], [jxval2.negate(), jyval0.negate()])
                constraint.add_implies_all(E, [ixval2, iyval1], [jxval2.negate(), jyval1.negate()])
                constraint.add_implies_all(E, [ixval2, iyval2], [jxval2.negate(), jyval2.negate()])
                constraint.add_implies_all(E, [ixval2, iyval3], [jxval2.negate(), jyval3.negate()])
                constraint.add_implies_all(E, [ixval3, iyval0], [jxval3.negate(), jyval0.negate()])
                constraint.add_implies_all(E, [ixval3, iyval1], [jxval3.negate(), jyval1.negate()])
                constraint.add_implies_all(E, [ixval3, iyval2], [jxval3.negate(), jyval2.negate()])
                constraint.add_implies_all(E, [ixval3, iyval3], [jxval3.negate(), jyval3.negate()])
                constraint.add_implies_all(E, [ixval4, iyval0], [jxval4.negate(), jyval0.negate()])
                constraint.add_implies_all(E, [ixval4, iyval1], [jxval4.negate(), jyval1.negate()])
                constraint.add_implies_all(E, [ixval4, iyval2], [jxval4.negate(), jyval2.negate()])
                constraint.add_implies_all(E, [ixval4, iyval3], [jxval4.negate(), jyval3.negate()])
                

                                             
      
def laser_constraints(p1, p2, p3, p4, king, l):
 
    all_pieces = [p1, p2, p3, p4]
    # Laser cannot be in more than one x or y value at the same time.
    xvals = [l.x_val[0], l.x_val[1], l.x_val[2], l.x_val[3], l.x_val[4]]
    yvals = [l.y_val[0], l.y_val[1], l.y_val[2], l.y_val[3]]
    dvals = [l.d_val[0], l.d_val[1], l.d_val[2], l.d_val[3]]
    constraint.add_exactly_one(E, *(xvals))
    constraint.add_exactly_one(E, *(yvals))
    
    # Laser cannot have more than one direction.
    constraint.add_exactly_one(E, *(dvals))

    # Laser cannot travel out of bounds
    x = l.get_x()
    y = l.get_y()
    
    if (x > 4):
        E.add_constraint(l.x_val[x].negate())
        
    if (x < 0):
        E.add_constraint(l.x_val[x].negate())
            
    if (y > 3):
        E.add_constraint(l.y_val[y].negate())
            
    if (y < 0):
        E.add_constraint(l.y_val[y].negate())
    
    # Laser only continues if it does not make contact with any pieces and does not go out of bounds.
    laser_check = true
    for p in all_pieces:
        for i in range(5):
            for j in range(4):
                if (l.x_val[i] != p.x_val[i] and l.y_val[j] != p.y_val[j]):
                    laser_check = true
                else:
                    laser_check = false


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

def example_theory():
    p1 = Piece(1, 0, 3)
    p2 = Piece(4, 0, 3)
    p3 = Piece(2, 2, 1)
    p4 = Piece(0, 2, 0)
    king = King()
    l = Laser(0, 0, 1)
    
    piece_constraints(p1, p2, p3, p4, king, l)
    laser_constraints(p1, p2, p3, p4, king, l)
    

    return E


# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
                                             

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
    for v,vn in zip([], 'abcxyz'):
        # Ensure that you only send these functions NNF formulas
        # Literals are compiled to NNF here
        print(" %s: %.2f" % (vn, likelihood(T, v)))
    print()
