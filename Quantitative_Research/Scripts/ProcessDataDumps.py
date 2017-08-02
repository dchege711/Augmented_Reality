'''
Processes CSV data produced by different sources.
'''
#_______________________________________________________________________________

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import re
import os

#_______________________________________________________________________________

# Useful IP Addresses
laptopIPv4 = os.environ['LAPTOP_IPV4']
holoLensIPv4Chege = os.environ['HL_CHEGE_IPV4']
holoLensIPv4Maria = os.environ['HL_MARIA_IPV4']

dataPath = 'C:/Users/dchege711/Documents/Augmented_Reality/Quantitative_Research/Data_Dumps/Report_03/'

data = {
    'noData_data'       : [dataPath + '08-01-12_45_59_Wireshark_noData.csv', '12:45:59'],
    'noData_Chege'      : [dataPath + '08-01-12_41_45_HL_Performance_Chege_noData.txt', '12:41:45'],
    'noData_Maria'      : [dataPath + '08-01-12_41_51_HL_Performance_Maria_noData.txt', '12:41:51'],
    '4kVectors_data'    : [dataPath + '08-01-13_36_13_Wireshark_4kVectors.csv', '13:36:13'],
    '4kVectors_Chege'   : [dataPath + '08-01-13_36_22_HL_Performance_Chege_4kVectors.txt', '13:36:22'],
    '4kVectors_Maria'   : [dataPath + '08-01-13_36_25_HL_Performance_Maria_4kVectors.txt', '13:36:25'],
    '8kVectors_data'    : [dataPath + '08-01-18_10_12_Wireshark_8kVectors.csv', '18:10:12'],
    '8kVectors_Chege'   : [dataPath + '08-01-18_10_20_HL_Performance_Chege_8kVectors.txt', '18:10:20'],
    '8kVectors_Maria'   : [dataPath + '08-01-18_10_26_HL_Performance_Maria_8kVectors.txt', '18:10:26'],
    '12kInts_data'      : [dataPath + '08-02-09_44_42_Wireshark_12kInts.csv', '09:44:42'],
    '12kInts_Chege'     : [dataPath + '08-02-09_44_55_HL_Performance_Chege_12kInts.txt', '09:44:55'],
    '12kInts_Maria'     : [dataPath + '08-02-09_44_54_HL_Performance_Maria_12kInts.txt', '09:44:54']
}

#_______________________________________________________________________________

