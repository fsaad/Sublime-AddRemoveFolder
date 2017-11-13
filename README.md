# AddRemoveFolder

Sublime text plugin which provides command palette entries to add or remove a
folder from current project. It is also possible to open a file/folder in a
new window.

The main features of this plugin are (i) a folder can be added without needing
to open an external file manager, and (ii) a folder can be removed without
needing to use the mouse.

### Usage

The following options are available in the command palette `ctrl+shift+p`:

- __Add Folder__: Type the name of the file/folder to add to the project.
  Suggestions are shown in the status bar.

- __Remove Folder__: Type the name of the folder to remove from the project.
  Suggestions are shown in the quick panel.

### Default Shortcuts

- __Open File/Folder in New Window__: `ctrl+alt+shift+n`
- __Add File/Folder To Current Project__: `ctrl+alt+shift+m`
- __Remove Folder__: `ctrl+alt+shift+u`

### Installation

Using [Package Control](https://packagecontrol.io/packages/AddRemoveFolder),
type `ctrl+shift+p` > "Package Control: Install Package" > "AddRemoveFolder".

Alternatively, clone this repository directly into
`~/.config/sublime-text-3/Packages/`.
