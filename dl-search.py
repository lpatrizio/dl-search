#import mpv doesn't work for some damn reason. Error is apparently that I'm using 64bit python with 32bit mpv but my python is 32bit
from __future__ import unicode_literals
import os
import youtube_dl
import random
import time

ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s', 'quiet':True})

def playlistMode(): #plays an entire playlist, with the options to either shuffle the playlist or start from a specific point. Requires playlist link.
    randomized = False
    beginning = 0
    isRandom = input("PLAYLIST MODE: Randomize? y/n ")
    if isRandom == 'y': randomized = True
    playlist = input("Insert playlist: ")
    with ydl:
        print("Extracting....")
        results = ydl.extract_info(playlist, download=False)
    foundResults = []
    for i in range (len(results['entries'])):   #Grabbing just the entries themselves
        foundResults.append(results['entries'][i])
    stored = []
    for i in range (len(foundResults)):
        stored.insert(i, [foundResults[i]['webpage_url'], foundResults[i]['duration'], foundResults[i]['title']])
    if (randomized == True):
        random.shuffle(stored)
    if (randomized == False):
        for i in range(len(stored)):
            print(str(i)+":", stored[i][2])
        beginning = input("Start where? ")
        if (beginning == "exit"):
            return
    for i in range (beginning, len(stored)):
        print(i, ': ', stored[i][2]+'. Playing...')
        os.system('mpv.exe '+stored[i][0])
        time.sleep(5)      
    return

def searchMode(search, channel = False):    #standard mode for searching. Can either search for videos or channels
    if (channel == True):  #Since there's THREE different possible URLs for channels, I have to search for the channel and grab it's url. Asking user would be tedious, so just search for 3. Youtube-dl can't directly search channels, this instead just searches the name, and USUALLY Youtube will give you that channel's most popular videos.
        with ydl:
            print("Extracting...")
            results = ydl.extract_info('ytsearch3:'+search,download=False)
    else:
        amount = input("How many results do you want to find? ")
        with ydl:
            print("Extracting...")
            results = ydl.extract_info('ytsearch'+amount+':'+search,download=False)

    stored = searchCleaner(results)

    if (channel == True):       
        found = False
        for i in range(len(stored)):
            if (stored[i][1] == search):
                found = True
                ChannelNo = i
                break
        if (found == False):
            for i in range (len(stored)):
                print("Result "+str(i)+": ", stored[i][1])
            channelReq = input("Choose the correct channel: ")
            if (channelReq == "exit"):
                return
        else:
            print("Found channel")
            channelReq = ChannelNo
        amount = int(input("How many results do you want to find? "))
        search = stored[int(channelReq)][3]
        ydl_opts = {'playlistend':amount, 'quiet':True, 'ignoreerrors':True}    #need to ignore errors because it triggers when youtube-dl tries to extract a video set to premiere, which is annoying
        cydl = youtube_dl.YoutubeDL(ydl_opts)
        with cydl:
            print("Extracting...")
            results = cydl.extract_info(search+'/videos',download=False )
        stored = searchCleaner(results)
        optionSelect(stored)
        return
    else:
        optionSelect(stored)
        return

def optionSelect(results):  #Basic method for displaying all extracted results and playing
    if (len(results) == 0):
        print("No results! Please try again")
        return
    if (len(results) == 1):
        print("Only one result. Playing...")
        os.system('mpv.exe '+results[0][2])
        return
    for i in range (len(results)):
            print("Result "+str(i)+": ", results[i][0], "||", results[i][1])
    requested = input("Choose an option: " )
    if (requested == 'exit'):
        return
    #very spaghetti way to get mpv working
    os.system('mpv.exe '+results[int(requested)][2])

def searchCleaner(extracted): #utility for cleaning up stuff found with ytextractor
    foundResults = []
    for i in range (len(extracted['entries'])):   #Grabbing just the entries themselves
        foundResults.append(extracted['entries'][i])
    stored = []
    errors = 0
    for i in range (len(foundResults)):   #cleaning up
        if foundResults[i] == None: #skipping nonetypes that exist because an error was hit (like premiere videos)
            errors+=1
        else:
            stored.insert(i, [foundResults[i]['title'], foundResults[i]['uploader'], foundResults[i]['webpage_url'], foundResults[i]['uploader_url']])
    if (errors >0):
        print("Extractor failed to extract",errors,"videos. Only displaying", (len(stored)), "results.")        
    return stored

#Ask the user what they're searching for
search = ''
while (search!= 'exit'):
    search = input("What are you looking for? ")
    if (search == 'exit'):
        exit(0)
    if (search == 'p'):
        playlistMode()
    elif(search == 'c'):
        search = input("Input channel name: ")
        searchMode(search, True)
    else:
        searchMode(search)
