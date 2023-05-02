# Just a little keylogger 

### pip install keybhook

#### Tested against Windows 10 / Python 3.10 / Anaconda

This script allows you to hook into the Windows keyboard events and capture the keys that are pressed on the keyboard.


### How to use it

```python
from keybhook import start_hook, config, VK_CODELETTER
VK_CODELETTER[193] = ('?', False) # adds not mapped chars (https://learn.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes), on my keyboard "?" has the code 193 -  it might be different on yours. (2nd value: True if numpad else False)
config.done = False 
start_hook()
# example
oldlen = 0
co = 0
while True:
    newlen = len(config.results)
    if newlen > oldlen:
        print(config.results[-1]) # prints the last captured letter 
        co += 1

    oldlen = newlen
    if co == 20: 
        config.done # break when we have 20 characters 
        break
# 
# 
# 
# ('letter', 'is_numpad', 'event_code', 'event', 'scan_code', 'flags', 'time')
# ('enter', False, 257, 'KEY_UP', 28, 129, 87485609)
# ('right shift', False, 256, 'KEY_DOWN', 54, 1, 87486906)
# ('h', False, 256, 'KEY_DOWN', 35, 0, 87487062)
# ('h', False, 257, 'KEY_UP', 35, 128, 87487125)
# ('right shift', False, 257, 'KEY_UP', 54, 129, 87487156)
# ('e', False, 256, 'KEY_DOWN', 18, 0, 87487234)
# ('e', False, 257, 'KEY_UP', 18, 128, 87487328)
# ('l', False, 256, 'KEY_DOWN', 38, 0, 87487500)
# ('l', False, 257, 'KEY_UP', 38, 128, 87487593)
# ('l', False, 256, 'KEY_DOWN', 38, 0, 87487640)
# ('l', False, 257, 'KEY_UP', 38, 128, 87487718)
# ('o', False, 256, 'KEY_DOWN', 24, 0, 87487796)
# ('o', False, 257, 'KEY_UP', 24, 128, 87487890)
# ('right shift', False, 256, 'KEY_DOWN', 54, 1, 87488156)
# ('?', False, 256, 'KEY_DOWN', 115, 0, 87488359)
# ('?', False, 257, 'KEY_UP', 115, 128, 87488500)
# ('right shift', False, 257, 'KEY_UP', 54, 129, 87488515)
# ('spacebar', False, 256, 'KEY_DOWN', 57, 0, 87490890)
# ('spacebar', False, 257, 'KEY_UP', 57, 128, 87491000)

```
