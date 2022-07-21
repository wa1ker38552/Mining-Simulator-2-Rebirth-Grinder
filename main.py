import pyautogui as computer
from threading import Thread
from PIL import Image
import pytesseract
import keyboard
import random
import time

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe'

computer.alert('Click to start grinding')
computer.click()
res = computer.size()

# declare variables
blocks_dug = 0

backpack_size = 660000
blocks_to_check = 5 # check status of backpack after 5 blocks

def go_to(x_ratio, y_ratio):
    computer.moveTo(res.width/x_ratio, res.height/y_ratio)
    time.sleep(0.5)

def surface():
    global res
    go_to(1.05, 1.9)
    # pause before clicking
    time.sleep(0.5)
    computer.click()
    time.sleep(1)

def walk(key, distance):
    keyboard.press(key)
    time.sleep(distance)
    keyboard.release(key)

def dig(distance):
    computer.mouseDown()
    time.sleep(distance)
    computer.mouseUp()

def jump():
    keyboard.press('space')
    time.sleep(0.05)
    keyboard.release('space')

def check_rebirths_required():
    # declare multipliers
    multipliers = {'m': 1000000, 'M': 1000000, 'b': 1000000000, 'B': 1000000000, 't': 1000000000000, 'T': 1000000000000}

    go_to(6.8, 2.7)
    computer.click()
    time.sleep(1)

    # capture screen
    computer.screenshot('image.png', region=(res.width/2.06, res.height/1.6, 150, 70))
    required_rebirth = pytesseract.image_to_string(Image.open('image.png').convert('L'))

    # parse AI output
    required_rebirth = list(filter(None, [char if char in list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
                                               else '.' for char in required_rebirth]))
    for i, char in enumerate(required_rebirth):
        if char in list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'):
            try:
                required_rebirth = float(''.join(required_rebirth[:i]))*multipliers[char]
            except ValueError:
                # AI screenreading failsafe (rebirth exit)
                go_to(1.8, 1.8)
                computer.click()

                go_to(1.55, 3.5)
                computer.click()

                chat('[NOTIFICATION]: AI rebirth scan failed! (exiting...)')
                return 0

    # close out
    go_to(1.55, 3.5)
    computer.click()

    return round(required_rebirth)

def check_coins():
    # declare multipliers
    multipliers = {'m': 1000000, 'M': 1000000, 'b': 1000000000, 'B': 1000000000, 't': 1000000000000, 'T': 1000000000000}

    computer.screenshot('image.png', region=(res.width/17.75, res.height/2, 150, 45))
    coins = pytesseract.image_to_string(Image.open('image.png').convert('L'))

    # parse AI output
    coins = list(filter(None, [char if char in list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
                                    else '.' for char in coins]))
    # 3 -> S failsafe
    if 'S' in coins: coins.replace(coins.index('S'), '3')
    for i, char in enumerate(coins):
        if char in list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'):
            # More failsafe (.. -> . / . .. -> .)
            if '..' in ''.join(coins[:i]):
                coins = float(''.join(coins[:i]).replace('..', '.')) * multipliers[char]
            else:
                coins = float(''.join(coins[:i])) * multipliers[char]
            return round(coins)
    return 0

def rebirth():
    go_to(6.8, 2.7)
    computer.click()
    time.sleep(1)

    go_to(2, 1.5)
    computer.click()
    time.sleep(0.5)

    go_to(2.2, 2.1)
    computer.click()
    time.sleep(2)

def chat(message):
    keyboard.press('/')
    time.sleep(0.5)
    keyboard.release('/')
    computer.write(message)
    time.sleep(0.01*len(message))
    keyboard.press('enter')
    time.sleep(0.5)
    keyboard.release('enter')
    go_to(2, 2)
    computer.click()


while True:
    rebirth_threshold = check_rebirths_required()
    coins_threshold = check_coins()

    chat(f'[NOTIFICATION]: New dig cycle started!')
    chat(f'[LOGGING]: Rebirths: {rebirth_threshold}')
    chat(f'[LOGGING]: Coins: {coins_threshold}')

    # initiate move-dig-sell loop
    while rebirth_threshold > coins_threshold:
        # position player
        surface()

        # move to start of mine
        walk('s', 0.8)

        # move randomly to location
        for i in range(3):
            walk('s', float(f'0.{random.randint(1,9)}'))
            if random.randint(1,2) == 1:
                Thread(target=jump).start()

        go_to(2, 2)
        dig(0.5)

        # jiggle movements
        for i in range(5):
            walk('w', 0.08)
            walk('d', 0.08)
            walk('s', 0.08)
            walk('a', 0.08)
        walk('s', 0.08)

        # dig down
        while True:
            dig(0.5*blocks_to_check)

            computer.screenshot('image.png', region=(res.width/22, res.height/2.35, 210, 50))
            blocks_dug = pytesseract.image_to_string(Image.open('image.png'))

            # get only numbers from the generated text
            blocks_dug = list(filter(None, [char if char in list('1234567890') else None for char in blocks_dug]))
            blocks_dug = ''.join(blocks_dug).replace(str(backpack_size), '')

            # check blocks dug
            try:
                if int(blocks_dug) == backpack_size:
                    # sell blocks
                    go_to(2.3, 2)
                    computer.click()

                    time.sleep(1)
                    surface()
                    break
            except ValueError:
                # bad scanning due to grayed out background
                go_to(2.3, 2)
                computer.click()

                time.sleep(1)
                surface()
                break

        time.sleep(0.5)
        coins_threshold = check_coins()
        chat(f'[NOTIFICATION]: Dig cycle ended!')
        chat(f'[LOGGING]: Coins: {coins_threshold}')
        time.sleep(1)

    chat(f'[NOTIFICATION]: Ready to rebirth!')

    # rebirth
    rebirth()
    chat(f'[NOTIFICATION]: Succesfully rebirthed!')
