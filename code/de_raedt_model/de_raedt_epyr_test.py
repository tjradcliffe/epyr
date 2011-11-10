
if __name__ == "__main__":
    import os
    import sys
    strNewPath = os.path.abspath("../")
    sys.path.append(strNewPath)
    
# local imports
import epyr_detector
import epyr_source

import math
import random

class TestSource(epyr_source.EPyRSource):
    
    def __init__(self, lstArgs):
        pass
        
    def GenerateUncorrelatedPair(self, nCount, fTime):
        
        fTheta1 = random.random()*math.pi*2
        fTheta2 = random.random()*math.pi*2
        return (str(nCount)+":"+str(fTime)+":"+str((fTheta1)), str(fTime)+":"+str((fTheta2)))
        
    def GenerateCorrelatedPair(self, nCount, fTime):
        
        fTheta = random.random()*math.pi*2
        return (str(nCount)+":"+str(fTime)+":"+str(fTheta), str(nCount)+":"+str(fTime)+":"+str(fTheta))
        
class TestDetector(epyr_detector.EPyRDetector):
    
    def __init__(self, strDetectorName, lstArgs):
        
        # set detector name
        epyr_detector.EPyRDetector.__init__(self, strDetectorName, lstArgs)

    def ProcessPhoton(self, fDetectorAngle, strPhoton):
        
        (strCount, strTime, strPhotonAngle) = strPhoton.split(":")
        fTime = float(strTime)
        nCount = int(strCount)
        fPhotonAngle = float(strPhotonAngle)

        # The time we get here is the time the photon was emited, which is
        # by hypothesis identical for the pair (this is not the case in
        # Aspect's experiments, for example, which involve an intermediate
        # state that results in one photon being delayed significantly after
        # the other, as an early criticism of the experiments argued.
        
        # Since all we care about is our ability to tag the photon, we're just
        # going to look at the transit time through the appartus, which is
        # going to be dependent on the setting of the polarizer angles.  However,
        # to make the argument work there must be some jitter in the apparatus,
        # which we add at the end.  If there were not, then the delay would
        # not have the desired effect, but would instead result in a sharp
        # cutoff at a particular angle difference.  What we are doing in effect
        # is low-pass filtering the effect of the delay across the full interval.
        
        fDelay = math.cos(fPhotonAngle-fDetectorAngle) # completely deterministic delay
        #fJitter = 2*(0.5-random.random()) # quasi-random jitter in detection time
        
        # for now use de Raedt's prescription blindly and assume it can be made physical
        fTimeTag = random.random()*(1.0 - fDelay**2)**1.5
            
        strResult = "R"     # result will be either R or L
        if fDelay < 0.0:    # this is the correlation between delay and polarizer arm
            strResult = "L"
            
        # notice that there is now a correlation between the time tag
        # and the polarization measurement result
        return (nCount, fTimeTag, fDetectorAngle, strResult)

if __name__ == "__main__":
    
    strNewPath = os.path.abspath("../")
    sys.path.append(strNewPath)
    
    pSource = TestSource([])
    pDetector = TestDetector("T", [3.0, 200])
    
    (strPhoton1, strPhoton2) = pSource.GenerateCorrelatedPair(42, 4.0)
    print strPhoton1
    print strPhoton2
    print pDetector.ProcessPhoton(0.12345, strPhoton1)
