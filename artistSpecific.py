import json
import time
from random import random

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

url = 'https://www.azlyrics.com/t/twentyonepilots.html'

def extractArtistSong(url, filePath):
    print(f'\n{1}/1 - search - {url} -------------------------------------------------------------------------------------------')
    time.sleep(random() + 1)
    aList, artistName = urlExtractByClassForSong(url, "col-xs-12 col-md-6 text-center", 'div')
    print("Artist Name: " + artistName);
    song = {}
    print(aList);
    for a in aList:
        element = str(a)
        start = element.index("href=\"") + 9
        end = element.index("\"", start)
        song[a.string] = 'https://www.azlyrics.com/'+element[start:end]
    data = {}
    try:
        with open(filePath, 'r', encoding='utf-8') as file:
                data = json.load(file)
    except:
        data = {}
    with open(filePath, 'w', encoding='utf-8') as file:
        data[artistName] = song
        json.dump(data, file, ensure_ascii=False, indent=4)
    print(song)