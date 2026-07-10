from pynput import keyboard
import threading
import queue

current = set()
wake_key = {keyboard.Key.ctrl, keyboard.Key.shift}
type_key = {keyboard.Key.ctrl, keyboard.Key.alt}

wake_done = threading.Event()
type_done = threading.Event()
input_queue = queue.Queue()

type_buffer = ""

def on_press(key):
    global type_buffer
    current.add(key)

    if key == keyboard.Key.enter:
        if type_buffer.strip():
            input_queue.put(type_buffer.strip())
        type_buffer = ""
    
    elif key == keyboard.Key.space:
        type_buffer += " "
    
    elif key == keyboard.Key.backspace:
        type_buffer = type_buffer[:-1]

    elif hasattr(key, "char") and key.char is not None:
        type_buffer += key.char

def on_release(key):
    if all(k in current for k in wake_key):
        wake_done.set()
    
    if all(k in current for k in type_key):
        type_done.set()
    
    current.discard(key)

def global_listener():
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    return listener

