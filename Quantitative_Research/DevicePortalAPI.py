import requests
import json
import sys
import os
from datetime import datetime as dt
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# I'm a baaaad boy :-D
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

holoLensIPv4 = os.environ['HL_CHEGE_IPV4']
baseURL = "https://" + holoLensIPv4 + "/"
USERNAME = os.environ['WDP_USERNAME']
PASSWORD = os.environ['WDP_PASSWORD_HL_CHEGE']
dtFormat = "%Y-%m-%d %H:%M:%S.%f"
fileNameDTFormat = "%m-%d-%H_%M"

def logPerformanceStats(outputFile):
    '''
    Prints out performance stats (tab-delimited) to the specified text file.
    The stats are:
        TimeStamp, CPULoad, DedicatedMemory, DedicatedMemoryUsed, SystemMemory,
        SystemMemoryUsed, EnginesUtilization

    Sample result from the GET request...
    {'Reason': ' {
        "AvailablePages" : 230370,
        "CommitLimit" : 764290,
        "CommittedPages" : 382810,
        "CpuLoad" : 42,
        "IOOtherSpeed" : 13311247,
        "IOReadSpeed" : 0,
        "IOWriteSpeed" : 0,
        "NonPagedPoolPages" : 47010,
        "PageSize" : 4096,
        "PagedPoolPages" : 19875,
        "TotalInstalledInKb" : 2097152,
        "TotalPages" : 502146,
        "GPUData" : {
            "AvailableAdapters" : [
                {
                    "DedicatedMemory" : 119537664,
                    "DedicatedMemoryUsed" : 81920,
                    "Description" : "HoloLens Graphics",
                    "SystemMemory" : 1028395008,
                    "SystemMemoryUsed" : 48226304,
                    "EnginesUtilization" : [6.194690,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000]
                }
            ]
        },
        "NetworkingData" : {
            "NetworkInBytes" : 11000,
            "NetworkOutBytes" : 24000
        }
        }
    '}
    '''
    performanceURL = baseURL + "api/resourcemanager/systemperf"
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


def writePerformanceStats():
    currentDir = os.path.dirname(__file__)
    fileName = dt.now().strftime(fileNameDTFormat) + "_HL_Performance.txt"
    print("Writing performance stats...")
    filePath = os.path.join(currentDir, 'Data_Dumps', fileName)
    outputFile = open(filePath, 'w')
    outputFile.write("TimeStamp\tCPULoad\tDedicatedMemory\tDedicatedMemoryUsed\t" +
                    "SystemMemory\tSystemMemoryUsed\tEnginesUtilization\n")
    while (True):
        try:
            logPerformanceStats(outputFile)
        except KeyboardInterrupt:
            print("Coolio! Exiting program...")
            sys.exit()

if __name__ == '__main__':
    writePerformanceStats()
