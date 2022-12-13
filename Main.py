from Ship_Monitor.monitor import monitor
from json import load

with open("config.json","r") as f:
    config = load(f)

with open('testData.json','r') as f:
    testData = load(f)

ship_monitor = monitor(
        URI= config['mongo']
    )

def main():
    pass
    # You can mess around with the package here

if __name__ == "__main__":
    main()