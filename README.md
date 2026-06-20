# ccstatusline-editor

A web-based visual editor for [ccstatusline](https://github.com/sirmalloc/ccstatusline) configuration files.

Instead of hand-editing the JSON config, open this in your browser and drag, drop, and click your status line into shape.

![ccstatusline-editor screenshot](screenshot.png)

## Features

- **Drag-and-drop** widgets within and between status lines
- **Widget palette** — all 83+ widget types grouped and searchable
- **30 Widget Presets** — curated selections for common workflows:
  - Context Watch, Cost Monitor, Project Orientation, Git Full Picture, Token Economy, Focus Mode, Performance Audit, and more
- **56 Color Themes** — named palettes (Ocean, Dracula, Gruvbox, Monokai, Tokyo Night, …)
- **Auto-separators** — insert your chosen separator character between all widgets in one click
- **Max lines** limit — apply presets truncated to a maximum number of status lines
- **Ctrl+S** to save directly to `~/.config/ccstatusline/settings.json`

## Requirements

- Python 3.8+
- Flask

## Install & run

```bash
pip install flask
python app.py
```

Then open http://localhost:5199 in your browser.

## Usage

1. **Palette (left)** — drag a widget type onto any line, or double-click to add to the last line
2. **Lines (centre)** — click a chip to edit its color and metadata; drag to reorder; ✕ to remove
3. **Schemes (toolbar)** — choose a widget preset or color theme and apply in one click
4. **+ Seps (toolbar)** — select a separator character, click to insert between all widgets
5. **Save / Ctrl+S** — writes back to your ccstatusline settings file

## License

MIT
