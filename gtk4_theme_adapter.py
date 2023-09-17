#!/usr/bin/env python3

"""
GTK4ThemeAdapter
"""

import sys
import os
import subprocess as sp

HOME_DIR = os.getenv('HOME')
CONFIG_DIR = f"{HOME_DIR}/.config"
USER_THEMES_DIR = f"{HOME_DIR}/.themes"
SYSTEM_THEMES_DIR = "/usr/share/themes"
GTK_DIR = f"{CONFIG_DIR}/gtk-4.0"


def run_command(command, action, error_msg=None, suppress_errors=False):
    """Helper function to run a command and handle errors."""
    result = sp.run(command, stdout=sp.PIPE, stderr=sp.PIPE)

    if result.returncode != 0 and not suppress_errors:
        error = error_msg if error_msg else result.stderr.decode("UTF-8").strip()
        print(f"Error during {action}: {error}")

    return result.returncode == 0


def get_all_themes():
    """Fetches themes from both user and system directories and checks their GTK 4.0 support."""
    user_themes, system_themes = [], []

    if os.path.exists(USER_THEMES_DIR):
        user_themes = [(theme, os.path.exists(f"{USER_THEMES_DIR}/{theme}/gtk-4.0")) for theme in
                       os.listdir(USER_THEMES_DIR)]

    if os.path.exists(SYSTEM_THEMES_DIR):
        system_themes = [(theme, os.path.exists(f"{SYSTEM_THEMES_DIR}/{theme}/gtk-4.0")) for theme in
                         os.listdir(SYSTEM_THEMES_DIR)]

    return user_themes, system_themes


def reset_theme():
    print("Resetting to default theme...")
    paths_to_remove = [
        f"{GTK_DIR}/gtk.css",
        f"{GTK_DIR}/gtk-dark.css",
        f"{GTK_DIR}/assets",
        f"{CONFIG_DIR}/assets"
    ]
    for path in paths_to_remove:
        run_command(["rm", path], action="theme reset")


def install_theme(theme_name, is_system_theme):
    source_dir = SYSTEM_THEMES_DIR if is_system_theme else USER_THEMES_DIR
    print(f"Setting theme to: {theme_name}")

    links_to_create = {
        f"{source_dir}/{theme_name}/gtk-4.0/gtk.css": f"{GTK_DIR}/gtk.css",
        f"{source_dir}/{theme_name}/gtk-4.0/gtk-dark.css": f"{GTK_DIR}/gtk-dark.css",
        f"{source_dir}/{theme_name}/gtk-4.0/assets": f"{GTK_DIR}/assets",
        f"{source_dir}/{theme_name}/assets": f"{CONFIG_DIR}/assets"
    }

    success = True
    for src, dest in links_to_create.items():
        if not os.path.exists(src):  # Check if the source file/folder exists before linking
            continue
        if not run_command(["ln", "-s", src, dest], action="theme installation",
                           error_msg=f"Failed to link {src} to {dest}", suppress_errors=True):
            success = False

    if success:
        print("Theme applied successfully.")
    else:
        print(f"Theme {theme_name} applied, albeit some files might be missing or could not be linked.")


def main():
    try:
        if "--reset" in sys.argv:
            reset_theme()
            return

        user_themes, system_themes = get_all_themes()

        if not user_themes and not system_themes:
            print("Neither user themes nor system themes directory was found. Exiting...")
            return

        print("Select theme:")

        i = -1  # Initialize i to cater for the case where there are no user themes
        for i, (theme, supported) in enumerate(user_themes):
            support_str = "Supported" if supported else "Not Supported"
            print(f'{i + 1}. {theme} (User) - {support_str}')

        for j, (theme, supported) in enumerate(system_themes, start=i + 1):
            support_str = "Supported" if supported else "Not Supported"
            print(f'{j + 1}. {theme} (System) - {support_str}')

        print(f"{j + 2}. Exit (or 'q')")
        choice = input("Your choice [Exit]: ").strip().lower()

        if not choice or choice in ['exit', 'q', str(j + 2)]:
            print("Exiting...")
            return

        theme_index = int(choice) - 1
        is_system_theme = theme_index > i
        chosen_theme, supported = system_themes[theme_index - i - 1] if is_system_theme else user_themes[theme_index]

        if not supported:
            print(f"Theme '{chosen_theme}' does not have complete GTK 4.0 support. Proceed with caution!")
            proceed = input("Do you want to continue? (y/n) [n]: ").strip().lower()
            if not proceed or proceed != 'y':
                print("Theme installation aborted.")
                return

        install_theme(chosen_theme, is_system_theme)

    except ValueError:
        print("Incorrect value! Please try again.")


if __name__ == "__main__":
    main()
