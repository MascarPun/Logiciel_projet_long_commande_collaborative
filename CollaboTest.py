def commandeCollabo(self):

    Kfor = self.parametres.getKfor()
    Tifor = self.parametres.getTifor()
    Tdfor = self.parametres.getTdfor()

    Kvit = self.parametres.getKvit()
    Tivit = self.parametres.getTivit()
    Tdvit = self.parametres.getTdvit()

    Kcour = self.parametres.getKcour()
    Ticour = self.parametres.getTicour()
    Tdcour = self.parametres.getTdcour()

    i = 0
    forces = []
    positions = []
    vitesses = []
    courants = []
    consigneForce = []
    consigneVit = []
    consigneCour = []
    courantImposePI = []
    mm2qc = 294
    # pPositionIs = c_long(0)
    erreurForce = [0, 0]
    #erreurPos = [0, 0]
    erreurVit = [0, 0]
    erreurCour = [0, 0]
    sommeErreurForce = 0
    #sommeErreurPos = 0
    sommeErreurVit = 0
    sommeErreurCour = 0

    while t - t0 < dureeExp:
        while time.time() - t < Te:
            a = 0
        t = time.time()

    ####### Mesure de la position actuelle #########################
        carteEpos.getPositionIs(pPositionIs, self.pErrorCode_i)  # mesure de position initiale
        positionLueMm = self.pPositionIs_i.contents.value / mm2qc  # conversion qc en mm
        positions.append(positionLueMm)

    #######  Mesure de la valeur de l'input en force sorti du capteur ##########
        InputNumber = c_int(1)

        carteEpos.getAnalogInput(InputNumber, pAnalogValue, pErrorCode_i)
        carteEpos.getAnalogInput2(InputNumber, pAnalogValue.contents, pErrorCode_i)

        forces.append(pAnalogValue.contents.value - 2499)
        print(forces[-1])


    ############ Elaboration Consigne Vitesse a partir de la Consigne Force ############

        a = Correcteurs.pos2velocity(Kfor, Tifor, Tdfor, forces[i], positionLueMm, erreurForce, sommeErreurForce)
        consigneVit.append(a[0])
        sommeErreurPos = sommeErreurPos + a[1]

    ############ Elaboration Consigne Courant a partir de la Consigne Vitesse ############
        carteEpos.getVelocityIs(pVelocityIs, self.pErrorCode_i)
        vitesseLue = self.pVelocityIs_i.contents.value  # en tour par minute ATTENTION ERREUR UNITE SOMMATEUR!
        vitesses.append(vitesseLue)
        a = Correcteurs.velocity2current(Kvit, Tivit, Tdvit, consigneVit[-1], vitesseLue,erreurVit, sommeErreurVit)
        consigneCour.append(a[0])
        sommeErreurVit = sommeErreurVit + a[1]

    ############ Elaboration Consigne Courant Envoye a partir de la Consigne Courant ############
        carteEpos.getCurrentIs(self.pCurrentIs_i, self.pErrorCode_i)
        courantLu = self.pCurrentIs_i.contents.value / 1000  # en A
        courants.append(courantLu)
        a = Correcteurs.courant_cmd(consigneCour[-1], courantLu, erreurCour, sommeErreurCour, Kcour, Ticour, Tdcour)
        courantImposePI.append(a[0])
        sommeErreurCour = sommeErreurCour + a[1]
        self.carteEpos.setCurrentMust(c_long(courantImposePI[-1]), self.pErrorCode_i)

        i = i + 1

    return ("fini")

    return ("fini")