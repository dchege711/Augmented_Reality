'''
Processes CSV data produced by different sources.
'''
#_______________________________________________________________________________

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

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

    # Initialize relevant variables
    holoLensToLaptop_timeStamps = []
    holoLensToLaptop_bytes = []
    laptopToHoloLens_timeStamps = []
    laptopToHoloLens_bytes = []

    with open(wdpDump) as myData:
        headerInfo = myData.readline()

        for line in myData:
            items = line.split(',')
            timeStamp = items[0]

            # We tested if the position of the message and its format is consistent
            # 'Message...' is always on index 5, but the content is not uniform
            # Instead of multiple if-statements, we'll do entire scans of the line

            # Look for the relevant strings
            for i in range(len(items)):
                labelAndItem = items[i].split(':')
                # Extract the destination address
                if labelAndItem[0] == 'daddr':
                    destAddress = labelAndItem[1]
                # Extract the sending address
                if labelAndItem[0] == 'saddr':
                    senderAddress = labelAndItem[1]
                # Extract the number of bytes transferred
                if labelAndItem[0] == 'size':
                    numberOfBytes = labelAndItem[1]

            # Update the holoLensToLaptop list
            if destAddress == laptopIPv4:
                # holoLensToLaptop.append((timeStamp, numberOfBytes))
                holoLensToLaptop_timeStamps.append(timeStamp)
                holoLensToLaptop_bytes.append(numberOfBytes)
            # Update the laptopToHoloLens list
            elif senderAddress == laptopIPv4:
                # laptopToHoloLens.append((timeStamp, numberOfBytes))
                laptopToHoloLens_timeStamps.append(timeStamp)
                laptopToHoloLens_bytes.append(numberOfBytes)

    # Communicate status to terminal and return the results
    # print(str(len(holoLensToLaptop)), "to laptop,", str(len(laptopToHoloLens)), "from laptop")
    return (holoLensToLaptop_timeStamps, holoLensToLaptop_bytes, laptopToHoloLens_timeStamps, laptopToHoloLens_bytes)

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
    # Indexes for accessing the Wireshark CSV data
    NUMBER = 0
    TIME = 1
    SOURCE = 2
    DESTINATION = 3
    PROTOCOL = 4
    LENGTH = 5
    INFO = 6

    # Initialize relevant variables
    holoLensToLaptop_timeStamps = []
    holoLensToLaptop_packets = []
    laptopToHoloLens_timeStamps = []
    laptopToHoloLens_packets = []

    with open(wiresharkDump) as myData:
        headerInfo = myData.readline()

        for line in myData:
            line = line.replace('"', '')    # Urgh, why did Wireshark do this?
            items = line.split(",")
            timeStamp = items[TIME]
            if items[SOURCE] == holoLensIPv4:
                # holoLensToLaptop.append((timeStamp, items[LENGTH]))
                holoLensToLaptop_timeStamps.append(timeStamp)
                holoLensToLaptop_packets.append(items[LENGTH])
            elif items[DESTINATION] == holoLensIPv4:
                # laptopToHoloLens.append((timeStamp, items[LENGTH]))
                laptopToHoloLens_timeStamps.append(timeStamp)
                laptopToHoloLens_packets.append(items[LENGTH])

    # Communicate status to terminal and return the results
    # print(str(len(holoLensToLaptop)), "to laptop,", str(len(laptopToHoloLens)), "from laptop")
    return (holoLensToLaptop_timeStamps, holoLensToLaptop_packets, laptopToHoloLens_timeStamps, laptopToHoloLens_packets)

#_______________________________________________________________________________

def compareDataOnGraph(title, datasetOneTime, dataSetOneData, datasetTwoTime, datasetTwoData):

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
    plt.plot_date(x = timeOne, y = dataSetOneData, fmt = 'r:')
    plt.show()

    plt.figure(2)
    plt.plot_date(x = timeTwo, y = datasetTwoData, fmt = 'b:')
    plt.show()

#_______________________________________________________________________________

def main():
    wdpStats = getWDPStats('Origami_Windows_Device_Portal.csv')
    wiresharkStats = getWiresharkStats('Origami_Wireshark.csv')
    compareDataOnGraph("Nah!", wiresharkStats[0], wiresharkStats[1], wdpStats[0], wdpStats[1])

#_______________________________________________________________________________

if __name__ == "__main__":
    main()
#_______________________________________________________________________________
