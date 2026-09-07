from Siri2 import handle_prompt
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer, Horizontal
from textual.widgets import Static, Markdown, TextArea, LoadingIndicator


class Spinner(Static):
    def on_mount(self):
        self.spinner_states = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.current_state = 0

        self.update(f"{self.spinner_states[self.current_state]} Running...")
        self.set_interval(0.1, self.update_spinner)

    def update_spinner(self):
        self.current_state = (self.current_state + 1) % len(self.spinner_states)
        self.update(self.spinner_states[self.current_state])

class SiriInput(TextArea):
    async def on_key(self, event):
            global prompt
            if event.key == "enter":
                event.prevent_default()

                prompt = self.text
                if prompt == "delete":
                    handle_prompt(prompt)
                    return

                response = handle_prompt(prompt)
                await self.app.convo_update(prompt, response)
                self.text = ""
                
            elif event.key == "shift+enter":
                self.insert("\n")

class SiriApp(App):
    async def convo_update(self, prompt, response):
        siri = self.query_one("#convo", ScrollableContainer)
        await siri.mount(Static("user> " + prompt, classes="user"))
        await siri.mount(Markdown("Siri> " + response, classes="convo"))

        siri.scroll_end(animate=True)

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
      # padding is spaces widget's border and its content, padding 1 is 1 cell of space between the border and the content

    def compose(self) -> ComposeResult:
        with Horizontal():
            with ScrollableContainer(id="convo"):
                pass

            with ScrollableContainer(id="terminal"):
                yield Static("""Siri Terminal
                Here\u2019s a more detHere\u2019s a more detailed look at how you can use a header with points underneath:\n\n### 1. Organizing Content  \n- **Clear hierarchy:** A header creates a visual anchor, making it easy to see where a section starts and ends.  \n- **Logical grouping:** Related bullet points or numbered items stay together, helping readers follow the flow.\n\n### 2. Outlining Essays or Reports  \n- **Structure:** Use headers for each major section (e.g., Introduction, Methods, Results).  \n- **Sub\u2011points:** List the key ideas you\u2019ll cover in each section, which can later become paragraphs.\n\n### 3. Creating Checklists & To\u2011Do Lists  \n- **Actionable items:** Each point can be a task, and the header tells you what the list is for (e.g., \u201cMorning Routine\u201d).  \n- **Progress tracking:** You can tick off items as you complete them.\n\n### 4. Summarizing Information  \n- **Quick reference:** A header like \u201cKey Takeaways\u201d followedailed look at how you can use a header with points underneath:\n\n### 1. Organizing Content  \n- **Clear hierarchy:** A header creates a visual anchor, making it easy to see where a section starts and ends.  \n- **Logical grouping:** Related bullet points or numbered items stay together, helping readers follow the flow.\n\n### 2. Outlining Essays or Reports  \n- **Structure:** Use headers for each major section (e.g., Introduction, Methods, Results).  \n- **Sub\u2011points:** List the key ideas you\u2019ll cover in each section, which can later become paragraphs.\n\n### 3. Creating Checklists & To\u2011Do Lists  \n- **Actionable items:** Each point can be a task, and the header tells you what the list is for (e.g., \u201cMorning Routine\u201d).  \n- **Progress tracking:** You can tick off items as you complete them.\n\n### 4. Summarizing Information  \n- **Quick reference:** A header like \u201cKey Takeaways\u201d followed""")
                yield LoadingIndicator(id="loading", )

        yield SiriInput(placeholder="Type here...", id="user")


if __name__ == "__main__":
    SiriApp().run()

