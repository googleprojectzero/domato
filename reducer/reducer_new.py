## GET DIRECTORY, FIND HTML FILES ##
import sys
import os
import shutil
import json
import glob
from time import sleep

if len(sys.argv) < 2 :
  print("enter html folder direction")
  exit()

dirname = sys.argv[1]
if not os.path.isdir(dirname) :
  print(f"folder doesn't exist: {dirname}")
  exit()

print(f"reducing files inside folder {dirname}")

fileList = os.listdir(dirname)

def isHTML(filename):
  return os.path.splitext(filename)[1] == ".html"

htmlList = list(filter(isHTML, fileList))

# REDUCED
if not os.path.exists(dirname + "/" + "reduced") :
  os.makedirs(dirname + "/" + "reduced")

exReduced = glob.glob(dirname + "/reduced/*")
for file in exReduced:
  os.remove(file)

sleep(1)

for htmlfile in htmlList:
  originpath = "/".join([dirname, htmlfile])
  newpath = "/".join([dirname, "reduced", htmlfile])
  shutil.copy(originpath, newpath)

reducedDirName = "/".join([dirname, "reduced"])

# STATISTIC
if not os.path.exists(dirname + "/" + "statistic") :
  os.makedirs(dirname + "/" + "statistic")

exStat = glob.glob(dirname + "/statistic/*")
for file in exReduced:
  os.remove(file)

statDirName = "/".join([dirname, "statistic"])


## OPEN HTML FILES, REDUCE ##
from selenium import webdriver

def reduceFile(htmltext, areaName, errorIndices, final=False):
  jsfuzzerBefore = htmltext.split(f'/* BEGIN {areaName} */')[0]
  jsfuzzerArea = htmltext.split(f'/* BEGIN {areaName} */')[1].split(f'/* END {areaName} */')[0]
  jsfuzzerAfter = htmltext.split(f'/* END {areaName} */')[1]

  jsfuzzerPreCodes = jsfuzzerArea.split('/* LINE */')[0]
  jsfuzzerEpilCodes = jsfuzzerArea.split('//endjs')[-1]

  jsfuzzerCodes = list(filter(lambda x : x.startswith('/* LINE */'), jsfuzzerArea.split('\n')))
  if final:
    jsfuzzerCodes = [ line.split('lineNo++;')[1].split('} catch(e)')[0] for line in jsfuzzerCodes ]

  codelen = len(jsfuzzerCodes)
  wholeIndices = range(codelen)
  validIndices = [x for x in wholeIndices if x not in errorIndices]

  jsfuzzerValidCodes = '\n'.join([jsfuzzerCodes[x] for x in validIndices])

  jsfuzzerReduced = '\n'.join([jsfuzzerBefore, f'/* BEGIN {areaName} */', jsfuzzerPreCodes, jsfuzzerValidCodes, '//endjs', jsfuzzerEpilCodes, f'/* END {areaName} */', jsfuzzerAfter])
  return jsfuzzerReduced


driver = webdriver.Chrome(executable_path='./chromedriver.exe')

