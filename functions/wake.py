from pynput import keyboard


current = set()
frames = []
sr = 32000

wake_key = {keyboard.Key.ctrl, keyboard.Key.shift}
def on_press(key):
    global recording
    current.add(key)

    if all(k in current for k in wake_key):
        print('Pressed...')

def on_release(key):
    global prompt
    if key in current:
        current.discard(key)
    
    if key in wake_key:
        listener.stop()
        prompt = ""


def wake():
    global listener

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    
    return True