def getWDPStats(wdpDump):
    '''
    Returns 2 lists of tuples of the form (timeStamp, bytesTransferred)
    The lists are holoLensToLaptop and laptopToHoloLens in that order

    '''
    '''
    Sample Windows Device Portal Data
    Timestamp,Provider,ID
    ....
    07/19/2017-16:02:12.9536544,Microsoft-Windows-Kernel-Network,11,Keyword:9223372036854776000,Level:4,Message:TCPv4: 124 bytes received from 10.X.XYZ.ABC:443 to 10.X.XYZ.XYZ:55939. ,PID:4,ProviderName:Microsoft-Windows-Kernel-Network,TaskName:KERNEL_NETWORK_TASK_TCPIP,connid:0,daddr:10.X.XYZ.XYZ,dport:55939,saddr:10.X.XYZ.ABC,seqnum:0,size:124,sport:443,WebbCompletePayload:message:tcpv4: 124 bytes received from 10.X.XYZ.ABC:443 to 10.X.XYZ.XYZ:55939. , pid:4, connid:0, daddr:10.X.XYZ.XYZ, dport:55939, saddr:10.X.XYZ.ABC, seqnum:0, size:124, sport:443,
    07/19/2017-16:02:12.9595648,Microsoft-Windows-Kernel-Network,10,Keyword:9223372036854776000,Level:4,Message:TCPv4: 143 bytes transmitted from 10.X.XYZ.ABC:443 to 10.X.XYZ.XYZ:55939. ,PID:4,ProviderName:Microsoft-Windows-Kernel-Network,TaskName:KERNEL_NETWORK_TASK_TCPIP,connid:0,daddr:10.X.XYZ.XYZ,dport:55939,endtime:931204,saddr:10.X.XYZ.ABC,seqnum:0,size:143,sport:443,startime:931204,WebbCompletePayload:message:tcpv4: 143 bytes transmitted from 10.X.XYZ.ABC:443 to 10.X.XYZ.XYZ:55939. , pid:4, connid:0, daddr:10.X.XYZ.XYZ, dport:55939, endtime:931204, saddr:10.X.XYZ.ABC, seqnum:0, size:143, sport:443, startime:931204,
    ...
    '''
    # The time stamps are pretty dense (numerous points per second)
    # We want to group the data using seconds as our resolution
    timeRegEx = r"\d{2}\/\d{2}\/\d{4}-\d{2}:\d{2}:\d{2}"
    laptopAsDestRegEx = r"daddr:10\.8\.227\.69"
    laptopAsSenderRegEx = r"saddr:10\.8\.227\.69"
    sizeRegEx = r"size:\d{0,}"

    # Initialize relevant variables
    holoLensToLaptop_timeStamps = []
    holoLensToLaptop_MB = []
    laptopToHoloLens_timeStamps = []
    laptopToHoloLens_MB = []

    sent = 0
    received = 0

    with open(wdpDump) as myData:
        # We don't need the header information
        myData.readline()

        # Initialize helper variables
        prevTimeStampSent = "07/19/2017-16:02:12"   #
        prevTimeStampReceived = "07/19/2017-16:02:12"
        runningDataSumSent = 0
        runningDataSumReceived = 0

        # The data is not uniformly formatted, hence regular expressions
        for line in myData:

            # Search for the relevant data points
            timeStamp = re.search(timeRegEx, line)[0] # Gets the text itself
            sendingToLaptop = re.search(laptopAsDestRegEx, line)
            receivingFromLaptop = re.search(laptopAsSenderRegEx, line)
            dataPresent = re.search(sizeRegEx, line)

            if sendingToLaptop and dataPresent:
                currentBytes = int(dataPresent[0].split(':')[1])
                # Increment the total if we're still in the same second
                if timeStamp == prevTimeStampSent:
                    runningDataSumSent += currentBytes
                # Append the total and reset sum if we've moved to a new sec
                else:
                    holoLensToLaptop_timeStamps.append(prevTimeStampSent)
                    holoLensToLaptop_MB.append(runningDataSumSent / (1024 * 1024))
                    sent += runningDataSumSent / (1024 * 1024)
                    prevTimeStampSent = timeStamp
                    runningDataSumSent = currentBytes

            if receivingFromLaptop and dataPresent:
                currentBytes = int(dataPresent[0].split(':')[1])
                # Increment the total if we're still in the same second
                if timeStamp == prevTimeStampReceived:
                    runningDataSumReceived += currentBytes
                # Append the total and reset sum if we've moved to a new sec
                else:
                    laptopToHoloLens_timeStamps.append(prevTimeStampReceived)
                    laptopToHoloLens_MB.append(runningDataSumReceived / (1024 * 1024))
                    received += runningDataSumReceived / (1024 * 1024)
                    prevTimeStampReceived = timeStamp
                    runningDataSumReceived = currentBytes

    # Communicate status to terminal
    print(  "Sent {0:.2f} MB".format(sent),
            ", received {0:.2f} MB".format(received),
            ", total = {0:.2f} MB".format(sent+received)
    )
    print("\nSent Array Length", str(len(holoLensToLaptop_timeStamps)), "/", str(len(holoLensToLaptop_MB)))
    print("\nReceived Array Length", str(len(laptopToHoloLens_timeStamps)), "/", str(len(laptopToHoloLens_MB)))

    # Return results
    return (holoLensToLaptop_timeStamps, holoLensToLaptop_MB, laptopToHoloLens_timeStamps, laptopToHoloLens_MB)

#_______________________________________________________________________________

