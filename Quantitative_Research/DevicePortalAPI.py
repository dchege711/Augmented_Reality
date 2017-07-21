import requests
import json
import os
from datetime import datetime as dt
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# I'm a baaaad boy :-D
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

holoLensIPv4 = os.environ['HL_CHEGE_IPV4']
baseURL = "https://" + holoLensIPv4 + "/"
USERNAME = os.environ['WDP_USERNAME']
PASSWORD = os.environ['WDP_PASSWORD_HL_CHEGE']

def logPerformanceStats():
    '''
    Returns a dict of the performance stats

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
    print(dt.now(), end = ", ")
    print(textAsDict['CpuLoad'], textAsDict['NetworkingData']['NetworkOutBytes'])

for i in range(3):
    logPerformanceStats()
