import subprocess
import logging
import shlex

class Toolbox:
    """
    Class for toolbox
    """

    ##############
    # Attributes #
    ##############
    TERMINAL_COMMANDS = {
        "auto": "xdg-terminal-exec",
        "kitty": "kitty --",
        "alacritty": "alacritty -e",
        "wezterm": "wezterm start --",
        "foot": "foot",
        "st": "st -e",
        "urxvt": "urxvt -e",
    }
    """Mapping of supported terminals to their commands"""

    # Ulauncher preferences
    terminal: str = "auto"
    """Terminal where to enter the toolbox"""

    image: str = ""
    """Podman image to base the toolbox on"""

    enter_command: str = "toolbox enter"
    """
    Command to enter the toolbox. Can contain '%name' to refer to toolbox name
    """

    # Logger
    logger: logging.Logger = logging.getLogger(__name__)

    ###########
    # Setters #
    ###########
    def setTerminal(self, terminal: str):
        self.terminal = terminal

    def setImage(self, image: str):
        self.image = image

    def setEnterCommand(self, enter_command: str):
        self.enter_command = enter_command

    #########
    # Utils #
    #########
    def get_toolbox_names(self) -> list[str]:
        """
        Get all toolboxes installed on the host

        Returns:
            a list of all toolboxes names
        """
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

            # Return a list of all toolboxes names
            return [n for n in result.stdout.strip().split("\n") if n]
        except Exception as e:
            # Log the error
            self.logger.error(e)

            # Return an empty list
            return []

    ###########
    # Methods #
    ###########
    def get_enter_command(self, toolboxName: str) -> str:
        """Returns the shell command to open the toolbox in a terminal"""
        terminal_bin = self.TERMINAL_COMMANDS.get(self.terminal, "xdg-terminal-exec")
    
        if '%name' in self.enter_command:
            user_cmd = self.enter_command.replace('%name', toolboxName)
        else:
            user_cmd = f"{self.enter_command} {toolboxName}"

        return f'{terminal_bin} sh -c {shlex.quote(user_cmd)}'

    def get_create_command(self, toolboxName: str) -> str:
        """Returns the shell command to create a toolbox in background"""
        safe_name = shlex.quote(toolboxName)
        img_flag = f"--image {shlex.quote(self.image)}" if self.image else ""
                
        return f"sh -c 'toolbox create {img_flag} -y {safe_name}' > /dev/null 2>&1 &"
    
    def get_remove_command(self, toolboxName: str) -> str:
        """Returns the shell command to remove a toolbox"""
        safe_name = shlex.quote(toolboxName)

        return f"sh -c 'toolbox rm -f {safe_name}' &"
