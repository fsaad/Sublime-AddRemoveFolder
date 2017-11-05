import os

import sublime
import sublime_plugin

class prompt_folder_remove(sublime_plugin.WindowCommand):

    def run(self):
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

    def run(self):
        self.window.show_input_panel(
            'Select folder', '', self.on_done, self.on_change, None)

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

def sort_file_list(filenames):
    hidden = [f for f in filenames if f.startswith('.')]
    regular = [f for f in filenames if not f.startswith('.')]
    return sorted(regular) + sorted(hidden)
