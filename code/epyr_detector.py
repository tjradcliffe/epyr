"""

Copyright (C) 2011 Predictive Patterns Software Inc
Author: Tom Radcliffe
Created: 2011-11-05
License: GPL2

Detector module for EPyR

"""

import math
import random
import socket
import sys

class EPyRDetector(object):
    
    def __init__(self, strDetectorName, lstArgs):
        self.strDetectorName = strDetectorName 
        self.lstArgs = lstArgs

    def GetName(self):
        return self.strDetectorName
        
    def ProcessPhoton(self, fDetectorAngle, strPhoton):
        strResult = "R"

        lstPhoton = strPhoton.split(":")
        nCount = int(lstPhoton[0])
        fTime = float(lstPhoton[1])
        fPolarizationAngle = float(lstPhoton[2])
        
        fProbability = math.cos(fPolarizationAngle-fDetectorAngle)**2
        
        if fProbability < random.random():
            strResult = "L"
            
        return (nCount, fTime, fDetectorAngle, strResult)
        
if __name__ == "__main__":
    #sanity test
    pDetector = EPyRDetector("Test", [])
    print pDetector.ProcessPhoton(0.0, "5:0.1234:1.2345")
    