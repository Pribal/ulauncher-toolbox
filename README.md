# Ulauncher Toolbox Manager

A fast and lightweight [Ulauncher](https://ulauncher.io/) extension to quickly search, filter, and enter your **Toolbox** or **Distrobox** containers directly from your favorite terminal.

## 🚀 Features

* **Instant Search**: List all your containers with a simple keyword.
* **Fuzzy Filtering**: Quickly find the right toolbox by typing its name.
* **Container Management**: Create or remove toolboxes directly from the search bar.
* **Terminal Choice**: Support for multiple terminal emulators (Kitty, Alacritty, WezTerm, etc.).
* **Smart Defaults**: Uses `xdg-terminal-exec` by default for better Linux desktop integration.

## 📦 Installation

1. Open Ulauncher Settings.
2. Go to the **Extensions** tab.
3. Click **Add Extension**.
4. Paste the following URL:
`https://github.com/Pribal/ulauncher-toolbox`

## ⚙️ Configuration

| Preference | Default | Description |
| --- | --- | --- |
| **Keyword** | `tb` | The trigger for the extension. |
| **Terminal** | `auto` | Select your preferred terminal emulator to launch the session. |
| **Image** | `''` | The default image used when creating a new toolbox. |
| **Enter Command** | `toolbox enter` | The command used to enter the container. You can use `%name` in command to refer to the toolbox name |

## 🛠 Usage

### Basic Commands

* **Search & Enter**: Type `tb` followed by the name of your toolbox. Press `Enter` to open it.
* **Create**: Type `tb create <name>` to initialize a new container.
* **Remove**: Type `tb rm <name>` to delete an existing container.

## 🤝 Requirements

* [Toolbox](https://github.com/containers/toolbox) or [Distrobox](https://github.com/89luca89/distrobox) installed.
* A supported terminal emulator.
