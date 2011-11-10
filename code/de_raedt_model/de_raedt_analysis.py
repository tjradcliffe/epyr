
def readData(strFilename):
    
    lstData = []
    inFile = open(strFilename, "r")
    nCount = 0
    for strLine in inFile:
        nCount += 1
        lstLine = strLine.split()
        nCount = int(lstLine[0])
        fTime = float(lstLine[1])
        fAngle = float(lstLine[2])
        strResult = lstLine[3]
        lstData.append((nCount, fTime, fAngle, strResult))
    inFile.close()
    return lstData

print "Reading data..."
lstD1 = readData("detector_d1_output.txt")
lstD2 = readData("detector_d2_output.txt")
print "Done read"

nBins = 18
lstNsame = [0 for nI in range(0, nBins)]
lstNdiff = [0 for nI in range(0, nBins)]

fTau = 0.0025 # window for accepting a coincidence
nMissed = 0
nHit = 0
outFile = open("combined.dat", "w")
lstAngles = [0 for nI in range(0, nBins)]
for nI in range(0, len(lstD1)):

    (nCount1, fT1, fA1, strR1) = lstD1[nI]
    (nCount2, fT2, fA2, strR2) = lstD2[nI]
    outFile.write(str(nCount1)+" "+str(fT1-fT2)+" "+str(fA1-fA2)+" "+str(strR1==strR2)+"\n")
    
    fTheta = fA1 - fA2
    if fTheta < 0.0:
        fTheta = fA2 - fA1
    if fTheta > 180:
        fTheta -= 180
    nIndex = int(nBins*fTheta/180) # should always be < 180
    lstAngles[nIndex] += 1
    
    if nCount1 != nCount2:
        print "Failed on count compare: "
        print nCount1
        print nCount2
        sys.exit(-1)
        
    if abs(fT1-fT2) < fTau:
        nHit += 1   # count the hits

        if strR1 == strR2:
            lstNsame[nIndex] += 1
        else:
            lstNdiff[nIndex] += 1
    else:
        nMissed += 1

outFile = open("correlation1.dat","w")
lstE = [0 for nI in range(0, nBins)]
for nI in range(0, nBins):
    fTotal = lstNsame[nI] + lstNdiff[nI]
    if fTotal > 0:
        lstE[nI] = float(lstNsame[nI]-lstNdiff[nI])/fTotal
    else:
        lstE[nI] = 0.0

    print str(180.0*nI/nBins)+" "+str(lstE[nI])+" "+str(fTotal)+" "+str(lstAngles[nI])
    outFile.write(str(180.0*nI/nBins)+" "+str(lstE[nI])+"\n")

outFile.close()

print "==========="
print nHit
print nMissed
