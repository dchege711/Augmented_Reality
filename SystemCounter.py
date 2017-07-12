import psutil	# install using "pip install psutil"
import time
from collections import namedtuple

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

def myWiFiStats():
	'''
	Returns a namedtuple object with the fields:
	('bytesSent', 'packetsSent', 'bytesReceived', 'packetsReceived')
	'''
	myNetworkStats = psutil.net_io_counters(pernic = True)
	bytesSent = myNetworkStats["Wi-Fi"].bytes_sent
	packetsSent = myNetworkStats["Wi-Fi"].packets_sent
	bytesReceived = myNetworkStats["Wi-Fi"].bytes_recv
	packetsReceived = myNetworkStats["Wi-Fi"].packets_recv

	wiFiStats = namedtuple('wiFiStats', ['bytesSent', 'packetsSent', 'bytesReceived', 'packetsReceived'])
	return wiFiStats(bytesSent, packetsSent, bytesReceived, packetsReceived)

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

def main(interval):
	print("Started ...")
	startTime = time.time()
	initialStats = myWiFiStats()
	time.sleep(interval)
	print("Finito...")
	endStats = myWiFiStats()
	endTime = time.time()

	# myWiFiStats returns a tuple
	megaBytesSent = (endStats.bytesSent - initialStats.bytesSent)/(1024 * 1024)
	megaBytesReceived = (endStats.bytesReceived - initialStats.bytesReceived)/(1024 * 1024)
	totalPacketsSent = (endStats.packetsSent - initialStats.packetsReceived)
	totalPacketsReceived = (endStats.packetsReceived - initialStats.packetsReceived)

	printNetworkStats(megaBytesSent, totalPacketsSent, megaBytesReceived, totalPacketsReceived)

if __name__ == "__main__":
	main(60)
