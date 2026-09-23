from textual import work
from Siri2 import handle_prompt
from functions.STT import STT
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer, Horizontal
from textual.widgets import Static, Markdown, TextArea, Button


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
            terminal = self.app.query_one("#terminal", ScrollableContainer)
            spinner = Spinner()            
            if event.key == "enter":
                event.prevent_default()
                

                text_prompt = self.text
                if text_prompt == "delete":
                    handle_prompt(text_prompt)
                    self.text = ""
                    return

                prompt = text_prompt# + voice_prompt
                self.text = prompt

                await terminal.mount(spinner)
                worker = self.app.process_prompt(prompt)
                await worker.wait()
                handler = worker.result

                response = handler.response

                if handler.terminal == None:
                    terminal_data = ""
                else:
                    terminal_data = handler.terminal
                
                await self.app.convo_update(prompt, response)
                await self.app.terminal_update(terminal_data)
                await spinner.remove()

                self.text = ""
                
            elif event.key == "shift+enter":
                self.insert("\n")


class Voice(Button):
    def on_button_pressed(self, event: Button.Pressed):
        prompt = STT()


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
        yield Voice(label="Voice",  id="SiriInput")


if __name__ == "__main__":
    SiriApp().run()

