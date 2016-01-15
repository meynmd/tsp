'''
tsp.py

An approximation algorithm for the TSP optimization problem. Based on a project
by Elliot Bates, Matthew Meyn and Marco Zamora. Tested with python 3.4.3. 
Makes use of Andrew Harrington's modification of John Zelle's graphics library.

tsp.py is a python 3 script that should be given one argument: the name of the
problem file, which should be located in the directory problems/ and should 
contain a list in the form 
'''

import vertex
import graph
from graphics import *

# open the input and output files
inFilename = sys.argv[1]
outFilename = inFilename + '.tour'
inFile = open( 'problems/' + inFilename, 'r' )
outFile = open( 'problems/' + outFilename, 'w' )

print('Input File: ' + inFilename)
print('Output File: ' + outFilename)

# read the problem from input file
count = 0
vertices = []
for line in inFile:
    line = line.strip()
    line = line.split()
    inputVals = [v for v in line]
    if len( inputVals ) == 3:
        vertices.append( vertex.Vertex( 
                                       int( inputVals[0]), 
                                       float( inputVals[1] ), 
                                       float( inputVals[2] ) 
                                       ) )
        count += 1
    else:
        print( 'Error: Line ' + count + ' does not have 3 values.' )
        exit( 1 )

# create an initial tour
g = graph.Graph( vertices )
g.makeTour( 0 )

win1 = GraphWin( 'Unoptimized Graph', 960, 960 )
g.display( win1 )

# optimize the tour
print('Optimizing...')
nSteps = g.optimize()

# write tour to file
for v in g.visit():
    outFile.write( str( v.id ) + '\n')

win2 = GraphWin( 'Optimized Graph', 960, 960 )
g.display( win2 )

print( 'Performed ' + str(nSteps) + ' optimizations.')
print( 'Total weight: ' + str( g.totalWeight() ) ) 

win2.getMouse()
win1.close()
win2.close()
