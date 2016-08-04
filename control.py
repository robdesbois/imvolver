import bisect
import pygame
import pygame.gfxdraw
import random
import sys

import optimiser
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

        self.models_ = [self.makeRandomModel() for i in range( self.genepoolSize_ )]
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
        renderedModels  = [(m, render(m)) for m in self.models_]

        self.evolve( renderedModels )
        # TODO: render doesn't belong here; rendering should be done by something
        #       that avoids re-rendering, perhaps a wrapper around the model?
        #       should be the same object as a population, since models have to be
        #       rendered for fitness calculation there anyway
        self.draw_model( render( self.models_[0] ))


    def evolve( self, renderedModels ):
        """renderedModels: [(fitness, surface, model)]"""

        self.models_ = optimiser.optimise( self.targetSurface_, renderedModels )

        print( self.models_ )


    def makeRandomModel( self ):
        m = image_model.ImageModel( self.size() )
        m.randomise()

        return m

    def size( self ):
        return (self.width_, self.height_)