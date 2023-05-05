# Chunk object
# Stores Chunk ID, number of resources and time spent mining whole chunk
class Chunk:
    def __init__(self, id):
        self._id = id
        self._resources = 0
        self._duration = 0

    # Increment resources by 1
    def addOneResource(self):
        self._resources += 1

    # Increment time mining by variable num
    def addDuration(self, num):
        self._duration += num

    # Getter for ID
    def getId(self):
        return self._id

    # Getter for resources
    def getResources(self):
        return self._resources

    # Getter for duration
    def getDuration(self):
        return self._duration
