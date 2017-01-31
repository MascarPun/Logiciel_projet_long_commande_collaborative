# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#!/usr/bin/python
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk as gtk


class HelloWorld:

    def __init__(self):

        interface = gtk.Builder()

        interface.add_from_file('proj.glade')

        self.posLabelValeurPosAct = interface.get_object("posLabelValeurPosAct")
        self.posLabelValeurPosAct.set_text('1')




        interface.connect_signals(self)

    def on_mainWindow_destroy(self, widget):
        print(1)
        gtk.main_quit()

#   changer affichage valeur actuelle position
#
#   def on_myButton_clicked(self, widget):
#        self.myLabel.set_text("World!")

if __name__ == "__main__":

    HelloWorld()

    gtk.main()


