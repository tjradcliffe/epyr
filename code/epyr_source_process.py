"""

Copyright (C) 2011 Predictive Patterns Software Inc
Author: Tom Radcliffe
Created: 2011-11-05
License: GPL2

Driver for EPyR simulation engine.  This spawns two independent Detector
processes, loads the user-supplied PhotonPair generator and enters the main
loop, which runs forever, or until the requested number of pairs have been
generated.

Running from the command line simply type:

python epyr_source_process.py nShots strTestFilename bCorrelated <other>

The optional nShots argument is the number of pairs to generate.  If omitted
the process will run until it is killed, or one of the detector processes is
killed.

The optional strTestFilename argument is the Python file that contains the TestSource
and TestDetector classes.  If omitted epyr_test.py in the current directory will
be used.

The optional bCorrelated argument is either True or False to indicate if the
generated pairs should be correlated or not.  True is the default.

All <other> arguments are passed on to the detector processes and source constructor.
"""

# standard imports
import random
import socket
import subprocess
import sys
import time

# process arguments
#
# python epyr_source_process.py nShots strTestFilename strCorrelation strAngleSetting <other>
#
# where nShots = -1 for endless
#       strTestFilename = epyr_test.py or similar
#       strCorrelation = UNCORRELATED for uncorrelated, anything else gives correlated
#       strAngleSetting = EPR for 0/45/22.5/67.5, anything else for uniform 0 => tau
#       
nShots = -1
strTestFilename = "epyr_test.py"
bCorrelated = True
strAngleSetting = "EPR" # alternative is "UNIFORM" for 0 => tau
if len(sys.argv) >= 2:
    nShots = int(sys.argv[1])
if len(sys.argv) >= 3:
    strTestFilename = sys.argv[2]
if len(sys.argv) >= 4:
    if "UNCORRELATED" == sys.argv[3]:
        bCorrelated = False
if len(sys.argv) >= 5:
    strAngleSetting == sys.argv[4]
lstArgs = []
if len(sys.argv) > 5:
    lstCmdArgs = sys.argv[5:]

# load the user file
testFile = open(strTestFilename, "r")
exec(testFile)
testFile.close()

# create photon source
pSource = TestSource(lstArgs)

# create two detectors creatively named "D1" and "D2" listening on sockets
strHost = "127.0.0.1"
strD1Port = "37001"
strD2Port = "37007"
lstArgs = ["python","epyr_detector_process.py","D1", strHost, strD1Port, strTestFilename, strAngleSetting]
lstArgs.extend(lstCmdArgs)
pDetector1 = subprocess.Popen(lstArgs)
lstArgs = ["python","epyr_detector_process.py","D2", strHost, strD2Port, strTestFilename, strAngleSetting]
lstArgs.extend(lstCmdArgs)
pDetector2 = subprocess.Popen(lstArgs)

# create connections to the newly-created detector processes
pD1Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pD1Socket.connect((strHost, int(strD1Port)))
pD2Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pD2Socket.connect((strHost, int(strD2Port)))

fTime = 0.0                   # keep track of time
strEnd = "==END_OXF_PHOTON==" # end of photon flag (keep comms one-way)
nCount = 0
while None == pDetector1.poll() and None == pDetector2.poll():
    
    nCount += 1 # if we are running for fixed number of pairs
    if nShots > 0 and nCount > nShots:
        break

    # generate pair of appropriate type
    if bCorrelated:
        (strPhoton1, strPhoton2) = pSource.GenerateCorrelatedPair(fTime)
    else:
        (strPhoton1, strPhoton2) = pSource.GenerateUncorrelatedPair(fTime)
        
    if -1 != strPhoton1.find(strEnd) or -1 != strPhoton2.find(strEnd):
        print "Illegal string found in photon: "+strEnd
        print "Please read the documentation more carefully"
        sys.exit(-1)
        
    pD1Socket.send(strPhoton1+"\n")
    pD1Socket.send(strEnd+"\n")
    pD2Socket.send(strPhoton2+"\n")
    pD2Socket.send(strEnd+"\n")
    fTime += random.random()
    if 0 == nCount%1000:
        print str(nCount)+" "+str(fTime)
    time.sleep(0.001)    # slow things down for more robust communication

try:    # shut down child processes
    pDetector1.kill()
    pDetector2.kill()
except Exception, e:
    pass
    
print "Done"

