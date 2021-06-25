# This is a sample commands.py.  You can add your own commands here.
#
# Please refer to commands_full.py for all the default commands and a complete
# documentation.  Do NOT add them all here, or you may end up with defunct
# commands when upgrading ranger.

# A simple command for demonstration purposes follows.
# -----------------------------------------------------------------------------

from __future__ import (absolute_import, division, print_function)

# You can import any python module as needed.
import os, sys

# You always need to import ranger.api.commands here to get the Command class:
from ranger.api.commands import Command
import re


# Any class that is a subclass of "Command" will be integrated into ranger as a
# command.  Try typing ":my_edit<ENTER>" in ranger!
class my_edit(Command):
    # The so-called doc-string of the class will be visible in the built-in
    # help that is accessible by typing "?c" inside ranger.
    """:my_edit <filename>

    A sample command for demonstration purposes that opens a file in an editor.
    """

    # The execute method is called when you run this command in ranger.
    def execute(self):
        # self.arg(1) is the first (space-separated) argument to the function.
        # This way you can write ":my_edit somefilename<ENTER>".
        if self.arg(1):
            # self.rest(1) contains self.arg(1) and everything that follows
            target_filename = self.rest(1)
        else:
            # self.fm is a ranger.core.filemanager.FileManager object and gives
            # you access to internals of ranger.
            # self.fm.thisfile is a ranger.container.file.File object and is a
            # reference to the currently selected file.
            target_filename = self.fm.thisfile.path

        # This is a generic function to print text in ranger.
        self.fm.notify("Let's edit the file " + target_filename + "!")

        # Using bad=True in fm.notify allows you to print error messages:
        if not os.path.exists(target_filename):
            self.fm.notify("The given file does not exist!", bad=True)
            return

        # This executes a function from ranger.core.acitons, a module with a
        # variety of subroutines that can help you construct commands.
        # Check out the source, or run "pydoc ranger.core.actions" for a list.
        self.fm.edit_file(target_filename)

    # The tab method is called when you press tab, and should return a list of
    # suggestions that the user will tab through.
    # tabnum is 1 for <TAB> and -1 for <S-TAB> by default
    def tab(self, tabnum):
        # This is a generic tab-completion function that iterates through the
        # content of the current directory.
        return self._tab_directory_content()


