import sys
from worker import Worker
from vehicle import Vehicle
import xml.etree.ElementTree as ET

#############
### Setup ###
#############

# Print help and close application
def print_help():
    print("Usage: python3 ./run_sp2.py -i <input file> -o <output file>")
    sys.exit()

# Argument count
if(len(sys.argv) != 5):
    print_help()

# Required arguments
if(sys.argv[1] != "-i" and sys.argv[3] != "-o"):
    print_help()

# Loading arguments
input_file = sys.argv[2].strip()
output_file = sys.argv[4].strip()

# Elements of ElementTree
eSim = ET.Element("Simulation")
eBlo = ET.Element("blockAverageDuration")
eRes = ET.Element("resourceAverageDuration")
eFer = ET.Element("ferryAverageWait")
eWor = ET.Element("Workers")
eVeh = ET.Element("Vehicles")

# Variables
simStart = 0
chunkCount = 0
chunkTime = 0
resourceCount = 0
ferryCount = 0
ferryTime = 0

# Lists of objects
workers = {}
vehicles = {}

###############
### Parsing ###
###############

# Load lines of input file
with open(input_file) as f:
    lines = f.read().splitlines()

# Extracting data
for line in lines:
    words = line.strip().split(";")

    # Worker logs
    if words[1] == "Worker":
        if words[2] in workers:
            worker = workers.get(words[2])
        else:
            worker = Worker(words[2])
            workers[words[2]] = worker

        if "Extracted" in words[3]:
            worker.addOneResourceToChunk(words[4], int(words[5]))
        continue

    # Lorry logs
    if words[1] == "Lorry":
        if words[2] in vehicles:
            vehicle = vehicles.get(words[2])
        else:
            vehicle = Vehicle(words[2], 1, 2)
            vehicles[words[2]] = vehicle

        if "Fully" in words[3]:
            vehicle.addLoading(int(words[4]))

        if "ferry" in words[3]:
            vehicle.addWaiting(int(words[4]))
            vehicle.setArrived(int(words[0]))

        if "final" in words[3]:
            waited = int(words[0]) - vehicle.getArrived()
            vehicle.addWaiting(int(words[4]))
            vehicle.addWaiting(waited)
        continue

    # Ferry logs
    if words[1] == "Ferry":
        ferryCount += 1
        ferryTime += int(words[4])
        continue

    # Foreman logs
    if words[1] == "Foreman":
        simStart = int(words[0])
        chunkCount = words[4]
        resCount = words[5]

##################
### Output XML ###
##################

# Sort dictionaries by key
workers = {key: workers[key] for key in sorted(workers, key=lambda x: int(x))}
vehicles = {key: vehicles[key] for key in sorted(vehicles, key=lambda x: int(x))}

# Fill respective roots with items
for id, worker in workers.items():
    chunkTime += worker.getChunksTotalTime()
    resourceCount += worker.getChunksResources()
    eWor.append(worker.createElement())

for id, vehicle in vehicles.items():
    eVeh.append(vehicle.createElement())

# Compute statistics
simDuration = int(words[0]) - int(simStart)
chunkAvg = int(chunkTime) / int(chunkCount)
resourceAvg = int(chunkTime) / int(resourceCount)
ferryAvg = int(ferryTime) / int(ferryCount)

# Statistics
eSim.set("duration", str(simDuration))
eBlo.set("totalCount", str(chunkCount))
eBlo.text = str(chunkAvg)
eRes.set("totalCount", str(resourceCount))
eRes.text = str(resourceAvg)
eFer.set("totalCount", str(ferryCount))
eFer.text = str(ferryAvg)

# Append elements to tree
eSim.append(eBlo)
eSim.append(eRes)
eSim.append(eFer)
eSim.append(eWor)
eSim.append(eVeh)

# Write ElementTree to output file
ET.ElementTree(eSim).write(output_file)
