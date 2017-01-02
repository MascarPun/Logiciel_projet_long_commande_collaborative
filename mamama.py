# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#!/usr/bin/python

from gi.repository import Gtk as gtk


class HelloWorld:

    def __init__(self):

        interface = gtk.Builder()

        interface.add_from_file('mamama.glade')

        

        self.myLabel = interface.get_object("myLabel")

        interface.connect_signals(self)


    def on_mainwindow_destroy(self, widget):

        gtk.main_quit()


    def on_myButton_clicked(self, widget):

        self.myLabel.set_text("World!")


if __name__ == "__main__":

    HelloWorld()

    gtk.main()


