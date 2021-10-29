
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood

# Encoding that will store all of your constraints
E = Encoding()



size_x = 5
size_y = 4
board = [size_x][size_y]

def init_King(pos_y):
    grid = []
    for y in range(size_y):
        grid.append("-")
    grid[pos_y] = True
    return grid

#d for Piece represents the ordinal direction of the mirrored side
#0 = NE
#1 = SE
#2 = SW
#3 = NW
def init_Piece(pos_x, pos_y, d):
    col = []
    for x in range(size_x):
        row = []
        for y in range(size_y):
            dirc = []
            for i in range(4):
                dirc.append("-")
            row.append(dirc)
        col.append(row)
    col[pos_x][pos_y][d] = True
    return col

#d means something different for laser vs piece
#0 = N
#1 = E
#2 = S
#3 = W
def init_Laser(pos_x, pos_y, d):
    col = []
    for x in range(size_x):
        row = []
        for y in range(size_y):
            dirc = []
            for i in range(4):
                dirc.append("-")
            row.append(dirc)
        col.append(row)
    col[pos_x][pos_y][d] = True
    return col
            
        


p1 = init_Piece()
p2 = init_Piece()
p3 = init_Piece()
p4 = init_Piece()
k = init_King()
l = init_Laser()
l[0][0][1] = True



b = BasicPropositions("b")   
c = BasicPropositions("c")
d = BasicPropositions("d")
e = BasicPropositions("e")
# At least one of these will be true
x = FancyPropositions("x")
y = FancyPropositions("y")
z = FancyPropositions("z")



# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def example_theory():
    # Add custom constraints by creating formulas with the variables you created. 
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

