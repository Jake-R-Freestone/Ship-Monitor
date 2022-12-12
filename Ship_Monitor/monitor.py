from pymongo import MongoClient
from datetime import datetime
from arrow import get

class monitor:
    def __init__(self,URI):
        self.mongo = MongoClient(URI)
        self.DB = self.mongo['Ship_Monitor']
        self.vesselDB = self.DB['vessels']
        self.portDB = self.DB['ports']
        self.mapViewsDB = self.DB['mapviews']
        self.dataDB = self.DB['data']

        # cleaning the collections 
        self.vesselDB.delete_many({})
        self.portDB.delete_many({})
        self.mapViewsDB.delete_many({})
        self.dataDB.delete_many({})

    # Insert a batch of AIS messages (Static Data and/or Position Reports) 
    # Jake (Done)
    def insertData(self,data:list) -> int: # Number of insertions
        return len(self.dataDB.insert_many(data).inserted_ids)

    # Insert an AIS message (Position Report or Static Data)
    # Jake (Done)
    def insertAISMessage(self,data:dict) -> int: # 1/0 for Success/Failure
        try:
            self.dataDB.insert_one(data)
        except Exception:
            return 0
        return 1
    
    def insertPortData(self,data:dict) -> int:
        try:
            self.portDB.insert_one(data)
        except Exception:
            return 0
        return 1
        
    # Delete all AIS messages whose timestamp is more than 5 minutes older than current time
    # Jake (Needs Testing)
    def deleteOldMesssages(self,currentTime:datetime) -> int: # Number of deletions
        return self.dataDB.delete_many({"Timestamp":{"$lt":get(currentTime).shift(minutes=-5).datetime}}).deleted_count

    # Read all most recent ship positions
    #Dawson (working)
    def getRecentShipPositions(self) -> list: # Array of ship documents
        if self.stub_mode:
            return []
        return [self.portDB.find().sort({"Position":-1})]

    # Read most recent position of given MMSI
    #Dawson (working)
    def getMostRecentPosition(self,MMSI:str) -> dict: # Position document of the form {"MMSI": ..., "lat": ..., "long": ..., "IMO": ... }
        if self.stub_mode:
            return []
        return dict(self.dataDB.find_one({"MMSI":{}}))

    # Read permanent or transient vessel information matching the given MMSI, and 0 or more additional criteria: IMO, Name, CallSign
    # Dawson (working)
    def getVesselData(self,MMSI:str) -> dict: # a Vessel document, with available and/or relevant properties.
        if self.stub_mode:
            return []
        return 

    # Read all most recent ship positions in the given tile
    # Dawson (working)
    def shipPositionByTile(self,tileID:str) -> list: # Array of ship documents
        pass

    # Read all ports matching the given name and (optional) country
    # Derek (working)
    def getPorts(self,portName:str,country:str=None) -> list: # Array of Port documents
        if country:
            return list(self.portDB.find({"port_location":portName,"country":country}))
        return list(self.portDB.find({"port_location":portName}))

    # Read all ship positions in the tile of scale 3 containing the given port
    # Derek (working)
    def getShipPositionByPort(self,portName:str,country:str=None) -> list: # If unique matching port: Array of Position documents (see above). Otherwise: an Array of Port documents.
        return [self.portDB.find({"Position": portName})]

    # Read last 5 positions of given MMSI
    # Derek (working)
    def getLastFivePositions(self,MMSI:str) -> list: # Document of the form {MMSI: ..., Positions: [{"lat": ..., "long": ...}, ...], "IMO": ... }
        pass

    # Read most recents positions of ships headed to port with given Id
    # Derek (working)
    def getShipPositionHeadedToPort(self,portID:str) -> list: # Document of the form {MMSI: ..., Positions: [{"lat": ..., "long": ...}, ...], "IMO": ... }
        pass

    # Read most recent positions of ships headed to given port (as read from static data, or user input)
    # Derek (working)
    def getShipPostionHeadedToPorts(self,portnamee:str,country:str) -> dict: # If unique matching port: array of of Position documents of the form {"MMSI": ..., "lat": ..., "long": ..., "IMO": ...}10 Otherwise: an Array of Port documents.
        pass

    # Given a background map tile for zoom level 1 (2), find the 4 tiles of zoom level 2 (3) that are contained in it
    def getBackgroundTilefromZoon1to2(self,tileId:str) -> list: # list<map tile description documents>
        pass

    # Given a tile Id, get the actual tile (a PNG file)
    # Jake (Done)
    def getTileImage(self,tileID:str) -> bytearray:
        with open(f".\\Ship_Monitor\\tiles\\{tileID}.png","rb") as f:
            return bytearray(f.read())

if __name__ == "__main__":
    pass