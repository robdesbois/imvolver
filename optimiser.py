import pygame
import random
import bisect


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

        evaluatedModels   = [(evaluate(targetSurface, rm[1]), rm[1], rm[0]) for rm in renderedModels]
        descendingFitness = lambda a,b: cmp(b[0], a[0])
        evaluatedModels   = sorted( evaluatedModels, descendingFitness )

        bestCandidate = evaluatedModels[0]

        print("--------------------------------------------------------")
        print("Best fitness: {:3.8f}".format( 100 * bestCandidate[0] ))
        print("Polygons:     {:4d}"  .format( len( bestCandidate[2].shapes() )))

        models = self.select( evaluatedModels )
        return models

    def select( self, evaluatedModels ):
        # roulette wheel selection
        # generate cumulative distribution function of fitnesses
        # typically uses normalised fitness, but scaling adds no benefit here
        fitnessCDF = []
        cumFit     = 0
        for m in evaluatedModels:
            cumFit = cumFit + m[0]
            fitnessCDF.append( cumFit )

        models = [ elite[2] for elite in evaluatedModels[0:self.numElites_] ]
        for _ in range( len( models ), len( evaluatedModels )):
            ran   = random.uniform( 0, cumFit )
            pos   = bisect.bisect_left( fitnessCDF, cumFit )
            model = evaluatedModels[ pos ]
            models.append( model[2] )
        return models

def optimise( targetSurface, renderedModels ):
    o = Optimiser()
    return o.run( targetSurface, renderedModels )
