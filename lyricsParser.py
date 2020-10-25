import json
import collections
import operator
import time
import random
import string
from tkinter.ttk import Progressbar
import tkinter.ttk as ttk

from graphics import *
import matplotlib.pyplot as plt
# import matplotlib
# matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
import numpy as np

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

def urlExtract(url, blockIdentifier, blockType='div'):
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    gottenData = html_soup.find_all(blockType, class_=blockIdentifier)
    return gottenData

def urlExtractById(url, blockIdentifier, blockType='div'):
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    gottenData = html_soup.find_all(blockType, id=blockIdentifier)
    return gottenData


def urlExtractByIdForSyllable(url, blockIdentifier, blockType='div'):
    try:
        response = get(url)
    except:
        return 0, '0-error1'
    html_soup = BeautifulSoup(response.text, 'html.parser')
    check = html_soup.find_all('span', id='Link_CTAs_SylRul_TopLeft')
    if len(check) > 0:
        return 0,''
    gottenData = html_soup.find_all(blockType, id=blockIdentifier)
    syllable = gottenData[0].find_all('span', class_='Answer_Red')
    if len(syllable) > 1:
        syllable = syllable[1].text
    elif len(syllable) > 0:
        syllable = syllable[0].text
    else:
        return 0,''
    numOfSyllable = syllable.count('-')+1
    return numOfSyllable, syllable

def urlExtractByClassForLyrics(url, blockIdentifier, blockType='div'):
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    gottenData = html_soup.find_all(blockType, class_=blockIdentifier)
    lyrics = gottenData[0].find_all('div')
    # print(len(lyrics)) 17
    return lyrics[5]

def urlExtractByIdForSong(url, blockIdentifier, blockType='div'):
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    # print(html_soup);
    gottenData = html_soup.find_all(blockType, id=blockIdentifier)
    gottenData = gottenData[0].find_all('a')
    artistName = html_soup.find_all('strong')
    return gottenData, artistName[0].text[:-7]

def urlExtractByClassForSong(url, blockIdentifier, blockType='div'):
    response = get(url)
    if 'Our systems have detected unusual activity from your IP address (computer network).' in response or 'Your IP address will be unblocked soon. Thank you for your patience.' in response:
        while True:
            userInput = input("Type 'continue' to continue': ")
            if userInput == 'continue':
                response = get(url)
                if not 'Our systems have detected unusual activity from your IP address (computer network).' in response or 'Your IP address will be unblocked soon. Thank you for your patience.' in response:
                    break;
    html_soup = BeautifulSoup(response.text, 'html.parser')
    # print(html_soup)
    gottenData = html_soup.find_all(blockType, class_=blockIdentifier)
    #getting littler
    test = gottenData[0].find_all('div', id='listAlbum')
    if len(test) > 0:
        gottenData = test
    gottenData = gottenData[0].find_all('a')
    artistName = html_soup.find_all('strong')
    return gottenData, artistName[0].text[:-7]

def htmlStringExtract(htmlString, blockIdentifier, blockType='div'):
    extracted = htmlString.find_all(blockType, blockIdentifier)
    return extracted

def getUrlList(filePath):
    returnVar = {};
    with open(filePath, 'r') as file:
        returnVar = json.load(file)
    return returnVar

def parseDictToBar(dict):
    to = 9
    d_sorted_by_value = collections.OrderedDict(sorted(dict.items(), key = lambda kv:(kv[1], kv[0]), reverse= True))
    # d_sorted_by_value = dict
    returnVarX = []
    returnVarY = []
    count = 0
    for key in d_sorted_by_value.keys():
        returnVarX.append(key)
        returnVarY.append(dict[key])
        count += 1
        if count > to:
            break
    return returnVarX, returnVarY

def parseDictToBarUpBottom(dict):
    to = 9
    d_sorted_by_value = collections.OrderedDict(sorted(dict.items(), key = lambda kv:(kv[1], kv[0]), reverse= True))
    returnVarX = []
    returnVarY = []
    count = 0
    keys = list(d_sorted_by_value.keys())
    rangeList = []
    if len(keys) > 10:
        rangeList = [0, 1, 2, 3, 4, len(keys) - 5, len(keys) - 4, len(keys) - 3, len(keys) - 2, len(keys) - 1]
    else:
        rangeList = range(len(keys))

    # print(rangeList)
    for i in rangeList:
        key = keys[i]
        returnVarX.append(key)
        returnVarY.append(dict[key])
    return returnVarX, returnVarY


