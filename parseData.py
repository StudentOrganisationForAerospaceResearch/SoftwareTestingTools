import serial
import time
import binascii
import platform
import cobs
import sys
import glob

order = 'big'
class AvionicsData:
    def __init__(self):
        self.imu = [0] * 9
        self.bar = [0] * 2
        self.gps = [0] * 4
        self.oxi = 0
        self.cmb = 0
        self.phs = -1
        self.vnt = 0

    def __str__(self):
        phases = ["NA!", "PRELAUNCH", "BURN", "COAST", "DROGUE_DESCENT", "MAIN_DESCENT", "ABORT"]

        string="IMU - ACCEL:\t"+ str(self.imu[0:3])+"\n"
        string+="IMU - GYRO:\t"+ str(self.imu[3:6])+"\n"
        string+="IMU - MAG:\t" + str(self.imu[6:9]) +"\n"
        string+="BAR - PRESS:\t"+ str(self.bar[0]) +"\n"
        string+="BAR - TEMP:\t"+  str(self.bar[1])+"\n"
        string+="GPS - ALT:\t"+ str(self.gps[0])+"\n"
        string+="GPS - TIME:\t"+ str(self.gps[1])+"\n"
        string+="GPS - LAT:\t"+ str(self.gps[2])+"\n"
        string+="GPS - LONG:\t"+ str(self.gps[3])+"\n"
        string+="OXI - PRESS:\t"+ str(self.oxi)+"\n"
        string+="CMB - PRESS:\t"+ str(self.cmb)+"\n"
        string+="VNT - STATUS:\t"+ str(self.vnt)+"\n"
        string+="PHS -  PHASE:\t"+ str(phases[self.phs + 1])+"\n"

        return string

def arm(ser):
    ser.write(bytearray.fromhex('2100'))
    time.sleep(1)
    print('Arm Command Sent!\n')

def heartbeat(ser):
    ser.write(bytearray.fromhex('4600'))
    time.sleep(1)
    print('Heartbeat Command Sent!\n')


def reset(ser):
    ser.write(bytearray.fromhex('4F00'))
    time.sleep(1)
    print('Reset Command Sent!\n')

def fire(ser):
    ser.write(bytearray.fromhex('2000'))
    time.sleep(1)
    print('Fire Command Sent!\n')

def openInjectionValve(ser):
    ser.write(bytearray.fromhex('2A00'))
    time.sleep(1)
    print('Open Injection Valve Command Sent!\n')


def closeInjectionValve(ser):
    ser.write(bytearray.fromhex('2B00'))
    time.sleep(1)
    print('Close Injection Valve Command Sent!\n')


def abort(ser):
    ser.write(bytearray.fromhex('2F00'))
    time.sleep(1)
    print('Abort Command Sent!\n')

def setBaud(ser,baud):
	ser.baudrate = baud
	time.sleep(1)
	ser.flush()
	print("Baudrate set to: ", baud)

def fillOpen(ser):
    ser.write(bytearray.fromhex('2200'))
    time.sleep(1)
    print('Fill Valve Open Sent!\n')

def fillClose(ser):
    ser.write(bytearray.fromhex('2300'))
    time.sleep(1)
    print('Fill Valve Close Sent!\n')


def help():
    print('\nList of commands:\n----------------------------------')
    print('abort\t\t send the abort command 0x2F')
    print('arm\t\t send the arm command 0x21')
    print('clear\t\t clears the terminal')
    print('disconnect\t disconnect and connect to another comm port')
    print('fire\t\t send the fire command 0x20')
    print('help\t\t prints this help menu')
    print('fill [open|close]\t opens or closes the Nitrous Fill Valve (command 0x22/0x23)')
    print('quit\t\t closes the serial terminal and program')
    print('read\t\t reads the serial buffer and displays the latest data\n')

def connect(port):
    ser = serial.Serial(port, 4800, timeout=0)
    time.sleep(2)
    return ser

def disconnect(ser):
    ser.close()
    time.sleep(1)
    return None
def quit():
    exit()


def readHex(ser):
    line = ser.readline()
    print(line.hex())

