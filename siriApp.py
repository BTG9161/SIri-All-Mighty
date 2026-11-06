import asyncio
import subprocess
from queue import Queue
from textual import work
from functions.STT import STT
from Siri2 import handle_prompt
from functions.wake import WakeWord
from textual.app import App, ComposeResult
from functions.InputStream import SoundDevice
from functions.eleven_call import eleven_call
from functions.execute_tool_call import player
from textual.containers import ScrollableContainer, Horizontal
from textual.widgets import Static, Markdown, TextArea, Button


audio_input = SoundDevice()
wakeword = WakeWord(audio_input)

input_queue = Queue()

voice_output = False
voice_convo = False

class Spinner(Static):
    def on_mount(self):
        self.spinner_states = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.current_state = 0

        self.update(f"{self.spinner_states[self.current_state]} Running...")
        self.timer = self.set_interval(0.1, self.update_spinner)

    def update_spinner(self):
        self.current_state = (self.current_state + 1) % len(self.spinner_states)
        self.update(f"{self.spinner_states[self.current_state]} Running...")


class SiriInput(TextArea):
    async def on_key(self, event):
        global voice_prompt, prompt, voice_output

        prompt = ""

        terminal = self.app.query_one("#terminal", ScrollableContainer)
        spinner = Spinner()

        input_queue.put(self.text)
        while not input_queue.empty():
            prompt += input_queue.get()


        if event.key == "enter":
            event.prevent_default() 

            text_prompt = self.text

            if text_prompt == "delete":
                handle_prompt(text_prompt)
                await self.app.convo_update(text_prompt, "Memory file deleted!")
                self.text = ""
                return

            if 'bye' in text_prompt.lower():
                worker = self.app.process_prompt(prompt)
                await worker.wait()
                handler = worker.result
                response = handler.response
                await self.app.convo_update(text_prompt, response)
                self.text = ""
                return
            
            self.text = prompt

            await terminal.mount(spinner)
            if prompt is None:
                pass
            else:
                worker = self.app.process_prompt(prompt)
                await worker.wait()
                handler = worker.result

            response = handler.response

            if handler.terminal == None:
                terminal_data = ""
            else:
                terminal_data = handler.terminal
            
            await self.app.convo_update(prompt, response)
            for data in terminal_data:
                await self.app.terminal_update(data)

            await spinner.remove()

            if voice_output:
                eleven_call(response)

                subprocess.Popen(
                    [
                        "mpv",
                        "--no-terminal",
                        "output.mp3",
                    ]
                )

            self.text = ""
            
        elif event.key == "shift+enter":
            self.insert("\n")


class SiriVoice(Button):
    async def on_button_pressed(self, event: Button.Pressed):
        self.loading = True
        global voice_prompt
        
        voice_prompt = ""

        try:
            audio_input.start()
            worker = self.app.stt_worker()
            await worker.wait()

            voice_prompt = worker.result

            siriInput = self.app.query_one(SiriInput)
            siriInput.insert(voice_prompt)

        finally:
            audio_input.stop()
            self.loading = False
        
class Player_Button(Button):
    def __init__(self, *args, **kwargs): # Take the args and kwargs
        super().__init__(*args, **kwargs)# And pass them to the parent class
        self.paused = False

    def on_button_pressed(self, event: Button.Pressed):
        if self.paused:
            player.resume()
            self.paused = False

        else:
            player.pause()
            self.paused = True

class Voice_Acivation_Button(Button):
    def on_button_pressed(self, event: Button.Pressed):
        global voice_output

        if voice_output:
            voice_output = False
        else:
            voice_output = True

class Voice_Convo(Button):
    def on_button_pressed(self, event: Button.Pressed):
        global voice_convo, voice_output

        if voice_convo:
            voice_convo = False
            voice_output = False
            audio_input.stop()

        else:
            voice_convo = True
            voice_output = True

            self.app.wakeword_worker()
            self.app.voice_convo_worker()


