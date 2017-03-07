import ctypes

from ctypes import *

EposCmd = ctypes.windll.LoadLibrary("EposCmd64.dll")

class EposData:

     def __init__(self):

        Mode = c_int(1)

        EPOS_i = c_char_p(b'EPOS2')
        EPOS = byref(EPOS_i)

        MAXON_SERIAL_V2_i = c_char_p(b'MAXON SERIAL V2')
        MAXON_SERIAL_V2 = byref(MAXON_SERIAL_V2_i)

        USB_i = c_char_p(b'USB')
        USB = byref(USB_i)

        USB0_i = c_char_p(b'USB0')
        USB0 = byref(USB0_i)

        Baudrate_i = c_long(100000)

        NodeId_i = c_int(1)

        #global pErrorCode_i
        pErrorCode = ctypes.POINTER(ctypes.c_long)
        pErrorCode2 = ctypes.c_long(0)
        self.pErrorCode_i = ctypes.cast(ctypes.addressof(pErrorCode2), pErrorCode)

        #global pIsEnabled_i
        pIsEnabled = ctypes.POINTER(ctypes.c_bool)
        pIsEnabled2 = ctypes.c_bool(0)
        self.pIsEnabled_i = ctypes.cast(ctypes.addressof(pIsEnabled2), pIsEnabled)

        #global pPositionIs_i
        pPositionIs = ctypes.POINTER(ctypes.c_long)
        pPositionIs2 = ctypes.c_long(0)
        self.pPositionIs_i = ctypes.cast(ctypes.addressof(pPositionIs2), pPositionIs)

        #global pAnalogValue
        pAnalogValue_i = ctypes.POINTER(ctypes.c_int)
        pAnalogValue2 = ctypes.c_int(0)
        self.pAnalogValue = ctypes.cast(ctypes.addressof(pAnalogValue2), pAnalogValue_i)

        #global pVelocityIs_i
        pVelocityIs = ctypes.POINTER(ctypes.c_long)
        pVelocityIs2 = ctypes.c_long(0)
        self.pVelocityIs_i = ctypes.cast(ctypes.addressof(pVelocityIs2), pVelocityIs)

        #global pCurrentIs_i
        pCurrentIs = ctypes.POINTER(ctypes.c_short)
        pCurrentIs2 = ctypes.c_short(0)
        self.pCurrentIs_i = ctypes.cast(ctypes.addressof(pCurrentIs2), pCurrentIs)

        self.EposDLL = 'EposCmd'
        self.EposHeader = 'Definition.h'
        self.DeviceName = EPOS_i
        self.ProtocolStackName = MAXON_SERIAL_V2_i
        self.InterfaceName = USB_i
        self.PortName = USB0_i
        self.Baudrate = Baudrate_i
        self.NodeId = NodeId_i
        self.exitEpos(self.pErrorCode_i)
        self.initEpos(self.pErrorCode_i)



     #Classe EposData (hérite de la classe handle)
