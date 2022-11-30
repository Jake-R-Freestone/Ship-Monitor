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
    assert ship_monitor.insertData([testData[0],testData[1]]) == 2, "TEST FAILED"

def test_InsertData_2():
    assert ship_monitor.insertData([testData[2]]) == 1, "TEST FAILED"

def test_InsertData_3():
    assert ship_monitor.insertData([testData[1]]) != 3, "TEST FAILED"