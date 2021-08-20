import os

PWD = os.path.dirname(__file__) # dotfiles abs path
USER = os.environ.get("USER") # username
HOME = os.environ.get("HOME") # username

DOIT_CONFIG = {'default_tasks': ['home', 'config', 'bin']}

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

def task_ranger():
    """Install ranger and dragon for drag and drop from ranger"""
    return {
        'actions':[
            f'pip3 install --user ranger-fm',
            f'git clone https://github.com/mwh/dragon ~/.local/share/dragon',
            f'cd ~/.local/share && make install',
            f'rm -rf ~/.local/share/dragon'
        ],
        'targets':[
            '~/.local/bin/ranger',
            '~/.local/bin/dragon'
            ],
        'clean':[
            'pip3 uninstall ranger-fm',
            'rm -rf ~/.local/bin/dragon'
        ]
    }

def task_vim_plugins():
    return {
        'actions':["git clone https://github.com/VundleVim/Vundle.vim.git "
                   f"{HOME}/.vim/bundle/Vundle.vim",
                   "vim +PluginInstall +qall",
                   "cd ~/.vim/bundle/YouCompleteMe && python3 install.py"
                   ],
        'targets': [f"{HOME}/.vim/bundle/Vundle.vim"],
        'clean': [f'rm -rf {HOME}/.vim/bundle']
    }

def task_neovim():
    return {
            "targets": [f"{HOME}/.local/bin/nvim"],
            "actions": [f'mkdir -p {HOME}/.local/bin',
                        f'curl -fLo {HOME}/.local/bin/nvim https://github.com/neovim/neovim/releases/download/nightly/nvim.appimage',
                        f'ln -s {HOME}/.local/bin/nvim {HOME}/.local/bin/vim',
                        f'chmod +x {HOME}/.local/bin/nvim {HOME}/.local/bin/vim'],
            "clean" : [f'rm {HOME}/.local/bin/nvim {HOME}/.local/bin/vim']
            }

def task_mojibar():
    return {
            "targets":[f"{HOME}/.local/bin/mojibar"],
            "actions":[f"curl -o {HOME}/.local/share/mojibar.zip 'https://github.com/dumbPy/mojibar/releases/download/vim/Mojibar-linux-x64.zip'",
                       f"unzip {HOME}/.local/share/mojibar.zip -d {HOME}/.local/share",
                       f"rm {HOME}/.local/share/mojibar.zip",
                       f"ln -s {HOME}/.local/share/Mojibar-linux-x64/Mojibar {HOME}/.local/bin/mojibar"
                ],
            "clean": [f"rm -rf {HOME}/.local/share/Mojibar-linux-x64 {HOME}/.local/bin/mojibar"]
        }
