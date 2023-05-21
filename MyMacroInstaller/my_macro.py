import webbrowser
from pynput import keyboard as keyboard
from pynput.keyboard import Key, Controller
import psutil
import time

ctrl_a      = '\\x01'
ctrl_alt_a  = '<65>'
ctrl_tag    = '<192>'
alt         = 'alt' 
shift       = 'shift' 
tag         = '`' 

holdFlags = {
    'shift': False, 
    'alt': False, 
    'ctrl': False, 
    'tag': False, 
    'a': False,
    }
sequentialClicks = {
    'F11': 0, 
    'F12': 0,
    }

def setHoldingFlag(flagName, val): holdFlags[flagName] = val
def setHoldingFlags(flagNames, val): 
    for flag in flagNames: holdFlags[flag] = val
def resetHoldingFlags():
    for flag in holdFlags: holdFlags[flag] = False
def addSequentialClick(counterName): sequentialClicks[counterName] += 1
def resetSequentialClick(counterName): sequentialClicks[counterName] = 0  
def resetSequentialClicks(): 
    for counter in sequentialClicks: sequentialClicks[counter] = 0

def updateSequentialClick(keyName, isKey, event): 
    if (not isRelease(event)):
        return
    if (isKey(event)):    addSequentialClick(keyName)
    else:                   resetSequentialClick(keyName)


keyboard_controller = Controller()

def tap(key):
    time.sleep(0.2)
    k = Controller()
    k.tap(key)

def tapWithCtrl(key):
    time.sleep(0.2)
    k = Controller()
    k.press(Key.ctrl)
    k.tap(key)
    k.release(Key.ctrl)

def tapWithCmd(key):
    time.sleep(0.2)
    k = Controller()
    k.press(Key.cmd)
    k.tap(key)
    k.release(Key.cmd)

def tapWithShift(key):
    time.sleep(0.2)
    k = Controller()
    k.press(Key.shift)
    k.tap(key)
    k.release(Key.shift)

def gotoTab(num):           tapWithCtrl(str(num)) 
def closeTab(num):          
    gotoTab(num)
    time.sleep(1)
    tapWithCtrl('w')

def moveWindow():
    time.sleep(0.5)
    k = Controller()
    k.press(Key.alt)
    k.press(Key.tab)
    k.release(Key.tab)
    k.release(Key.alt)

def closeWindow():
    time.sleep(0.2)
    k = Controller()
    k.press(Key.alt)
    k.press(Key.f4)
    k.release(Key.f4)
    k.release(Key.alt)


def getAllProcesses():    return psutil.process_iter(['pid', 'name'])
def isChrome(proc):     return proc.info['name'] == 'chrome.exe'
def isChromeRunning():  return len(list(filter(isChrome, getAllProcesses()))) > 0

def isRelease(e):   return 'Release' in str(e)
def isPress(e):     return not isRelease(e)

def isA(event):         return '\'a\'' in str(event) 
def isTag(event):       return tag in str(event) 
def isCtrlTag(event):   return ctrl_tag in str(event)
def isCtrlA(event):     return ctrl_a in str(event)
def isCtrlAltA(event):  return ctrl_alt_a in str(event)
def isAlt(event):       return 'alt' in str(event)
def isTag(event):       return '`' in str(event)
def isCtrl(event):      return 'ctrl' in str(event)

def isShift(event):     return event.key == Key.shift
def isF11(event):       return event.key == Key.f11
def isF12(event):       return event.key == Key.f12

def openLink(url):
    webbrowser.open(url)
    time.sleep(1)
def openChrome(): openLink('HTTP:')
def openMoodle():    openLink('https://moodle.bgu.ac.il/moodle/local/mydashboard/')
def openMyButtons(): openLink('https://opsidezi.wixsite.com/my-useful-links')

def login():
    for i in range(9): tap(Key.tab)
    tap(Key.enter)

def loginSameWindow():
    if (not isChromeRunning()): openChrome()
    openMoodle()
    openMyButtons()
    # wait for moodle to load in background
    time.sleep(10)
    # login afte moodle loaded
    k = Controller()
    gotoTab(1)
    login()
    gotoTab(2)
    # wait for login submission to register and then close tab
    time.sleep(4)
    closeTab(1)

def loginNewWindow():
    if (not isChromeRunning()): openChrome()
    openChrome()
    time.sleep(1)
    openMoodle()
    # wait for moodle to load in background
    moveWindow()
    time.sleep(3)
    # login afte moodle loaded
    moveWindow()
    time.sleep(3)
    login()
    # wait for login submission to register and then close tab
    moveWindow()
    time.sleep(3)
    moveWindow()
    closeWindow()


def onControlAltTag():
    if holdFlags['shift']: loginNewWindow()
    else: openMyButtons()
    # reset holdFlags
    resetHoldingFlags()

def onControlAltA():
    tapWithCtrl(Key.f4)
    tapWithShift(Key.f10)
    for i in range(3):
        tap(Key.down)
    tap(Key.enter)
    resetHoldingFlags()

def onF11Trice():
    # send pc to sleep
    tapWithCmd('x')
    tap(Key.up)
    tap(Key.up)
    tap(Key.right)
    tap(Key.down)
    tap(Key.enter)
    resetSequentialClicks()

def onF12Trice():
    # shut down pc
    tapWithCmd('x')
    tap(Key.up)
    tap(Key.up)
    tap(Key.right)
    tap(Key.down)
    tap(Key.down)
    tap(Key.enter)
    resetSequentialClicks()


with keyboard.Events() as events:
    for event in events:
# -----TO TEST THE MACRO--------------------------------
        # break for testing purposes
        # if event.key == Key.esc: 
        #     break
        # if (isRelease(event)):
        #     print(event)
        #     # print only the true holdingFlags
        #     print ({isHolding: flag for isHolding, flag in holdFlags.items() if flag == True})
# ----------------------------------------------------
        # # check if alt ctrl tag is pressed
        if (isRelease(event) and holdFlags['alt'] and holdFlags['ctrl'] and holdFlags['tag'] and holdFlags['shift']): onControlAltTag()
        # if (isRelease(event) and holdFlags['alt'] and holdFlags['ctrl'] and holdFlags['tag']): onControlAltTag()

        # if (isRelease(event) and holdFlags['alt'] and holdFlags['ctrl'] and holdFlags['a']): onControlAltA()

        # # flag if a is pressed
        # if (isA(event)): setHoldingFlag('a', isPress(event))
        # flag if alt is pressed
        if (isAlt(event)): setHoldingFlag('alt', isPress(event))
        # flag if ctrl is pressed
        if (isCtrl(event)): setHoldingFlag('ctrl', isPress(event))
        # # flag if ctrl a is pressed
        # if (isCtrlA(event)): setHoldingFlags(['ctrl', 'a'], isPress(event))
        # # flag if ctrl alt a is pressed
        # if (isCtrlAltA(event)): setHoldingFlags(['ctrl', 'alt', 'a'], isPress(event))

        # flag if shift is pressed
        if (isShift(event)): setHoldingFlag('shift', isPress(event))
        # flag if ctrl tag is pressed
        if (isCtrlTag(event)): setHoldingFlags(['ctrl', 'tag'], isPress(event))
        # flag if tag is pressed
        if (isTag(event)): setHoldingFlag('tag', isPress(event))
        # # count continous presses of F11
        # updateSequentialClick('F11', isF11, event)
        # updateSequentialClick('F12', isF12, event)

        # if (sequentialClicks['F11'] >= 3): onF11Trice()
        # if (sequentialClicks['F12'] >= 3): onF12Trice()
        