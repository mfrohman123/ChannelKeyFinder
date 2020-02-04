import keyfinder
import youtube_dl
import glob
import csv
import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)
        
def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading')

""" Helper for scrolling to bottom of channel page """
def scroll(driver):

    # Get scroll height.
    lastHeight = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
    
        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

        # Wait to load the page.
        time.sleep(2)

        # Calculate new scroll height and compare with last scroll height.
        newHeight = driver.execute_script("return document.documentElement.scrollHeight")

        if newHeight == lastHeight:
            break

        lastHeight = newHeight


""" Helper to download videos """
def downloadVideo(url):

    ydl_opts = { # Save as mp3 rather than entire video
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
    }
    
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try: # error if the file is too large
            ydl.download([url])
        except: # just ignore this link
            print("ERROR with:", url)
            return
    
    # To save space, we delete each file after analysis
    # Therefore, we can assume that there is only one mp3 file, the current one
    # Use glob to get the filename
    newFile = glob.glob("*.mp3")[0]
    key = keyfinder.key(newFile)
    print("Doing", newFile)
    
    # If optimal key, add to CSV of good songs.
    if str(key) == 'Ab' or str(key) == 'Fm':
        with open('goodSongs.csv', 'a') as csvList:
            list = csv.writer(csvList, delimiter=',', quotechar='|')
            list.writerow([url, newFile])
            
    # If possible, add to CSV of potential songs
    elif str(key) == 'Cm' or str(key) == 'Eb':
        with open('potentialSongs.csv', 'a') as csvList:
            list = csv.writer(csvList, delimiter=',', quotechar='|')
            list.writerow([url, newFile])
            
    elif str(key) == 'Bbm' or str(key) == 'Db':
        with open('potentialSongs.csv', 'a') as csvList:
            list = csv.writer(csvList, delimiter=',', quotechar='|')
            list.writerow([url, newFile])
            
    elif str(key) == 'Bb' or str(key) == 'Gm':
        with open('potentialSongs.csv', 'a') as csvList:
            list = csv.writer(csvList, delimiter=',', quotechar='|')
            list.writerow([url, newFile])

    # Delete mp3 to save space
    os.remove(newFile)

""" Gets all video links from a channel, analyzes each link """
def main(option, channelName):
    channel = 'https://www.youtube.com/{}/{}/videos'
    base = 'https://www.youtube.com'
    
    driver = webdriver.Chrome()
    driver.get(channel.format(option, channelName))
    time.sleep(2)
    
    scroll(driver) # scroll to bottom of page
    html = BeautifulSoup(driver.page_source, "html.parser") # create BS object from page
    
    # Get all links from driver, and concatenate to base
    links = [base + url['href'] for url in html.find_all('a', attrs = {'id' : 'thumbnail', 'class' : 'yt-simple-endpoint inline-block style-scope ytd-thumbnail'}, href = True)]
    
    # Perform analysis on each individual link
    for link in links:
        downloadVideo(link)
        
main('user', 'HungOverGargoyle') #electronic gems
main('channel', 'UC5rKZH0zjx-idLAzA3PeD1Q') #XVII Collective
main('channel', 'UC7UkUQITjpLsDge73gCad6w') #Synthwave Music Channel
main('channel', 'UCHSv5KYYBSlOS340sdHK2ew') #disconnected from the interweb
main('channel', 'UC6hBefyLMtG7FXhZ55da3Vw') #Artzie Music
main('channel', 'UCEcnMr7tLhUp7c-2dxNjlVg') #Stuxnet
main('channel', 'UCyyKYOiJGnKcg02rELfUreg') #GRAEDA Music
main('channel', 'UC2qRXfOSx3wc8cBMuetAaIg') #DylanFRM
main('channel', 'UCTQuSKpt5ZLQvC_DoBxuZQQ') #VvporTV
main('channel', 'UCjPLBJtP7zq16YVcT3_gmkg') #Polychora
main('channel', 'UCi0546b2gr4OBN0f1_qV8BA') #Synthwave Legends
main('channel', 'UCrtvQEADq7OO7K4sNtUAPdw') #NeonAether
main('channel', 'UCR4G6GUtZ7WRudlrsFNM4Ig') #Kuzau
main('channel', 'UCwd4I7sAJfdAtGNJuj6fiMQ') #Nightware
main('channel', 'UC2fa42GxXrN03Yd3LV821mg') #XLightningStormL
main('channel', 'UCtUrx37ILOaDkVmICB5q6Rw') #::: e radio
main('channel', 'UCQA95v0kYvNnw80GBb7ZwhA') #DRIVE Radio
main('channel', 'UCSJ4gkVC6NrvII8umztf0Ow') #ChilledCow
main('channel', 'UCte1snz2ymJyJHld_EmF97g') #Pseudonym
main('channel', 'UC0HuJHX6zVVBpHlGn_nUJVQ') #ChillWave
main('channel', 'UCdq6IKFvxx2PYp8bdf4Qe7Q') #Daily Earfood
main('channel', 'UCx9VLMFd5DdqpfKSJo2jRjA') #Majestic Sounds
main('channel', 'UCOa-zIys4wcrsGPMvvd6Syw') #Dreamwave
main('channel', 'UCCCS8cRSiJjAqgwvmP7VxJw') #Vapor Memory
main('channel', 'UCD-4g5w1h8xQpLaNS_ghU4g') #NewRetroWave
main('channel', 'UCqf9MRHECH46mX5YDXIM5iQ') #LuigiDonatello
main('channel', 'UCRUOfuNIb_sk__7snjK3aVg') #ElFamosoDemon
main('channel', 'UC6hBefyLMtG7FXhZ55da3Vw') #Artzie Music
main('channel', 'UC6hBefyLMtG7FXhZ55da3Vw') #Artzie Music
main('channel', 'UC6hBefyLMtG7FXhZ55da3Vw') #Artzie Music
main('channel', 'UC6hBefyLMtG7FXhZ55da3Vw') #Artzie Music
main('channel', 'UC6hBefyLMtG7FXhZ55da3Vw') #Artzie Music
