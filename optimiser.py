import pygame
import random
import bisect

import image_model

class RouletteSelectionOperator():
    """roulette wheel selection operator"""

    def __init__( self, evaluatedModels ):
        self.evaluatedModels_ = evaluatedModels

        # generate cumulative distribution function of fitnesses
        # typically uses normalised fitness, but scaling adds no benefit here
        self.fitnessCDF_ = []
        self.cumFit_     = 0
        for m in self.evaluatedModels_:
            self.cumFit_ = self.cumFit_ + m[0]
            self.fitnessCDF_.append( self.cumFit_ )

    def select( self ):
        ran   = random.uniform( 0, self.cumFit_ )
        pos   = bisect.bisect_left( self.fitnessCDF_, self.cumFit_ )
        model = self.evaluatedModels_[ pos ]
        return model[2]


# Return value in [0, 1] representing fitness of candidate compared to target
# Both candidate & target must be pygame.Surface renderings.
# TODO: make this work. Fitnesses are all coming out above 0.99
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

class Optimiser():
    def __init__( self ):
        self.numElites_ = 1

    def run( self, targetSurface, renderedModels ):
        """
        targetSurface:  the optimiser objective. TODO: get this out of the GA! It's part of the evaluator
        renderedModels: (model, surface)
        """
        evaluatedModels = self.evaluate_models( targetSurface, renderedModels )

        bestCandidate = evaluatedModels[0]
        print("--------------------------------------------------------")
        print("Best fitness: {:3.8f}".format( 100 * bestCandidate[0] ))
        print("Polygons:     {:4d}"  .format( len( bestCandidate[2].shapes() )))

        models = self.select( evaluatedModels )
        return models

    def evaluate_models( self, targetSurface, renderedModels ):
        evaluatedModels   = [(evaluate(targetSurface, rm[1]), rm[1], rm[0]) for rm in renderedModels]
        descendingFitness = lambda a,b: cmp(b[0], a[0])
        evaluatedModels   = sorted( evaluatedModels, descendingFitness )
        return evaluatedModels

    def select( self, evaluatedModels ):
        selector = RouletteSelectionOperator( evaluatedModels )

        models = [ elite[2] for elite in evaluatedModels[0:self.numElites_] ]
        while len( models ) < len( evaluatedModels ):
            parents = [selector.select() for _ in range(0,2)]
            models.append( self.crossover( parents[0], parents[1] ))
        return models

    def crossover( self, a, b ):
        pos  = random.randint( 0, len( a.shapes() ) - 1)
        head = a.shapes()[:pos]
        tail = b.shapes()[pos:]

        offspring = image_model.ImageModel( a.size() )
        offspring.set_shapes( head + tail )
        return offspring

def optimise( targetSurface, renderedModels ):
    o = Optimiser()
    return o.run( targetSurface, renderedModels )
