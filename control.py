import pygame
import pygame.gfxdraw
import sys

import view
import image_model

# could try optimising rendering by caching intermediate results:
# where there are repetitions of the same polygon sub-sequence (in rendering order)
# the result of rendering these independently of the rest of the sequence in any
# given rendering could then be applied to the result of head, and followed
# by the tail.
# this may not work though: I don't think alpha-blending is associative. It may
# still be possible to determine a way to refactor the mathematical expression to
# allow sub-sequences to be prerendered.

# Return ImageModel rendered onto pygame.Surface
def render( imageModel ):
    # target surface
    s = pygame.Surface( imageModel.size(), pygame.SRCALPHA | pygame.HWSURFACE, 32 )

    s.fill( 0x00000000 )
    s.fill( 0xFFFFFFFF )

    for shape in imageModel.shapes():
        # draw shape
        # use gfxdraw because draw.polygon doesn't support alpha-blending and the
        # alternative is dog-slow.
        pygame.gfxdraw.aapolygon(     s, shape["points"], shape["colour"]);
        pygame.gfxdraw.filled_polygon(s, shape["points"], shape["colour"]);

    return s

# Return value in [0, 1] representing fitness of candidate compared to target
# Both candidate & target must be pygame.Surface renderings.
def evaluate( target, candidate ):
    targetPix    = pygame.PixelArray( target )
    candidatePix = pygame.PixelArray( candidate )

    diffPix = targetPix.compare( candidatePix )
    diffs   = 0
    for px in diffPix:
        for px_ in px:
            diffs = diffs + px_ / float(0xFFFFFFFF)

    # normalize to [0, 1]
    return diffs / (target.get_width() * target.get_height())

def compareEvalutedModels( a, b ):
    return cmp( a[0], b[0] )

class Control():
    def __init__( self ):
        self.genepoolSize_ = 10

    def run( self, targetImagePath ):
        # enable alpha-blending
        # uses display format for fast blitting
        self.targetSurface_ = pygame.image.load( targetImagePath )
        self.targetSurface_ = self.targetSurface_.convert( 32, pygame.SRCALPHA | pygame.HWSURFACE )
        self.width_  = self.targetSurface_.get_width()
        self.height_ = self.targetSurface_.get_height()

        self.mainView_ = view.View( self.width_, self.height_ )

        self.update_model()
        # for i in range(0, 2):
        while True:
            for event in pygame.event.get():
                self._on_event( event )

    def _on_event( self, event ):
        """Handle a pygame event"""
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            self._on_keydown( event )

    def _on_keydown( self, event ):
        """Handle a pygame keydown event"""
        if event.key == pygame.K_RETURN:
            self.update_model()

    def draw_model( self, m ):
        self.mainView_.draw( m )

    def update_model( self ):
            self.models_ = [self.makeRandomModel() for i in range( self.genepoolSize_ )]
            renderedModels  = [render(m) for m in self.models_]

            # (fitness, surface, model)
            evaluatedModels = [(evaluate(self.targetSurface_, rm), rm, m) for rm in renderedModels]


            evaluatedModels = sorted( evaluatedModels, lambda a,b: cmp(a[0], b[0]) )

            bestCandidate = evaluatedModels[0]
            print("--------------------------------------------------------")
            print("Best fitness: {:3.8f}".format( 100 * bestCandidate[0] ))
            print("Polygons:     {:4d}"  .format( len( bestCandidate[2].shapes() )))

            self.draw_model( bestCandidate[1] )

    def makeRandomModel( self ):
        m = image_model.ImageModel( self.size() )
        m.randomise()

        return m

    def size( self ):
        return (self.width_, self.height_)