for htmlname in htmlList:
  htmlpath = '/'.join([reducedDirName, htmlname])
  htmlpath = os.path.abspath(htmlpath)
  print(f"reduce start: {htmlpath}")

  try:
    history = {
      "totalLine": {
        "jsfuzzer": [],
        "eventhandler1": [],
        "eventhandler2": [],
        "eventhandler3": [],
        "eventhandler4": [],
        "eventhandler5": []
      },
      "errorLine": {
        "jsfuzzer": [],
        "eventhandler1": [],
        "eventhandler2": [],
        "eventhandler3": [],
        "eventhandler4": [],
        "eventhandler5": []
      }
    }

    # jsfuzzer reduce
    while True :
      driver.get("file://" + htmlpath)
      driver.implicitly_wait(time_to_wait=1)

      runLines = driver.execute_script("return runLines")
      errorLines = driver.execute_script("return errorLines")

      history["totalLine"]["jsfuzzer"].append(runLines["jsfuzzer"])
      history["errorLine"]["jsfuzzer"].append(len(errorLines["jsfuzzer"]))

      print(f"jsfuzzer errorline: {len(errorLines['jsfuzzer'])}")
      if len(errorLines['jsfuzzer']) == 0 :
        break

      htmltext = open(htmlpath, 'r').read()
      reducedtext = reduceFile(htmltext, 'jsfuzzer', errorLines['jsfuzzer'])
      open(htmlpath, 'w').write(reducedtext)
    
    htmltext = open(htmlpath, 'r').read()
    reducedtext = reduceFile(htmltext, 'jsfuzzer', [], True)
    open(htmlpath, 'w').write(reducedtext)
    
    # eventhandler1 reduce
    while True :
      driver.get("file://" + htmlpath)
      driver.implicitly_wait(time_to_wait=1)

      runLines = driver.execute_script("return runLines")
      errorLines = driver.execute_script("return errorLines")

      history["totalLine"]["eventhandler1"].append(runLines["eventhandler1"])
      history["errorLine"]["eventhandler1"].append(len(errorLines["eventhandler1"]))

      print(f"eventhandler1 errorline: {len(errorLines['eventhandler1'])}")
      if len(errorLines['eventhandler1']) == 0 :
        break

      htmltext = open(htmlpath, 'r').read()
      reducedtext = reduceFile(htmltext, 'eventhandler1', errorLines['eventhandler1'])
      open(htmlpath, 'w').write(reducedtext)
    
    htmltext = open(htmlpath, 'r').read()
    reducedtext = reduceFile(htmltext, 'eventhandler1', [], True)
    open(htmlpath, 'w').write(reducedtext)

    # eventhandler2 reduce
    while True :
      driver.get("file://" + htmlpath)
      driver.implicitly_wait(time_to_wait=1)

      runLines = driver.execute_script("return runLines")
      errorLines = driver.execute_script("return errorLines")

      history["totalLine"]["eventhandler2"].append(runLines["eventhandler2"])
      history["errorLine"]["eventhandler2"].append(len(errorLines["eventhandler2"]))

      print(f"eventhandler2 errorline: {len(errorLines['eventhandler2'])}")
      if len(errorLines['eventhandler2']) == 0 :
        break

      htmltext = open(htmlpath, 'r').read()
      reducedtext = reduceFile(htmltext, 'eventhandler2', errorLines['eventhandler2'])
      open(htmlpath, 'w').write(reducedtext)
    
    htmltext = open(htmlpath, 'r').read()
    reducedtext = reduceFile(htmltext, 'eventhandler2', [], True)
    open(htmlpath, 'w').write(reducedtext)

    # eventhandler3 reduce
    while True :
      driver.get("file://" + htmlpath)
      driver.implicitly_wait(time_to_wait=1)

      runLines = driver.execute_script("return runLines")
      errorLines = driver.execute_script("return errorLines")

      history["totalLine"]["eventhandler3"].append(runLines["eventhandler3"])
      history["errorLine"]["eventhandler3"].append(len(errorLines["eventhandler3"]))
      
      print(f"eventhandler3 errorline: {len(errorLines['eventhandler3'])}")
      if len(errorLines['eventhandler3']) == 0 :
        break

      htmltext = open(htmlpath, 'r').read()
      reducedtext = reduceFile(htmltext, 'eventhandler3', errorLines['eventhandler3'])
      open(htmlpath, 'w').write(reducedtext)
    
    htmltext = open(htmlpath, 'r').read()
    reducedtext = reduceFile(htmltext, 'eventhandler3', [], True)
    open(htmlpath, 'w').write(reducedtext)

    # eventhandler4 reduce
    while True :
      driver.get("file://" + htmlpath)
      driver.implicitly_wait(time_to_wait=1)

      runLines = driver.execute_script("return runLines")
      errorLines = driver.execute_script("return errorLines")

      history["totalLine"]["eventhandler4"].append(runLines["eventhandler4"])
      history["errorLine"]["eventhandler4"].append(len(errorLines["eventhandler4"]))
      
      print(f"eventhandler4 errorline: {len(errorLines['eventhandler4'])}")
      if len(errorLines['eventhandler4']) == 0 :
        break

      htmltext = open(htmlpath, 'r').read()
      reducedtext = reduceFile(htmltext, 'eventhandler4', errorLines['eventhandler4'])
      open(htmlpath, 'w').write(reducedtext)
    
    htmltext = open(htmlpath, 'r').read()
    reducedtext = reduceFile(htmltext, 'eventhandler4', [], True)
    open(htmlpath, 'w').write(reducedtext)
    
    # eventhandler5 reduce
    while True :
      driver.get("file://" + htmlpath)
      driver.implicitly_wait(time_to_wait=1)

      runLines = driver.execute_script("return runLines")
      errorLines = driver.execute_script("return errorLines")

      history["totalLine"]["eventhandler5"].append(runLines["eventhandler5"])
      history["errorLine"]["eventhandler5"].append(len(errorLines["eventhandler5"]))
      
      print(f"eventhandler5 errorline: {len(errorLines['eventhandler5'])}")
      if len(errorLines['eventhandler5']) == 0 :
        break

      htmltext = open(htmlpath, 'r').read()
      reducedtext = reduceFile(htmltext, 'eventhandler5', errorLines['eventhandler5'])
      open(htmlpath, 'w').write(reducedtext)
    
    htmltext = open(htmlpath, 'r').read()
    reducedtext = reduceFile(htmltext, 'eventhandler5', [], True)
    open(htmlpath, 'w').write(reducedtext)

    
    statpath = '/'.join([statDirName, os.path.basename(htmlname) + ".json"])
    statpath = os.path.abspath(statpath)
    open(statpath, 'w').write(json.dumps(history))
    
  except:
    print(f"failed: {htmlpath}")
  