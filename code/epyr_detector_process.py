"""

Copyright (C) 2011 Predictive Patterns Software Inc
Author: Tom Radcliffe
Created: 2011-11-05
License: GPL2

Detector process for EPyR

This process is normally started from epyr_source_process.py.  The <other>
arguments are the argument list from that process (sys.argv) and are passed
on to the TestDetector constructor.

"""

import math
import random
import socket
import sys

nBuffer = 100
lstRandom = [random.random() for nI in range(0,nBuffer)]
def Random():
    global lstRandom
    nIndex = int(nBuffer*random.random())
    fRandom = lstRandom[nIndex]
    lstRandom[nIndex] = random.random()
    return fRandom

if len(sys.argv) < 5:   # rudimentary sanity check
    print "Syntax is: python detector.py strDetectorName strHost strPort strTestFilename <other>"
    sys.exit(-1)

try:
    strDetector = sys.argv[1]    # convenience identifier for this detector
    strHost = sys.argv[2]        # localhost only
    strPort = int(sys.argv[3])   # Arbitrary non-privileged port
    strTestFilename = sys.argv[4]# epyr_test.py by default
    strSettings = sys.argv[5]    # type of angles to use (EPR or UNIFORM)
    bEPRAngles = False
    if strSettings == "EPR":
        bEPR = True
    elif strSettings != "UNIFORM":
        raise Exception()
    
    # load the user file
    testFile = open(strTestFilename, "r")
    exec(testFile)
    testFile.close()

    lstAngles = [0, math.pi/4, math.pi/8, 3*math.pi/8]

    outFile = open("detector_"+strDetector.lower()+"_output.txt", "w")
        
    lstArgs = []
    if len(sys.argv) > 6:
        lstArgs = sys.argv[6:]
    pDetector = TestDetector(strDetector, lstArgs)
    print "Detector: "+strDetector

    pSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    pSocket.bind((strHost, strPort))
    pSocket.listen(1)
    pConnection, strAddress = pSocket.accept()
    print 'Connected by', strAddress
    
    strEnd = "==END_OXF_PHOTON=="
    strDone = "==END_OXF_RUN=="
    bAccepting = True
    strDataBlock = ""
    while bAccepting:
        try:
            strPhoton = ""
            bReading = True
            while bReading:
                strData = pConnection.recv(1024)    # will block
                strDataBlock += strData
                
                if -1 != strDataBlock.find(strDone):
                    bAccepting = False  # we are done
                    break
                    
                if -1 != strDataBlock.find(strEnd):
                    lstBlocks = strDataBlock.split(strEnd)
                    strPhoton = lstBlocks[0]
                    if len(lstBlocks) > 1:
                        strDataBlock = strEnd.join(lstBlocks[1:])
                    bReading = False
                    
            if 0 < len(strPhoton):
                nIndex = int(Random()*len(lstAngles))
                if bEPRAngles:
                    fDetectorAngle = lstAngles[nIndex]
                else:
                    fDetectorAngle = math.pi # D1 is fixed to get uniform angular distribution
                    if pDetector.strDetectorName == "D2":
                        fDetectorAngle = 2*math.pi*Random()
                (nCount, fTime, fDetectorAngle, strResult) = pDetector.ProcessPhoton(fDetectorAngle, strPhoton)
                outFile.write(str(nCount)+" "+str(fTime)+" "+str(180*fDetectorAngle/math.pi)+" "+strResult+"\n")
        except Exception, e:
            print e

    pConnection.close()

    outFile.close()
    
except Exception, e:
    
    print e
    import traceback
    print "\n"+traceback.format_exc()
    print "Hit any key to close"
    raw_input()
