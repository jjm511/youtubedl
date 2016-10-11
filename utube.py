import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
use_adblock_filters = True
def search():
    print('Enter a playlist name on youtube:')
    playlist = input()
    playlist = ''.join(playlist.split())
    searchplaylist = 'https://www.youtube.com/results?q='+playlist+'&sp=EgIQAw%253D%253D'
    r3 = requests.get(searchplaylist)
    r3 = r3.text
    soup2 = BeautifulSoup(r3, 'html.parser')
    playlistitle = soup2.findAll('a' ,{'class': 'yt-uix-tile-link'})
    playarray = []
    q = 0
    while q < len(playlistitle):
        if q == 0:
            q += 1
            continue
        else:
            playarray.append(playlistitle[q].contents[0].strip())
            print(q,'.',playarray[q-1])
            q += 1
    watchlinklist = []
    for watchlinks in soup2.findAll('a', href = True):
        if '/playlist' in watchlinks['href'] and 'googleads' not in watchlinks['href']:
            watchlinklist.append(watchlinks['href'])
        else:
            pass
    print('Which playlist would you like? Enter the number:')
    ans1 = input()
    global enteredplaylist
    if len(playarray) == 19:
        enteredplaylist = 'https://www.youtube.com'+watchlinklist[int(ans1)]
    else:
        enteredplaylist = 'https://www.youtube.com' + watchlinklist[int(ans1)-1]
def get_songs():
    r = requests.get(enteredplaylist)  #will change eventually to make program dynamic
    r = r.text  #organizes into more orderly text for BeautifulSoup
    global soup
    soup = BeautifulSoup(r, 'html.parser') #move to BSoup for class searchin
    global vids
    vids = soup.findAll('a', {'class': 'pl-video-title-link'}) #search for class containing video titles
    global linklist
    linklist = []
    for links in soup.findAll('a', href = True):
        if '/watch' in links['href'] and 'index=' in links['href']:  #if link is a watch link, add to the list
            linklist.append(links['href'])
        else:
            pass
    linklist.pop(0)  #for some reason the first link gets added twice, not an error on my part, error in HTML, this removes the duplicate first link
def dlhelper():
    global songnumlist
    songnumlist = []
    thing = True
    while thing == True: #allows for adding multiple songs to DL list
        print('Enter the number of the song you wish to download:')
        songnum = input()
        songnumlist.append(songnum)
        print('Would you like to download any more songs?')
        ans1 = input()
        if 'y' in ans1.lower():
            continue
        elif 'n' in ans1.lower():
            thing = False
        else:
            print('Error, going back to the beginning of the download segment')
            songnumlist = []
    print('You chose to download:')
    z = 0
    while z < len(songnumlist): #janky formula to get # of songs DL-ed
        print(songs[int(songnumlist[z])-1])
        z+= 1

def dlwork():
    for y in songnumlist:
        profile = webdriver.FirefoxProfile()
        profile.set_preference('browser.download.folderList' ,2)
        profile.set_preference('browser.download.manage.showWhenStarting', False)
        profile.set_preference('browser.download.dir', 'C:\\Users\\Josh\\Downloads\\\YoutubeDL')
        profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'audio/mpeg3')
        driver = webdriver.Firefox(firefox_profile=profile)
        #driver.implicitly_wait(2)  # wait because otherwise other parts of loop will not work
        driver.get('http://www.youtube2mp3.cc/')
        input = driver.find_element_by_id('input')
        input.send_keys('www.youtube.com',linklist[int(y)-1])
        button = driver.find_element_by_id('button').click()
        download = driver.find_element_by_id('download').click()
        time.sleep(2)
        driver.quit()

def work():
    print('How many songs do you want to look up?')
    enter = input()
    x = 0
    global songs
    songs = []
    while x < int(enter):
        songs.append(vids[x].contents[0].strip()) #adds song title from previous HTML group to list
        print(x+1,'.', songs[x])
        x += 1
    print('\nDo you want to download any of these songs?')
    ans = input()
    if 'y' in ans.lower():
        dlhelper()
    elif 'n' in ans.lower():
        exit
    else:
        print('Error, breaking')
        exit

if __name__ == "__main__":
    search()
    get_songs()
    work()
    dlwork()
###TODO:Have way to open songs in program like VLC?
###TODO: Make gui with tkinter?
###TODO: Find way to roll out program to everyone including those who do not have python installed
###TODO: Work with git and github
###TODO: Add song search?
###TODO: Exceptions/loops for wrong answers
###TODO: DL entire playlists?