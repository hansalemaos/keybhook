import ctypes
from ctypes import wintypes, Structure, POINTER
from time import sleep
import kthread
import sys
from ctypes.wintypes import (
    HANDLE,
    DWORD,
    BOOL,
    ULONG,
    LPARAM,
    WPARAM,
    HINSTANCE,
    HHOOK,
    LPMSG,
    HWND,
)

LPDWORD = POINTER(DWORD)
LPHANDLE = POINTER(HANDLE)
ULONG_PTR = POINTER(ULONG)

kernel32 = ctypes.CDLL("kernel32")
user32 = ctypes.WinDLL("user32", use_last_error=True)


config = sys.modules[__name__]
config.done = False
config.keyboard_hook_id = 0
config.results = []



class KBDLLHOOKSTRUCT(Structure):
    _fields_ = [
        ("vkCode", wintypes.DWORD),
        ("scanCode", wintypes.DWORD),
        ("flags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR),
    ]


# dict from https://pypi.org/project/keyboard/



events = {
    0x100: "KEY_DOWN",
    0x101: "KEY_UP",
    0x104: "KEY_DOWN_SYS",
    0x105: "KEY_UP_SYS",
}

VK_CODELETTER = {
    0x03: ("control-break processing", False),
    0x08: ("backspace", False),
    0x09: ("tab", False),
    0x0C: ("clear", False),
    0x0D: ("enter", False),
    0x10: ("shift", False),
    0x11: ("ctrl", False),
    0x12: ("alt", False),
    0x13: ("pause", False),
    0x14: ("caps lock", False),
    0x15: ("ime kana mode / ime hanguel mode / ime hangul mode ", False),
    0x17: ("ime junja mode", False),
    0x18: ("ime final mode", False),
    0x19: ("ime hanja mode / ime kanji mode", False),
    0x1B: ("esc", False),
    0x1C: ("ime convert", False),
    0x1D: ("ime nonconvert", False),
    0x1E: ("ime accept", False),
    0x1F: ("ime mode change request", False),
    0x20: ("spacebar", False),
    0x21: ("page up", False),
    0x22: ("page down", False),
    0x23: ("end", False),
    0x24: ("home", False),
    0x25: ("left", False),
    0x26: ("up", False),
    0x27: ("right", False),
    0x28: ("down", False),
    0x29: ("select", False),
    0x2A: ("print", False),
    0x2B: ("execute", False),
    0x2C: ("print screen", False),
    0x2D: ("insert", False),
    0x2E: ("delete", False),
    0x2F: ("help", False),
    0x30: ("0", False),
    0x31: ("1", False),
    0x32: ("2", False),
    0x33: ("3", False),
    0x34: ("4", False),
    0x35: ("5", False),
    0x36: ("6", False),
    0x37: ("7", False),
    0x38: ("8", False),
    0x39: ("9", False),
    0x41: ("a", False),
    0x42: ("b", False),
    0x43: ("c", False),
    0x44: ("d", False),
    0x45: ("e", False),
    0x46: ("f", False),
    0x47: ("g", False),
    0x48: ("h", False),
    0x49: ("i", False),
    0x4A: ("j", False),
    0x4B: ("k", False),
    0x4C: ("l", False),
    0x4D: ("m", False),
    0x4E: ("n", False),
    0x4F: ("o", False),
    0x50: ("p", False),
    0x51: ("q", False),
    0x52: ("r", False),
    0x53: ("s", False),
    0x54: ("t", False),
    0x55: ("u", False),
    0x56: ("v", False),
    0x57: ("w", False),
    0x58: ("x", False),
    0x59: ("y", False),
    0x5A: ("z", False),
    0x5B: ("left windows", False),
    0x5C: ("right windows", False),
    0x5D: ("applications", False),
    0x5F: ("sleep", False),
    0x60: ("0", True),
    0x61: ("1", True),
    0x62: ("2", True),
    0x63: ("3", True),
    0x64: ("4", True),
    0x65: ("5", True),
    0x66: ("6", True),
    0x67: ("7", True),
    0x68: ("8", True),
    0x69: ("9", True),
    0x6A: ("*", True),
    0x6B: ("+", True),
    0x6C: ("separator", True),
    0x6D: ("-", True),
    0x6E: ("decimal", True),
    0x6F: ("/", True),
    0x70: ("f1", False),
    0x71: ("f2", False),
    0x72: ("f3", False),
    0x73: ("f4", False),
    0x74: ("f5", False),
    0x75: ("f6", False),
    0x76: ("f7", False),
    0x77: ("f8", False),
    0x78: ("f9", False),
    0x79: ("f10", False),
    0x7A: ("f11", False),
    0x7B: ("f12", False),
    0x7C: ("f13", False),
    0x7D: ("f14", False),
    0x7E: ("f15", False),
    0x7F: ("f16", False),
    0x80: ("f17", False),
    0x81: ("f18", False),
    0x82: ("f19", False),
    0x83: ("f20", False),
    0x84: ("f21", False),
    0x85: ("f22", False),
    0x86: ("f23", False),
    0x87: ("f24", False),
    0x90: ("num lock", False),
    0x91: ("scroll lock", False),
    0xA0: ("left shift", False),
    0xA1: ("right shift", False),
    0xA2: ("left ctrl", False),
    0xA3: ("right ctrl", False),
    0xA4: ("left menu", False),
    0xA5: ("right menu", False),
    0xA6: ("browser back", False),
    0xA7: ("browser forward", False),
    0xA8: ("browser refresh", False),
    0xA9: ("browser stop", False),
    0xAA: ("browser search key", False),
    0xAB: ("browser favorites", False),
    0xAC: ("browser start and home", False),
    0xAD: ("volume mute", False),
    0xAE: ("volume down", False),
    0xAF: ("volume up", False),
    0xB0: ("next track", False),
    0xB1: ("previous track", False),
    0xB2: ("stop media", False),
    0xB3: ("play/pause media", False),
    0xB4: ("start mail", False),
    0xB5: ("select media", False),
    0xB6: ("start application 1", False),
    0xB7: ("start application 2", False),
    0xBB: ("+", False),
    0xBC: (",", False),
    0xBD: ("-", False),
    0xBE: (".", False),
    0xE5: ("ime process", False),
    0xF6: ("attn", False),
    0xF7: ("crsel", False),
    0xF8: ("exsel", False),
    0xF9: ("erase eof", False),
    0xFA: ("play", False),
    0xFB: ("zoom", False),
    0xFC: ("reserved ", False),
    0xFD: ("pa1", False),
    0xFE: ("clear", False),
}

def keyboard_hook(nCode, wParam, lParam):
    if config.done:
        user32.UnhookWindowsHookEx(config.keyboard_hook_id)
        return 0
    if nCode >= 0:
        kb_struct = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents

        vocodeletter = VK_CODELETTER.get(kb_struct.vkCode, "")
        if len(vocodeletter) <2:
            vocodeletter = (kb_struct.vkCode, None)

        config.results.append(
            (
                *vocodeletter,
                wParam,events.get(wParam, ""),
                kb_struct.scanCode,
                kb_struct.flags,
                kb_struct.time,
            )
        )
    return user32.CallNextHookEx(None, nCode, wParam, lParam)


def _start_hook():
    config.results.append(('letter', 'is_numpad', 'event_code', 'event', 'scan_code', 'flags', 'time'))
    keyboard_hook_cb = ctypes.WINFUNCTYPE(
        ctypes.c_int, WPARAM, LPARAM, ctypes.POINTER(ctypes.c_void_p)
    )
    keyboard_hook_ptr = keyboard_hook_cb(keyboard_hook)
    user32.SetWindowsHookExW.argtypes = [
        ctypes.c_int,
        keyboard_hook_cb,
        HINSTANCE,
        DWORD,
    ]
    user32.SetWindowsHookExW.restype = HHOOK
    user32.CallNextHookEx.restype = ctypes.c_int
    user32.UnhookWindowsHookEx.argtypes = [HHOOK]
    user32.UnhookWindowsHookEx.restype = BOOL

    config.keyboard_hook_id = user32.SetWindowsHookExW(13, keyboard_hook_ptr, None, 0)

    user32.GetMessageW.argtypes = [LPMSG, HWND, ctypes.c_uint, ctypes.c_uint]
    user32.GetMessageW.restype = BOOL

    user32.TranslateMessage.argtypes = [LPMSG]
    user32.TranslateMessage.restype = BOOL

    user32.DispatchMessageA.argtypes = [LPMSG]

    try:
        msg = ctypes.wintypes.MSG()
        while (
            user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0
        ) and not config.done:
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageA(ctypes.byref(msg))
        user32.UnhookWindowsHookEx(config.keyboard_hook_id)
    except Exception:
        try:
            user32.UnhookWindowsHookEx(config.keyboard_hook_id)
        except Exception:
            pass

    return


def killcheck(t):
    while t.is_alive():
        sleep(1)
        if config.done:
            sleep(2)
            try:
                if t.is_alive():
                    t.kill()
            except Exception:
                pass

def start_hook():
    t = kthread.KThread(target=_start_hook)
    t.start()
    t2 = kthread.KThread(target=killcheck, args=(t,))
    t2.start()



