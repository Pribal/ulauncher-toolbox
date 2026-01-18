# Client
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener

# Events
from ulauncher.api.shared.event import (
    KeywordQueryEvent,
    PreferencesEvent,
    PreferencesUpdateEvent,
)

# UI
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

# Actions
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction

# Toolbox
from toolbox import Toolbox


class ToolBoxExtension(Extension):
    toolbox: Toolbox

    def __init__(self):
        super().__init__()

        self.toolbox = Toolbox()

        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(PreferencesEvent, PreferencesEventListener())
        self.subscribe(PreferencesUpdateEvent, PreferencesUpdateEventListener())


class PreferencesEventListener(EventListener):
    """Initial loading of user preferences"""

    def on_event(self, event, extension):
        # Get preferences
        preferences = event.preferences

        # Get user preferences
        terminal = preferences.get("terminal", "auto")
        image = preferences.get("image", "")
        enter_command = preferences.get("enter_command", "toolbox enter")

        # Set them globally
        extension.toolbox.setTerminal(terminal)
        extension.toolbox.setImage(image)
        extension.toolbox.setEnterCommand(enter_command)


class PreferencesUpdateEventListener(EventListener):
    """Update preferences while the extension is running"""

    def on_event(self, event, extension):
        if event.id == "terminal":
            extension.toolbox.setTerminal(event.new_value)
        elif event.id == "enter_command":
            extension.toolbox.setEnterCommand(event.new_value)
        elif event.id == "image":
            extension.toolbox.setImage(event.new_value)


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        query = event.get_argument() or ""

        if query.startswith("create"):
            name = query.replace("create", "", 1).strip()
            return RenderResultListAction(self.handle_create_toolbox(name, extension))
            
        elif query.startswith("rm"):
            search = query.replace("rm", "", 1).strip()
            return RenderResultListAction(self.handle_remove_toolbox(search, extension))
            
        else:
            return RenderResultListAction(self.handle_enter_toolbox(query.strip(), extension))

    def handle_create_toolbox(
        self, toolboxName: str, extension
    ) -> list[ExtensionResultItem]:
        if not toolboxName:
            return [
                ExtensionResultItem(
                    icon="images/add_toolbox.png",
                    name="Enter a name for the new toolbox...",
                    on_enter=HideWindowAction(),
                )
            ]

        cmd = extension.toolbox.get_create_command(toolboxName)

        return [
            ExtensionResultItem(
                icon="images/add_toolbox.png",
                name=f"Create toolbox {toolboxName}",
                on_enter=RunScriptAction(cmd),
            )
        ]

    def handle_remove_toolbox(
        self, userSearch: str, extension
    ) -> list[ExtensionResultItem]:
        toolboxes = extension.toolbox.get_toolbox_names()
        founded_toolboxes = []

        for toolbox in toolboxes:
            if not userSearch or userSearch in toolbox.lower():
                cmd = extension.toolbox.get_remove_command(toolbox)
                founded_toolboxes.append(
                    ExtensionResultItem(
                        icon="images/remove_toolbox.png",
                        name=f"Remove {toolbox}",
                        on_enter=RunScriptAction(cmd),
                    )
                )

        return founded_toolboxes if founded_toolboxes else self.noToolboxFound()

    def handle_enter_toolbox(
        self, userSearch: str, extension
    ) -> list[ExtensionResultItem]:
        toolboxes = extension.toolbox.get_toolbox_names()
        founded_toolboxes = []

        for toolbox in toolboxes:
            if not userSearch or userSearch in toolbox.lower():
                cmd = extension.toolbox.get_enter_command(toolbox)
                founded_toolboxes.append(
                    ExtensionResultItem(
                        icon="images/icon.png",
                        name=toolbox.capitalize(),
                        description=f"Enter {toolbox}",
                        on_enter=RunScriptAction(cmd),
                    )
                )

        return founded_toolboxes if founded_toolboxes else self.noToolboxFound()

    def noToolboxFound(self) -> list[ExtensionResultItem]:
        return [
            ExtensionResultItem(
                icon="images/icon.png",
                name="No toolbox found",
                on_enter=HideWindowAction(),
            )
        ]


if __name__ == "__main__":
    ToolBoxExtension().run()
