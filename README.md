# ccstatusline-editor

A web-based visual editor for [ccstatusline](https://github.com/sirmalloc/ccstatusline) configuration files.

Instead of hand-editing the JSON config, open this in your browser and drag, drop, and click your status line into shape.

![ccstatusline-editor screenshot](screenshot.png)

## Features

- **Drag-and-drop** widgets within and between status lines
- **Widget palette** — all 85+ widget types grouped and searchable
- **30 Widget Presets** — curated selections for common workflows:
  - Context Watch, Cost Monitor, Project Orientation, Git Full Picture, Token Economy, Focus Mode, Performance Audit, and more
- **68 Color Themes** — named palettes (Ocean, Dracula, Gruvbox, Monokai, Tokyo Night, …)
- **Auto-separators** — insert your chosen separator character between all widgets in one click
- **Max lines** limit — apply presets truncated to a maximum number of status lines
- **Ctrl+S** to save directly to `~/.config/ccstatusline/settings.json`

## Requirements

- Python 3.8+
- Flask

## Install & run

```bash
pip install ccstatusline-editor
ccstatusline-editor
```

Then open http://localhost:5199 in your browser.

By default the editor reads/writes `~/.config/ccstatusline/settings.json`. Point it at a
different file with `--config`:

```bash
ccstatusline-editor --config /path/to/settings.json
```

### Editable install

To hack on the editor itself, install it in editable mode so the `ccstatusline-editor`
command runs straight from your working copy:

```bash
git clone https://github.com/dpc00/ccstatusline-editor.git
cd ccstatusline-editor
pip install -e .
```

## Usage

1. **Palette (left)** — drag a widget type onto any line, or double-click to add to the last line
2. **Lines (centre)** — click a chip to edit its color and metadata; drag to reorder; ✕ to remove
3. **Schemes (toolbar)** — choose a widget preset or color theme and apply in one click
4. **+ Seps (toolbar)** — select a separator character, click to insert between all widgets
5. **Save / Ctrl+S** — writes back to your ccstatusline settings file

## Sublime Text integration

This repo doubles as a Sublime Text package: symlink it into your Packages directory and
you get a command-palette entry and keybinding that launch the editor and open it in your
browser.

```bash
# macOS
ln -s "$(pwd)" "$HOME/Library/Application Support/Sublime Text/Packages/ccstatusline-editor"

# Linux
ln -s "$(pwd)" "$HOME/.config/sublime-text/Packages/ccstatusline-editor"
```

```powershell
# Windows (run as Administrator, or enable Developer Mode for unprivileged symlinks)
New-Item -ItemType SymbolicLink -Path "$env:APPDATA\Sublime Text\Packages\ccstatusline-editor" -Target (Get-Location)
```

Requires `ccstatusline-editor` to already be installed (`pip install ccstatusline-editor` or
the editable install above) and on your `PATH`.

- **Command palette** — "CC Statusline Editor"
- **Keybinding** — <kbd>Ctrl+Alt+L</kbd>
- To point the launched editor at a non-default config path, add to your
  `Preferences.sublime-settings`:

  ```json
  {
      "ccstatusline_config_path": "/path/to/settings.json"
  }
  ```

## License

MIT
