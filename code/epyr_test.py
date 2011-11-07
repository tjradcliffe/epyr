# local imports
import epyr_detector
import epyr_source

import math
import random

class TestSource(epyr_source.EPyRSource):
    
    def __init__(self, lstArgs):
        epyr_source.EPyRSource.__init__(self, lstArgs)
        
    def GenerateUncorrelatedPair(self, fTime):
        
        fPolarizationAngle1 = random.random()*math.pi*2
        fPolarizationAngle2 = random.random()*math.pi*2
        return (str(fTime)+":"+str(fPolarizationAngle1), str(fTime)+":"+str(fPolarizationAngle2))
        
    def GenerateCorrelatedPair(self, fTime):
        
        fPolarizationAngle = random.random()*math.pi*2
        return (str(fTime)+":"+str(fPolarizationAngle), str(fTime)+":"+str(fPolarizationAngle))
        
class TestDetector(epyr_detector.EPyRDetector):
    
    def __init__(self, strDetectorName, lstArgs):
        epyr_detector.EPyRDetector.__init__(self, strDetectorName, lstArgs)    

    def ProcessPhoton(self, fDetectorAngle, strPhoton):
        
        strResult = "R"

        lstPhoton = strPhoton.split(":")
        fTime = float(lstPhoton[0])
        fPolarizationAngle = float(lstPhoton[1])
        
        fProbability = math.cos(fPolarizationAngle-fDetectorAngle)**2
        
        if fProbability < 0.5:
            strResult = "L"
            
        return (fTime, fDetectorAngle, strResult)

if __name__ == "__main__":
    
    pSource = TestSource([])
    pDetector = TestDetector("T", [])
    
    (strPhoton1, strPhoton2) = pSource.GenerateCorrelatedPair(4.0)
    print pDetector.ProcessPhoton(0.12345, strPhoton1)
    