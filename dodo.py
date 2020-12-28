import os

PWD = os.path.dirname(__file__) # dotfiles abs path
USER = os.environ.get("USER") # username
HOME = os.environ.get("HOME") # username

def task_home():
    """deploy rc file as dotfiles in home"""
    for file in os.listdir(f"{PWD}/home"):
        yield {
            'name': file,
            'actions': [f"ln -s {PWD}/home/{file} {HOME}/.{file}"],
            'targets': [f'{HOME}/.{file}'],
            'clean': [f'rm {HOME}/.{file}']
        }

def task_config():
    """deploy config files inside ~/.config folder"""
    for file in os.listdir(f"{PWD}/config"):
        yield {
            'name': file,
            'actions': [f"ln -s {PWD}/config/{file} {HOME}/.config/{file}"],
            'targets': [f'{HOME}/.config/{file}'],
            'clean': [f'rm {HOME}/.config/{file}']
        }

def task_bin():
    "symlink all bin files into ~/.local/bin"
    for file in os.listdir(f"{PWD}/bin"):
        yield {
            'name': file,
            'actions': [f"ln -s {PWD}/bin/{file} {HOME}/.local/bin/{file}"],
            'targets': [f'{HOME}/.local/bin/{file}'],
            'clean': [f'rm {HOME}/.local/bin/{file}']
        }
