import sys
import gui
from PyQt5.QtWidgets import QApplication,QDialog
from serialThreadFile import serialThreadClass 
import random
import numpy as np
import graph
class MainClass (QDialog,gui.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.update_graph()
        self.onButton.clicked.connect(self.OnButtonClicked) #Btn On
        self.offButton.clicked.connect(self.OffButtonClicked) #Btn Off
        self.onFanButton.clicked.connect(self.FanOn) # Fan On
        self.offFanButton.clicked.connect(self.FanOff) # Fan Off
        self.increaseTempButton.clicked.connect(self.IncreaseTemp) # Increase Temp
        self.decreaseTempButton.clicked.connect(self.DecreaseTemp) # Decrease Temp
        self.sendButton.clicked.connect(self.SendTemp) # Send temperature command


        self.mySerial = serialThreadClass()
        self.mySerial.received_temp.connect(self.updateTemp)
        self.mySerial.received_tension.connect(self.updateTension)
        #self.mySerial.start() # run thread fun
        
        
    def updateTemp(self):
        self.label_temp.setText(self.mySerial.temperature)

        # Plot in real time
        self.graph.canvas.axes.clear()
        self.graph.canvas.axes.set_ylim(0, 60)
        self.graph.canvas.axes.plot(self.mySerial.time, self.mySerial.listTemp)
        self.graph.canvas.draw()

    def updateTension(self):
        self.label_tension.setText(self.mySerial.tension)
        self.graph.canvas.draw()

    def IncreaseTemp(self):
        if(self.tempToSend < 60):
            self.tempToSend += 1
        elif(self.tempToSend >= 60):
            self.tempToSend = 60
        self.tempValue.setText(str(self.tempToSend))

    def DecreaseTemp(self):
        if(self.tempToSend > 0):
            self.tempToSend -= 1
        elif(self.tempToSend <= 25):
            self.tempToSend = 25
        self.tempValue.setText(str(self.tempToSend))

    def SendTemp(self):
        self.send_msg = "T"+str(self.tempToSend)
        self.mySerial.seriport.write(self.send_msg.encode('utf8'))
        print("\r\n", self.send_msg)
        
    def OnButtonClicked(self):
        if(self.mySerial.uart == False):
            self.mySerial.uart = True
        self.mySerial.start()
        
    def OffButtonClicked(self):
        self.mySerial.uart = False
        print(self.mySerial.tabTemp)
    
    def FanOn(self):
        self.send_msg = "F01"
        self.mySerial.seriport.write(self.send_msg.encode('utf8'))
        print("\r\n", self.send_msg)

        

    def FanOff(self):
        self.send_msg = "F00"
        self.mySerial.seriport.write(self.send_msg.encode('utf8'))
        print("\r\n", self.send_msg)
        
                
    def update_graph(self):
        
        """"
        self.graph.canvas.axes.clear()
        self.graph.canvas.axes.plot(t, temp)
        #self.graph.canvas.axes.plot(t, sinus_signal)
        #self.graph.canvas.axes.legend(('cosinus', 'sinus'),loc='upper right')
        self.graph.canvas.axes.set_title('Cosinus - Sinus Signal')
        self.graph.canvas.draw()"""
        
if __name__ == '__main__':
    test = QApplication(sys.argv)
    test2 = MainClass()
    test2.show()
    test.exec_()