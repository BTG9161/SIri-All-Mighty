from Siri2 import handle_prompt
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer, Horizontal
from textual.widgets import Static, Input, TextArea

class SiriInput(TextArea):
    def on_key(self, event):
            global user_input
            if event.key == "enter":
                event.prevent_default()

                prompt = self.text

                handle_prompt(prompt)
                self.text = ""
                
            elif event.key == "shift+enter":
                self.text + "\n"

class SiriApp(App):

    # When we run the SiriApp, it first reads the CSS as a set of rules and then creates the container according to the rules
    CSS = """
    #siri {
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
        """
      # padding is spaces widget's border and its content, padding 1 is 1 cell of space between the border and the content

    def compose(self) -> ComposeResult:
        global user_input
        with Horizontal():
            with ScrollableContainer(id="siri"):
                yield Static("Siri>")

            with ScrollableContainer(id="terminal"):
                yield Static("Terminal")

        yield SiriInput(placeholder="Type here...", id="user")

    async def siri_response(self, response):
        siri = self.query_one("#siri", ScrollableContainer)
        await siri.mount(Static(response))

        self.siri_response("Hi")


if __name__ == "__main__":
    SiriApp().run()

