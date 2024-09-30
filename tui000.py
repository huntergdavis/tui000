from textual.app import App
from textual.widgets import Static
from textual.events import Key

class Tui000(App):

    async def on_mount(self) -> None:
        # Create the 9x9 square box
        box_content = "\n".join(["#" * 9 for _ in range(9)])
        box = Static(box_content)

        # Add the box to the view
        await self.view.dock(box, edge="top", size=10)  # 9x9 box plus 1 space

        # Create the menu row with highlighted letters
        menu_content = "([b]S[/b]ave) ([b]L[/b]oad) ([b]G[/b]raveyard) ([b]O[/b]ptions) ([b]Q[/b]uit)"
        menu = Static(menu_content)

        # Add the menu to the bottom
        await self.view.dock(menu, edge="bottom", size=1)

    async def on_key(self, event: Key) -> None:
        # Exit the program when 'q' is pressed
        if event.key.lower() == "q":  # Check for lowercase 'q'
            await self.action_quit()  # Use Textual's built-in quit action

    async def on_ready(self) -> None:
        print("App is ready. Press 'q' to quit.")

if __name__ == "__main__":
    try:
        Tui000.run(log="textual.log")
    except Exception as e:
        print(f"An error occurred: {e}")
    except asyncio.CancelledError:
        print("The application was cancelled.")