#
#PROPRIETES :    
#    EposDLL : nom du fichier dll
#    EposHeader : nom du fichier des définitions
#
#OpenDevice (inputs) :
#    DeviceName : EPOS ou EPOS2
#    ProtocolStackName : MAXON_RS232, MAXON SERIAL V2, CANopen
#    InterfaceName : RS323, USB, ...
#    PortName : COM1, USB0, CAN0
#
#OpenDevice (outputs) :
#    Handle
#
#SetProtocolStackSettings
#    Baudrate : 1000000 (default value)
#    Timeout : 500 ms (default value)
#
#NodeId
    

     EposCmd.VCS_OpenDevice.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, POINTER(c_long)]
     EposCmd.VCS_OpenDevice.restype = ctypes.c_int
     
     EposCmd.VCS_CloseAllDevices.argtypes = [ POINTER(c_long)]
     EposCmd.VCS_CloseAllDevices.restype = ctypes.c_bool
   
     EposCmd.VCS_SetProtocolStackSettings.argtypes = [c_int, c_long, c_long,POINTER(c_long)]
     EposCmd.VCS_SetProtocolStackSettings.restype = ctypes.c_bool
    
     EposCmd.VCS_ClearFault.argtypes = [c_int, c_int, POINTER(c_long)]
     EposCmd.VCS_ClearFault.restype = ctypes.c_bool
     
     EposCmd.VCS_SetOperationMode.argtypes = [c_int, c_int, c_int,POINTER(c_long)]
     EposCmd.VCS_SetOperationMode.restype = ctypes.c_bool
      
     EposCmd.VCS_GetOperationMode.argtypes = [c_int, c_int, POINTER(c_int),POINTER(c_long)]
     EposCmd.VCS_GetOperationMode.restype = ctypes.c_bool
      
     EposCmd.VCS_SetEnableState.argtypes = [c_int, c_int, POINTER(c_long)]
     EposCmd.VCS_SetEnableState.restype = ctypes.c_bool      
      
     EposCmd.VCS_SetDisableState.argtypes = [c_int, c_int, POINTER(c_long)]
     EposCmd.VCS_SetDisableState.restype = ctypes.c_bool    
     
     EposCmd.VCS_GetEnableState.argtypes = [c_int, c_int, POINTER(c_bool), POINTER(c_long)]
     EposCmd.VCS_GetEnableState.restype = ctypes.c_bool    
     
     EposCmd.VCS_WaitForTargetReached.argtypes = [c_int, c_int, c_long, POINTER(c_long)]
     EposCmd.VCS_WaitForTargetReached.restype = ctypes.c_bool    
     
     EposCmd.VCS_GetAnalogInput.argtypes = [c_int, c_int, c_int, POINTER(c_int), POINTER(c_long)]
     EposCmd.VCS_GetAnalogInput.restype = ctypes.c_bool 
     
     EposCmd.VCS_GetPositionIs.argtypes = [c_int, c_int, POINTER(c_long),POINTER(c_long)]
     EposCmd.VCS_GetPositionIs.restype = ctypes.c_bool 
     
     EposCmd.VCS_MoveWithVelocity.argtypes = [c_int, c_int, c_long, POINTER(c_long)]
     EposCmd.VCS_MoveWithVelocity.restype = ctypes.c_bool
     
     EposCmd.VCS_MoveToPosition.argtypes = [c_int, c_int, c_long, c_bool, c_bool, POINTER(c_long)]
     EposCmd.VCS_MoveToPosition.restype = ctypes.c_bool
     
     
     EposCmd.VCS_SetVelocityMust.argtypes =  [c_int, c_int, c_long, POINTER(c_long)]
     EposCmd.VCS_SetVelocityMust.restype = ctypes.c_bool

     
     EposCmd.VCS_SetCurrentMust.argtypes =  [c_int, c_int, c_short, POINTER(c_long)]
     EposCmd.VCS_SetCurrentMust.restype = ctypes.c_bool

     EposCmd.VCS_SetDcMotorParameter.argtypes = [c_int, c_int, c_int, c_int, c_int,POINTER(c_long) ]
     EposCmd.VCS_SetDcMotorParameter.restype = ctypes.c_bool
      
     EposCmd.VCS_SetMaxAcceleration.argtypes = [c_int, c_int, c_long,POINTER(c_long) ]
     EposCmd.VCS_SetMaxAcceleration.restype = ctypes.c_bool
      
      
     # ---------------- Initialisation
     def initEpos(self,pErrorCode_i): 
        global Handle
        Handle = c_int(EposCmd.VCS_OpenDevice(self.DeviceName,self.ProtocolStackName,self.InterfaceName,self.PortName,pErrorCode_i))
        EposCmd.VCS_OpenDevice(self.DeviceName,self.ProtocolStackName,self.InterfaceName,self.PortName,pErrorCode_i)
        if not(Handle == 0): # connexion réussie
            res = 1
            if not(EposCmd.VCS_ClearFault(Handle, self.NodeId, pErrorCode_i)):
                print('ClearFault : échec')   
