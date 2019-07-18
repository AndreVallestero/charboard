import os
from os import listdir
from os.path import isfile, join
from ctypes import windll

def char_matches_keys(char, keyList):
    if char.upper() in keyList:
        return True
    try:
        return bool(keyboardState[CHAR_DICT[char]])
    except:
        return False

WORKING_DIR = os.getcwd()
RES_DIR = "res//"
CHAR_DICT = {"+": 16, # Shift key
             "^": 17, # Control key
             "!": 18, # Alt key
             "#": 91} # Windows Key

keyboardState = None
oldKeyboardState = [0] * 256

while True:
    resFiles = [file for file in listdir(RES_DIR) if isfile(join(RES_DIR, file))]
    
    keyboardState = [windll.user32.GetAsyncKeyState(i) & 0x8000 for i in range(256)]
    pressedKeys = [chr(i) for i in range(256) if (not oldKeyboardState[i] and keyboardState[i])]

    if len(pressedKeys):
        for file in resFiles:
            filename, ext = os.path.splitext(file)

            for char in filename:
                if not char_matches_keys(char, pressedKeys):
                    break
            else:
                print("Match found for " + file)
                os.startfile(WORKING_DIR + "\\" + RES_DIR + file)
                
    oldKeyboardState = keyboardState
