''' 
tsp nearest-neighbor plus 2-opt implementation

An approximation algorithm for the TSP optimization problem. Based on a project
by Elliot Bates, Matthew Meyn and Marco Zamora. Tested with python 3.4.3. 
Makes use of Andrew Harrington's modification of John Zelle's graphics library.

Graph class given vertex list can construct an approximate tsp tour   
'''

import math
import vertex
import heapq
from graphics import *

padding = 40  # padding for graph window

def dist( x1, y1, x2, y2 ):
    return math.sqrt( ( y1 - y2 ) ** 2 + ( x1 - x2 ) ** 2 )

'''
Graph class
    for making a graph with Hamiltonian tour
    
    instantiate by passing a list of Vertex objects.
    
    makeTour(startVert): to make an initial tour
    visit( [n], [start], [end] ): to get an iterator following the tour
    display( window ): to display the graph in a graphics window
    optimize(): to try to minimize total edge weight
    totalWeight(): to find current total weight of tour
'''
class Graph:
    def __init__( self, vertList ):
        self.vertices = []
        for v in vertList:
            self.vertices.append( v )
        self.numVertices = len( self.vertices )
        
        # for displaying purposes
        self.xMin = self.vertices[0].x
        self.xMax = self.vertices[0].x
        self.yMin = self.vertices[0].y
        self.yMax = self.vertices[0].y
        # self.edgeList = []
        self.makeDistQueue()
    
    '''
    makeDistQueue  
        for each vertex in graph, build priority queue of every other vertex
    
        Each element in the queue is a tuple consisting of the distance to that
        vertex and a reference to the vertex itself:
        (distanceToV, v)
    ''' 
    def makeDistQueue( self ):
        for vertex in self.vertices:
            # update minimum coordinates
            if self.xMin > vertex.x:
                self.xMin = vertex.x
            if self.yMin > vertex.y:
                self.yMin = vertex.y
            if self.xMax < vertex.x:
                self.xMax = vertex.x
            if self.yMax < vertex.y:
                self.yMax = vertex.y
            # record the distance to every other vertex        
            for otherVertex in self.vertices:
                if vertex.id == otherVertex.id:
                    continue
                else:
                    distance = dist( vertex.x, vertex.y,
                                     otherVertex.x, otherVertex.y )                    
                    heapq.heappush( 
                                   vertex.vertQueue, ( distance, otherVertex ) 
                                  )
                    
    '''
    makeTour
        a greedy algorithm to constuct an initial tour. Populates the prev and
        next field in each vertex. Also populates self.edgeList.
    '''
    def makeTour( self, startVert ):
        count = 1
        v = self.vertices[startVert]
        while v.next == None and count < self.numVertices:
            # connect to the closest unconnected vertex
            for target in sorted( v.vertQueue, key = self.compareFirst ):
                t = target[1]
                tDist = target[0]
                if t.prev == None and t.next == None:
                    v.next = ( tDist, t )
                    t.prev = ( tDist, v )
                    # heapq.heappush( self.edgeList, ( tDist, v, t ) )
                    # self.edgeList.append( ( tDist, v, t ) )
                    count += 1                   