#            if not(EposCmd.VCS_SetProtocolStackSettings(Handle, self.Baudrate, c_long(500), pErrorCode_i)):
#                print('SetProtocolStackSettings : échec de connexion')
#                return [res,self]
            print('OpenDevice : EPOS connecté')
            return [res,self]
        else:
            res = 0
            print('OpenDevice : échec de connexion')          
            return [res,self]
     # initEpos
            
            
            
     # ---------------- Fermeture
     def exitEpos(self, pErrorCode_i):
        bool1=  EposCmd.VCS_CloseAllDevices(pErrorCode_i);
        if not(bool1):
            print('CloseAllDevices : échec')
            return
        else:
            print('CloseAllDevices : EPOS déconnecté')
            res = bool1
            return res
     # exitEpos
            
     def resetDevice(self, pErrorCode_i):
        bool1=  EposCmd.VCS_ResetDevice(Handle, self.NodeId, pErrorCode_i);
        if not(bool1):
            print('ResetDevice : échec')
            return
        else:
            print('ResetDevice : effectué')
            res = bool1
            return res
     # resetDevice           
            
            
     def setState(self, State, pErrorCode_i):
        bool1=  EposCmd.VCS_SetState(Handle, self.NodeId, State, pErrorCode_i);
        if not(bool1):
            print('SetState : échec')
            return
        else:
            print('Setstate : effectué')
            res = bool1
            return res
     # setState        
            
            
     def setOperationMode(self,Mode,pErrorCode_i):
        bool1 = EposCmd.VCS_SetOperationMode(Handle, self.NodeId, Mode, pErrorCode_i)
        if not(bool1):
            print('SetOperationMode : échec')
            return
        else:
            print(str('SetOperationMode : mode '+ str(Mode.value) + ' activé'))
        res = bool1
     # setOperationMode
        
        
     def  getOperationMode(self,pMode,pErrorCode_i):
        bool1 =  EposCmd.VCS_GetOperationMode(Handle, self.NodeId, pMode, pErrorCode_i)
        if not(bool1):
            print('GetOperationMode : échec')

     def  getOperationMode2(self,pMode,pErrorCode_i):   
        if pMode.value<10 :
            print(str('GetOperationMode : mode ' + str(pMode.value) + ' en cours'))
            if (pMode.value== 1):
              print('    * Position Profile Mode')
            elif (pMode.value== 3):
              print('    * Velocity Profile Mode')
            elif (pMode.value== 6):
              print('    * Homing Mode')
            elif (pMode.value== 7):
              print('    * Interpolated Position Mode')
            elif (pMode.value== -1):
              print('    * Position Mode')
            elif (pMode.value== -2):
              print('    * Velocity Mode')
            elif (pMode.value== -3):
              print('    * Current Mode')
            elif (pMode.value== -5):
              print('    * Master Encoder Mode')
            elif (pMode.value== -6):
              print('    * Step Direction Mode')
            else:
              print('    ! MODE NON DEFINI !')
        else : 
            print(str('GetOperationMode : mode ' + str(pMode.value-256) + ' en cours'))
            if (pMode.value-256== 1):
                print('    * Position Profile Mode')
            elif (pMode.value-256== 3):
                print('    * Velocity Profile Mode')
            elif (pMode.value-256== 6):
                print('    * Homing Mode')
            elif (pMode.value-256== 7):
                print('    * Interpolated Position Mode')
            elif (pMode.value-256== -1):
                print('    * Position Mode')
            elif (pMode.value-256== -2):
                print('    * Velocity Mode')
            elif (pMode.value-256== -3):
                print('    * Current Mode')
            elif (pMode.value-256== -5):
                print('    * Master Encoder Mode')
            elif (pMode.value-256== -6):
                print('    * Step Direction Mode')
            else:
                print('    ! MODE NON DEFINI !')
              # switch pMode.value
           # if ~EposCmd.VCS_GetOperationMode(Handle, self.NodeId, pMode.contents, pErrorCode_i)
        res = True

     def setEnableState(self,pErrorCode_i):
        bool1 = EposCmd.VCS_SetEnableState(Handle, self.NodeId, pErrorCode_i)
        if not(bool1):
            print('SetEnableState : échec')
            return
        else:
              print('SetEnableState : EPOS activé')
        res = bool1
       # setDisableState 
 
 
     def setDisableState(self, pErrorCode_i):
        bool1 = EposCmd.VCS_SetDisableState(Handle, self.NodeId, pErrorCode_i)
        if not(bool1):
            print('SetDisableState : échec')
            return
        else:
            print('SetDisableState : EPOS desactivé')
        res = bool1
       # setDisableState
        
        
     def getEnableState(self, pIsEnabled, pErrorCode_i):
        bool1 = EposCmd.VCS_GetEnableState(Handle, self.NodeId, pIsEnabled, pErrorCode_i)
        if not(bool1):
            print('GetEnableState : échec')
            return
        else:
            pIsEnabled.value = True
            print(str('GetEnableState : enabled = ' + str(pIsEnabled.value)))
        res = bool1
          # getEnableState
        
     def waitForTargetReached(self,Timeout_i,pErrorCode_i):
        bool1 = EposCmd.VCS_WaitForTargetReached(Handle, self.NodeId,Timeout_i,pErrorCode_i)
        if not(bool1):
            print('WaitForTargetReached : Time Out')
            return
        else:
            print(str('WaitForTargetReached : OK '))
        res = bool1
      # waitForTargetReached
        
     def getAnalogInput(self,InputNumber,pAnalogValue,pErrorCode_i):
        bool1 = EposCmd.VCS_GetAnalogInput(Handle, self.NodeId,InputNumber,pAnalogValue,pErrorCode_i)
        if not(bool1):
            print('GetAnalogInput : échec')
         
      # getAnalogInput
        
     def getAnalogInput2(self,InputNumber,pAnalogValue,pErrorCode_i):
        print(str('GetAnalogInput : value = ' + str(pAnalogValue.value)));
        res = True
        
        
     def getPositionIs(self,pPositionIs, pErrorCode_i):
        bool1 = EposCmd.VCS_GetPositionIs(Handle, self.NodeId, pPositionIs, pErrorCode_i)
        if not(bool1):
            print('GetPositionIs : échec')

     def getPositionIs2(self,pPositionIs, pErrorCode_i):
        print(str('GetPositionIs : value = ' + str(pPositionIs.value)))
        res = True
      # getPositionIs
        
        
     def moveWithVelocity(self,TargetVelocity,pErrorCode_i):
        bool1 = EposCmd.VCS_MoveWithVelocity(Handle, self.NodeId,TargetVelocity,pErrorCode_i)
        if not(bool1):
            print('MoveWithVelocity : échec')
            return
        else:
            print(str('MoveWithVelocity : OK '))
        res = bool1
      # moveWithVelocity
        
        
     def moveToPosition(self, TargetPosition, Absolute, Immediately,pErrorCode_i):
        bool1 = EposCmd.VCS_MoveToPosition(Handle, self.NodeId, TargetPosition, Absolute, Immediately,pErrorCode_i)
        if not(bool1):
            print('MoveToPosition : échec')
            return
        else:
            print(str('MoveToPosition : done'))
        res = bool1
      # moveToPosition
        
        
     def setPositionMust(self,PositionMust,pErrorCode_i):
         bool1 = EposCmd.VCS_SetPositionMust(Handle, self.NodeId, PositionMust, pErrorCode_i)
         if not(bool1):
            print('SetPositionMust : échec')
            return
         else:
            print(str('SetPositionMust : done'))
         res = bool1
    #setPositionMust
         
         
         
         
     def setVelocityMust(self,VelocityMust,pErrorCode_i):
         bool1 = EposCmd.VCS_SetVelocityMust(Handle, self.NodeId, VelocityMust, pErrorCode_i)
         if not(bool1):
            print('SetVelocityMust : échec')
            return
         else:
            print(str('SetVelocityMust : done'))
         res = bool1
    #setVelocityMust
         
     def setCurrentMust(self,CurrentMust,pErrorCode_i):
         bool1 = EposCmd.VCS_SetCurrentMust(Handle, self.NodeId, CurrentMust, pErrorCode_i)
         if not(bool1):
            print('SetCurrentMust : échec')
            return
         else:
            print(str('SetCurrentMust : done'))
         res = bool1
    #setCurrentMust

     def getVelocityIs(self,pVelocityIs, pErrorCode_i):
        bool1 = EposCmd.VCS_GetVelocityIs(Handle, self.NodeId, pVelocityIs, pErrorCode_i)
        if not(bool1):
            print('GetVelocityIs : échec')

     def getVelocityIs2(self,pVelocityIs, pErrorCode_i):
        print(str('GetVelocityIs : value = ' + str(pVelocityIs.value)))
        res = True
      # getVelocityIs


     def getCurrentIs(self,pCurrentIs, pErrorCode_i):
        bool1 = EposCmd.VCS_GetCurrentIs(Handle, self.NodeId, pCurrentIs, pErrorCode_i)
        if not(bool1):
            print('GetCurrentIs : échec')

     def getCurrentIs2(self,pCurrentIs, pErrorCode_i):
        print(str('GetCurrentIs : value = ' + str(pCurrentIs.value)))
        res = True
      # getCurrentIs
         
     def setDcMotorParameter(self, NominalCurrent, MaxOutputCurrent, ThermalTimeConstant, pErrorCode_i) :
         bool1 = EposCmd.VCS_SetDcMotorParameter(Handle, self.NodeId,NominalCurrent, MaxOutputCurrent, ThermalTimeConstant, pErrorCode_i)
         if not(bool1):
            print('SetDcMotorParameter : échec')
            return
         else:
            print(str('SetDcMotorParameter : done'))
         res = bool1
         
         
     def setMaxAcceleration(self, MaxAcceleration, pErrorCode_i) :
         bool1 = EposCmd.VCS_SetMaxAcceleration(Handle, self.NodeId,MaxAcceleration, pErrorCode_i)
         if not(bool1):
             print('SetMaxAcceleration : échec')
             return
         else:
                 print(str('SetMaxAcceleration : done'))
         res = bool1