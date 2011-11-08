# local imports
import epyr_detector
import epyr_source

import math
import random

class TestSource(epyr_source.EPyRSource):
    
    def __init__(self, lstArgs):
        pass
        
    def GenerateUncorrelatedPair(self, fTime):
        
        fPhi1 = random.random()*math.pi*2
        fZ1 = -1 + random.random()*2
        fX1 = math.sqrt(1.0-fZ1**2)*math.cos(fPhi1)
        fY1 = math.sqrt(1.0-fZ1**2)*math.sin(fPhi1)
        fPhi2 = random.random()*math.pi*2
        fZ2 = -1 + random.random()*2
        fX2 = math.sqrt(1.0-fZ2**2)*math.cos(fPhi2)
        fY2 = math.sqrt(1.0-fZ2**2)*math.sin(fPhi2)
        return (str(fTime)+":"+str((fX1, fY1, fZ1)), str(fTime)+":"+str((-fX2, -fY2, -fZ2)))
        
    def GenerateCorrelatedPair(self, fTime):
        
        fPhi = random.random()*math.pi*2
        fZ = -1 + random.random()*2
        fX = math.sqrt(1.0-fZ**2)*math.cos(fPhi)
        fY = math.sqrt(1.0-fZ**2)*math.sin(fPhi)
        return (str(fTime)+":"+str((fX, fY, fZ)), str(fTime)+":"+str((-fX, -fY, -fZ)))
        
class TestDetector(epyr_detector.EPyRDetector):
    
    def __init__(self, strDetectorName, lstArgs):
        
        # set detector name
        epyr_detector.EPyRDetector.__init__(self, strDetectorName, lstArgs)

        print lstArgs
        
        self.fD = float(lstArgs[0]) # model parameter
        nM = int(lstArgs[1])        # number of directions
        
        # need to keep track of the last time a photon
        # passed through this detector
        self.fLastTime = 0.0

        self.lstDirections = [] # populate direction vectors
        for nI in range(0, nM):
            fTheta = random.random()*math.pi*2
            fPhi = random.random()*math.pi
            self.lstDirections.append((math.cos(fTheta)*math.sin(fPhi), math.sin(fTheta)*math.sin(fPhi), math.cos(fPhi)))

    def ProcessPhoton(self, fDetectorAngle, strPhoton):
        
        # pick random direction index (we really ought to use fDetectorAngle here...)
        nDirectionIndex = int(len(self.lstDirections)*random.random())
        lstDirection = self.lstDirections[nDirectionIndex]
        
        (strTime, strList) = strPhoton.split(":")
        lstPhoton = map(float, strList[1:-2].split(","))
        fTime = float(strTime)
        
        # note:  there is no way to do this calculation without having
        # the detector remember the last time a photon passed through it
        fDeltaT = fTime - self.fLastTime
        fProjection = sum([lstPhoton[nI]*lstDirection[nI] for nI in range(0, 3)])
        fDeltaT *= (1.0 - fProjection**2)**(self.fD/2)
        fTimeTag = self.fLastTime + fDeltaT
        self.fLastTime = fTime
            
        strResult = "R" # result will be either R or L
        if fProjection < 0.0:
            strResult = "L"
            
        # notice that there is now a correlation between the time tag
        # and the polarization measurement result
        return (fTimeTag, fDetectorAngle, strResult)

if __name__ == "__main__":
    
    pSource = TestSource([])
    pDetector = TestDetector("T", [3.0, 200])
    
    (strPhoton1, strPhoton2) = pSource.GenerateCorrelatedPair(4.0)
    (strTime, strList1) = strPhoton1.split(":")
    lstPhoton1 = map(float, strList1[1:-2].split(","))
    print sum([lstPhoton1[nI]**2 for nI in range(0, 3)])
    (strTime, strList2) = strPhoton2.split(":")
    lstPhoton2 = map(float, strList2[1:-2].split(","))
    print sum([lstPhoton2[nI]**2 for nI in range(0, 3)])

    print pDetector.ProcessPhoton(0.12345, strPhoton1)
