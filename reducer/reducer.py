import sys

print(sys.argv)

filePath = sys.argv[1]
freeTry = False
if len(sys.argv) > 2:
  print(sys.argv[2])
  freeTry = True

rawFile = open(filePath, 'r')
fileContent = rawFile.read()

jsfuzzerBefore = fileContent.split('/* BEGIN jsfuzzer */')[0]
jsfuzzerArea = fileContent.split('/* BEGIN jsfuzzer */')[1].split('/* END jsfuzzer */')[0]
jsfuzzerAfter = fileContent.split('/* END jsfuzzer */')[1]

jsfuzzerPreCodes = jsfuzzerArea.split('/* LINE */')[0]
jsfuzzerEpilCodes = jsfuzzerArea.split('//endjs')[-1]

jsfuzzerCodes = list(filter(lambda x : x.startswith('/* LINE */'), jsfuzzerArea.split('\n')))
if freeTry :
  jsfuzzerCodes = [ line.split('lineNo++;')[1].split('} catch(e)')[0] for line in jsfuzzerCodes ]
  print(jsfuzzerCodes[:10])

codelen = len(jsfuzzerCodes)
wholeIndices = range(codelen)
# errorIndices = [8,15,41,54,68,89,103,108,114,151,193,200,313,317,332,349,374,389,395,411,426,428,429,430,445,447,470,479,482,493,593,600,604,606,610,626,666,668,688,714,715,718,738,759,773,789,791,795,807,848,854,856,883,887,900,926,954,959,966,980,991]
# errorIndices = [39,97,98,106,137,377,406,422,454,458,491,498,572,591,607,630,696,716,740,744,748,759,804,805,820,838,850,871,898,907]
# errorIndices = [96,215,449,481,487,796]
errorIndices = []
validIndices = [x for x in wholeIndices if x not in errorIndices]

jsfuzzerValidCodes = '\n'.join([jsfuzzerCodes[x] for x in validIndices])

jsfuzzerReduced = '\n'.join([jsfuzzerBefore, '/* BEGIN jsfuzzer */', jsfuzzerPreCodes, jsfuzzerValidCodes, '//endjs', jsfuzzerEpilCodes, '/* END jsfuzzer */', jsfuzzerAfter])

writeFile = open('./a.html', 'w')
writeFile.write(jsfuzzerReduced)