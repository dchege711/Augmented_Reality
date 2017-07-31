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

def getWiresharkStats(wiresharkDump, holoLensName, startingTimeStamp):
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
        LENGTH = 5

        for line in myData:
            line = line.replace('"', '')    # Urgh, why did Wireshark do this?
            items = line.split(",")
            timeStamp = items[TIME].split('.')[0].split()[1]
            packets = int(items[LENGTH])

            if items[SOURCE] == holoLensIPv4:
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


            elif items[DESTINATION] == holoLensIPv4:

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
    chegeWireshark10v = getWiresharkStats('Chege_Maria_Wireshark_07311256_10vectors.csv', 'Chege', '12:53:27')
    chegeWireshark20v = getWiresharkStats('Chege_Maria_Wireshark_07311427_20vectors.csv', 'Chege', '14:24:09')
    chegeWireshark30i = getWiresharkStats('Chege_Maria_Wireshark_07311544_30ints.csv', 'Chege', '15:39:04')
    mariaWireshark30i = getWiresharkStats('Chege_Maria_Wireshark_07311544_30ints.csv', 'Maria', '15:39:04')
    # mariaWireshark = getWiresharkStats('Chege_Maria_Wireshark_07311256.csv', 'Maria', '12:53:27')
    # chegeHLStats = getHLPerformanceStats('Chege_07-31-12_53_HL_Performance.txt', '12:53:39')
    # mariaHLStats = getHLPerformanceStats('Maria_07-31-12_53_HL_Performance.txt', '12:53:42')
    plotData = [
        (getRange(chegeWireshark10v[0]), getCumSum(chegeWireshark10v[1]), "Chege HL to Laptop (10 vectors per sec)"),
        (getRange(chegeWireshark30i[0]), getCumSum(chegeWireshark30i[1]), "Chege HL to Laptop (30 ints per sec)"),
        (getRange(chegeWireshark20v[0]), getCumSum(chegeWireshark20v[1]), "Chege HL to Laptop (20 vectors per sec)")
        # (getRange(mariaWireshark30i[2]), getCumSum(mariaWireshark30i[3]), "Laptop to Maria HL Packets (30 ints every second)")
    ]
    xyLabels = ['Time in Seconds', 'Cumulative Sum of Packets Transferred']
    compareDataOnGraph("Stats", plotData, xyLabels)

#_______________________________________________________________________________

if __name__ == "__main__":
    main()
#_______________________________________________________________________________