def parseDictToBarRandom(dict):
    to = 9
    returnVarX = []
    returnVarY = []
    count = 0
    keys = list(dict.keys())
    for i in [random.randrange(0, len(keys), 1) for i in range(to)]:
        key = keys[i]
        returnVarX.append(key)
        returnVarY.append(dict[key])
    return returnVarX, returnVarY

def parseListToGraph(list):
    # print(list)
    x = []
    y = []
    z = []
    for item in list:
        x.append(item[0])
        y.append(item[1])
        z.append(item[2])
    return x, y, z

from mpl_toolkits.mplot3d import axes3d, Axes3D

def parseListToScatter(list):
    x = []
    y = []
    for item in list:
        x.append(item[0])
        y.append(item[1])
    return x, y

def parseDisplay(jsonPath):
    # sample values
    wordUsed = {}
    syllablesFreqPos = []
    freqPos = []
    syllablePos = {}

    """
    wordUsed = {'you': 3}
    syllablesFreqPos = [[2, 40, 80]]
    freqPos = [[0, 0]]
    syllablePos = {'al': 80}
"""
    # window
    window = Tk()
    frame = Frame(window)
    frame.pack()

    #setup elements

    #word Used Bar graph
    fig1 = Figure(figsize=(5, 4), linewidth=1, edgecolor="#04253a")
    wordUsedAxis = fig1.add_subplot(111)

    tempX, tempY = parseDictToBar(wordUsed)
    wordUsedAxis.bar(tempX, tempY, align='center', alpha=0.5)

    wordUsedAxis.set_title("Frequency of Words", fontsize=16)
    wordUsedAxis.set_ylabel("frequency", fontsize=14)
    wordUsedAxis.set_xlabel("word", fontsize=14)

    wordUsedDisplay = FigureCanvasTkAgg(fig1, master=frame)
    wordUsedDisplay.get_tk_widget().pack(side=LEFT)
    wordUsedDisplay.draw()

    # number of syllable - frequency - position
    fig2 = plt.figure(figsize=(5,4), linewidth=1, edgecolor="#04253a")
    syllableFreqPosAxis = fig2.add_subplot(111, projection='3d')
    tempX, tempY, tempZ = parseListToGraph(syllablesFreqPos)
    zdata = 15 * np.random.random(len(syllablesFreqPos))
    syllableFreqPosAxis.scatter3D(tempX, tempY, tempZ, c=zdata, cmap='Greens');

    syllableFreqPosAxis.set_title("# of Syllables in relation to freq and pos", fontsize=16)
    syllableFreqPosAxis.set_ylabel("# of syllables", fontsize=12)
    syllableFreqPosAxis.set_xlabel("frequency", fontsize=12)
    syllableFreqPosAxis.set_zlabel("position", fontsize=12)

    syllableFreqPosDisplay = FigureCanvasTkAgg(fig2, master=frame)
    syllableFreqPosDisplay.get_tk_widget().pack(side=LEFT)
    syllableFreqPosDisplay.draw()


    frame2 = Frame(window)
    frame2.pack()

    # frequency of words - Position
    fig3 = Figure(figsize=(5, 4), linewidth=1, edgecolor="#04253a")
    freqPosAxis = fig3.add_subplot(111)
    tempX, tempY = parseListToScatter(freqPos)

    # ax.scatter(x, y, alpha=0.8, c=color, edgecolors='none', s=30, label=group)
    freqPosAxis.scatter(tempX, tempY, alpha=0.8)

    freqPosAxis.set_title("Frequency of Words in relation to Position", fontsize=16)
    freqPosAxis.set_ylabel("position", fontsize=14)
    freqPosAxis.set_xlabel("frequency", fontsize=14)


    freqPosDisplay = FigureCanvasTkAgg(fig3, master=frame2)
    freqPosDisplay.get_tk_widget().pack(side=LEFT)
    freqPosDisplay.draw()

    #word Used Bar graph
    fig4 = Figure(figsize=(5, 4), linewidth=1, edgecolor="#04253a")
    syllablePosAxis = fig4.add_subplot(111)
    tempX, tempY = parseDictToBar(syllablePos)

    syllablePosAxis.bar(tempX, tempY, align='center', alpha=0.5)

    syllablePosAxis.set_title("Position of Syllables", fontsize=16)
    syllablePosAxis.set_ylabel("position", fontsize=12)
    syllablePosAxis.set_xlabel("syllable", fontsize=12)

    syllablePosDisplay = FigureCanvasTkAgg(fig4, master=frame2)
    syllablePosDisplay.get_tk_widget().pack(side=LEFT)
    syllablePosDisplay.draw()

    frame3 = Frame(window)
    frame3.pack(fill=tk.BOTH)

    s = ttk.Style()
    s.theme_use('clam')
    s.configure("red.Horizontal.TProgressbar", foreground='red', background='red')

    songProgress = Progressbar(frame3, orient=HORIZONTAL, length=100)
    artistProgress = Progressbar(frame3, orient=HORIZONTAL, style="red.Horizontal.TProgressbar", length=100)
    songProgress.pack(fill=tk.BOTH)
    artistProgress.pack(fill=tk.BOTH)

    window.update_idletasks()
    window.update()

    # resetting values
    # types of stored data
    wordUsed = {}
    syllablesFreqPos = [[0, 0, 0]]
    freqPos = [[0, 0]]
    syllablePos = {}


    # get urls from json and generate graph through them
    # ignore artist
    artistList = getUrlList(jsonPath)
    urlList = []
    for key, object in artistList.items():
        for songKey, songObject in artistList[key].items():
            urlList.append([songKey, songObject])
    urlCount = 0
    for url in urlList:
        #get each song
        songName = url[0]
        url = url[1]
        urlCount += 1
        lyric = urlExtractByClassForLyrics(url, "col-xs-12 col-lg-8 text-center")
        lyric = lyric.getText()
        lyric = lyric.split("\n")
        lyric = [x for x in lyric if len(x) > 1]

        wordUsed = {}
        syllablesFreqPos = []
        freqPos = []
        syllablePos = {}

        print(f"Parsing {songName} ---------------------------------------")

        lineCount = 0
        for line in lyric:
            lineCount += 1
            print(f"    {lineCount}/{len(lyric)} - {line}")
            words = line.split(' ')
            for i in range(len(words)):
                word = words[i]
                try:
                    numOfSyllable, syllable = urlExtractByIdForSyllable("https://www.howmanysyllables.com/words/"+word.lower(), 'SyllableContentContainer', 'p')
                except:
                    numOfSyllable, syllable = 0, "0-error"
                # word frequency graph
                frequency = 0
                position = (line.index(word)/len(line)) * 100;
                if word in wordUsed.keys():
                    number = wordUsed[word]
                    wordUsed[word] = number + 1
                    frequency = number + 1
                else:
                    wordUsed[word] = 1
                    frequency = 1

                # numOfSyllable - time used - position
                syllablesFreqPos += [[numOfSyllable, frequency, position]]

                syllableParts = syllable.split('-')
                # a syllable - position
                for sy in syllableParts:
                    if sy in syllablePos.keys():
                        number = syllablePos[sy]
                        syllablePos[sy] = (position + number)/2
                    else:
                        syllablePos[sy] = position

                # frequency - position
                freqPos += [[frequency,  position]]

                #update and store
                tempX, tempY = parseDictToBar(wordUsed)
                wordUsedAxis.clear()
                wordUsedAxis.bar(tempX, tempY, align='center', alpha=0.5)
                wordUsedAxis.set_title("Frequency of Words", fontsize=16)
                wordUsedAxis.set_ylabel("frequency", fontsize=14)
                wordUsedAxis.set_xlabel("word", fontsize=14)
                wordUsedAxis.set_xticks(range(len(tempX)), tempX)
                wordUsedDisplay.draw()

                tempX, tempY, tempZ = parseListToGraph(syllablesFreqPos)
                zdata = 15 * np.random.random(len(syllablesFreqPos))
                syllableFreqPosAxis.clear()
                syllableFreqPosAxis.scatter3D(tempX, tempY, tempZ, c=zdata, cmap='Greens')
                syllableFreqPosAxis.set_title("# of Syllables in relation to freq and pos", fontsize=16)
                syllableFreqPosAxis.set_ylabel("# of syllables", fontsize=12)
                syllableFreqPosAxis.set_xlabel("frequency", fontsize=12)
                syllableFreqPosAxis.set_zlabel("position", fontsize=12)
                syllableFreqPosDisplay.draw()

                tempX, tempY = parseListToScatter(freqPos)
                freqPosAxis.clear()
                freqPosAxis.scatter(tempX, tempY, alpha=0.8)
                freqPosAxis.set_title("Frequency of Words in relation to Position", fontsize=16)
                freqPosAxis.set_ylabel("position", fontsize=14)
                freqPosAxis.set_xlabel("frequency", fontsize=14)
                freqPosDisplay.draw()

                tempX, tempY = parseDictToBarUpBottom(syllablePos)
                syllablePosAxis.clear()
                syllablePosAxis.set_title("Position of Syllables", fontsize=16)
                syllablePosAxis.set_ylabel("position", fontsize=12)
                syllablePosAxis.set_xlabel("syllable", fontsize=12)
                syllablePosAxis.bar(tempX, tempY, align='center', alpha=0.5)
                syllablePosAxis.set_xticks(range(len(tempX)), tempX)
                syllablePosDisplay.draw()

                songProgress['value'] = (lineCount/len(lyric)) * 99
                artistProgress['value'] = (urlCount/len(urlList)) * 99

                window.update_idletasks()
                window.update()
            with open('data.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
            with open('data.json', 'w', encoding='utf-8') as file:
                wordUsed = collections.OrderedDict(sorted(wordUsed.items(), key=lambda kv: (kv[1], kv[0]), reverse=True))
                syllablePos = collections.OrderedDict(sorted(syllablePos.items(), key=lambda kv: (kv[1], kv[0]), reverse=True))
                data[songName] = {'wordUsed': wordUsed, 'syllablePos': syllablePos, 'syllablesFreqPos': syllablesFreqPos, 'freqPos': freqPos}
                json.dump(data, file, ensure_ascii=False, indent=4)
        fig1.savefig(songName+"--"+''.join([random.choice(string.ascii_letters + string.digits) for n in range(14)])+'.png', dpi=200)
        fig2.savefig(songName+"--"+''.join([random.choice(string.ascii_letters + string.digits) for n in range(14)])+'.png', dpi=200)
        fig3.savefig(songName+"--"+''.join([random.choice(string.ascii_letters + string.digits) for n in range(14)])+'.png', dpi=200)
        fig4.savefig(songName+"--"+''.join([random.choice(string.ascii_letters + string.digits) for n in range(14)])+'.png', dpi=200)
        print(f"   Finish {songName} --")
        # canvas.create_image(20, 20, anchor=NW, image=plt)
    window.mainloop()



def parseSongDisplay(url, songName, dataPath):
    # sample values
    wordUsed = {}
    syllablesFreqPos = []
    freqPos = []
    syllablePos = {}

    """
    wordUsed = {'you': 3}
    syllablesFreqPos = [[2, 40, 80]]
    freqPos = [[0, 0]]
    syllablePos = {'al': 80}
"""
    # window
    window = Tk()
    frame = Frame(window)
    frame.pack()

    #setup elements

    #word Used Bar graph
    fig1 = Figure(figsize=(5, 4), linewidth=1, edgecolor="#04253a")
    wordUsedAxis = fig1.add_subplot(111)

    tempX, tempY = parseDictToBar(wordUsed)
    wordUsedAxis.bar(tempX, tempY, align='center', alpha=0.5)

    wordUsedAxis.set_title("Frequency of Words", fontsize=16)
    wordUsedAxis.set_ylabel("frequency", fontsize=14)
    wordUsedAxis.set_xlabel("word", fontsize=14)

    wordUsedDisplay = FigureCanvasTkAgg(fig1, master=frame)
    wordUsedDisplay.get_tk_widget().pack(side=LEFT)
    wordUsedDisplay.draw()

    # number of syllable - frequency - position
    fig2 = plt.figure(figsize=(5,4), linewidth=1, edgecolor="#04253a")
    syllableFreqPosAxis = fig2.add_subplot(111, projection='3d')
    tempX, tempY, tempZ = parseListToGraph(syllablesFreqPos)
    zdata = 15 * np.random.random(len(syllablesFreqPos))
    syllableFreqPosAxis.scatter3D(tempX, tempY, tempZ, c=zdata, cmap='Greens');

    syllableFreqPosAxis.set_title("# of Syllables in relation to freq and pos", fontsize=16)
    syllableFreqPosAxis.set_ylabel("# of syllables", fontsize=12)
    syllableFreqPosAxis.set_xlabel("frequency", fontsize=12)
    syllableFreqPosAxis.set_zlabel("position", fontsize=12)

    syllableFreqPosDisplay = FigureCanvasTkAgg(fig2, master=frame)
    syllableFreqPosDisplay.get_tk_widget().pack(side=LEFT)
    syllableFreqPosDisplay.draw()


    frame2 = Frame(window)
    frame2.pack()

    # frequency of words - Position
    fig3 = Figure(figsize=(5, 4), linewidth=1, edgecolor="#04253a")
    freqPosAxis = fig3.add_subplot(111)
    tempX, tempY = parseListToScatter(freqPos)

    # ax.scatter(x, y, alpha=0.8, c=color, edgecolors='none', s=30, label=group)
    freqPosAxis.scatter(tempX, tempY, alpha=0.8)

    freqPosAxis.set_title("Frequency of Words in relation to Position", fontsize=16)
    freqPosAxis.set_ylabel("position", fontsize=14)
    freqPosAxis.set_xlabel("frequency", fontsize=14)


    freqPosDisplay = FigureCanvasTkAgg(fig3, master=frame2)
    freqPosDisplay.get_tk_widget().pack(side=LEFT)
    freqPosDisplay.draw()

    #word Used Bar graph
    fig4 = Figure(figsize=(5, 4), linewidth=1, edgecolor="#04253a")
    syllablePosAxis = fig4.add_subplot(111)
    tempX, tempY = parseDictToBar(syllablePos)

    syllablePosAxis.bar(tempX, tempY, align='center', alpha=0.5)

    syllablePosAxis.set_title("Position of Syllables", fontsize=16)
    syllablePosAxis.set_ylabel("position", fontsize=12)
    syllablePosAxis.set_xlabel("syllable", fontsize=12)

    syllablePosDisplay = FigureCanvasTkAgg(fig4, master=frame2)
    syllablePosDisplay.get_tk_widget().pack(side=LEFT)
    syllablePosDisplay.draw()

    frame3 = Frame(window)
    frame3.pack(fill=tk.BOTH)

    s = ttk.Style()
    s.theme_use('clam')
    s.configure("red.Horizontal.TProgressbar", foreground='red', background='red')

    songProgress = Progressbar(frame3, orient=HORIZONTAL, length=100)
    artistProgress = Progressbar(frame3, orient=HORIZONTAL, style="red.Horizontal.TProgressbar", length=100)
    songProgress.pack(fill=tk.BOTH)
    artistProgress.pack(fill=tk.BOTH)

    window.update_idletasks()
    window.update()

    # resetting values
    # types of stored data
    wordUsed = {}
    syllablesFreqPos = [[0, 0, 0]]
    freqPos = [[0, 0]]
    syllablePos = {}

    lyric = urlExtractByClassForLyrics(url, "col-xs-12 col-lg-8 text-center")
    lyric = lyric.getText()
    lyric = lyric.split("\n")
    lyric = [x for x in lyric if len(x) > 1]

    wordUsed = {}
    syllablesFreqPos = []
    freqPos = []
    syllablePos = {}

    print(f"Parsing {songName} ---------------------------------------")

    lineCount = 0
    for line in lyric:
        lineCount += 1
        print(f"    {lineCount}/{len(lyric)} - {line}")
        words = line.split(' ')
        for i in range(len(words)):
            word = words[i]
            try:
                numOfSyllable, syllable = urlExtractByIdForSyllable("https://www.howmanysyllables.com/words/"+word.lower(), 'SyllableContentContainer', 'p')
            except:
                numOfSyllable, syllable = 0, "0-error"
            # word frequency graph
            frequency = 0
            position = (line.index(word)/len(line)) * 100;
            if word in wordUsed.keys():
                number = wordUsed[word]
                wordUsed[word] = number + 1
                frequency = number + 1
            else:
                wordUsed[word] = 1
                frequency = 1

            # numOfSyllable - time used - position
            syllablesFreqPos += [[numOfSyllable, frequency, position]]

            syllableParts = syllable.split('-')
            # a syllable - position
            for sy in syllableParts:
                if sy in syllablePos.keys():
                    number = syllablePos[sy]
                    syllablePos[sy] = (position + number)/2
                else:
                    syllablePos[sy] = position

            # frequency - position
            freqPos += [[frequency,  position]]

            #update and store
            tempX, tempY = parseDictToBar(wordUsed)
            wordUsedAxis.clear()
            wordUsedAxis.bar(tempX, tempY, align='center', alpha=0.5)
            wordUsedAxis.set_title("Frequency of Words", fontsize=16)
            wordUsedAxis.set_ylabel("frequency", fontsize=14)
            wordUsedAxis.set_xlabel("word", fontsize=14)
            wordUsedAxis.set_xticks(range(len(tempX)), tempX)
            wordUsedDisplay.draw()

            tempX, tempY, tempZ = parseListToGraph(syllablesFreqPos)
            zdata = 15 * np.random.random(len(syllablesFreqPos))
            syllableFreqPosAxis.clear()
            syllableFreqPosAxis.scatter3D(tempX, tempY, tempZ, c=zdata, cmap='Greens')
            syllableFreqPosAxis.set_title("# of Syllables in relation to freq and pos", fontsize=16)
            syllableFreqPosAxis.set_ylabel("# of syllables", fontsize=12)
            syllableFreqPosAxis.set_xlabel("frequency", fontsize=12)
            syllableFreqPosAxis.set_zlabel("position", fontsize=12)
            syllableFreqPosDisplay.draw()

            tempX, tempY = parseListToScatter(freqPos)
            freqPosAxis.clear()
            freqPosAxis.scatter(tempX, tempY, alpha=0.8)
            freqPosAxis.set_title("Frequency of Words in relation to Position", fontsize=16)
            freqPosAxis.set_ylabel("position", fontsize=14)
            freqPosAxis.set_xlabel("frequency", fontsize=14)
            freqPosDisplay.draw()

            tempX, tempY = parseDictToBarUpBottom(syllablePos)
            syllablePosAxis.clear()
            syllablePosAxis.set_title("Position of Syllables", fontsize=16)
            syllablePosAxis.set_ylabel("position", fontsize=12)
            syllablePosAxis.set_xlabel("syllable", fontsize=12)
            syllablePosAxis.bar(tempX, tempY, align='center', alpha=0.5)
            syllablePosAxis.set_xticks(range(len(tempX)), tempX)
            syllablePosDisplay.draw()

            songProgress['value'] = (lineCount/len(lyric)) * 99

            window.update_idletasks()
            window.update()
        try:
            with open(dataPath, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except:
            data = {}
        with open(dataPath, 'w', encoding='utf-8') as file:
            wordUsed = collections.OrderedDict(sorted(wordUsed.items(), key=lambda kv: (kv[1], kv[0]), reverse=True))
            syllablePos = collections.OrderedDict(sorted(syllablePos.items(), key=lambda kv: (kv[1], kv[0]), reverse=True))
            data[songName] = {'wordUsed': wordUsed, 'syllablePos': syllablePos, 'syllablesFreqPos': syllablesFreqPos, 'freqPos': freqPos}
            json.dump(data, file, ensure_ascii=False, indent=4)
    fig1.savefig(songName+"--"+''.join([random.choice(string.ascii_letters + string.digits) for n in range(14)])+'.png', dpi=200)
    fig2.savefig(songName+"--"+''.join([random.choice(string.ascii_letters + string.digits) for n in range(14)])+'.png', dpi=200)
    fig3.savefig(songName+"--"+''.join([random.choice(string.ascii_letters + string.digits) for n in range(14)])+'.png', dpi=200)
    fig4.savefig(songName+"--"+''.join([random.choice(string.ascii_letters + string.digits) for n in range(14)])+'.png', dpi=200)
    print(f"   Finish {songName} --")
        # canvas.create_image(20, 20, anchor=NW, image=plt)
    window.mainloop()
