# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#!/usr/bin/python
# import gi
# gi.require_version('Gtk','3.0')
# from gi.repository import Gtk as gtk
import Controleur

class Vue:

    def __init__(self):
        self.controleur
        # interface = gtk.Builder()
        #
        # interface.add_from_file('proj.glade')
        #
        # self.posLabelValeurPosAct = interface.get_object("posLabelValeurPosAct")
        # self.posLabelValeurPosAct.set_text('1')

        #
        #
        # self.posEntryFreq = interface.get_object("posEntryFreq")
        # self.posEntryAmplitude = interface.get_object("posEntryAmplitude")
        # self.posEntryRampe = interface.get_object("posEntryRampe")
        # self.posEntryEchelon = interface.get_object("posEntryEchelon")
        # self.posEntryK = interface.get_object("posEntryK")
        # self.posEntryTi = interface.get_object("posEntryTi")
        # self.posEntryTd = interface.get_object("posEntryTd")
        #
        # self.posBoutonEchelon = interface.get_object("posBoutonEchelon")
        # self.posBoutonRampe = interface.get_object("posBoutonRampe")
        # self.posBoutonSinus = interface.get_object("posBoutonSinus")
        #
        # self.posDureeExp = interface.get_object("posEntryDuree")
        #
        # self.posBoutonRun = interface.get_object("posBoutonRun")

        # interface.connect_signals(self)

    def on_mainWindow_destroy(self, widget):
        print(1)
        gtk.main_quit()


    def on_posBoutonRun_clicked(self, widget):
        if self.posBoutonEchelon.get_active():
            print('posEchelon')
            # controleur.setMode(posEchelon)
        if self.posBoutonRampe.get_active():
            print('posRampe')
            # controleur.setMode(posRampe)
        if self.posBoutonSinus.get_active():
            print('posSinus')
            # controleur.setMode(posSinus)


        # On met a jour les correcteurs
        self.controleur.setCorPos([])
        #self.controleur.setCorVit()   Faire attention si case vide
        #self.controleur.setCorCour()


        # print(self.posEntryAmplitude.get_text())
        # print(self.posEntryFreq.get_text())
        # print(self.posEntryRampe.get_text())
        # print(self.posEntryEchelon.get_text())
        # print(self.posEntryK.get_text())
        # print(self.posEntryTi.get_text())
        # print(self.posEntryTd.get_text())
        # print(self.posDureeExp.get_text())

        print("running")
        self.controleur.run()


#   changer affichage valeur actuelle position
#
#   def on_myButton_clicked(self, widget):
#        self.myLabel.set_text("World!")

if __name__ == "__main__":

    Vue()

    gtk.main()


