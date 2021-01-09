import sys
import json
import urllib.request
import urllib.parse
import urllib.error
import matplotlib.pyplot as plt
import math
import numpy as np


username = input("Enter the handle of the user: ")
if(len(username) < 1):
    print("Enter a username!")

params = {'handle': username}
details = urllib.parse.urlencode(params)
url = 'https://codeforces.com/api/user.rating?'
finalurl = url+details
encodeddata = urllib.request.urlopen(finalurl)
data = encodeddata.read().decode()
try:
    jsondata = json.loads(data)
except:
    print("Unable to read")
if jsondata['status'] == 'OK':
    print("Recieved handles successfully.")
    json_formatted_str = json.dumps(jsondata, indent=2)
    # print(json_formatted_str)
else:
    print("Handle not recieved.\nPlease check the handle name.")
    exit()


contests = {}
y = list()
x = list()
xax = list()
for contest in jsondata['result']:
    y.append(contest['newRating'])
    x.append(math.floor((contest['ratingUpdateTimeSeconds'] -
                         jsondata['result'][0]['ratingUpdateTimeSeconds'])/86400))
    xax.append(contest['contestName'])
print(len(x))
print(len(y))


#
fig = plt.figure()
plt.plot(x, y, 'c-o', markerfacecolor='r')
bars = plt.bar(x, y, color=(0.2, 0.4, 0.6, 0))
print(len(bars))
plt.grid(True)
contest = dict()


def readelements():
    global i
    i = 0
    global contests, jsondata
    for bar in bars:
        contest = jsondata['result'][i]
        x = bar.get_x()+bar.get_width()/2.
        y = bar.get_y()+bar.get_height()
        contests[(x, y)] = {'contest': contest['contestName'], 'rank': contest['rank'],
                            'change': contest['newRating']-contest['oldRating'], 'Rating': contest['newRating']}
        i = i+1

        # contests['contest'].append(contest['contestName'])
        # contests['rank'].append(contest['rank'])
        # contests['change'].append(contest['newRating']-contest['oldRating'])
readelements()
print(contests)
yax = [1200, 1400, 1600, 1900, 2100, 2300, 2400, 2600, 3000, 4000]
# print(len(xax),len(yax))
# plt.xticks(np.arange(len(xax),xax))
ax = plt.subplot()
# plt.yticks(np.arange(len(yax)), yax)

annot = ax.annotate("", xy=(0, 0), xytext=(-20, 20), textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="red", ec="b", lw=2),
                    arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)


def update_annot(bar):
    x = bar.get_x()+bar.get_width()/2.
    y = bar.get_y()+bar.get_height()
    annot.xy = (x, y)
    contest = contests[(x, y)]['contest']
    rank = contests[(x, y)]['rank']
    rating = contests[(x, y)]['Rating']
    change = contests[(x, y)]['change']
    text = "Contest : {}\nInc/Dec : {}\nRank : {}\nRating : {}".format(
        contest, change, rank, rating)
    annot.set_text(text)
    annot.get_bbox_patch().set_alpha(0.4)


def hover(event):
    vis = annot.get_visible()
    if event.inaxes == ax:
        for bar in bars:
            cont, ind = bar.contains(event)
            if cont:
                update_annot(bar)
                annot.set_visible(True)
                fig.canvas.draw_idle()
                i = i+1
                return
    if vis:
        annot.set_visible(False)
        fig.canvas.draw_idle()


fig.canvas.mpl_connect("motion_notify_event", hover)

plt.show()
