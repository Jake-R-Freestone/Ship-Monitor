from pymongo import MongoClient
from datetime import datetime
from arrow import get

class monitor:
    def __init__(self,URI):
        self.mongo = MongoClient(URI)
        self.vesselDB = self.mongo['AISTestData']['vessels']
        self.portDB = self.mongo['AISTestData']['ports']
        self.mapViewsDB = self.mongo['AISTestData']['mapviews']
        self.dataDB = self.mongo['AISTestData']['aisdk_20201118']
    
    # Insert a batch of AIS messages (Static Data and/or Position Reports)
    def insertData(self,data:list) -> int: # Number of insertions
        return len(self.dataDB.insert_many(data).inserted_ids)

    # Insert an AIS message (Position Report or Static Data)
    def insertAISMessage(self,data:dict) -> int: # 1/0 for Success/Failure
        if self.dataDB.insert_one(data).acknowledged:
            return 1
        return 0
        
    # Delete all AIS messages whose timestamp is more than 5 minutes older than current time
    def deleteOldMesssages(self,currentTime:datetime,timeStamp:datetime) -> int: # Number of deletions
        return len(self.dataDB.delete_many({"$gte":get(currentTime).shift(minutes=-5).datetime}).deleted_count)

    # Read all most recent ship positions
    def getRecentShipPositions(self) -> list: # Array of ship documents
        pass

    # Read most recent position of given MMSI
    def getMostRecentPosition(self,MMSI:str) -> dict: # Position document of the form {"MMSI": ..., "lat": ..., "long": ..., "IMO": ... }
        return self.dataDB.find_one({"MMSI":MMSI},{"sort":{"Timestamp":-1},"projection":{"_id":0,"MMSI":1,"lat":"$Position.cordinates[0]","long":"$Position.cordinates[1]","IMO":1}})

    # Read permanent or transient vessel information matching the given MMSI, and 0 or more additional criteria: IMO, Name, CallSign
    def getVesselData(self,MMSI:str) -> dict: # a Vessel document, with available and/or relevant properties.
        pass

    # Read all most recent ship positions in the given tile
    def shipPositionByTile(self,tileID:str) -> list: # Array of ship documents
        pass

    # Read all ports matching the given name and (optional) country
    def getPorts(self,portName:str,country:str=None) -> list: # Array of Port documents
        return self.portDB.find({""}) # Port doesnt have a name field

    # Read all ship positions in the tile of scale 3 containing the given port
    def getShipPositionByPort(self,portName:str,country:str) -> list: # If unique matching port: Array of Position documents (see above). Otherwise: an Array of Port documents.
        pass

    # Read last 5 positions of given MMSI
    def getLastFivePositions(self,MMSI:str) -> list: # Document of the form {MMSI: ..., Positions: [{"lat": ..., "long": ...}, ...], "IMO": ... }
        return self.dataDB.find({"MMSI":MMSI,"MsgType":"position_report"},{"project":{"_id":0,"MMSI":1,"Positions":[{"lat":"","long":"","IMO":""}]}})

    # Read most recents positions of ships headed to port with given Id
    def getShipPositionHeadedToPort(portID:str) -> list: # Document of the form {MMSI: ..., Positions: [{"lat": ..., "long": ...}, ...], "IMO": ... }
        pass

    # Read most recent positions of ships headed to given port (as read from static data, or user input)
    def getShipPostionHeadedToPorts(portnamee:str,country:str) -> dict: # If unique matching port: array of of Position documents of the form {"MMSI": ..., "lat": ..., "long": ..., "IMO": ...}10 Otherwise: an Array of Port documents.
        pass

    # Given a background map tile for zoom level 1 (2), find the 4 tiles of zoom level 2 (3) that are contained in it
    def getBackgroundTilefromZoon1to2(tileId:str) -> list: # list<map tile description documents>
        pass

    # Given a tile Id, get the actual tile (a PNG file)
    def getTileImage(tileID:str) -> None: # Needs to return binary image 
        with open(f"./tiles/{tileID}.png","rb") as f:
            return bytearray(f.read())

if __name__ == "__main__":
    pass