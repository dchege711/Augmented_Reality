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
    'noData_data'       : [dataPath + '08-02-10_51_19_Wireshark_noData.csv', '10:51:19'],
    'noData_Chege'      : [dataPath + '08-02-10_51_28_HL_Performance_Chege_noData.txt', '10:51:28'],
    'noData_Maria'      : [dataPath + '08-02-10_51_25_HL_Performance_Maria_noData.txt', '10:51:25'],
    '4kVectors_data'    : [dataPath + '08-03-11_45_57_Wireshark_4kVectors.csv', '11:45:57'],
    '4kVectors_Chege'   : [dataPath + '08-03-11_46_11_HL_Performance_Chege_4kVectors.txt', '11:46:11'],
    '4kVectors_Maria'   : [dataPath + '08-03-11_46_08_HL_Performance_Maria_4kVectors.txt', '11:46:08'],
    '8kVectors_data'    : [dataPath + '08-03-12_11_55_Wireshark_8kVectors.csv', '12:11:55'],
    '8kVectors_Chege'   : [dataPath + '08-03-12_12_01_HL_Performance_Chege_8kVectors.txt', '12:12:01'],
    '8kVectors_Maria'   : [dataPath + '08-03-12_11_58_HL_Performance_Maria_8kVectors.txt', '12:11:58'],
    '12kInts_data'      : [dataPath + '08-03-13_09_43_Wireshark_12kInts.csv', '13:09:43'],
    '12kInts_Chege'     : [dataPath + '08-03-13_09_50_HL_Performance_Chege_12kInts.txt', '13:09:50'],
    '12kInts_Maria'     : [dataPath + '08-03-13_09_43_HL_Performance_Maria_12kInts.txt', '13:09:43'],
    'fragments_Maria'   : [dataPath + '08-03-11_03_07_HL_Performance_Maria_Fragments.txt', '11:03:07']
}

bytesInKB = 1024.0

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
                    holoLensToLaptop_MB.append(runningDataSumSent / (bytesInKB * bytesInKB))
                    sent += runningDataSumSent / (bytesInKB * bytesInKB)
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
                    laptopToHoloLens_MB.append(runningDataSumReceived / (bytesInKB * bytesInKB))
                    received += runningDataSumReceived / (bytesInKB * bytesInKB)
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

