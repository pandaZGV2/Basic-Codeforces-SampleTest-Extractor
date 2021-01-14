import sys
import json
import urllib.request, urllib.parse, urllib.error
import matplotlib.pyplot as plt
import math
import numpy as np
import seaborn as sns
import warnings

sns.set_theme()
# sns.set_style('white')
sns.set_style('ticks')
sns.set_style('dark')
warnings. filterwarnings('ignore')
username = input("Enter the handle of the user: ")
if(len(username) < 1):
    print("Enter a username!")

params = {'handle': username}
details = urllib.parse.urlencode(params)
url = 'https://codeforces.com/api/user.rating?'
try:
    # TRY REQUESTING INFORMATION FROM THE CODEFORCES API
    # IN THE EVENT OF AN ERROR (EXAMPLE HTTP 404 NOT FOUND) GO TO EXCEPT CODE BLOCK AND EXIT THE PROGRAM

    finalurl = url+details
    encodeddata = urllib.request.urlopen(finalurl)
    data = encodeddata.read().decode()
    jsondata = json.loads(data)
except:
    print("Unable to read")
    exit()
if jsondata['status'] == 'OK':
    # CHECK IF THE DATA RECEIVED HAS 'OK' STATUS, IF NOT EXIT THE PROGRAM.

    print("Recieved handles successfully.")
    # json_formatted_str = json.dumps(jsondata, indent=2)
    # print(json_formatted_str)
else:
    print("Handle not recieved.\nPlease check the handle name.")
    exit()


contests = dict()
y = list()
x = list()
xax = list()
# READ X-AXIS AND Y-AXIS DETAILS

for contest in jsondata['result']:
    y.append(contest['newRating'])
    x.append(math.floor((contest['ratingUpdateTimeSeconds'] -
                         jsondata['result'][0]['ratingUpdateTimeSeconds'])/86400))
    # xax.append(str(contest['contestId']))
# print(len(x))
# print(len(y))


# SET PLOT STYLES (SUBJECT TO CHANGE)

fig = plt.figure()
plt.title(username+" - Rating plot")
plt.plot(x, y, color="black", linewidth="2",
         markerfacecolor='white', markersize="7", marker="o")
plt.ylim([0, 4000])
# plt.xlim([10, x[-2]])

# SET BAR COLORS AND STYLES

bars = plt.bar(x, y, color=(0.2, 0.4, 0.6, 0))
# print(len(bars))
plt.grid(True)
contest = dict()

# READ THE NECESSARY DETAILS FROM JSONDATA TO PLOT THE GRAPH


def readelements():
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
yax = [1200, 1400, 1600, 1900, 2100, 2300, 2400, 2600, 3000, 4000]
# plt.semilogy(yax)
ax = plt.subplot()
ax.set_yticks(yax)
# plt.grid(color='#cccccc')
ax.set_xticklabels([])
# ax.set_xticklabels(xax, rotation='20')

# SET ANNOTATION STYLES

annot = ax.annotate("", xy=(0, 0), xytext=(-20, 20), textcoords="offset points",
                    bbox=dict(boxstyle="round", fc=(1, 1, 0), ec="r", lw=2),
                    arrowprops=dict(arrowstyle="-|>"))
annot.set_visible(False)

# SET THE BACKGROUND COLOR FOR THE GRAPH

ax.axhspan(0, 1200, facecolor=('#CCCCCC'), alpha=0.75)
ax.axhspan(1200, 1400, facecolor='lime', alpha=0.75)
ax.axhspan(1400, 1600, facecolor='cyan', alpha=0.75)
ax.axhspan(1600, 1900, facecolor='indigo', alpha=0.75)
ax.axhspan(1900, 2100, facecolor='purple', alpha=0.75)
ax.axhspan(1900, 2100, facecolor='purple', alpha=0.75)
ax.axhspan(2100, 2300, facecolor=(1, 1, 0), alpha=0.5)
ax.axhspan(2300, 2400, facecolor=(1, 1, 0), alpha=0.75)
ax.axhspan(2400, 2600, facecolor='red', alpha=0.35)
ax.axhspan(2600, 3000, facecolor='red', alpha=0.75)
ax.axhspan(3000, 4000, facecolor='red', alpha=1)

# SET ANNOTATION DETAILS


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

# FUNCTION TO DETECT EVENTS AND ACCORDINGLY DISPLAY THE REQUIRED ANNOTATION


def hover(event):
    vis = annot.get_visible()
    if event.inaxes == ax:
        for bar in bars:
            cont, ind = bar.contains(event)
            if cont:
                update_annot(bar)
                annot.set_visible(True)
                fig.canvas.draw_idle()
                return
    if vis:
        annot.set_visible(False)
        fig.canvas.draw_idle()


# SET FUNCTION HOVER AS THE FUNCTION TO BE USED WHEN AN EVENT TAKES PLACE
fig.canvas.mpl_connect("motion_notify_event", hover)

plt.show()