class SiriApp(App):
    def __init__(self):
        super().__init__()
        self.spin: bool

    @work(thread=True)
    def process_prompt(self, prompt):
        handler = handle_prompt(prompt)
        return handler

    @work(thread=True)
    def stt_worker(self):
        return STT(audio_input)

    @work(thread=True)
    def wakeword_worker(self):
        audio_input.start()
        wakeword.passive_wakeword_detection()
        return wakeword.wake_done

    @work
    async def voice_convo_worker(self):
        global voice_convo, voice_output, voice_prompt

        spinner = Spinner()
        terminal = self.query_one("#terminal", ScrollableContainer)
        siri_input = self.query_one("#user",SiriInput)

        while voice_convo:
            if not wakeword.wake_done:
                await asyncio.sleep(0.1) # We use asyncio because we are in an async function, and we want this to also to be async, and time.sleep() is a blocking function.
                continue

            wakeword.predict = True
            stt = self.stt_worker()
            await stt.wait()
            voice_prompt = stt.result
            siri_input.text = voice_prompt

            await terminal.mount(spinner)
            worker = self.process_prompt(voice_prompt)

            await worker.wait()
            handler = worker.result

            response = handler.response

            if handler.terminal == None:
                terminal_data = ""
            else:
                terminal_data = handler.terminal

            await self.convo_update(voice_prompt, response)
            for data in terminal_data:
                await self.terminal_update(data)
        
            await spinner.remove()

            if voice_output:
                eleven_call(response)

                subprocess.Popen(
                    [
                        "mpv",
                        "--no-terminal",
                        "output.mp3",
                    ]
                )

            siri_input.text = ""

            wakeword.wake_received = True
            while wakeword.wake_received:
                await asyncio.sleep(0.05)

    async def convo_update(self, prompt, response):
        siri = self.query_one("#convo", ScrollableContainer)
        await siri.mount(Static("user> " + prompt, classes="user"))
        await siri.mount(Markdown("Siri> " + response, classes="siri"))

        siri.scroll_end(animate=True)

    async def terminal_update(self, terminal_data):
        terminal = self.query_one("#terminal", ScrollableContainer)
        await terminal.mount(Markdown(terminal_data + "\n", classes="terminal"))

    # When we run the SiriApp, it first reads the CSS as a set of rules and then creates the container according to the rules
    CSS = """
    #convo {
        width: 70%;
        height: 1fr;
        border: round cyan;
        padding: 1;
        }
    
    #terminal {
        width: 30%;
        height: 1fr;
        border: round red;
        padding: 1;
        }
        
    #user {
        width: 1fr;
        height: 30%;
        border: round blue;
        }
    
    #controls {
        height: 4;
        dock: bottom;
        layout: horizontal;
        align: center middle;
        }
    
    #controls Button {
        margin: 0 1;
        }
    
    .user{
        text-align: right;
        padding-left: 35;
        margin: 1 0 1 0;
        }
    
    .siri{
        width: 70%;
        }
        """
      # padding is spaces between the widget's border and its content, padding 1 is 1 cell of space between the border and the content

    def compose(self) -> ComposeResult:
        with Horizontal():
            with ScrollableContainer(id="convo"):
                pass

            with ScrollableContainer(id="terminal"):
                yield Static("Terminal \n")

        yield SiriInput(placeholder="Type here...", id="user")

        # Button tray:
        with Horizontal(id="controls"):
            yield SiriVoice(label="Voice",  id="SiriInput")
            yield Player_Button(label="Pause/Play", id="Player")
            yield Voice_Acivation_Button(label="Toggle Voice", id="Voice_Output")
            yield Voice_Convo(label="Voice Convo", id="Voice_Convo")


if __name__ == "__main__":
    try:
        SiriApp().run()
    except Exception as e:
        print(f"Error: {e}")

