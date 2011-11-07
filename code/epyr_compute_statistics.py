
def readData(strFilename):
    
    lstData = []
    inFile = open(strFilename, "r")
    for strLine in inFile:
        lstLine = strLine.split()
        fTime = float(lstLine[0])
        strAngle = lstLine[1]
        strResult = lstLine[2]
        lstData.append((fTime, strAngle, strResult))
    inFile.close()
    return lstData

lstD1 = readData("detector_d1_output.txt")
lstD2 = readData("detector_d2_output.txt")

mapAngle = {"0.0:22.5":0 , "0.0:67.5":1, "45.0:22.5":2, "45.0:67.5":3}
lstNrr = [0 for nI in range(0, 4)]
lstNll = [0 for nI in range(0, 4)]
lstNrl = [0 for nI in range(0, 4)]
lstNlr = [0 for nI in range(0, 4)]

nSame = 0   # coincidence count when analyzers have the same setting
nSet = 0    # count of times analyzers are set the same

nMissed = 0
nHit = 0
nJLast = 0
for nI in range(0, len(lstD1)):
    
    (fT1, strA1, strR1) = lstD1[nI]
    bFound = False
    for nJ in range(nJLast, len(lstD2)):
        (fT2, strA2, strR2) = lstD2[nJ]
        if abs(fT1-fT2) < 0.01:
            bFound = True
            nJLast = nJ
            break
    
    if bFound:
        nHit += 1   # count the hits

        if strA1 == strA2:  # analyzers set the same
            nSet += 1
            if strR1 == strR2:  # results are the same
                nSame += 1
            
        strKey = strA1+":"+strA2
        if strKey in mapAngle.keys():
            nIndex = mapAngle[strKey]
            if strR1 == "R" and strR2 == "R":
                lstNrr[nIndex] += 1
            elif strR1 == "L" and strR2 == "L":
                lstNll[nIndex] += 1
            elif strR1 == "R" and strR2 == "L":
                lstNrl[nIndex] += 1
            elif strR1 == "L" and strR2 == "R":
                lstNlr[nIndex] += 1
    else:
        nMissed += 1

lstE = [0 for nI in range(0, 4)]
for nI in range(0, 4):
    lstE[nI] = (float(lstNrr[nI]+lstNll[nI]-lstNrl[nI]-lstNlr[nI])/
                     (lstNrr[nI]+lstNll[nI]+lstNrl[nI]+lstNlr[nI]))
             
fS = lstE[0] - lstE[1] + lstE[2] + lstE[3]

print nMissed
print nHit
print fS
print float(nSame)/nSet
