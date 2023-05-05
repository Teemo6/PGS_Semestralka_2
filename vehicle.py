import xml.etree.ElementTree as ET

# Vehicle object
# Stores Vehicle ID, time spent loading, time spent waiting at ferry/traveling and time when it arrived at ferry
class Vehicle:
    def __init__(self, id, loading, waiting):
        self._id = id
        self._loading = loading
        self._waiting = waiting
        self._arrived = 0

    # Increment loading time by variable num
    def addLoading(self, num):
        self._loading += num

    # Increment waiting time by variable num
    def addWaiting(self, num):
        self._waiting += num

    # Store time of arriving at ferry
    def setArrived(self, num):
        self._arrived = num

    # Getter for ID
    def getId(self):
        return self._id

    # Getter for loading
    def getLoading(self):
        return self._loading

    # Getter for waiting
    def getWaiting(self):
        return self._waiting

    # Getter for time arrived at ferry
    def getArrived(self):
        return self._arrived

    # Returns Element of ElementTree containing vehicle data
    def createElement(self):
        root = ET.Element("Vehicle")
        root.set("id", str(self._id))

        load = ET.SubElement(root, "loadTime")
        load.text = str(self._loading)

        trans = ET.SubElement(root, "transportTime")
        trans.text = str(self._waiting)

        return root
