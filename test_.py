from pytest import fixture
from Ship_Monitor.monitor import monitor
from json import load
from arrow import utcnow

with open('config.json','r') as f:
    config = load(f)

with open('testData.json','r') as f:
    testData = load(f)

ship_monitor = monitor(
        URI= config['mongo']
    )

# Used to insert a document before a test is ran
@fixture
def insertMessage():
    ship_monitor.insertAISMessage({"Timestamp":utcnow().shift(minutes=-7).datetime})

@fixture
def insertPort():
    ship_monitor.insertPortData({"port_location": "Denmark"})

# ---------------------------------  Insert Data Tests  ---------------------------------
class TestInserData:
    def test_InsertData_1(self):
        assert ship_monitor.insertData([testData['AIS Messages'][0],testData['AIS Messages'][1]]) == 2, "TEST FAILED"

    def test_InsertData_2(self):
        assert ship_monitor.insertData([testData['AIS Messages'][2]]) == 1, "TEST FAILED"

# ---------------------------------  Insert AIS Message Tests  ---------------------------------
class TestInserAISMessage:
    def test_insertAISMessage_1(self):
        assert ship_monitor.insertAISMessage(testData['AIS Messages'][3]) == 1, "TEST FAILED"

    def test_insertAISMessage_2(self):
        assert ship_monitor.insertAISMessage(testData['AIS Messages'][3]) == 0, "TEST FAILED"

# ---------------------------------  Delete Old Messages Tests  ---------------------------------
class TestDeleteOldMessages:
    def test_deleteOldMesssages_1(self):
        assert ship_monitor.deleteOldMesssages(utcnow().datetime) == 0,"TEST FAILED"

    def test_deleteOldMesssages_2(self,insertMessage):
        assert ship_monitor.deleteOldMesssages(utcnow().datetime) == 1,"TEST FAILED"

# ---------------------------------  Get Tile Image Tests  ---------------------------------
class TestGetTileImage:
    def test_getTileImage_1(self):
        assert ship_monitor.getTileImage("38F7") == bytearray(open(".\\Ship_Monitor\\tiles\\38F7.png","rb").read()), "TEST FAILED"

    def test_getTileImage_2(self):
        assert ship_monitor.getTileImage("38F93") == bytearray(open(".\\Ship_Monitor\\tiles\\38F93.png","rb").read()), "TEST FAILED"

# ---------------------------------  Get Ports  ---------------------------------
class TestGetPorts:
    def test_getPorts_1(self):
        assert len(ship_monitor.getPorts("Copenhagen")) == 0, "TEST FAILED"
    
    def test_getPorts_2(self,insertPort):
        assert len(ship_monitor.getPorts("Denmark")) == 1, "TEST FAILED"

# ---------------------------------  Get Ship Position By Port  ---------------------------------

class GetShipPositionByPort:
    def test_getShipPositionByPort_1(self):
        assert ship_monitor.getShipPositionByPort("Copenhagen") == [], "TEST FAILED"

    def test_getShipPositionByPort_2(self):
        assert len(ship_monitor.getShipPositionByPort("Denmark")) > 0, "TEST FAILED"