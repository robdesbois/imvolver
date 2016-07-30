import pygame


class View():
    def __init__( self, width, height ):
        self.screen   = pygame.display.set_mode( (width, height) )

    def draw( self, surface ):
        self.screen.fill( 0x000000 )
        self.screen.blit( surface, (0, 0) )

        pygame.display.flip()

