from chunk import Chunk
import xml.etree.ElementTree as ET

# Worker object
# Stores Worker ID and dictionary of assigned chunks
class Worker:
    def __init__(self, id):
        self._id = id
        self._chunks = {}

    # Returns total time spent mining all assigned chunks
    def getChunksTotalTime(self):
        total = 0
        for id, chunk in self._chunks.items():
            total += chunk.getDuration()
        return total

    # Returns sum of all resources in assigned chunks
    def getChunksResources(self):
        total = 0
        for id, chunk in self._chunks.items():
            total += chunk.getResources()
        return total

    # Adds one resource to existing chunk or creates new one
    def addOneResourceToChunk(self, id, dur):
        if id in self._chunks.keys():
            chunk = self._chunks[id]
        else:
            chunk = Chunk(id)
            self._chunks[id] = chunk
        chunk.addOneResource()
        chunk.addDuration(dur)

    # Returns Element of ElementTree containing worker data
    def createElement(self):
        resourceCount = 0
        miningDuration = 0

        for id, chunk in self._chunks.items():
            resourceCount += chunk.getResources()
            miningDuration += chunk.getDuration()

        root = ET.Element("Worker")
        root.set("id", str(self._id))

        res = ET.SubElement(root, "resources")
        res.text = str(resourceCount)

        dur = ET.SubElement(root, "workDuration")
        dur.text = str(miningDuration)
        
        return root
