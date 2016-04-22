#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Problem description:

Author: Santiago Narváez Rivas.
Date:
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio

class SimpleBackupWindow(Gtk.Window):
    def __init__(self):
        # Main Window
        Gtk.Window.__init__(self, title='Simple Backup')
        self.set_border_width(10)
        self.set_default_size(800, 400)

        #Header Bar
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = 'Simple Backup'
        self.set_titlebar(hb)

        button = Gtk.Button(label='Backup')
        button.connect("clicked", self.on_backup_clicked)
        hb.pack_end(button)

    def on_backup_clicked(self, button):
        #TODO: Implementar aquí lógica backup
        print("Backup clicked")



def main():
    win = SimpleBackupWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
    return


if __name__ == '__main__':
    main()