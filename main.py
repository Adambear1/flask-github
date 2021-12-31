import sys
from datetime import datetime
import requests

def main():
    try:
        name = sys.argv[1]
        res = requests.get(f"https://api.github.com/users/{name}/events").json()
        print(f"Latest github event for {name} was at " + datetime.fromisoformat(res[0]["created_at"][:-1]).strftime("%Y-%m-%d %H:%M:%S"))
    except KeyError:
        print(f"User {name} does not exist! Try again!")

if __name__ == "__main__":
    main()