class open_with(Command):

    def execute(self):
        app, flags, mode = self._get_app_flags_mode(self.rest(1))
        files = self._get_files(self.rest(1))
        if files:
            self.fm.execute_file(
                files = files,
                app=app,
                flags=flags,
                mode=mode)

    def tab(self, tabnum):
        return self._tab_through_executables()

    def _get_files(self, string):
        """Extracts the application, flags, mode and files from a string.
        the files should be passed after `--` double dash. if no file is passed,
        uses self.fm.thistab.get_selection(). supports regex to match file name
        in the current directory
        the `./` before filename or regex is optional except when wanting to open
        current directory
        Note: if no filename is provided after `--`, all files in current directory
        will be returned

        examples:
        If file_A, file_B are in curent tab

        "xdg-open f 1 -- ./" => [self.fm.thisdir]
        "mplayer f 1 -- " => [self.fm.thisdir.files] # all files in cwd
        "editor f 1 -- file_A" => [file_A]
        "editor f 1 -- ./file_A" => [file_A]
        "xdg-open f 1 -- ./file.*" => [file_A, file_B] # regex with ./
        "vim f 1 -- .*_.*" => [file_A, file_B] # regex without ./

        fallback to old method when `--` not in string

        "mplayer f 1" => [self.fm.thistab.get_selection()]
        "atool 4" => [self.fm.thistab.get_selection()]
        "p" => [self.fm.thistab.get_selection()]
        "" => [self.fm.thistab.get_selection()]
        """
        if not "--" in string:
            return [f for f in self.fm.thistab.get_selection()]
        else:
            string = string.split("--")[-1].strip()
            if string.startswith("./"):
                if len(string) > 2:
                    regex_str = string[2:]
                else:
                    return [self.fm.thisdir]
            else:
                regex_str = string
            files =  [f for f in self.fm.thisdir.files
                    if re.match(regex_str, f.basename)]
            if files:
                return files

    def _get_app_flags_mode(self, string):  # pylint: disable=too-many-branches,too-many-statements
        """Extracts the application, flags and mode from a string.

        examples:
        "xdg-open f 1 -- somefile" => ("xdg-open", "f", 1)
        "mplayer f 1" => ("mplayer", "f", 1)
        "atool 4" => ("atool", "", 4)
        "p" => ("", "p", 0)
        "" => None
        """

        app = ''
        flags = ''
        mode = 0
        if '--' in string:
            string = string.split('--')[0].strip()
        split = string.split()

        if len(split) == 1:
            part = split[0]
            if self._is_app(part):
                app = part
            elif self._is_flags(part):
                flags = part
            elif self._is_mode(part):
                mode = part

        elif len(split) == 2:
            part0 = split[0]
            part1 = split[1]

            if self._is_app(part0):
                app = part0
                if self._is_flags(part1):
                    flags = part1
                elif self._is_mode(part1):
                    mode = part1
            elif self._is_flags(part0):
                flags = part0
                if self._is_mode(part1):
                    mode = part1
            elif self._is_mode(part0):
                mode = part0
                if self._is_flags(part1):
                    flags = part1

        elif len(split) >= 3:
            part0 = split[0]
            part1 = split[1]
            part2 = split[2]

            if self._is_app(part0):
                app = part0
                if self._is_flags(part1):
                    flags = part1
                    if self._is_mode(part2):
                        mode = part2
                elif self._is_mode(part1):
                    mode = part1
                    if self._is_flags(part2):
                        flags = part2
            elif self._is_flags(part0):
                flags = part0
                if self._is_mode(part1):
                    mode = part1
            elif self._is_mode(part0):
                mode = part0
                if self._is_flags(part1):
                    flags = part1

        return app, flags, int(mode)

    def _is_app(self, arg):
        return not self._is_flags(arg) and not arg.isdigit()

    @staticmethod
    def _is_flags(arg):
        from ranger.core.runner import ALLOWED_FLAGS
        return all(x in ALLOWED_FLAGS for x in arg)

    @staticmethod
    def _is_mode(arg):
        return all(x in '0123456789' for x in arg)


class fzf_select(Command):
    """
    :fzf_select

    Find a file using fzf.

    With a prefix argument select only directories.

    See: https://github.com/junegunn/fzf
    """
    def execute(self):
        import subprocess
        import os.path
        if self.quantifier:
            # match only directories
            command="find -L . \( -path '*/\.*' -o -fstype 'dev' -o -fstype 'proc' \) -prune \
            -o -type d -print 2> /dev/null | sed 1d | cut -b3- | fzf +m"
        else:
            # match files and directories
            command="find -L . \( -path '*/\.*' -o -fstype 'dev' -o -fstype 'proc' \) -prune \
            -o -print 2> /dev/null | sed 1d | cut -b3- | fzf +m"
        fzf = self.fm.execute_command(command, universal_newlines=True, stdout=subprocess.PIPE)
        stdout, stderr = fzf.communicate()
        if fzf.returncode == 0:
            fzf_file = os.path.abspath(stdout.rstrip('\n'))
            if os.path.isdir(fzf_file):
                self.fm.cd(fzf_file)
            else:
                self.fm.select_file(fzf_file)

class code(Command):
  """
  :code
  Opens current directory in VSCode
  """

  def execute(self):
    dirname = self.fm.thisdir.path
    codecmd = ["code", dirname]
    self.fm.execute_command(codecmd)

class print(Command):
    """
    :print <options>
    prints the selected files with lp command using default printer.
    supports options for lp command
    make sure you set the default printer on cups ui on http://localhost:631/printers
    """
    def execute(self):
        import subprocess
        from ranger.ext.shell_escape import shell_escape as esc
        selections = self.fm.thistab.get_selection()
        paths = [esc(selection.path) for selection in selections]
        subprocess.run("lp -s "+self.rest(1)+" -- "+" ".join(paths), shell=True)

    def tab(self, tabnum):
        options = ["-P"] # output page number. see `man lp` for more
        return (self.start(1) + option for option in options)
        