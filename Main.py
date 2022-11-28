from Ship_Monitor.monitor import monitor
from json import load

with open("config.json","r") as f:
    config = load(f)

def main():

    ship_monitor = monitor(
        URI=f"mongodb://{config['username']}:{config['password']}@{config['host']}:{config['port']}/"
    )

    # Tests

    





if __name__ == "__main__":
    pass