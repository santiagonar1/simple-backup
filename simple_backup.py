#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Problem description:

Author: Santiago Narváez Rivas.
Date:
"""
import backup_utility
import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk

FOLDER_ICON = 'folder-symbolic'
FILE_ICON = 'text-x-generic-symbolic'

class SimpleBackupWindow(Gtk.Window):
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file('simple_backup.glade')
        builder.connect_signals(self)

        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = 'Simple Backup'
        button_backup = Gtk.Button(label='Backup')
        button_backup.get_style_context().add_class('suggested-action')
        button_backup.connect('clicked', self.on_backup_clicked)
        hb.pack_end(button_backup)

        self.window = builder.get_object('main_window')
        self.window.set_titlebar(hb)
        self.window.show_all()

        self.entry_location = builder.get_object('entry_backup_location')

        self.tree_view_selector = builder.get_object('tree_view_selector')
        self.list_files_backup = builder.get_object('liststore_files_backup')

        self.button_remove = builder.get_object('button_remove')

        # Here we save the selected rows from the tree view
        self.row_references = []

    def on_delete_window(self, *args):
        Gtk.main_quit(*args)

    def on_backup_location_clicked(self, button):
        filepath = create_dialog('Please choose a folder',
                                 self.window,
                                 Gtk.FileChooserAction.SELECT_FOLDER)

        if filepath:
            self.entry_location.set_text(filepath)

    def on_remove_clicked(self, button):
        for tree_row_reference in self.row_references:
            del self.list_files_backup[tree_row_reference.get_path()]
        self.tree_view_selector.unselect_all()
        self.button_remove.set_sensitive(False)

    def on_add_clicked(self, button):
        if Gtk.Buildable.get_name(button) == 'button_add_file':
            action = Gtk.FileChooserAction.OPEN
        else:
            action = Gtk.FileChooserAction.SELECT_FOLDER

        filenames = create_dialog('Please choose a folder',
                                 self.window,
                                 action,
                                 multiple=True)

        if filenames:
            self.tree_view_selector.unselect_all()
            filenames_in_tree = self.get_filenames()
            for filename in filenames:
                if filename not in filenames_in_tree:
                    entry = backup_utility.Entry(filename)
                    icon_name = FILE_ICON if entry.is_file() else FOLDER_ICON
                    self.list_files_backup.append([entry.path, entry.get_readable_size(), icon_name])

    def on_backup_clicked(self, button):
        destiny = self.entry_location.get_text()
        if destiny:
            entries = [backup_utility.Entry(f) for f in self.get_filenames()]
            backup = backup_utility.Backup(entries, destiny)
            #TODO: elegir commonpath de acuerdo a las preferencias
            backup.start()
        else:
            dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.ERROR,
            Gtk.ButtonsType.OK, "No destiny selected")
            dialog.format_secondary_text(
                "Please choose where do you want to save the backup")
            dialog.run()
            dialog.destroy()


    def on_tree_selection_changed(self, selection):
        self.row_references = []
        for path in selection.get_selected_rows()[1]:
            tree_row_reference = Gtk.TreeRowReference(self.list_files_backup, path)
            self.row_references.append(tree_row_reference)
        self.button_remove.set_sensitive(True)

    def get_filenames(self):
        filenames = []
        for row in self.list_files_backup:
            filenames.append(row[0])
        return filenames

def create_dialog(title, parent, action, multiple=False):
    dialog =  Gtk.FileChooserDialog(title, parent,
            action, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            "Select", Gtk.ResponseType.OK))
    dialog.set_default_size(800, 400)
    current_folder = os.path.expanduser('~')
    dialog.set_current_folder(current_folder)
    dialog.set_select_multiple(multiple)

    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        result = dialog.get_filenames() if multiple else dialog.get_filename()
        dialog.destroy()
        return result
    elif response == Gtk.ResponseType.CANCEL:
        dialog.destroy()
        return None

def main():
    SimpleBackupWindow()
    Gtk.main()


if __name__ == '__main__':
    main()
