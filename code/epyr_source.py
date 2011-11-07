"""

Copyright (C) 2011 Predictive Patterns Software Inc
Author: Tom Radcliffe
Created: 2011-11-05
License: GPL2

Source module for EPyR

"""

import math
import random

class EPyRSource(object):

    def __init__(self, lstArgs):
        self.lstArgs = lstArgs

    def GenerateUncorrelatedPair(self, fTime):
        
        fPolarizationAngle1 = random.random()*math.pi*2
        fPolarizationAngle2 = random.random()*math.pi*2
        return (str(fTime)+":"+str(fPolarizationAngle1), str(fTime)+":"+str(fPolarizationAngle2))
        
    def GenerateCorrelatedPair(self, fTime):
        
        fPolarizationAngle = random.random()*math.pi*2
        return (str(fTime)+":"+str(fPolarizationAngle), str(fTime)+":"+str(fPolarizationAngle))
                
if __name__ == "__main__":
    # sanity test
    pSource = EPyRSource([])
    print pSource.GeneratePair(0)
