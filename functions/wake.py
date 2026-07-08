from pynput import keyboard
import threading
import queue


current = set()
frames = []
sr = 32000
input_queue = queue.Queue()
type_buffer = ""

wake_key = {keyboard.Key.ctrl, keyboard.Key.shift}
type_key = {keyboard.Key.alt, keyboard.Key.ctrl}


def on_press(key):
    global recording, type_buffer
    current.add(key)

    if key == keyboard.Key.enter:
        if type_buffer.strip():
            input_queue.put(type_buffer.strip())
        type_buffer = ""
    
    elif key == keyboard.Key.space:
        type_buffer += " "
    
    elif key == keyboard.Key.backspace:
        type_buffer -= type_buffer[-1]
    
    elif hasattr(key, "char") and key.char is not None: # 'a', 'b', 1, $, etc have .char attr(which is set to the char), and ctrl+D also have a char attr, but it is set to None.
        type_buffer += key.char


def wake_on_release(key):
    if all(k in current for k in wake_key):
        wake_listener.stop()
    
    if key in current:
        current.discard(key)

def type_on_release(key):
    if all(k in current for k in type_key):
        type_listener.stop()
    
    if key in current:
        current.discard(key)


def wake():
    global wake_listener

    with keyboard.Listener(on_press=on_press, on_release=wake_on_release) as wake_listener:
        wake_listener.join()
    
    return True

def type():
    global type_listener

    with keyboard.Listener(on_press=on_press, on_release=wake_on_release) as type_listener:
        type_listener.join()
    
    return True