def getWiresharkStats(label, wiresharkDump, holoLensName, startingTimeStamp):
    '''
    Returns 4 lists:
        holoLensToLaptop_timeStamps
        holoLensToLaptop_MB
        laptopToHoloLens_timeStamps
        laptopToHoloLens_MB

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
    holoLensToLaptop_MB = []
    holoLensToLaptop_Protocols = {}
    laptopToHoloLens_timeStamps = []
    laptopToHoloLens_MB = []
    laptopToHoloLens_Protocols = {}

    sent = 0
    received = 0

    with open(wiresharkDump) as myData:
        headerInfo = myData.readline()

        # Initialize helper variables
        prevTimeStampSent = startingTimeStamp
        prevTimeStampReceived = startingTimeStamp
        runningDataSumSent = 0
        runningProtocolSumSent = {}
        runningDataSumReceived = 0
        runningProtocolSumRecvd = {}

        # Indexes of the data that we get from Wireshark
        TIME = 1
        SOURCE = 2
        DESTINATION = 3
        PROTOCOL = 4
        LENGTH = 5

        for line in myData:
            line = line.replace('"', '')    # Urgh, why did Wireshark do this?
            items = line.split(",")
            timeStamp = items[TIME].split('.')[0].split()[1] # Get time only up to the seconds
            numOfBytes = int(items[LENGTH])

            if items[SOURCE] == holoLensIPv4:
                # Keep track of the data count.
                sent += numOfBytes
                protocol = items[PROTOCOL]

                # Create timeStamp and data slots if it's a newly observed protocol
                if protocol not in holoLensToLaptop_Protocols:
                    holoLensToLaptop_Protocols[protocol] = ([], [])
                    runningProtocolSumSent[protocol] = 0

                # If we're still within the same second, aggregate the data
                if timeStamp == prevTimeStampSent:
                    runningDataSumSent += numOfBytes
                    runningProtocolSumSent[protocol] += numOfBytes

                # Otherwise, save the aggregated data for the last elapsed second
                else:
                    holoLensToLaptop_timeStamps.append(prevTimeStampSent)
                    holoLensToLaptop_MB.append(runningDataSumSent / (bytesInKB * bytesInKB))

                    # Note down all the sums of the data sent per protocol and reset count
                    for protocol in holoLensToLaptop_Protocols:
                        holoLensToLaptop_Protocols[protocol][0].append(prevTimeStampSent)
                        holoLensToLaptop_Protocols[protocol][1].append(runningProtocolSumSent[protocol] / (bytesInKB * bytesInKB))
                        # Reset the counter
                        runningProtocolSumSent[protocol] = numOfBytes

                    # Reset the counter variables
                    prevTimeStampSent = timeStamp
                    runningDataSumSent = numOfBytes

            elif items[DESTINATION] == holoLensIPv4:

                received += numOfBytes
                protocol = items[PROTOCOL]

                # Create timeStamp and data slots if it's a newly observed protocol
                if protocol not in laptopToHoloLens_Protocols:
                    laptopToHoloLens_Protocols[protocol] = [], []
                    runningProtocolSumRecvd[protocol] = 0
                    # print("New :", protocol, "\nContent :", laptopToHoloLens_Protocols[protocol])

                # If we're still within the same second, aggregate the data
                if timeStamp == prevTimeStampReceived:
                    runningDataSumReceived += numOfBytes
                    runningProtocolSumRecvd[protocol] = numOfBytes

                # Otherwise, save the aggregated data for the last elapsed second
                else:
                    laptopToHoloLens_timeStamps.append(prevTimeStampReceived)
                    laptopToHoloLens_MB.append(runningDataSumReceived / (bytesInKB * bytesInKB))

                    # Note down all the sums of the data received per protocol and reset count
                    for protocol in laptopToHoloLens_Protocols:
                        laptopToHoloLens_Protocols[protocol][0].append(prevTimeStampReceived)
                        laptopToHoloLens_Protocols[protocol][1].append(runningProtocolSumRecvd[protocol] / (bytesInKB * bytesInKB))
                        # Reset the counter
                        runningProtocolSumRecvd[protocol] = numOfBytes

                    prevTimeStampReceived = timeStamp
                    runningDataSumReceived = numOfBytes

    # Communicate status to terminal
    print(  "{0:18}".format(label) + "{0:8}".format(holoLensName),
            "Sent : {0:6,.2f} MB".format(sent/ (bytesInKB * bytesInKB)), "({0:3d} sec)  ".format(len(holoLensToLaptop_timeStamps)),
            "Received : {0:6,.2f} MB".format(received/ (bytesInKB * bytesInKB)), "({0:3d} sec)".format(len(laptopToHoloLens_timeStamps))
    )
    return (holoLensToLaptop_timeStamps, holoLensToLaptop_MB, holoLensToLaptop_Protocols,
            laptopToHoloLens_timeStamps, laptopToHoloLens_MB, laptopToHoloLens_Protocols)

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

def getRange(incomingList):
    '''
    Makes an incremental list [0, 1, 2, 3, ...] equal to the length of the
    list passed along as a parameter.
    '''
    return list(range(0, len(incomingList)))

def getCumSum(listOfValues):
    '''
    Given a list of values, this method returns a list in which the value
    at index i is the cumulative sum of all values from 0 to i, inclusive.
    '''
    cumSumArray = []
    cumsum = 0
    for i in range(len(listOfValues)):
        cumsum += listOfValues[i]
        cumSumArray.append(cumsum)
    return cumSumArray

def queryWiresharkStats(keyName, holoLensName, usesTimeStamps = False):
    '''
    I was too lazy to re-type the method names each time...
    '''
    return getWiresharkStats(keyName, data[keyName][0], holoLensName, data[keyName][1])

#_______________________________________________________________________________

def main():
    # wiresharkStats ==> hlToLap_timeStamps, hlToLap_packets, hlToLap_protocols,
    #                    lapToHl_timeStamps, lapToHl_packets, lapToHl_protocols
    # hlPerfStats ==> timeStamps, cpuLoad, dedicatedMemoryUsed, systemMemoryUsed, engineOne, restOfEngines
    # noDataChege = queryWiresharkStats('noData_data', 'Chege')
    # noDataMaria = queryWiresharkStats('noData_data', 'Maria')
    # chegeData4kV = queryWiresharkStats('4kVectors_data', 'Chege')
    # mariaData4kV = queryWiresharkStats('4kVectors_data', 'Maria')
    # chegeData8kV = queryWiresharkStats('8kVectors_data', 'Chege')
    # mariaData8kV = queryWiresharkStats('8kVectors_data', 'Maria')
    chegeData12kI = queryWiresharkStats('12kInts_data', 'Chege')
    # mariaData12kI = queryWiresharkStats('12kInts_data', 'Maria')

    plotProtocolData = []
    for protocol in chegeData12kI[2]:
        cumulativeData = getCumSum(chegeData12kI[2][protocol][1])
        print("Total under", protocol, " :", cumulativeData[-1])
        plotProtocolData.append((
            chegeData12kI[2][protocol][0],      # Time stamps
            cumulativeData,                     # Cumulative data in MBs
            "Chege to Laptop: " + protocol      # Label showing type of protocol
        ))

    # plotData = [
    #     (getRange(chegeData12kI[0]), getCumSum(chegeData12kI[1]), "Chege to Laptop : All Protocols, 12k ints per sec"),
    #     (getRange(chegeData12kI[3]), getCumSum(chegeData12kI[4]), "Laptop to Chege : All Protocols, 12k ints per sec"),
    #     (getRange(mariaData12kI[0]), getCumSum(mariaData12kI[1]), "Maria to Laptop : All Protocols, 12k ints per sec"),
    #     (getRange(mariaData12kI[3]), getCumSum(mariaData12kI[4]), "Laptop to Maria : All Protocols, 12k ints per sec")
    # ]

    xyLabels = ['Time', 'Cumulative Data Transferred in MB']
    compareDataOnGraph("Comparing Data Transfer by Protocol", plotProtocolData, xyLabels, usesTimeStamps = True)

#_______________________________________________________________________________

if __name__ == "__main__":
    main()
#_______________________________________________________________________________
