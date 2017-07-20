'''
Processes CSV data produced by different sources.
'''
#_______________________________________________________________________________

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import re

#_______________________________________________________________________________

# Useful IP Addresses
laptopIPv4 = "10.8.227.69"
holoLensIPv4 = "10.8.113.245"

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
    07/19/2017-16:02:12.9536544,Microsoft-Windows-Kernel-Network,11,Keyword:9223372036854776000,Level:4,Message:TCPv4: 124 bytes received from 10.8.113.245:443 to 10.8.227.69:55939. ,PID:4,ProviderName:Microsoft-Windows-Kernel-Network,TaskName:KERNEL_NETWORK_TASK_TCPIP,connid:0,daddr:10.8.227.69,dport:55939,saddr:10.8.113.245,seqnum:0,size:124,sport:443,WebbCompletePayload:message:tcpv4: 124 bytes received from 10.8.113.245:443 to 10.8.227.69:55939. , pid:4, connid:0, daddr:10.8.227.69, dport:55939, saddr:10.8.113.245, seqnum:0, size:124, sport:443,
    07/19/2017-16:02:12.9595648,Microsoft-Windows-Kernel-Network,10,Keyword:9223372036854776000,Level:4,Message:TCPv4: 143 bytes transmitted from 10.8.113.245:443 to 10.8.227.69:55939. ,PID:4,ProviderName:Microsoft-Windows-Kernel-Network,TaskName:KERNEL_NETWORK_TASK_TCPIP,connid:0,daddr:10.8.227.69,dport:55939,endtime:931204,saddr:10.8.113.245,seqnum:0,size:143,sport:443,startime:931204,WebbCompletePayload:message:tcpv4: 143 bytes transmitted from 10.8.113.245:443 to 10.8.227.69:55939. , pid:4, connid:0, daddr:10.8.227.69, dport:55939, endtime:931204, saddr:10.8.113.245, seqnum:0, size:143, sport:443, startime:931204,
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
    "17","2017-07-19 16:02:12.778552","10.8.227.69","10.8.113.245","TLSv1.2","178","Application Data"
    "18","2017-07-19 16:02:12.801502","10.8.113.245","10.8.227.69","TCP","54","443  >  55939 [ACK] Seq=226 Ack=477 Win=258 Len=0"
    ...
    '''
    # Initialize relevant variables
    holoLensToLaptop_timeStamps = []
    holoLensToLaptop_megapackets = []
    laptopToHoloLens_timeStamps = []
    laptopToHoloLens_megapackets = []

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
            megaPackets = float(items[LENGTH]) / 1000000

            if items[SOURCE] == holoLensIPv4:
                sent += megaPackets
                if timeStamp == prevTimeStampSent:
                    runningDataSumSent += megaPackets
                else:
                    holoLensToLaptop_timeStamps.append(prevTimeStampSent)
                    holoLensToLaptop_megapackets.append(runningDataSumSent)
                    prevTimeStampSent = timeStamp
                    runningDataSumSent = megaPackets


            elif items[DESTINATION] == holoLensIPv4:

                received += megaPackets
                if timeStamp == prevTimeStampReceived:
                    runningDataSumReceived += megaPackets
                else:
                    laptopToHoloLens_timeStamps.append(prevTimeStampReceived)
                    laptopToHoloLens_megapackets.append(runningDataSumReceived)
                    prevTimeStampReceived = timeStamp
                    runningDataSumReceived = megaPackets

    # Communicate status to terminal
    print(  "Sent {0:.2f} megapackets".format(sent),
            ", received {0:.2f} megapackets".format(received),
            ", total = {0:.2f} megapackets".format((sent+received))
    )
    print("\nSent Array Length", str(len(holoLensToLaptop_timeStamps)), "/", str(len(holoLensToLaptop_megapackets)))
    print("\nReceived Array Length", str(len(laptopToHoloLens_timeStamps)), "/", str(len(laptopToHoloLens_megapackets)))

    return (holoLensToLaptop_timeStamps, holoLensToLaptop_megapackets, laptopToHoloLens_timeStamps, laptopToHoloLens_megapackets)

#_______________________________________________________________________________

def compareDataOnGraph(titleAndLabels, datasetOneTime, dataSetOneData, datasetTwoTime, datasetTwoData):

    # timeOne, valuesDataSetOne = np.loadtxt(dataSetOne, unpack = True,
    #                             converters = )
    # wdp gives date-time as 07/19/2017-16:02:20.2227616 while
    # Wireshark gives 2017-07-19 16:02:02.739335
    # Numpy only works with formats like 2010-10-17 07:15:30. Microsoft, why??
    # ...
    # (07/19/2017-16:02:20.2227616, 45)
    # ...
    # (2017-07-19 16:02:02.739335, 12)

    # The simple case. Each separately
    timeOne = pd.to_datetime(datasetOneTime)
    timeTwo = pd.to_datetime(datasetTwoTime)

    plt.figure(1)
    plt.grid(True)
    plt.xlabel('Time')
    plt.ylabel('Rate of Data Transfer (Megapackets))')
    plt.title(titleAndLabels[0])
    plt.plot_date(x = timeOne, y = dataSetOneData, fmt = 'r-', label = titleAndLabels[1])
    plt.plot_date(x = timeTwo, y = datasetTwoData, fmt = 'b-', label = titleAndLabels[2])
    plt.legend(loc = 'best')
    plt.show()

#_______________________________________________________________________________

def main():
    wdpStats = getWDPStats('Origami_Windows_Device_Portal.csv')
    wiresharkStats = getWiresharkStats('Origami_Wireshark.csv')
    titleAndLabels = [  'Data Transfer by the Origami App',
                        'HoloLens to Laptop',
                        'Laptop to HoloLens'
    ]
    compareDataOnGraph(titleAndLabels, wiresharkStats[0], wiresharkStats[1], wiresharkStats[2], wiresharkStats[3])

#_______________________________________________________________________________

if __name__ == "__main__":
    main()
#_______________________________________________________________________________