#                    print(str(v.id) + ' -> ' + str(t.id))
                    v = t
                    break
        vtDist = dist( 
                      v.x,
                      v.y,
                      self.vertices[startVert].x,
                      self.vertices[startVert].y 
                      )
        v.next = ( vtDist, self.vertices[startVert] )
        self.vertices[startVert].prev = ( vtDist, v )
        # heapq.heappush( self.edgeList, ( vtDist, v, v.next[1] ) )
        # self.edgeList.append( ( vtDist, v, v.next[1] ) )
        # return True
    
    '''
    visit   
        generates an iterator pointing to the vertex at index start and each 
        vertex that follows in the tour up to the vertex at index end
        
        needs some fixing because actually now it just visits every vertex 
    '''
    def visit( self, n = None, start = 0, end = 0 ):
        if n == None:
            n = len( self.vertices ) + 1
        
        startV = None
        endV = None
        for vert in self.vertices:  
            if vert.id == start:
                startV = vert
            if vert.id == end:
                endV = vert 
        v = startV
        count = 0
        while count < n:  # or v != endV.next[1]:
            yield v
            count += 1
            v = v.next[1]

    '''
    display
        draws the graph in window
    '''        
    def display( self, window ):
        wWidth = window.width - padding
        wHeight = window.height - padding
        gWidth = self.xMax - self.xMin
        gHeight = self.yMax - self.yMin
        p = None
        q = None
        
        for v in self.visit():  
            gX = v.x - self.xMin
            gY = v.y - self.yMin
            wX = gX * wWidth / gWidth + padding / 2
            wY = gY * wHeight / gHeight + padding / 2
            p = q 
            q = Point( wX, wY )
            dot = Circle( q, 3 )
            dot.setFill( 'green' )
            dot.draw( window )
            num = Text( Point( wX, wY - 12 ), str( v.id ) )
            num.setSize( 10 )
            num.draw( window )
                     
            if p:
                e = Line( p, q )
                e.setOutline( 'black' )
                e.setArrow( 'last' )
                e.draw( window )
                prevDist = Text( 
                                Point( ( p.x + q.x ) / 2, ( p.y + q.y ) / 2 ),
                                '{0:.1f}'.format( v.prev[0] ) )
                prevDist.setSize( 8 )
                prevDist.draw( window )

    '''
    buildEdgeList
        build the graph's edge list
    '''
    def buildEdgeList( self ):
        el = []
        for vert in self.vertices:
            heapq.heappush( el, ( vert.next[0], vert, vert.next[1] ) )
        return el
    
    def compareFirst( self, t ):
        return t[0]

    '''
    optimize
        makes swaps to optimize the graph
    '''            
    def optimize( self ):
        # build the graph's edge list
        edgeQueue = self.buildEdgeList()
        optCount = 0
        oldOptCount = -1  # so the while loop will begin
        
        # the optimization loop. Keep going until there are no more available    
        while optCount != oldOptCount:
            oldOptCount = optCount
            u1 = None
            u2 = None
            v1 = None
            v2 = None
            s2Candidate = None
            t2Candidate = None
            s2t2Dist = None
            s2t2Dist = None
            s1t1Dist = None
            
            # check the 100 heaviest edges in order to see if we can transpose
            for heaviestEdge in heapq.nlargest( 
                                               100, 
                                               edgeQueue, 
                                               key = self.compareFirst ):
                # find heaviest edge (s1, t1)
                bestSwap = 0.00
                s1 = heaviestEdge[1]
                t1 = heaviestEdge[2]                

                # where else could we connect s1?
                for vert in sorted( s1.vertQueue ):
                    # ignore if it's already connected to s1 or t1
                    if vert[1].prev[1] == s1 or vert[1].next[1] == s1 \
                            or vert[1] == s1 or vert[1].prev[1] == t1 \
                            or vert[1].next[1] == t1 or vert[1] == t1:
                        continue
                    # let's consider it
                    t2Candidate = vert[1]    
                    s2Candidate = t2Candidate.prev[1]
                    # new edge weights
                    s1s2Dist = dist( s1.x, s1.y, s2Candidate.x, s2Candidate.y )
                    t2t1Dist = dist( t2Candidate.x, t2Candidate.y, t1.x, t1.y )            
                    # old edge weights
                    s2t2Dist = t2Candidate.prev[0]
                    s1t1Dist = heaviestEdge[0]
                    # check if a swap will result in lower total weight
                    improvement = s1t1Dist + s2t2Dist - ( s1s2Dist + t2t1Dist )
                    if improvement < 0.01:
                        continue
                    else:
                        if improvement > bestSwap:
                            bestSwap = improvement
                            u1 = t1
                            u2 = s1
                            v1 = t2Candidate
                            v2 = s2Candidate
                            u2v2Dist = s1s2Dist
                            u1v1Dist = t2t1Dist
                
                # if there's a good transposition, perform it
                if bestSwap > 0.01:
                    # connect u1 -> v1
                    v1.prev = ( u1v1Dist, u1 )                    
                    tmp = u1.next                    
                    u1.next = ( u1v1Dist, v1 )
                    u1.prev = tmp
                    
                    # connect  u2 -> v2                   
                    tmp = v2.prev
                    v2.prev = ( u2v2Dist, u2 )                    
                    v2.next = tmp
                    u2.next = ( u2v2Dist, v2 )
                    
                    # reverse all edge directions from u1 to v1
                    current = v2.next[1]
                    while current != u1:
                        tmp = current.prev
                        current.prev = current.next
                        current.next = tmp
                        current = current.next[1]
                    
                    # rebuild the edge list and start the process over
                    edgeQueue = self.buildEdgeList()
                    optCount += 1
                    break
        
        return optCount
    
    '''
    totalWeight
        find the total weight of edges in the graph
    '''
    def totalWeight( self ):
        total = 0.0
        for v in self.visit( len( self.vertices ) ):
            total += v.next[0]                    
        return total
