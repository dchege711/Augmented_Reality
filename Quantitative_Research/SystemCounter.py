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
	outputFile = open('StationaryCube.txt', 'w')

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

def getNDataPoints(numberOfMeasurements):
	# From timeTheOperation(), the average time per iteration is 0.018 sec (N was 10,000)
	# We can therefore set an interval of ~ 0.982 sec to get data per second
	# We confirmed this delay empirically
	intervalInSeconds = 0.995
	i = 0
	dataPoints = []
	previousStats = wiFiStats()
	while (i < numberOfMeasurements):
		time.sleep(intervalInSeconds)
		currentStats = wiFiStats()
		dataPoints.append(netWiFiStats(previousStats, currentStats))
		previousStats = currentStats
		print(i)
		i += 1
	return dataPoints

def main(numberOfDataPoints):
	startTime = time.time()
	# Get 10 reference points to check for background noise
	first10 = getNDataPoints(10)
	print("\nNow connect to the HoloLens!\n")
	# Get many measurements while HoloLens is connected
	middleBunch = getNDataPoints(numberOfDataPoints - 30)
	# Get 20 reference points at the end of the experiment
	print("\nDisconnect the HoloLens!\n")
	last20 = getNDataPoints(20)
	endTime = time.time()
	# Export the results to a text file
	dataPoints = first10 + middleBunch + last20
	exportAsTextFile(dataPoints)
	print("\nApproximately", str((endTime - startTime)/numberOfDataPoints), "sec per iteration.")
	print("\nCoolio! We're done.")

def timeTheOperation():
	# Set a reference point
	numberOfTrials = 10
	i = 0
	previousStats = wiFiStats()
	dataPoints = []
	startTime = time.time()
	while (i < numberOfTrials):
		currentStats = wiFiStats()
		dataPoints.append(netWiFiStats(previousStats, currentStats))
		time.sleep(0.995)
		previousStats = currentStats
		print(i)
		i += 1
	stopTime = time.time()
	averageTime = (stopTime - startTime) / numberOfTrials
	print(str(averageTime), "seconds per call")

if __name__ == "__main__":
	numberOfReadings = 200
	main(numberOfReadings)	# Each takes ~1 sec (See getNDataPoints())
	# timeTheOperation()
