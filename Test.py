from Ship_Monitor.monitor import monitor
from json import load

with open('config.json','r') as f:
    config = load(f)

with open('testData.json','r') as f:
    testData = load(f)

ship_monitor = monitor(
        URI= config['mongo']
    )

# ---------------------------------  Insert Data Tests  ---------------------------------

def test_InsertData_1():
    assert ship_monitor.insertData([testData['AIS Messages'][0],testData['AIS Messages'][1]]) == 2, "TEST FAILED"

def test_InsertData_2():
    assert ship_monitor.insertData([testData['AIS Messages'][2]]) == 1, "TEST FAILED"

# ---------------------------------  Insert AIS Message Tests  ---------------------------------

def test_insertAISMessage_2():
    assert ship_monitor.insertAISMessage(testData['AIS Messages'][3]) == 1, "TEST FAILED"

def test_insertAISMessage_3():
    assert ship_monitor.insertAISMessage({"_id":"6384d77aaca926202b19ee30"}) == 0, "TEST FAILED"

# ---------------------------------  Delete Old Messages Tests  ---------------------------------
def test_deleteOldMesssages_1():
    assert ship_monitor.deleteOldMesssages() == 5,"TEST FAILED"

def test_deleteOldMesssages_2():
    assert ship_monitor.deleteOldMesssages() == 5,"TEST FAILED"

# ---------------------------------  Get Tile Image Tests  ---------------------------------

def test_getTileImage_1():
    assert ship_monitor.getTileImage("38F7") == bytearray(open(".\\Ship_Monitor\\tiles\\38F7.png","rb").read()), "TEST FAILED"

def test_getTileImage_2():
    assert ship_monitor.getTileImage("38F93") == bytearray(open(".\\Ship_Monitor\\tiles\\38F93.png","rb").read()), "TEST FAILED"