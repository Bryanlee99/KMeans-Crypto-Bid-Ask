import json
from sklearn import cluster
import numpy as np
import matplotlib.pyplot as plt

# file info and split terms
word = "mid_price"
end_string = "}]}"
file_name = "orderbook_bitflyer_2017-10-10.txt"

# file processing
f = open(file_name, "r").read()
p = f.split(word)
num = len(p)

# process text
first_pos = f.find(word)
begin = first_pos - 2
end = 0
table = []
for i in range(num):
    pos = f.find(word, begin + len(word))
    end = f.find(end_string, end + len(end_string))
    table.insert(len(table), f[begin:end] + end_string)
    begin = pos - 2

data = []

# process JSON Objects
for i in range(len(table)-1):
    f2 = open("jsontest2.txt", "w")
    f2.write(table[i])
    f2.close()
    with open('jsontest2.txt') as json_file:
        data.insert(0, json.load(json_file))

# inserts the bidPrices and cumulative bid volumes
cumSumBids = []
bidPrice = []
for j in range(0, len(data)):
    cumSumBids.insert(0, [])
    bidPrice.insert(0, [])
    for i in range(0, len(data[j]['bids'])):
        if len(cumSumBids[0]) == 0:
            cumSumBids[0].insert(0, 0 + data[j]['bids'][i]['size'])
        else:
            cumSumBids[0].insert(0, cumSumBids[0][0] + data[j]['bids'][i]['size'])
        bidPrice[0].insert(0, data[j]['bids'][i]['price'])

# inserts the ask P and cumulative bid volumes
cumSumAsks = []
askPrice = []
for j in range(0, len(data)):
    cumSumAsks.insert(0, [])
    askPrice.insert(0, [])
    for i in range(0, len(data[j]['asks'])):
        if len(cumSumAsks[0]) == 0:
            cumSumAsks[0].insert(0, 0 + data[j]['asks'][i]['size'])
        else:
            cumSumAsks[0].insert(0, cumSumAsks[0][0] + data[j]['asks'][i]['size'])
        askPrice[0].insert(0, data[j]['asks'][i]['price'])

# fills the ask and bid price arrays with data points near the spread
askPriceArray = []
for i in range(len(askPrice)):
    askPriceArray.insert(0, np.asarray(askPrice[i][250:400]))

bidPriceArray = []
for i in range(len(bidPrice)):
    bidPriceArray.insert(0, np.asarray(bidPrice[i][2200:2700]))

# k-means implementation
k_meansAsks = cluster.KMeans(n_clusters=5)
k_meansAsks.fit(askPriceArray)

k_meansBids = cluster.KMeans(n_clusters=5)
k_meansBids.fit(bidPriceArray)

# plots the resulting means
for i in range(5):
     plt.plot(k_meansAsks.cluster_centers_[i], cumSumAsks[0][250:400], color = (0, 0.2 * i, 0))
     plt.plot(k_meansBids.cluster_centers_[i], cumSumBids[0][2200:2700], color = (0, 0.2 * i, 0))

plt.show()
