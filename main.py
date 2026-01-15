# Ulauncher API
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction

# Libs
import logging
import subprocess

logger = logging.getLogger(__name__)


class ToolBoxExtension(Extension):
    """Main Extension class to handle Ulauncher lifecycle."""

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    """Listener for user keyword input."""

    # Map of terminal IDs to their execution commands
    TERMINAL_COMMANDS = {
        "auto": "xdg-terminal-exec",
        "kitty": "kitty -e",
        "alacritty": "alacritty -e",
        "wezterm": "wezterm start --",
        "foot": "foot",
        "st": "st -e",
        "urxvt": "urxvt -e",
    }

    @staticmethod
    def get_toolbox_names():
        try:
            result = subprocess.run(
                [
                    "podman",
                    "ps",
                    "-a",
                    "--filter",
                    "label=com.github.containers.toolbox=true",
                    "--format",
                    "{{.Names}}",
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            return [name for name in result.stdout.strip().split("\n") if name]
        except Exception:
            return []

    def on_event(self, event, extension):
        # Normalize query input
        query = (event.get_argument() or "").strip().lower()

        # Get terminal preference with a safe fallback
        terminal_key = extension.preferences.get("terminal", "auto")
        terminal_cmd = self.TERMINAL_COMMANDS.get(terminal_key, "xdg-terminal-exec")

        try:
            toolbox_names = self.get_toolbox_names()
        except Exception as e:
            logger.error(f"Failed to fetch toolboxes: {e}")
            return RenderResultListAction(
                [
                    ExtensionResultItem(
                        icon="images/icon.png",
                        name="Error fetching toolboxes",
                        description="Make sure 'toolbox' or 'distrobox' is installed.",
                        on_enter=HideWindowAction(),
                    )
                ]
            )

        items = []

        # Filter and build result items
        for name in toolbox_names:
            if not query or query in name.lower():
                items.append(
                    ExtensionResultItem(
                        icon="images/icon.png",
                        name=name.capitalize(),
                        description=f"Open {name} in {terminal_key}",
                        on_enter=RunScriptAction(
                            f"{terminal_cmd} toolbox enter {name}"
                        ),
                    )
                )

        # Handle empty results
        if not items:
            items.append(
                ExtensionResultItem(
                    icon="images/icon.png",
                    name="No toolboxes found",
                    description="Try a different search term or create a new toolbox.",
                    on_enter=HideWindowAction(),
                )
            )

        return RenderResultListAction(items)


if __name__ == "__main__":
    ToolBoxExtension().run()