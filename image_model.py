import random

# mutations:
#   reorder shapes
#   adjust shape orientation, colour, dimensions
#   add/remove shapes

class ImageModel():
    # size is (width, height) in pixels
    def __init__( self, size ):
        self.size_   = size
        self.shapes_ = []

    def size( self ):
        return self.size_

    # shape:
    #   - points: array of (x,y)
    #   - colour: (r,g,b,a)
    def shapes( self ):
        return self.shapes_

    def set_shapes( self, shapes ):
        self.shapes_ = shapes

    def randomise( self ):
        self.shapes_ = []
        ns = self.num_shapes()
        print(ns)
        for i in range( ns ):
            s = self.random_shape()
            # print(s)
            # print(s["colour"][3])
            self.shapes_.append( s )

    def random_shape( self ):
        ran255 = lambda: random.randint(0, 255)

        alpha = min( 255, (ran255()))
        return {
            "points": [self.random_point() for i in range(3)],
            "colour": ( ran255(), ran255(), ran255(), alpha )
        }


    def random_point( self ):
        return (
            random.randint( 0, self.size_[0] - 1 ),
            random.randint( 0, self.size_[1] - 1 ) )

    def num_shapes( self ):
        # best-guess values; could adjust this to/towards population mean,
        # with some randomness, to improve resolution. Evolving the GA
        # simulated annealing may be more appropriate - this is comparable
        # to SA's 'temperature' that decreases randomness in exploration
        # of solution space.
        mean   = 100
        stdDev = 15
        return abs( int( random.gauss( mean, stdDev )))


