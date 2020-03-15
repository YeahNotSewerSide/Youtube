from win32clipboard import *
import pyautogui
#from Words import words
import random
from Youtube import Videos
import time


done = []

def set_to_clipboard(data:str):
    OpenClipboard()
    EmptyClipboard()
    SetClipboardText(data,CF_UNICODETEXT)
    CloseClipboard()

def ctrl_v():
    pyautogui.hotkey('ctrl','v')
    pyautogui.press('enter')



def good_stuff(view_rate=100,req = ''):
    #done = []
    word = req#random.choice(words)
    print(word)
    vid = Videos()
    pgtoken = ''
    itct = ''
    count = 0
    while True:
        
        #print(count)
        data = vid.get_videos(word,pgtoken,itct)
        for key,item in vid.parse_main_videos_info(data).items():
            if item <= view_rate:
                if key in done:
                    continue
                else:
                    #done.append(key)
                    #set_to_clipboard('https://www.youtube.com/watch?v='+key+' ля шо нашел')
                    #ctrl_v()
                    #time.sleep(0.5)
                    return key
        try:
            pgtoken = data[1]['response']['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['continuations'][0]['nextContinuationData']['continuation']
            itct = data[1]['response']['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['continuations'][0]['nextContinuationData']['clickTrackingParams']
        except:
            try:
                pgtoken = data[1]['response']['continuationContents']['itemSectionContinuation']['continuations'][0]['nextContinuationData']['continuation']
                itct = data[1]['response']['continuationContents']['itemSectionContinuation']['continuations'][0]['nextContinuationData']['clickTrackingParams']
            except:
                return ''
        count += 1
    return ''


if __name__ == '__main__':
    
    id = good_stuff(5,'q')
    print('https://www.youtube.com/watch?v='+id)
    input()

    #while True:      
    #    id = good_stuff(5)
    #    print(id)
    #    #break
    #    if id == '':
    #        continue
    #    else:
    #        print(id)
    #        input()
    #    set_to_clipboard('https://www.youtube.com/watch?v='+id+' ля шо нашел')
    #    ctrl_v()
        
