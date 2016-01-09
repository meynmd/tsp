# class to represent a vertex in 2D space
# inplements > and < according to numeric order of id
# works with Python 3.4.3

'''
Vertex class
    given ID number, x and y coordinate, represents a vertex
    fields for previous, next vertices in directed graph
    vertQueue lists distances to every other vertex in tuple
        (distance, other-vertex)
'''
class Vertex:
    def __init__(self, ID, x, y):
        self.id = ID
        self.x = x
        self.y = y
        self.prev = None
        self.next = None
        self.vertQueue = []
        
    def __lt__(self, other):
        return self.id < other.id
    
    def __gt__(self, other):
        return self.id > other.id
        
    def toString(self):
        return 'Vertex ID: ' + str(self.id) + '\t\t' + \
            '(' + str(self.x) + ', ' + str(self.y) + ')' + '\t\t' + \
            'prev: ' + str(self.prev[1].id) + '\t\tnext: ' + str(self.next[1].id)

