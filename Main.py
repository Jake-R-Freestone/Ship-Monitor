from Ship_Monitor.monitor import monitor
from json import load

with open("config.json","r") as f:
    config = load(f)

ship_monitor = monitor(
        URI= config['mongo']
    )

def main():
    print("\n\n")
    print(ship_monitor.getTileImage("38F7"))
    print("\n\n")

if __name__ == "__main__":
    main()