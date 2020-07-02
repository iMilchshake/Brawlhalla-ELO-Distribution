import requests as rq
import time

# Goal is to find the end of the leaderboard with the least possible steps

# SETTINGS:
API_KEY = "< YOUR API KEY >"
BRACKET = "1v1"  # 2v2/1v1
REGION = "eu"  # eu/all
START = 1  # start searching from here

COMPARES = 0

# returns whether page x is in the leaderboard
def inclusive(x):
    global COMPARES
    response = rq.get("https://api.brawlhalla.com/rankings/%s/%s/%s?api_key=%s" % (BRACKET, REGION, x, API_KEY))

    while True:
        if response.status_code == 200:  # success
            if len(response.json()) > 0:
                time.sleep(0.2)
                COMPARES += 1
                return True
            else:
                time.sleep(0.2)
                COMPARES += 1
                return False
        else:
            print('Invalid Request (%s) ! waiting for 1 minute..' % response.json())
            time.sleep(60)
            return inclusive(x)  # try again!


def find_border():
    i = START  # current guess
    g = 1  # grow by

    while True:
        stepped = False
        while inclusive(i):
            stepped = True
            i = i + g
            g = int(g * 2)
            print("%s %s" % (i, g))

        if stepped:  # go back to last inclusive
            g = int(g / 2)
            i = i - g

        g = int(g / 2)  # half the growth and try again next iteration
        print("%s %s" % (i, g))

        if g == 1 and inclusive(i) and not inclusive(i + 1):
            break

    print("-> Last Page is %s" % i)


if __name__ == "__main__":
    find_border()
    print("Server requests done: %s" % COMPARES)
