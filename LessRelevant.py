from win32clipboard import *
import pyautogui
#from Words import words
import random
from Youtube import Videos
import time


#done = []

def set_to_clipboard(data:str):
    OpenClipboard()
    EmptyClipboard()
    SetClipboardText(data,CF_UNICODETEXT)
    CloseClipboard()

def ctrl_v():
    pyautogui.hotkey('ctrl','v')
    pyautogui.press('enter')



def good_stuff(view_rate=100,req = ''):
    done = []
    word = req#random.choice(words)
    print(word)
    vid = Videos()
    while True:
        
        #print(count)
        try:
            data = vid.get_videos(word)
        except:
            data = vid.get_videos(word)

        for key,item in vid.parse_main_videos_info(data[0]).items():
            if item <= view_rate:
                if key in done:
                    continue
                else:
                    done.append(key)
        if not data[1]:
            break
    return done


if __name__ == '__main__':
    
    while True:
        try:
            stuf = good_stuff(req = None)
        except Exception as e:
            input(e)
