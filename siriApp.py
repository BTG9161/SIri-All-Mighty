from functions.execute_tool_call import player
from queue import Queue
from textual import work
from functions.STT import STT
from Siri2 import handle_prompt
from functions.player import Player
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer, Horizontal
from textual.widgets import Static, Markdown, TextArea, Button, LoadingIndicator

input_queue = Queue()

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
            global voice_prompt, prompt

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

                self.text = ""
                
            elif event.key == "shift+enter":
                self.insert("\n")


class SiriVoice(Button):
    def on_button_pressed(self, event: Button.Pressed):
        self.loading = True
        global voice_prompt
        
        voice_prompt = ""
        
        voice_prompt = STT()
        

        siriInput = self.app.query_one(SiriInput)
        siriInput.insert(voice_prompt)
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


class SiriApp(App):
    def __init__(self):
        super().__init__()
        self.spin: bool

    @work(thread=True)
    def process_prompt(self, prompt):
        handler = handle_prompt(prompt)
        return handler

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
        yield SiriVoice(label="Voice",  id="SiriInput")
        yield Player_Button(label="Pause/Play", id="Player")



if __name__ == "__main__":
    SiriApp().run()