def readSerial(ser,data):
    line = ser.readline().hex()
    i = 0
    print(line)
    while(i<len(line)):
        #IMU Data
        if((line[i:i+4]==0x31313131) and (len(line)-i>=41)):
            if(line[i+40]==0x00):
                for j in range(9):
                    data.imu[j] = int.from_bytes(line[i+4+(j*4):line[i+8+(j*4)]], byteorder=order, signed=True)
                i+=41
            else: i+=1

        # Barometer Data
        elif((line[i:i+8])==0x32323232 and len(line)-i>=25):
            input = str(line[i+8:i+24])
            print(input)
            print(bytes.fromhex(input[2:18]))
            if(line[i+24:i+26]==b'00'):
                data.bar[0] = int.from_bytes(bytes.fromhex(input[2:10]), byteorder=order, signed=True)
                data.bar[1] = int.from_bytes(bytes.fromhex(input[10:18]), byteorder=order, signed=True)
                i+=25
            else:
                i+=1

        #GPS Data
        elif((line[i:i+4]==0x33333333) and (len(line)-i>=21)):
            if(line[i+20]==0x00):
                for j in range(9):
                    data.imu[j] = int.from_bytes(line[i+4+(j*4):i+8+(j*4)], byteorder=order, signed=True)
                i+=21
            else: i+=1

        #Oxidizer Tank Pressure
        elif((line[i:i+4]==0x34343434) and (len(line)-i>=9)):
            if(line[i+8]==0x00):
                data.oxi = int.from_bytes(line[i+4:i+8], byteorder=order, signed=True)
                i+9
            else: i+=1

        #Combustion Chamber Pressure
        elif((line[i]==0x35353535) and (len(line)-i>=9)):
            if(line[i+8]==0x00):
                data.cmb = int.from_bytes(line[i+4:i+8], byteorder=order, signed=True)
                i+=9
            else: i+=1

        #Flight Phase
        elif((line[i:i+8]==0x36363636) and (len(line)-i>=12)):
            if(line[i+10:i+11]==b'00'):
                data.phs = line[i+8:i+9]
                i+=11
            else: i+=1

        #Vent Status
        elif((line[i]==0x37373737) and (len(line)-i>=6)):
            if(line[i+5]==0x00):
                data.vnt = line[i+4]
                i+=6
            else: i+=1

        #No packet detected
        else: i+=1  
    print(data)


if __name__ == "__main__":
    ser = None
    data = AvionicsData()
    while(True):

        while(ser!=None):
            time.sleep(1)
            readSerial(ser, data)
            # comm = input("Awaiting command (enter help for list of commands):")
            # if(comm == 'arm'): arm(ser)
            # elif(comm == 'heartbeat'): heartbeat(ser)
            # elif(comm == 'reset'): reset(ser)
            # elif(comm == 'openinj'): openInjectionValve(ser)
            # elif(comm == 'closeinj'): closeInjectionValve(ser)
            # elif(comm == 'fire'): fire(ser)
            # elif(comm == 'abort'): abort(ser)
            # elif(comm == 'help'): help()
            # elif(comm == 'disconnect'): ser = disconnect(ser)
            # elif(comm == 'quit'): exit()
            # elif(comm == 'hex'): readHex(ser)
            # elif(comm == 'read'): readSerial(ser, data)
            # elif(comm[0:4] == 'baud'): setBaud(ser, int(comm[5:]))
            # elif(comm == 'fill open'): fillOpen(ser)
            # elif(comm == 'fill close'): fillClose(ser)
            # elif(comm == 'clear' or comm == 'cls'): print(chr(27) + "[2J")
            # else: print(comm,': Command Not Found')
        
        if(platform.system() == 'Linux'):
            ser = connect(input('Enter a Serial Port to connect to:'))
        elif(platform.system() == 'Windows'):
            ser = connect(input('Enter a COM Port to connect to (COMX):'))
        help()

# Functions to Launch Tests
def launchTest(ser,data):
    line = ser.readline().hex()
    i = 0
    #reads the flight phase
    flightphase = line[i + 8:i + 9]
    launchStatus = False
    while(True):
        if(launchStatus == False):
            #read the start byte to make sure we are reading the right code (for flight phase)
            if ((line[i:i+8] == 0x36363636) and (len(line) - i >= 12)):
                #make sure the stop byte is right too
                if (line[i+10:i+11] == 0x00):
                    #check if flight phase is 0
                    if(flightphase != 0x00):
                        print("Launch Test failed")
                        return
                    #fire the rocket
                    fire(ser)
                    launchStatus = True
                    print("Launch Test successful!")
        else:
            #if the flighphase = 1, that means the rocket has launched
            if(flightphase == 0x01):
                line = binascii.hexlify(ser.readline())
                break

def cobsTest(ser):
    encoded = cobs.encode(b'\x45\x00\x00\x2c\x4c\x79\x00\x00\x40\x06\x4F\x37')
    ser.write(bytearray(encoded))
