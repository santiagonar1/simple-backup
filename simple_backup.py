#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Problem description:

Author: Santiago Narváez Rivas.
Date:
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk

class SimpleBackupWindow(Gtk.Window):
    def __init__(self):
        # ---- Main Window ------
        Gtk.Window.__init__(self, title='Simple Backup')
        self.set_border_width(10)
        self.set_default_size(800, 400)

        # ---- Header Bar ----
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = 'Simple Backup'
        self.set_titlebar(hb)

        button_backup = Gtk.Button(label='Backup')
        button_backup.get_style_context().add_class("suggested-action")
        button_backup.set_sensitive(True)
        button_backup.connect("clicked", self.on_backup_clicked)
        hb.pack_end(button_backup)

        # ---- Body ----
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox.props.spacing = 6
        self.add(vbox)

        # 1. Select the backups destiny View
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hbox.props.spacing = 10
        hbox.set_size_request(-1, 20)

        label = Gtk.Label.new_with_mnemonic('_Save to')

        self.entry_destiny = Gtk.Entry()
        self.entry_destiny.set_size_request(500, -1)

        button_destiny = Gtk.Button()
        icon = Gio.ThemedIcon(name="document-open-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button_destiny.add(image)
        button_destiny.connect('clicked', self.on_destiny_clicked)

        label.set_mnemonic_widget(button_destiny)

        hbox.pack_start(label, False, False, 0)
        hbox.pack_start(self.entry_destiny, True, True, 0)
        hbox.pack_start(button_destiny, False, False, 0)

        vbox.pack_start(hbox, False, False, 0)

        # 2. Files to backup View
        scrollable_treelist = Gtk.ScrolledWindow()
        scrollable_treelist.set_vexpand(True)

        self.files_to_bakcup = Gtk.ListStore(str, str)
        self.files_to_bakcup.append(['/esto/es/un/ejemplo', '45 MB'])

        self.treeview = Gtk.TreeView(self.files_to_bakcup)
        select = self.treeview.get_selection()
        select.connect('changed', self.on_tree_selection_changed)
        select.set_mode(Gtk.SelectionMode.MULTIPLE)

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn('File', renderer, text=0)
        column.set_expand(True)
        self.treeview.append_column(column)

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn('Size', renderer, text=1)
        self.treeview.append_column(column)

        scrollable_treelist.add(self.treeview)

        vbox.pack_start(scrollable_treelist, True, True, 0)

        # 3. Add files to backup
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hbox.props.spacing = 6
        hbox.set_size_request(-1, 20)

        self.button_add = Gtk.Button()
        self.button_add.connect('clicked', self.on_add_clicked)

        hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hbox2.props.spacing = 6
        icon = Gio.ThemedIcon(name="list-add-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        label = Gtk.Label.new_with_mnemonic('_Add')
        hbox2.pack_start(image, False, False, 0)
        hbox2.pack_start(label, True, True, 0)
        self.button_add.add(hbox2)

        self.button_remove = Gtk.Button()
        self.button_remove.set_sensitive(False)
        self.button_remove.connect('clicked', self.on_remove_clicked)

        hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hbox2.props.spacing = 6
        icon = Gio.ThemedIcon(name="list-remove-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        label = Gtk.Label.new_with_mnemonic('_Remove')
        hbox2.pack_start(image, False, False, 0)
        hbox2.pack_start(label, True, True, 0)
        self.button_remove.add(hbox2)

        hbox.pack_end(self.button_remove, False, False, 0)
        hbox.pack_end(self.button_add, False, False, 0)

        vbox.pack_start(hbox, False, False, 0)


    def on_backup_clicked(self, button):
        #TODO: Aqui iniciar el backup
        print("Backup clicked")

    def on_destiny_clicked(self, button):
        dialog = Gtk.FileChooserDialog("Please choose a folder", self,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             "Select", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.entry_destiny.set_text(dialog.get_filename())

        dialog.destroy()

    def on_add_clicked(self, button):
        #TODO: Add files
        self.files_to_bakcup.append(['/esto/es/un/ejemplo', '45 MB'])

    def on_remove_clicked(self, button):
        for tree_row_reference in sorted(self.row_references):
            del self.files_to_bakcup[tree_row_reference.get_path()]
        self.treeview.get_selection().unselect_all()
        self.button_remove.set_sensitive(False)

    def on_tree_selection_changed(self, selection):
        self.row_references = []
        for path in selection.get_selected_rows()[1]:
            tree_row_reference = Gtk.TreeRowReference(self.files_to_bakcup, path)
            self.row_references.append(tree_row_reference)
        self.button_remove.set_sensitive(True)


def main():
    window = SimpleBackupWindow()
    window.connect("delete-event", Gtk.main_quit)
    window.show_all()
    Gtk.main()


if __name__ == '__main__':
    main()
