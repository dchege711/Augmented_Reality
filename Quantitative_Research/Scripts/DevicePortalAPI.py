'''
Makes API requests to the Windows Developers Portal's RESTful API

'''
#_______________________________________________________________________________

import requests
import json
import sys
import os
from datetime import datetime as dt
from requests.packages.urllib3.exceptions import InsecureRequestWarning

#_______________________________________________________________________________

# No matter who you are, whatever you do, please, don't try this at home.
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#_______________________________________________________________________________

# Initialize variables. (They'll be used as read-only)
holoLensIPv4Chege = os.environ['HL_CHEGE_IPV4']
holoLensIPv4Maria = os.environ['HL_MARIA_IPV4']
baseURLChege = "https://" + holoLensIPv4Chege + "/"
baseURLMaria = "https://" + holoLensIPv4Maria + "/"
USERNAME = os.environ['WDP_USERNAME']
PASSWORD = os.environ['WDP_PASSWORD_HL_CHEGE']
dtFormat = "%Y-%m-%d %H:%M:%S.%f"
fileNameDTFormat = "%m-%d-%H_%M"

#_______________________________________________________________________________

def logPerformanceStats(outputFile, whichHoloLens):
    '''
    Prints out performance stats (tab-delimited) to the specified text file.
    The stats are:
        TimeStamp, CPULoad, DedicatedMemory, DedicatedMemoryUsed, SystemMemory,
        SystemMemoryUsed, EnginesUtilization
    '''
    if whichHoloLens == 'Chege':
        performanceURL = baseURLChege + "api/resourcemanager/systemperf"
    else:
        performanceURL = baseURLMaria + "api/resourcemanager/systemperf"
    # Note: This is bad programming practice.
    # We've suppressed the warnings and ignored verifications
    r = requests.get(performanceURL, verify = False, auth = (USERNAME, PASSWORD))
    textAsDict = json.loads(r.json()['Reason'])
    gpuData = textAsDict['GPUData']['AvailableAdapters'][0]
    outputFile.write(
            dt.now().strftime(dtFormat) + "\t" +
            str(textAsDict['CpuLoad']) + "\t" +
            str(gpuData['DedicatedMemory']) + "\t" +
            str(gpuData['DedicatedMemoryUsed']) + "\t" +
            str(gpuData['SystemMemory']) + "\t" +
            str(gpuData['SystemMemoryUsed']) + "\t" +
            str(gpuData['EnginesUtilization']) + "\n"
    )

#_______________________________________________________________________________

def writePerformanceStats(whichHoloLens):
    '''
    Creates a time-stamped data file and calls writePerformanceStats()
    To stop logging, use the keyboard interrupt (Command + C)
    '''

    print("Writing performance stats...")

    # Open the file that will be used as output
    currentDir = os.path.dirname(__file__)
    fileName = whichHoloLens + "_" + dt.now().strftime(fileNameDTFormat) + "_HL_Performance.txt"
    filePath = os.path.join(currentDir, fileName)
    outputFile = open(filePath, 'w')

    # Include header information to make the output file easily understandable
    outputFile.write("TimeStamp\tCPULoad\tDedicatedMemory\tDedicatedMemoryUsed\t" +
                    "SystemMemory\tSystemMemoryUsed\tEnginesUtilization\n")

    # Keep logging until user presses Command + C
    while (True):
        try:
            logPerformanceStats(outputFile, whichHoloLens)
        except KeyboardInterrupt:
            print("Coolio! Exiting program...")
            sys.exit()

#_______________________________________________________________________________

if __name__ == '__main__':
    writePerformanceStats(sys.argv[1])

#_______________________________________________________________________________
