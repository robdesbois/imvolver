import numpy as np
import pygame
import unittest

import optimiser

def square( size, colour ):
    s = pygame.Surface( (size,size), pygame.HWSURFACE, 32 )
    s.fill( colour )
    return s

def drop( v, aList ):
    aList.remove( v )
    return aList

class TestOptimiser( unittest.TestCase ):
    def test_evaluate_single_colour_against_itself_gives_1( self ):
        colours = [
            pygame.Color(0xFF, 0xFF, 0xFF, 0xFF),
            pygame.Color(0x00, 0x00, 0x00, 0xFF),
            pygame.Color(0xFF, 0x00, 0x00, 0xFF),
            pygame.Color(0x00, 0xFF, 0x00, 0xFF),
            pygame.Color(0x00, 0x00, 0xFF, 0xFF),
            pygame.Color(0x12, 0x34, 0x56, 0xFF)
         ]

        for c in colours:
            p = square( 2, c )
            self.assertEqual( 1.0, optimiser.evaluate( p, p ))

    def test_evaluate_black_against_white_gives_1( self ):
        black = square( 2, pygame.Color( 0x00, 0x00, 0x00, 0xFF ))
        white = square( 2, pygame.Color( 0xFF, 0xFF, 0xFF, 0xFF ))

        self.assertEqual( 0.0, optimiser.evaluate( black, white ))
        self.assertEqual( 0.0, optimiser.evaluate( white, black ))

    # 255's prime factorisation is 3.5.17
    # to test fitness values other than 0 and 1, need to use values that will
    # yield a total difference averaging to an integer, otherwise we get into
    # unpleasant territory with the floating point comparisons
    def test_integer_fractions_of_255_against_black_or_white_gives_half( self ):
        black   = square( 2, pygame.Color( 0x00, 0x00, 0x00, 0xFF ))
        white   = square( 2, pygame.Color( 0xFF, 0xFF, 0xFF, 0xFF ))
        factors = [3, 5, 17]

        for factor in [3]:
            otherFactors = drop( factor, factors )
            divisor      = reduce( lambda x,y: x*y, otherFactors )
            v = 255 / divisor

            colour     = square( 2, pygame.Color( v, v, v, 0xFF ))
            expFitness = 1.0 - (1.0 / divisor)
            self.assertAlmostEqual(     expFitness, optimiser.evaluate( black, colour ))
            self.assertAlmostEqual( 1 - expFitness, optimiser.evaluate( white, colour ))


if __name__ == "__main__":
    unittest.main()