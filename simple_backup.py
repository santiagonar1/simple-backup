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
        # Main Window
        Gtk.Window.__init__(self, title='Simple Backup')
        self.set_border_width(10)
        self.set_default_size(800, 400)

        # Header Bar
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = 'Simple Backup'
        self.set_titlebar(hb)

        button_backup = Gtk.Button(label='Backup')
        button_backup.get_style_context().add_class("suggested-action")
        button_backup.set_sensitive(True)
        button_backup.connect("clicked", self.on_backup_clicked)
        hb.pack_end(button_backup)

        # Body
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox.props.spacing = 6
        self.add(vbox)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hbox.props.spacing = 10
        hbox.set_size_request(-1, 20)

        label = Gtk.Label('Save to')

        self.entry_destiny = Gtk.Entry()
        self.entry_destiny.set_size_request(500, -1)

        button_destiny = Gtk.Button()
        icon = Gio.ThemedIcon(name="document-open-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button_destiny.add(image)
        button_destiny.connect('clicked', self.on_destiny_clicked)

        hbox.pack_start(label, False, False, 0)
        hbox.pack_start(self.entry_destiny, True, True, 0)
        hbox.pack_start(button_destiny, False, False, 0)

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



def main():
    window = SimpleBackupWindow()
    window.connect("delete-event", Gtk.main_quit)
    window.show_all()
    Gtk.main()


if __name__ == '__main__':
    main()
