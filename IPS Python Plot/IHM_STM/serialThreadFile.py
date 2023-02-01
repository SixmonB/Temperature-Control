import serial
from PyQt5.QtCore import pyqtSignal,QThread

class serialThreadClass(QThread):
  received_temp= pyqtSignal(str)
  received_tension = pyqtSignal(str)
  
  def __init__(self,parent=None):
        super(serialThreadClass,self).__init__(parent)
        self.uart = True
        self.seriport = serial.Serial(port='COM13', baudrate=115200,timeout= 1)
        print("serial port", self.seriport.name + " opened")
        self.listTemp = []
        self.send_msg = "F00"
        self.time = []
    
      
  def run(self):
      while self.uart:
        line = self.seriport.readline().decode('utf8')
        split_line = line.split(";")
        if(split_line[0] == "T"):
            # T = Temperature identifier
            self.temperature=split_line[1]
            try:
                if(len(self.listTemp) < 250):
                    self.listTemp.append(float(self.temperature))
                    self.time = range(0, len(self.listTemp))
                else:
                    self.listTemp.pop(0)
                    self.time = range(0, len(self.listTemp))
                    self.listTemp.append(float(self.temperature))
                    self.time = range(0, len(self.listTemp))
                    

            except ValueError:
                pass
            self.received_temp.emit(str(self.temperature))
            #print("\r\n", self.listTemp)
        elif(split_line[0] == "V"):
            # V = Tension identifier
            self.tension=split_line[1]
            # tension percentage for the duty cycle
            # 20V max tension value
            self.tension = int(float(self.tension)/20*100)
            self.tension = str(self.tension)+"%"
            self.received_tension.emit(self.tension)

            
             
            
  
  def sendSerial(self):
      self.seriport.write(b'A')
      
  