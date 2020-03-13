from win32clipboard import *
import pyautogui
from Words import words
import random
from Youtube import Videos
import time




def good_staff(view_rate=100):
    done = []
    word = random.choice(words)
    print(word)
    vid = Videos()
    pgtoken = ''
    itct = ''
    count = 0
    while True:
        print(count)
        data = vid.get_videos(word,pgtoken,itct)
        for key,item in vid.parse_main_videos_info(data).items():
            if item <= 100:
                if key in done:
                    continue
                else:
                    done.append(key)
                    return key
        try:
            pgtoken = data[1]['response']['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['continuations'][0]['nextContinuationData']['continuation']
            itct = data[1]['response']['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['continuations'][0]['nextContinuationData']['clickTrackingParams']
        except:
            pgtoken = data[1]['response']['continuationContents']['itemSectionContinuation']['continuations'][0]['nextContinuationData']['continuation']
            itct = data[1]['response']['continuationContents']['itemSectionContinuation']['continuations'][0]['nextContinuationData']['clickTrackingParams']
        count += 1
    return ''

def set_to_clipboard(data:str):
    OpenClipboard()
    EmptyClipboard()
    SetClipboardText('https://www.youtube.com/watch?v='+data+' ля шо нашел',CF_UNICODETEXT)
    CloseClipboard()

def ctrl_v():
    pyautogui.hotkey('ctrl','v')
    pyautogui.press('enter')

if __name__ == '__main__':
    while True:      
        id = good_staff(5)
        print(id)    
        set_to_clipboard(id)
        ctrl_v()
        time.sleep(5)
