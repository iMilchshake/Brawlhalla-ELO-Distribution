import numpy as np
import matplotlib.pyplot as plt

# Settings
FILENAME = "data/elocurve_1v1_jpn_cap_1220_start_1_max_7_multip_1.05_371.csv"   # file to display

# Brawlhalla ELO Tiers
bins = [(200, 719),
        (720, 757),
        (758, 795),
        (796, 833),
        (834, 872),
        (872, 909),
        (910, 953),
        (954, 997),
        (998, 1041),
        (1042, 1085),
        (1086, 1129),
        (1130, 1181),
        (1182, 1233),
        (1234, 1285),
        (1286, 1337),
        (1338, 1389),
        (1390, 1447),
        (1448, 1505),
        (1506, 1563),
        (1564, 1621),
        (1622, 1679),
        (1680, 1743),
        (1744, 1807),
        (1808, 1871),
        (1872, 1935),
        (1936, 1999),
        (2000, 4000)]

# get data from .csv file
ratings = list()
file = open(FILENAME, "r")
for rating in file:
    data = rating
    data = data.split(';')[1]
    ratings.append(int(data))
file.close()

# count player in bins
rating_bins = list()
n = 0
for b in bins:
    count = 0
    for rating in ratings:
        if b[0] <= rating <= b[1]:
            count += 1
    print("%s,%s,%s" % (b[0], b[1], count))
    n += count
    rating_bins.append(count)

# convert counts to percentages
for i in range(len(rating_bins)):
    rating_bins[i] /= n

# calculate percentages for each Rank (Tin, Silver, ...)
p_tin = '{0:.2g}'.format(sum(rating_bins[0:6]) * 100)
p_bronze = '{0:.2g}'.format(sum(rating_bins[6:11]) * 100)
p_silver = '{0:.2g}'.format(sum(rating_bins[11:16]) * 100)
p_gold = '{0:.2g}'.format(sum(rating_bins[16:21]) * 100)
p_plat = '{0:.2g}'.format(sum(rating_bins[21:26]) * 100)
p_dia = '{0:.2g}'.format((rating_bins[26]) * 100)
print("percentages: ")
print("tin: %s" % p_tin)
print("bronze: %s" % p_bronze)
print("silver: %s" % p_silver)
print("gold: %s" % p_gold)
print("plat: %s" % p_plat)
print("dia: %s" % p_dia)

# plotting
SMALL_SIZE = 10
MEDIUM_SIZE = 12
BIGGER_SIZE = 16
plt.style.use('grayscale')

plt.rc('font', size=SMALL_SIZE)  # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)  # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

fig, ax = plt.subplots()
tin = ax.bar(np.arange(0, 6), rating_bins[0:6], color='#325432', linewidth=1, edgecolor='black')
bronze = ax.bar(np.arange(6, 11), rating_bins[6:11], color='#b58957', linewidth=1, edgecolor='black')  # e7c076
silver = ax.bar(np.arange(11, 16), rating_bins[11:16], color='#b0b0b0', linewidth=1, edgecolor='black')
gold = ax.bar(np.arange(16, 21), rating_bins[16:21], color='#e4ae45', linewidth=1, edgecolor='black')  # 830314
plat = ax.bar(np.arange(21, 26), rating_bins[21:26], color='#77c4f7', linewidth=1, edgecolor='black')
dia = ax.bar(26, rating_bins[26], color='#341a8e')

plt.xticks([2.5, 8, 13, 18, 23, 26], ["Tin\n%s%%" % p_tin,
                                      "Bronze\n%s%%" % p_bronze,
                                      "Silver\n%s%%" % p_silver,
                                      "Gold\n%s%%" % p_gold,
                                      "Platinum\n%s%%" % p_plat,
                                      "Diamond\n%s%%" % p_dia])

plt.title("Brawlhalla ELO Distribution - %s %s" % (FILENAME.split("_")[1].upper(), FILENAME.split("_")[2].upper()))
ax.set_xlabel('ELO')
ax.set_ylabel('Amount')
plt.show()
