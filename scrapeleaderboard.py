import requests as rq
import time
import math
from scipy.interpolate import interp1d

# SETTINGS
API_KEY = "<YOUR API KEY>"                  # Your API Key
BRACKET = "1v1"                             # 1v1 or 2v2
REGION = "jpn"                              # all/us-e/eu/sea/brz/aus/us-w/jpn
CAP = 1220                                  # last page of leaderboard
START_STEP = 1                              # starts with this step size
MAX_STEP = 10                               # maximum possible step size
STEP_MULTIPLIER = 1.05                      # step size will be multiplied after every step
START_PAGE = 1                              # start crawling from here


def approx():
    filename = "data/elocurve_%s_%s_cap_%s_start_%s_max_%s_multip_%s_%s.csv" % (BRACKET, REGION, CAP, START_STEP,
                                                                                MAX_STEP, STEP_MULTIPLIER,
                                                                                time.gmtime().tm_min * time.gmtime().tm_sec)
    print("filename: %s" % filename)
    print("this will take about %.2g Hours" % (CAP / (720 * MAX_STEP)))

    # initialize variables
    step = START_STEP
    page = START_PAGE
    last = False
    x = list()
    y = list()

    # scrape through the leaderboard
    while True:
        response = rq.get("https://api.brawlhalla.com/rankings/%s/%s/%s?api_key=%s" % (BRACKET, REGION, page, API_KEY))
        if response.status_code == 200:
            if len(response.json()) > 0:  # valid page found
                print("%s;%s" % (page, response.json()[0]['rating']))
                x.append(page)
                y.append(response.json()[0]['rating'])

                # increase step
                page += math.floor(step)
                if step < MAX_STEP:  # step cant exceed MAX_STEP
                    step = step * STEP_MULTIPLIER
                else:
                    step = MAX_STEP
            else:
                if last:
                    print("exceeded leaderboard, done...")
                    break
                last = True
                page = CAP
        else:
            print('Invalid Request (%s) ! waiting for 1 minute..' % response.json())
            time.sleep(60)

    # linear interpolate elo curve - should be close enough
    f = interp1d(x, y)

    # calculate interpolated values between the sample-points
    pages = range(1, x[-1] + 1)
    ratings = list()
    for p in pages:
        s = math.ceil(f(p))
        ratings.append(s)

    # saving all values as .csv
    print("writing into: %s" % filename)
    for p in zip(pages, ratings):
        with open(filename, "a") as file:
            file.write("%s;%s \n" % (p[0], p[1]))


if __name__ == "__main__":
    t = time.time()
    approx()
    print("Took %.2g Minutes" % ((time.time() - t)/60))