def getWiresharkStats(wiresharkDump, holoLensName, startingTimeStamp, udpFilter = False):
    '''
    Returns 4 lists:
        holoLensToLaptop_timeStamps
        holoLensToLaptop_packets
        laptopToHoloLens_timeStamps
        laptopToHoloLens_packets

    '''
    '''
    Sample Wireshark Data
    "No.","Time","Source","Destination","Protocol","Length","Info"
    ...
    "17","2017-07-19 16:02:12.778552","10.X.XYZ.XYZ","10.X.XYZ.ABC","TLSv1.2","178","Application Data"
    "18","2017-07-19 16:02:12.801502","10.X.XYZ.ABC","10.X.XYZ.XYZ","TCP","54","443  >  55939 [ACK] Seq=226 Ack=477 Win=258 Len=0"
    ...
    '''
    # Initialize relevant variables
    if holoLensName == 'Chege':
        holoLensIPv4 = holoLensIPv4Chege
    elif holoLensName == 'Maria':
        holoLensIPv4 = holoLensIPv4Maria
    else:
        print("Invalid HoloLens name. Valid options: 'Chege', 'Maria'")
        return

    holoLensToLaptop_timeStamps = []
    holoLensToLaptop_packets = []
    laptopToHoloLens_timeStamps = []
    laptopToHoloLens_packets = []

    sent = 0
    received = 0

    with open(wiresharkDump) as myData:
        headerInfo = myData.readline()

        # Initialize helper variables
        prevTimeStampSent = startingTimeStamp
        prevTimeStampReceived = startingTimeStamp
        runningDataSumSent = 0
        runningDataSumReceived = 0
        TIME = 1
        SOURCE = 2
        DESTINATION = 3
        PROTOCOL = 4
        LENGTH = 5

        for line in myData:
            line = line.replace('"', '')    # Urgh, why did Wireshark do this?
            items = line.split(",")
            timeStamp = items[TIME].split('.')[0].split()[1]
            packets = int(items[LENGTH])

            # If specified, filter on the UDP protocol
            # System data uses TCP, but game data is sent over UDP
            if udpFilter:
                countThisItem = items[PROTOCOL] == 'UDP'
            else:
                countThisItem = True

            if items[SOURCE] == holoLensIPv4 and countThisItem:
                sent += packets
                if timeStamp == prevTimeStampSent:
                    runningDataSumSent += packets
                    # print(str(packets), end = " + ")
                else:
                    holoLensToLaptop_timeStamps.append(prevTimeStampSent)
                    holoLensToLaptop_packets.append(runningDataSumSent)
                    # print(prevTimeStampSent, str(runningDataSumSent))
                    prevTimeStampSent = timeStamp
                    runningDataSumSent = packets


            elif items[DESTINATION] == holoLensIPv4 and countThisItem:

                received += packets
                if timeStamp == prevTimeStampReceived:
                    runningDataSumReceived += packets
                else:
                    laptopToHoloLens_timeStamps.append(prevTimeStampReceived)
                    laptopToHoloLens_packets.append(runningDataSumReceived)
                    prevTimeStampReceived = timeStamp
                    runningDataSumReceived = packets

    # Communicate status to terminal
    print(  holoLensName, "\t: Sent {0:12,d} packets\t ".format(sent),
            "Received {0:12,d} packets".format(received)
    )
    return (holoLensToLaptop_timeStamps, holoLensToLaptop_packets, laptopToHoloLens_timeStamps, laptopToHoloLens_packets)

#_______________________________________________________________________________

def getHLPerformanceStats(hlConsoleDump, firstTimeStamp):
    '''
    Sample Data
    TimeStamp	CPULoad	DedicatedMemory	DedicatedMemoryUsed	SystemMemory	SystemMemoryUsed	EnginesUtilization
    2017-07-27 11:16:25.544534	34	119537664	81920	1028395008	59297792	[48.228125, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    '''

    with open(hlConsoleDump) as hlConsoleDump:
        headers = hlConsoleDump.readline()

        # Set up helper variables
        timeStamps = []
        cpuLoad = []
        dedicatedMemoryUsed = []
        systemMemoryUsed = []
        engineOne = []
        restOfEngines = [] # I think the other engines are never engaged...
        prevTimeStamp = firstTimeStamp

        cpuSum = 0
        dedicatedMemSum = 0
        systemMemSum = 0
        engineOneSum = 0
        restOfEnginesSum = 0
        itemsInThatSecond = 0

        # Too lazy to write this out, or pass thousands of parameters around
        # def incrementSums(items):
        #     global cpuSum
        #     global dedicatedMemSum
        #     global systemMemSum
        #     global engineOneSum
        #     global restOfEnginesSum
        #     global itemsInThatSecond
        #
        #     itemsInThatSecond += 1
        #     cpuSum += int(items[1])
        #     dedicatedMemSum += int(items[3])
        #     systemMemSum += int(items[5])
        #     engineOneSum += float(items[5][0])
        #     restOfEnginesSum += float(items[5][1])

        for line in hlConsoleDump:
            items = line.split('\t')
            currentTimeStamp = items[0].split('.')[0].split()[1]

            # Aggregate all the data points in a given second
            if currentTimeStamp == prevTimeStamp:
                # incrementSums(items)
                itemsInThatSecond += 1
                cpuSum += int(items[1])
                dedicatedMemSum += int(items[3])
                systemMemSum += int(items[5])
                engineOneSum += float(items[5][0])
                restOfEnginesSum += float(items[5][1])

            else:
                # Append the averages to the tuples
                timeStamps.append(prevTimeStamp)
                cpuLoad.append(cpuSum / itemsInThatSecond)
                dedicatedMemoryUsed.append(dedicatedMemSum / itemsInThatSecond)
                systemMemoryUsed.append(systemMemSum / itemsInThatSecond)
                engineOne.append(engineOneSum / itemsInThatSecond)
                restOfEngines.append(restOfEnginesSum / itemsInThatSecond)
                # print(prevTimeStamp, str(cpuSum / itemsInThatSecond))
                # Reset the variables
                cpuSum, dedicatedMemSum, systemMemSum, engineOneSum = (0, 0, 0, 0)
                restOfEnginesSum, itemsInThatSecond = (0, 0)

                prevTimeStamp = currentTimeStamp

                # Restart the process
                # incrementSums(items)
                itemsInThatSecond += 1
                cpuSum += int(items[1])
                dedicatedMemSum += int(items[3])
                systemMemSum += int(items[5])
                engineOneSum += float(items[5][0])
                restOfEnginesSum += float(items[5][1])

    print("Successfully extracted", str(len(timeStamps)), "seconds of hololens data")
    return timeStamps, cpuLoad, dedicatedMemoryUsed, systemMemoryUsed, engineOne, restOfEngines

