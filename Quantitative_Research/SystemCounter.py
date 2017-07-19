#_______________________________________________________________________________

import psutil
import time
from collections import namedtuple
import sys

#_______________________________________________________________________________

# The IPv4 address used by Unity to connect to the HoloLens
holoLensIPv4 = '10.8.113.245'

#_______________________________________________________________________________

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

#_______________________________________________________________________________

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

#_______________________________________________________________________________

def netWiFiStats(initialStats, currentStats):
	'''
	Given two WiFi network stats from wiFiStats(), this method returns the
	difference between each of the fields.
	Returns a namedtuple object with the fields:
		megaBytesSent, packetsSent, megaBytesReceived, packetsReceived
	'''
	# initialStats and currentStats are namedtuples from wiFiStats()
	megaBytesSent = (currentStats.bytesSent - initialStats.bytesSent)/(1024 * 1024)
	megaBytesReceived = (currentStats.bytesReceived - initialStats.bytesReceived)/(1024 * 1024)
	totalPacketsSent = (currentStats.packetsSent - initialStats.packetsSent)
	totalPacketsReceived = (currentStats.packetsReceived - initialStats.packetsReceived)

	myNetWiFiStats = namedtuple('netWiFiStats', ['megaBytesSent', 'packetsSent', 'megaBytesReceived', 'packetsReceived'])
	return myNetWiFiStats(megaBytesSent, totalPacketsSent, megaBytesReceived, totalPacketsReceived)

#_______________________________________________________________________________

def printNetworkStats(megaBytesSent, packetsSent, megaBytesReceived, packetsReceived):
	'''
	Prints the network statistics to the console.
	'''
	print("_________\n")
	print("Wi-Fi Stats...")
	print("Sent\t\t: %6.2f MB," %megaBytesSent, packetsSent, "packets")
	print("Received\t: %6.2f MB," %megaBytesReceived, packetsReceived, "packets")
	print("_________")

#_______________________________________________________________________________

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

#_______________________________________________________________________________

def exportAsTextFile(dataPoints):
	'''
	Exports the data as a tab delimited text file, with header information
	'''
	outputFile = open('demo.txt', 'w')

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

#_______________________________________________________________________________

def getNDataPoints(numberOfMeasurements):
	'''
	Returns a list of N measurements of data transfer in MB and packets per second.
	'''
	dataPoints = []

	# We confirmed these delays empirically using timeTheOperation()
	intervalOrigami = 0.982
	intervalStaticCube = 0.995

	# Set interval between wi-fi stats measurements
	intervalInSeconds = intervalStaticCube

	# Take the required number of measurements
	previousStats = wiFiStats()
	for i in range(numberOfMeasurements):
		time.sleep(intervalInSeconds)
		currentStats = wiFiStats()
		dataPoints.append(netWiFiStats(previousStats, currentStats))
		previousStats = currentStats
		print(i)

	# Return the results
	return dataPoints

#_______________________________________________________________________________

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

#_______________________________________________________________________________

def timeTheOperation():
	'''
	Used to determine the duration of fetching WiFi stats when running another
	concurrent program.
	'''
	# Set a reference point
	numberOfTrials = 1000
	i = 0
	previousStats = wiFiStats()
	dataPoints = []
	startTime = time.time()
	for i in range(numberOfTrials):
		currentStats = wiFiStats()
		dataPoints.append(netWiFiStats(previousStats, currentStats))
		# time.sleep(0.995)
		previousStats = currentStats
		print(i)

	stopTime = time.time()
	averageTime = (stopTime - startTime) / numberOfTrials
	print(str(averageTime), "seconds per call")

#_______________________________________________________________________________

if __name__ == "__main__":
	numberOfReadings = 200
	# main(numberOfReadings)	# Each takes ~1 sec (See getNDataPoints())
	# timeTheOperation()
	print(getProcessID())
#_______________________________________________________________________________
