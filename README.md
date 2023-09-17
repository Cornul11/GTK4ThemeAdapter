# GTK4ThemeAdapter

Easily enable older GTK themes to the GTK 4.0 environment, including Libadwaita interfaces.

## Description

**GTK4ThemeAdapter** is a convenient command-line tool designed to bridge the gap between older GTK themes such
as [Dracula](https://github.com/dracula/gtk) and the modern GTK 4.0 UI components, such as the new Libadwaita. With this
tool, users can ensure a consistent look across their GNOME applications, including native apps like Nautilus, GNOME
Settings, and more.

## Features

- Automatically list themes from `~/.themes` and `/usr/share/themes`.
- Seamlessly apply older themes to GTK 4.0 UI components.
- Intuitive reset feature to revert to the default theme.
- User-friendly CLI with clear and concise prompts.

## Prerequisites

- Python 3.x
- Themes located in either `~/.themes` or `/usr/share/themes`

## Usage

### Directly Running the Script

```bash
chmod +x ./gtk4_theme_adapter.py
./gtk4_theme_adapter.py
```

### Running using Python

```bash
python3 gtk4_theme_adapter.py
```

### Arguments

- `--reset`: Conveniently resets the theme to its default.

### Instructions

1. Run the script.
2. Choose from a list of available themes. Themes sourced from `~/.themes` are labeled `(User)`, whereas those
   from `/usr/share/themes` are labeled `(System)`.
3. Input the number corresponding to your preferred theme.
4. To exit without making changes, either hit `Enter`, type `q`, or select the `Exit` option.  
