import pygame
import sys

import view
import image_model

# Return ImageModel rendered onto pygame.Surface
def render( imageModel ):
    # target surface
    s = pygame.Surface( imageModel.size(), pygame.SRCALPHA | pygame.HWSURFACE, 32 )

    # per-shape surface; required for blitting to target
    # as draw does not support alpha
    ss = pygame.Surface( imageModel.size(), pygame.SRCALPHA | pygame.HWSURFACE, 32 )
    ss.set_colorkey( 0x00000000 )

    for shape in imageModel.shapes():
        # draw shape
        ss.fill( 0x00000000 )
        # print(shape["colour"])
        pygame.draw.polygon( ss, shape["colour"], shape["points"] )

        ss.set_alpha( shape["colour"][3] )

        s.blit( ss, (0, 0) )

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
        self.targetSurface_ = pygame.image.load( "/media/rob/GEOFFREY/photos/2013-08-04 13.41.57.jpg" )
        self.width_  = self.targetSurface_.get_width()
        self.height_ = self.targetSurface_.get_height()

        self.mainView_ = view.View( self.width_, self.height_ )

        # enable alpha-blending
        # uses display format for fast blitting - must precede View creation
        self.targetSurface_ = self.targetSurface_.convert_alpha()

        self.genepoolSize_ = 1

    def run( self ):
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

    def update_model( self ):
            self.models_ = [self.makeRandomModel() for i in range( self.genepoolSize_ )]
            renderedModels  = [render(m) for m in self.models_]

            # (fitness, surface, model)
            evaluatedModels = [(evaluate(self.targetSurface_, rm), rm, m) for rm in renderedModels]

            self.mainView_.draw( renderedModels[0] )


            # evaluatedModels = sorted( evaluatedModels, lambda a,b: cmp(a[0], b[0]) )

            # for m in evaluatedModels:
            #     print(m[0])
            # print("--------------------------------------------------------{}\n".format(i))

            # self.mainView_.draw( self.targetSurface_ )

    def makeRandomModel( self ):
        m = image_model.ImageModel( self.size() )
        m.randomise()
        # colours = [
        #     (255,0,0,255),
        #     (0,255,0,128),
        #     (0,0,255,128),
        # ]
        # for s,c in zip(m.shapes_, colours):
        #     print("colour: {}".format(c))
        #     s["colour"] = c
        return m

    def size( self ):
        return (self.width_, self.height_)