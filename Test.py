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

def test_InsertData_3():
    assert ship_monitor.insertData([testData['AIS Messages'][3]]) != 3, "TEST FAILED"