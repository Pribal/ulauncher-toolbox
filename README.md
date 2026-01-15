# Ulauncher Toolbox Manager

A fast and lightweight [Ulauncher](https://ulauncher.io/) extension to quickly search, filter, and enter your **Toolbox** or **Distrobox** containers directly from your favorite terminal.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Ulauncher](https://img.shields.io/badge/Ulauncher-v5.0+-orange.svg)

## 🚀 Features

- **Instant Search**: List all your containers with a simple keyword.
- **Fuzzy Filtering**: Quickly find the right toolbox by typing its name.
- **Terminal Choice**: Support for multiple terminal emulators (Kitty, Alacritty, WezTerm, etc.).
- **Smart Defaults**: Uses `xdg-terminal-exec` by default for better Linux desktop integration.

## 📦 Installation

1. Open Ulauncher Settings.
2. Go to the **Extensions** tab.
3. Click **Add Extension**.
4. Paste the following URL:
   `https://github.com/Pribal/ulauncher-toolbox.git`

## ⚙️ Configuration

| Preference | Default | Description |
|------------|---------|-------------|
| **Keyword** | `tb` | The trigger for the extension. |
| **Terminal**| `auto` | Select your preferred terminal emulator to launch the session. |

## 🛠 Usage

1. Open Ulauncher (default: `Ctrl+Space`).
2. Type `tb` followed by the name of your toolbox.
3. Press `Enter` to open a new terminal window inside the selected container.

## 🤝 Requirements

- [Toolbox](https://github.com/containers/toolbox) or [Distrobox](https://github.com/89luca89/distrobox) installed.
- A supported terminal emulator.