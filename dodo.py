import os
import platform
from doit import task_params

PWD = os.path.dirname(__file__) # dotfiles abs path
USER = os.environ.get("USER") # username
HOME = os.environ.get("HOME") # username
PLATFORM = platform.system() # platform name 'Linux | Darwin'

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
        'actions':(
            [
                'pip3 install --user ranger-fm'
            ] +
            [
                'git clone https://github.com/mwh/dragon ~/.local/share/dragon',
                'cd ~/.local/share && make install',
                'rm -rf ~/.local/share/dragon'
            ] if PLATFORM == "Linux" else [] +
            [   'brew install cocoapods',
                'cd /tmp/ && git clone https://github.com/Wevah/dragterm && cd /tmp/dragterm/dragterm && g++ DTDraggingSourceView.m main.m  -framework Cocoa -o drag',
                'cp /tmp/dragterm/dragterm/drag ~/.local/bin/',
                'rm -rf /tmp/dragterm'
            ] if PLATFORM == 'Darwin' else []
            ),
        'targets':[
            '~/.local/bin/ranger',
            '~/.local/bin/dragon' if PLATFORM=='Linux' else '~/.local/bin/drag'
            ],
        'clean':[
            'pip3 uninstall ranger-fm',
            'rm -f ~/.local/bin/dragon ~/.local/bin/drag'
        ]
    }


def task_vim_plugins():
    """Install Vim plugins"""
    return {
        # 'actions':["git clone https://github.com/VundleVim/Vundle.vim.git "
        'actions':["git clone https://github.com/mckellygit/Vundle.vim.git "
                   f"{HOME}/.vim/bundle/Vundle.vim",
                   "vim +PluginInstall +qall",
                   ],
        'targets': [f"{HOME}/.vim/bundle/Vundle.vim"],
        'clean': [f'rm -rf {HOME}/.vim/bundle']
    }

@task_params([{ 'name': 'tag', 'long':'tag', 'type':str, 'default':'stable'}])
def task_neovim(tag:str):
    """Fetch neovim"""
    print(f"Fetching neovim {tag}")
    return {
            "targets": [f"{HOME}/.local/bin/nvim"],
            "actions": [f'mkdir -p {HOME}/.local/bin',
                        # f'curl -fLo {HOME}/.local/bin/nvim https://github.com/neovim/neovim/releases/download/nightly/nvim.appimage',
                        f'curl -fLo {HOME}/.local/bin/nvim https://github.com/neovim/neovim/releases/download/{tag}/nvim.appimage',
                        f'ln -s {HOME}/.local/bin/nvim {HOME}/.local/bin/vim',
                        f'chmod +x {HOME}/.local/bin/nvim {HOME}/.local/bin/vim']
                        if PLATFORM == "Linux" else [
                        f'mkdir -p {HOME}/.local/bin',
                        # f'curl -fLo {HOME}/.local/nvim.tar.gz https://github.com/neovim/neovim/releases/download/nightly/nvim-macos.tar.gz',
                        # f'curl -fLo {HOME}/.local/nvim.tar.gz https://github.com/neovim/neovim/releases/download/{tag}/nvim-macos-arm64.tar.gz',
                        f'curl -fLo {HOME}/.local/nvim.tar.gz https://github.com/neovim/neovim/releases/download/{tag}/nvim-macos.tar.gz',
                        f'tar -xzf {HOME}/.local/nvim.tar.gz -C {HOME}/.local/bin',
                        f'rm {HOME}/.local/nvim.tar.gz',
                        f'mv {HOME}/.local/bin/nvim-macos* {HOME}/.local/nvim',
                        f'ln -s {HOME}/.local/nvim/bin/nvim {HOME}/.local/bin/nvim',
                        f'ln -s {HOME}/.local/nvim/bin/nvim {HOME}/.local/bin/vim',
                        ],
            "clean" :   [f'rm {HOME}/.local/bin/nvim {HOME}/.local/bin/vim'] if PLATFORM == "Linux" else [
                        f'rm -rf {HOME}/.local/nvim {HOME}/.local/bin/nvim {HOME}/.local/bin/vim'
                        ]
            }

def task_mojibar():
    """Get Mojibar"""
    return {
            "targets":[f"{HOME}/.local/bin/mojibar"],
            "actions":[f"curl -L -o {HOME}/.local/share/mojibar.zip 'https://github.com/dumbPy/mojibar/releases/download/vim.and.currency/Mojibar-linux-x64.zip'",
                       f"unzip {HOME}/.local/share/mojibar.zip -d {HOME}/.local/share",
                       f"rm {HOME}/.local/share/mojibar.zip",
                       f"ln -s {HOME}/.local/share/Mojibar-linux-x64/Mojibar {HOME}/.local/bin/mojibar",
                       "systemctl --user enable mojibar && systemctl --user start mojibar"
                ],
            "clean": [f"rm -rf {HOME}/.local/share/Mojibar-linux-x64 {HOME}/.local/bin/mojibar",
                      "systemctl --user disable mojibar && systemctl --user disable mojibar"
                      ]
        }

def task_nvtop():
    """Get NVTOP
    requires libncurses5 to be preinstalled.
    sudo apt install libncurses5-dev
    """
    return {
            "targets":[f"{HOME}/.local/bin/nvtop"],
            "actions":[f"git clone https://github.com/Syllo/nvtop.git {HOME}/.local/share/nvtop",
                       f"mkdir -p {HOME}/.local/share/nvtop/build && cd {HOME}/.local/share/nvtop/build",
                       f"cd {HOME}/.local/share/nvtop/build && cmake .. -DNVIDIA_SUPPORT=ON -DAMDGPU_SUPPORT=ON && make",
                       f"ln -s {HOME}/.local/share/nvtop/build/src/nvtop {HOME}/.local/bin/nvtop"
                ],
            "clean": [f"rm -rf {HOME}/.local/share/nvtop {HOME}/.local/bin/nvtop",
                      ]
        }

def task_beans():
    """Get Rclone and start the systemd service"""
    return {
            "targets":[f"{HOME}/.local/bin/rclone",
                       f"{HOME}/.local/share/man/man1/rclone.1"
                ],
            "actions":[f"curl -L -o {HOME}/.local/share/rclone.zip 'https://downloads.rclone.org/rclone-current-linux-amd64.zip'",
                       f"unzip {HOME}/.local/share/rclone.zip -d {HOME}/.local/share",
                       f"rm {HOME}/.local/share/rclone.zip",
                       f"mv {HOME}/.local/share/rclone-*-linux-amd64 {HOME}/.local/share/rclone",
                       f"mv {HOME}/.local/share/rclone/rclone {HOME}/.local/bin/rclone",
                       f"chmod +x {HOME}/.local/bin/rclone",
                       f"mv {HOME}/.local/share/rclone/rclone.1 {HOME}/.local/share/man/man1/rclone.1",
                       f"rm -rf {HOME}/.local/share/rclone",
                       "systemctl --user enable rclone && systemctl --user start rclone"
                ],
            "clean": [f"rm {HOME}/.local/bin/rclone {HOME}/.local/share/man/man1/rclone.1",
                      "systemctl --user stop rclone && systemctl --user disable rclone"
                      ]
        }
