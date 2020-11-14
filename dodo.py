import os

PWD = os.path.dirname(__file__) # dotfiles abs path
USER = os.environ.get("USER") # username

def task_home():
    """deploy rc file as dotfiles in home"""
    for file in os.listdir(f"{PWD}/home"):
        yield {
            'name': file,
            'actions': [f"ln -s {PWD}/home/{file} /home/{USER}/.{file}"],
            'targets': [f'/home/{USER}/.{file}'],
            'clean': [f'rm /home/{USER}/.{file}']
        }

def task_config():
    """deploy config files inside ~/.config folder"""
    for file in os.listdir(f"{PWD}/config"):
        yield {
            'name': file,
            'actions': [f"ln -s {PWD}/config/{file} /home/{USER}/.config/{file}"],
            'targets': [f'/home/{USER}/.config/{file}'],
            'clean': [f'rm /home/{USER}/.config/{file}']
        }

def task_bin():
    "symlink all bin files into ~/.local/bin"
    for file in os.listdir(f"{PWD}/bin"):
        yield {
            'name': file,
            'actions': [f"ln -s {PWD}/bin/{file} /home/{USER}/.local/bin/{file}"],
            'targets': [f'/home/{USER}/.local/bin/{file}'],
            'clean': [f'rm /home/{USER}/.local/bin/{file}']
        }