#_______________________________________________________________________________

def compareDataOnGraph(title, plotData, xyLabels, usesTimeStamps = False):
    '''
    Plots multiple graphs on the same figure
    'title' is a string which will be set as the graph's title
    plotdata is a list of tuples of the form (time(list), values(list), label(string))
    '''

    # timeOne, valuesDataSetOne = np.loadtxt(dataSetOne, unpack = True,
    #                             converters = )
    # wdp gives date-time as 07/19/2017-16:02:20.2227616 while
    # Wireshark gives 2017-07-19 16:02:02.739335
    # Numpy only works with formats like 2010-10-17 07:15:30. Microsoft, why??
    # ...
    # (07/19/2017-16:02:20.2227616, 45)
    # ...
    # (2017-07-19 16:02:02.739335, 12)

    plt.figure(1)
    plt.grid(True)
    plt.xlabel(xyLabels[0])
    plt.ylabel(xyLabels[1])
    plt.title(title)
    formatSrings = ['b', 'r', 'c', 'm', 'g']

    index = 0
    for dataset in plotData:
        if usesTimeStamps:
            timeData = pd.to_datetime(dataset[0])
            plt.plot_date( x = timeData, y = dataset[1],
                           fmt = formatSrings[index % len(formatSrings)],
                           label = dataset[2])
        else:
            plt.plot( dataset[0], dataset[1],
                      color = formatSrings[index % len(formatSrings)],
                      label = dataset[2])
        index += 1

    plt.legend(loc = 'best')
    plt.show()

#_______________________________________________________________________________

def getRange(timeStampsArray):
    # print(list(range(1, len(timeStampsArray) + 1)))
    return list(range(0, len(timeStampsArray) + 0))

def getCumSum(arrayOfValues):
    cumSumArray = []
    cumsum = 0
    for i in range(len(arrayOfValues)):
        cumsum += arrayOfValues[i]
        cumSumArray.append(cumsum)
    # print(cumSumArray)
    return cumSumArray

def main():
    # wiresharkStats ==> hlToLap_timeStamps, hlToLap_packets, lapToHl_timeStamps, lapToHls_packets
    # hlPerfStats ==> timeStamps, cpuLoad, dedicatedMemoryUsed, systemMemoryUsed, engineOne, restOfEngines
    chegeData12kI = getWiresharkStats(data['12kInts_data'][0], 'Chege', data['30ints_data'][1])
    chegeData12kIUDP = getWiresharkStats(data['12kInts_data'][0], 'Chege', data['10vectors_data'][1], udpFilter = True)

    plotData = [
        (getRange(chegeData12kI[0]), getCumSum(chegeData12kI[1]), "HL to Laptop: All Protocols, 12k ints per sec"),
        (getRange(chegeData12kIUDP[0]), getCumSum(chegeData12kIUDP[1]), "HL to Laptop: UDP Protocol, 12k ints per sec")
    ]
    xyLabels = ['Time in Seconds', 'Cumulative Sum of Packets Transferred']
    compareDataOnGraph("Comparing General Data to UDP Protocol Data", plotData, xyLabels)

#_______________________________________________________________________________

if __name__ == "__main__":
    main()
#_______________________________________________________________________________
