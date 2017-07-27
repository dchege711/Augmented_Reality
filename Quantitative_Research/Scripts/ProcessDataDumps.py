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
holoLensIPv4 = os.environ['HL_CHEGE_IPV4']

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

def getWiresharkStats(wiresharkDump):
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
    holoLensToLaptop_timeStamps = []
    holoLensToLaptop_packets = []
    laptopToHoloLens_timeStamps = []
    laptopToHoloLens_packets = []

    sent = 0
    received = 0

    with open(wiresharkDump) as myData:
        headerInfo = myData.readline()

        # Initialize helper variables
        prevTimeStampSent = "2017-07-19 16:02:02"
        prevTimeStampReceived = "2017-07-19 16:02:02"
        runningDataSumSent = 0
        runningDataSumReceived = 0
        TIME = 1
        SOURCE = 2
        DESTINATION = 3
        LENGTH = 5

        for line in myData:
            line = line.replace('"', '')    # Urgh, why did Wireshark do this?
            items = line.split(",")
            timeStamp = items[TIME].split('.')[0]
            packets = int(items[LENGTH])

            if items[SOURCE] == holoLensIPv4:
                sent += packets
                if timeStamp == prevTimeStampSent:
                    runningDataSumSent += packets
                    # print(str(packets), end = " + ")
                else:
                    holoLensToLaptop_timeStamps.append(prevTimeStampSent)
                    holoLensToLaptop_packets.append(runningDataSumSent)
                    prevTimeStampSent = timeStamp
                    runningDataSumSent = packets
                    print(timeStamp, str(packets))


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
    print(  "Sent {0:.2f} packets".format(sent),
            ", received {0:.2f} packets".format(received),
            ", total = {0:.2f} packets".format((sent+received))
    )
    print("\nSent Array Length", str(len(holoLensToLaptop_timeStamps)), "/", str(len(holoLensToLaptop_packets)))
    print("\nReceived Array Length", str(len(laptopToHoloLens_timeStamps)), "/", str(len(laptopToHoloLens_packets)))

    return (holoLensToLaptop_timeStamps, holoLensToLaptop_packets, laptopToHoloLens_timeStamps, laptopToHoloLens_packets)

#_______________________________________________________________________________

def getHLPerformanceStats(hlConsoleDump):
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
        prevTimeStamp = "11:16:23" # Should be the first timestamp in the file

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

    print(str(len(timeStamps)), "time stamps,", str(len(cpuLoad)), "CPU measurements.")
    return timeStamps, cpuLoad, dedicatedMemoryUsed, systemMemoryUsed, engineOne, restOfEngines


#_______________________________________________________________________________

def compareDataOnGraph(title, plotData):
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
    plt.xlabel('Time')
    # plt.ylabel('Rate of Data Transfer (packets))')
    plt.title(title)
    formatSrings = ['b-', 'r-', 'c-', 'm-', 'g-', 'b-']

    index = 0
    for dataset in plotData:
        timeData = pd.to_datetime(dataset[0])
        plt.plot_date(x = timeData, y = dataset[1],
                      fmt = formatSrings[index % len(formatSrings)],
                      label = dataset[2])
        index += 1

    plt.legend(loc = 'best')
    plt.show()

#_______________________________________________________________________________

def main():
    # wdpStats = getWDPStats('Origami_Windows_Device_Portal.csv')
    # wiresharkStats = getWiresharkStats('Chege_Maria_Wireshark_07271121.csv')
    hololensStats = getHLPerformanceStats('Chege_07-27-11_16_HL_Performance.txt')
    plotData = [
        (hololensStats[0], hololensStats[1], "CPU Load"),
        (hololensStats[0], hololensStats[4], "Engine One")
    ]
    compareDataOnGraph("HoloLens Performance Stats", plotData)

#_______________________________________________________________________________

if __name__ == "__main__":
    main()
#_______________________________________________________________________________
