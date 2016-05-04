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
gi.require_version('Notify', '0.7')
from gi.repository import Gtk, Gdk, Notify
from observer import Observer

FOLDER_ICON = 'folder-symbolic'
FILE_ICON = 'text-x-generic-symbolic'
PROGRESSBAR_TEXT = '{0} of {1} files'
# Notify ID
APPINDICATOR_ID = 'simplebackup'
NOTIFY_ICON = 'dialog-information'

class SimpleBackup(Observer):
    def __init__(self):
        screen = Gdk.Screen.get_default()

        css_provider = Gtk.CssProvider()
        css_provider.load_from_path('style.css')

        context = Gtk.StyleContext()
        context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

        builder = Gtk.Builder()
        builder.add_from_file('simple_backup.glade')
        builder.connect_signals(self)

        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = 'Simple Backup'
        self.button_backup = Gtk.Button(label='Backup')
        self.button_backup.get_style_context().add_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)
        self.button_backup.connect('clicked', self.on_backup_clicked)
        self.spinner = Gtk.Spinner()
        hb.pack_end(self.button_backup)
        hb.pack_end(self.spinner)

        self.window = builder.get_object('main_window')
        self.window.set_titlebar(hb)
        self.window.show_all()

        self.entry_location = builder.get_object('entry_backup_location')

        self.tree_view_selector = builder.get_object('tree_view_selector')
        self.list_files_backup = builder.get_object('liststore_files_backup')
        self.list_files_backup.set_sort_func(1, compare_size, None)

        self.button_bakcup_location = builder.get_object('button_backup_location')
        self.button_remove = builder.get_object('button_remove')
        self.button_add_file = builder.get_object('button_add_file')
        self.button_add_dir = builder.get_object('button_add_dir')

        self.progressbar = builder.get_object('progressbar')

        # Here we save the selected rows from the tree view
        self.row_references = []

    def on_delete_window(self, *args):
        Gtk.main_quit(*args)

    def on_backup_location_clicked(self, button):
        filepath = create_dialog('Please Choose a Destination Folder',
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
            title = 'Please Choose File(s) to Backup'
        else:
            action = Gtk.FileChooserAction.SELECT_FOLDER
            title = 'Please Choose Folder(s) to Backup'

        filenames = create_dialog(title,
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
            self.progressbar.props.visible = True
            self.progressbar.set_text(PROGRESSBAR_TEXT.format(0, len(self.list_files_backup)))
            self.spinner.start()
            self.toggle_buttons()
            self.tree_view_selector.unselect_all()
            entries = [backup_utility.Entry(f) for f in self.get_filenames()]
            backup = backup_utility.Backup(entries, destiny)
            backup.add_observer(self)
            #TODO: elegir commonpath de acuerdo a las preferencias
            backup.start()
        else:
            dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.ERROR,
            Gtk.ButtonsType.OK, "No destiny selected")
            dialog.format_secondary_text(
                "Please choose where do you want to save the backup")
            dialog.run()
            dialog.destroy()

    def update(self, observable, event):
        # event[0] == entry number
        self.progressbar.set_text(PROGRESSBAR_TEXT.format(event[0], len(self.list_files_backup)))
        self.progressbar.set_fraction(event[0] / len(self.list_files_backup))
        if event[0] == len(self.list_files_backup):
            self.toggle_buttons()
            self.spinner.stop()
            make_notification('Backup Finished',
                              'All the files have been saved in the new destination',
                              NOTIFY_ICON)

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

    def toggle_buttons(self):
        self.button_add_dir.props.sensitive = not self.button_add_dir.props.sensitive
        self.button_add_file.props.sensitive = not self.button_add_file.props.sensitive
        self.button_bakcup_location.props.sensitive = not self.button_bakcup_location.props.sensitive
        self.button_remove.props.sensitive = False

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

def compare_size(model, row1, row2, user_data):
    sort_column, _ = model.get_sort_column_id()
    value1 = backup_utility.string_to_bytes(model.get_value(row1, sort_column))
    value2 = backup_utility.string_to_bytes(model.get_value(row2, sort_column))
    if value1 < value2:
        return 1
    elif value1 == value2:
        return 0
    else:
        return -1

def make_notification(title, body, icon):
    Notify.init(APPINDICATOR_ID)
    notification = Notify.Notification.new(title, body, icon)
    notification.set_timeout(Notify.EXPIRES_NEVER)
    notification.show()

def main():
    SimpleBackup()
    Gtk.main()


if __name__ == '__main__':
    main()
