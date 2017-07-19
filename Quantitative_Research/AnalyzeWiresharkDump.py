'''
Reads and analyzes CSV data produced by Wireshark
First delete all " " from the CSV file. It's easier that way.
'''
# Useful IP Addresses
laptopIPv4 = "10.8.227.69"
holoLensIPv4 = "10.8.113.245"

# Indexes for accessing the Wireshark CSV data
NUMBER = 0
TIME = 1
SOURCE = 2
DESTINATION = 3
PROTOCOL = 4
LENGTH = 5
INFO = 6

with open('spacemanPackets') as myData:
    packetsSent = 0
    packetsReceived = 0

    headerInfo = myData.readline().split(",")

    for line in myData:
        line = line.replace('"', '')
        items = line.split(",")
        # print(items[SOURCE], "!=", holoLensIPv4)
        if items[SOURCE] == holoLensIPv4:
            packetsReceived += int(items[LENGTH])
        elif items[DESTINATION] == holoLensIPv4:
            packetsSent += int(items[LENGTH])

    print("Received", str(packetsReceived), "\tSent", str(packetsSent))
