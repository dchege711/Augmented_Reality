import psutil	# install using "pip install psutil"
import time
from collections import namedtuple
import sys

holoLensIPv4 = '10.8.113.245'	# The IPv4 address used by Unity to connect to the HoloLens

def getProcessID():
	'''
	Shows my processes and corresponding process id's.
	Helps me identify process id's for programs of interest, e.g. Unity.exe
	The process id isn't fixed, if you close and reopen a program, it may have changed.
	'''
	for proc in psutil.process_iter():
		if proc.name() == 'Unity.exe':
			return (proc.pid)

	# If the application isn't running, return -1
	return -1

def wiFiStats():
	'''
	Returns a namedtuple object with the fields:
	('bytesSent', 'packetsSent', 'bytesReceived', 'packetsReceived')
	'''
	myNetworkStats = psutil.net_io_counters(pernic = True)
	bytesSent = myNetworkStats["Wi-Fi"].bytes_sent
	packetsSent = myNetworkStats["Wi-Fi"].packets_sent
	bytesReceived = myNetworkStats["Wi-Fi"].bytes_recv
	packetsReceived = myNetworkStats["Wi-Fi"].packets_recv

	myWiFiStats = namedtuple('wiFiStats', ['bytesSent', 'packetsSent', 'bytesReceived', 'packetsReceived'])
	return myWiFiStats(bytesSent, packetsSent, bytesReceived, packetsReceived)

def netWiFiStats(initialStats, currentStats):
	# myWiFiStats returns a tuple
	megaBytesSent = (currentStats.bytesSent - initialStats.bytesSent)/(1024 * 1024)
	megaBytesReceived = (currentStats.bytesReceived - initialStats.bytesReceived)/(1024 * 1024)
	totalPacketsSent = (currentStats.packetsSent - initialStats.packetsSent)
	totalPacketsReceived = (currentStats.packetsReceived - initialStats.packetsReceived)

	myNetWiFiStats = namedtuple('wiFiStats', ['bytesSent', 'packetsSent', 'bytesReceived', 'packetsReceived'])
	return myNetWiFiStats(megaBytesSent, totalPacketsSent, megaBytesReceived, totalPacketsReceived)

def printNetworkStats(megabytesSent, packetsSent, megabytesReceived, packetsReceived):
	print("_________\n")
	print("Wi-Fi Stats...")
	print("Sent\t\t: %6.2f MB," %megabytesSent, packetsSent, "packets")
	print("Received\t: %6.2f MB," %megabytesReceived, packetsReceived, "packets")
	print("_________")

def myProgramStats(programName):
	'''
	Explores the resources being used by a given program (process)
	cpu_percent, is_running()
	'''
	print("_________")
	processID = getProcessID(programName)
	p = psutil.Process(processID)
	processCreationTime = p.creation_time()
	print("Getting data for", p.name(), "...\n")
	print("IPv4 and IPv6 Connections...")
	for connection in p.connections(kind = 'inet'):
		print(connection)

def exportAsTextFile(dataPoints):
	outputFile = open('HoloLensOrigami.txt', 'w')

	headerInfo = dataPoints[0]._fields
	numOfItems = len(headerInfo)
	i = 0
	for header in headerInfo:
		if i < numOfItems - 1:
			outputFile.write(header + "\t")
		else:
			outputFile.write(header + "\n")

	for myNamedTuple in dataPoints:
		i = 0
		for data in myNamedTuple:
			if i < numOfItems - 1:
				outputFile.write(str(data) + "\t")
			else:
				outputFile.write(str(data) + "\n")
			i += 1

def main(numberOfDataPoints, interval):
	dataPoints = []
	# Set a reference point
	initialStats = wiFiStats()

	# Get 2 reference points to check for background noise
	time.sleep(interval)
	dataPoints.append(netWiFiStats(initialStats, wiFiStats()))
	time.sleep(interval)
	dataPoints.append(netWiFiStats(initialStats, wiFiStats()))
	time.sleep(interval)
	dataPointsSoFar = 2
	print("\nNow connect to the HoloLens!\n")

	while (dataPointsSoFar < numberOfDataPoints - 2):
		dataPoints.append(netWiFiStats(initialStats, wiFiStats()))
		time.sleep(interval)
		dataPointsSoFar += 1
		# print(netWiFiStats(initialStats, wiFiStats()))
		print(dataPointsSoFar)

	# Get 3 reference points at the end
	print("\nDisconnect the HoloLens\n")
	dataPoints.append(netWiFiStats(initialStats, wiFiStats()))
	time.sleep(interval)
	dataPoints.append(netWiFiStats(initialStats, wiFiStats()))
	time.sleep(interval)
	dataPoints.append(netWiFiStats(initialStats, wiFiStats()))

	exportAsTextFile(dataPoints)
	print("\nCoolio! We're done.")

if __name__ == "__main__":
	intervalInSeconds = 3
	numberOfReadings = 50
	main(numberOfReadings, intervalInSeconds)
