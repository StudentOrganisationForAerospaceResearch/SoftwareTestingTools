import serial
import time
import binascii
import csv

order = 'big'
class AvionicsData:
    def __init__(self):
        self.imu = [0] * 9
        self.bar = [0] * 2
        self.gps = [0] * 8
        self.oxi = -1
        self.cmb = -1
        self.phs = -1
        self.upperVnt = -1
        self.injValve = -1
        self.lowerVnt = -1

    def __str__(self):
        phases = ["NA", "PRELAUNCH", "ARM", "BURN", "COAST", "DROGUE_DESCENT", "MAIN_DESCENT", "POSTLAUNCH", 
        "ABORT_COMMAND_RECEIVED", "ABORT_COMMUNICATION_ERROR", "ABORT_OXIDIZER_PRESSURE", "ABORT_UNSPECIFIED_REASON"]
        valveStatus = ["NA","Closed", "Open"]

        string="IMU - ACCEL:\t\t"+ str(self.imu[0:3])+" mg"+"\n"
        string+="IMU - GYRO:\t\t"+ str(self.imu[3:6])+" mdps"+"\n"
        string+="BAR - PRESS:\t\t"+ str(self.bar[0]/100) +" mbar"+"\n"
        string+="BAR - TEMP:\t\t"+  str(self.bar[1]/100)+" degrees C"+"\n"
        string+="GPS - TIME:\t\t"+ str(self.gps[0]) + "\n"
        #Convert GPS coordinates to latitude/longitude that Google Maps accepts
        string+="GPS - LAT:\t\t"+ str(self.gps[1] + self.gps[2]/100000/60) + " " + str(self.gps[3]) + "\n"
        string+="GPS - LONG:\t\t"+ str(self.gps[4] + self.gps[5]/100000/60) + " " + str(self.gps[6]) + "\n"
        string+="GPS - ALT:\t\t" + str(self.gps[7]) + " m" + "\n"
        string+="OXI - P:\t\t"+ str(self.oxi/1000)+" psi"+"\n"
        string+="CMB - P:\t\t"+ str(self.cmb/1000)+" psi"+"\n"
        string+="PHS -  PHASE:\t\t"+ str(phases[self.phs+1])+"\n"
        string+="Inj Valve:\t\t" + str(valveStatus[self.injValve+1])+"\n"
        string+="Lower Vent:\t\t" + str(valveStatus[self.lowerVnt+1])+"\n"

        with open('fligthData.csv', 'a') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow([str(self.imu[0]), str(self.imu[1]), str(self.imu[2]), str(self.imu[3]), str(self.imu[4]), str(self.imu[5]), str(self.bar[0]), str(self.bar[1])])

        return string

def twos_complement(hexstr,bits):
    value = int(hexstr,16)
    if value & (1 << (bits-1)):
        value -= 1 << bits
    return value

def disconnect(ser):
    ser.close()
    time.sleep(1)
    return None

def readSerial(ser,data):
    line = ser.read(256).hex()
    i = 0
    print(line)
    while(i<len(line)):
        #IMU Data
        if((line[i:i+8]=='31313131') and (len(line)-i>=81)):
            if(line[i+80:i+82]=='00'):
                print(line[i:i+82])
                data.imu[0] = twos_complement(line[i+8:i+16], 32)
                data.imu[1] = twos_complement(line[i+16:i+24], 32)
                data.imu[2] = twos_complement(line[i+24:i+32], 32)
                data.imu[3] = twos_complement(line[i+32:i+40], 32)
                data.imu[4] = twos_complement(line[i+40:i+48], 32)
                data.imu[5] = twos_complement(line[i+48:i+56], 32)
                i+=81
            else: i+=1

        #Barometer Data
        elif((line[i:i+8])=='32323232' and len(line)-i>=25):
            if(line[i+24:i+26]=='00'):
                print(line[i:i+26])
                data.bar[0] = twos_complement(line[i+8:i+16], 32)
                data.bar[1] = twos_complement(line[i+16:i+24], 32)
                i+=25
            else:
                i+=1

        #GPS Data
        elif((line[i:i+8]=='33333333') and (len(line)-i>=57)):
            if(line[i+56:i+58]=='00'):
                data.gps[0] = (twos_complement(line[i+8:i+16], 32))/100
                data.gps[1] = (twos_complement(line[i+16:i+24], 32))
                data.gps[2] = (twos_complement(line[i+24:i+32], 32))
                if data.gps[1] < 0:
                    data.gps[3] = "S"
                    data.gps[1] *= -1
                    data.gps[2] *= -1
                else:
                    data.gps[3] = "N"
                data.gps[4] = (twos_complement(line[i+32:i+40], 32)) 
                data.gps[5] = (twos_complement(line[i+40:i+48], 32)) 
                if data.gps[4] < 0:
                    data.gps[6] = "W"
                    data.gps[4] *= -1
                    data.gps[5] *= -1
                else:
                    data.gps[6] = "E" 
                data.gps[7] = (twos_complement(line[i+48:i+56], 32))/10 
                i+=57
            else: i+=1

        #Oxidizer Tank Pressure
        elif((line[i:i+8]=='34343434') and (len(line)-i>=17)):
            if(line[i+16:i+18]=='00'):
                data.oxi = twos_complement(line[i+8:i+16], 32)
                i+=17
            else: i+=1

        #Combustion Chamber Pressure
        elif((line[i:i+8]=='35353535') and (len(line)-i>=17)):
            if(line[i+16:i+18]=='00'):
                data.cmb = twos_complement(line[i+8:i+16], 32)
                i+=17
            else: i+=1

        #Flight Phase
        elif((line[i:i+8]=='36363636') and (len(line)-i>=11)):
            if(line[i+10:i+12]=='00'):
                data.phs = int(line[i+8:i+10], 16)
                i+=11
            else: i+=1

        #Injection Valve Status
        elif((line[i:i+8]=='38383838') and (len(line)-i>=11)):
            if(line[i+10:i+12]=='00'):
                data.injValve = int(line[i+8:i+10], 16)
                i+=11
            else: i+=1

        #Lower Vent Valve
        elif((line[i:i+8]=='39393939') and (len(line)-i>=11)):
            if(line[i+10:i+12]=='00'):
                data.lowerVnt = int(line[i+8:i+10], 16)
                i+=11
            else: i+=1

        #No packet detected
        else: i+=1
    
    print(data)
    ser.flushInput()


if __name__ == "__main__":
    ser = None
    data = AvionicsData()
    while(True):
        port = input('Enter a Serial Port to connect to:') #Linux: /dev/ttyUSBx, Windows: COMx
        ser = serial.Serial(port, 9600, timeout=0)
        
        ser.flushInput()

        while(ser!=None):
            time.sleep(0.5)
            readSerial(ser, data)