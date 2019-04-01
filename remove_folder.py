# -*- coding: utf-8 -*-

# Copyright (c) 2017 Feras A. Saad <fsaad@mit.edu>
# Released under the MIT License; refer to LICENSE.txt.

import os
import subprocess

import sublime
import sublime_plugin

class prompt_folder_remove(sublime_plugin.WindowCommand):

    def run(self):
        # If user is has a project, do not activate this plugin.
        if 'project' in self.window.extract_variables():
            project = self.window.extract_variables()['project']
            sublime.status_message('Cannot remove folder from %s.' % (project,))
            return None
        self.open_folders = self.window.folders()
        if len(self.open_folders) == 0:
            sublime.status_message('No open folders')
            return
        def on_done(idx):
            if idx < 0:
                return
            foldername = self.open_folders[idx]
            self.window.run_command('remove_folder', {
                'dirs': [foldername]
            })
            sublime.status_message('Removed folder {}'.format(foldername))
            # XXX Add a setting to show again for removing multiple folders.
            # self.open_folders = self.window.folders()
            # self.window.show_quick_panel(self.open_folders, on_done)
        self.window.show_quick_panel(self.open_folders, on_done)


class prompt_folder_add(sublime_plugin.WindowCommand):

    def run(self, **kwargs):
        self.new_window = kwargs.get('new_window', None)
        # XXX Add a user setting to chose whether to initialize the path to
        # that of the current file, or the latest path chosen.
        variables = self.window.extract_variables()
        file_path_current = variables.get('file_path', '')
        file_path_last = self.get_last_path()
        initial_path = file_path_last or file_path_current
        self.current_files = os.listdir(initial_path) \
            if initial_path and os.path.isdir(initial_path) else []
        self.window.show_input_panel(
            'Select folder', initial_path, self.on_done, self.on_change, None)

    def on_change(self, filename):
        filename = os.path.expanduser(filename)
        if filename.endswith('/'):
            if os.path.exists(filename):
                self.current_directory = filename
                self.current_files = sort_file_list(
                    os.listdir(self.current_directory))
                sublime.status_message('|'.join(self.current_files))
            else:
                sublime.status_message('No such folder {}'.format(filename))
        else:
            prefix = os.path.basename(filename)
            self.matches = [f for f in self.current_files if f.startswith(prefix)]
            msg  = '|'.join(self.matches) if self.matches else 'No matches'
            sublime.status_message(msg)

    def on_done(self, filename):
        filename = os.path.expanduser(filename)
        if not os.path.exists(filename):
            if len(self.matches) == 1:
                filename = os.path.join(self.current_directory, self.matches[0])
            else:
                sublime.status_message('No such file {}'.format(filename))
        if os.path.exists(filename):
            self.last_path = filename
            if self.new_window:
                self.on_done_new(filename)
            else:
                self.on_done_add(filename)

    def on_done_add(self, filename):
        if os.path.isdir(filename):
            config = {'follow_symlinks': True, 'path': filename}
            data = self.window.project_data()
            if not data:
                data = {'folders': [config]}
                self.window.set_project_data(data)
            else:
                data['folders'].append(config)
                self.window.set_project_data(data)
            sublime.status_message('Added folder {}'.format(filename))
        else:
            self.window.open_file(filename)

    def on_done_new(self, filename):
        if filename.endswith('.sublime-project'):
            subprocess.Popen(['subl', '--project', filename])
        else:
            subprocess.Popen(['subl', '-n', filename])

    def get_last_path(self):
        if hasattr(self, 'last_path'):
            return self.last_path
        self.last_path = None
        return self.last_path

def sort_file_list(filenames):
    hidden = [f for f in filenames if f.startswith('.')]
    regular = [f for f in filenames if not f.startswith('.')]
    result = sorted(regular) + sorted(hidden)
    # XXX Hack make a better way to ignore files.
    return [r for r in result if not r.endswith('.sublime-workspace')]
