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
            'pip3 install --user ranger-fm',
            'git clone https://github.com/mwh/dragon ~/.local/share/dragon',
            'cd ~/.local/share && make install',
            'rm -rf ~/.local/share/dragon'
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
    """Install Vim plugins and YouCompleteMe"""
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
    """Fetch neovim"""
    return {
            "targets": [f"{HOME}/.local/bin/nvim"],
            "actions": [f'mkdir -p {HOME}/.local/bin',
                        f'curl -fLo {HOME}/.local/bin/nvim https://github.com/neovim/neovim/releases/download/nightly/nvim.appimage',
                        f'ln -s {HOME}/.local/bin/nvim {HOME}/.local/bin/vim',
                        f'chmod +x {HOME}/.local/bin/nvim {HOME}/.local/bin/vim'],
            "clean" : [f'rm {HOME}/.local/bin/nvim {HOME}/.local/bin/vim']
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
