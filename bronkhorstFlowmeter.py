from numpy import power import serial import struct
#Module for creating a certain humidity of a gas stream Antoine Equation 
#Parameters (P in mmHg, T in °C) No. A B C Tmin [°C] Tmax [°C] 1 
#8.07131 1730.63 233.426 1 100 2 8.14019 1810.94 244.485 99 374 
#Constants
aConst= 8.07131 
bConst= 1730.63 
cConst= 233.426 
atmConst= 1013.25 
idealConst=22.4 

def satVaporPressure(TC):
    return((power(10,aConst-(bConst/(cConst+TC)))*1.33322)) 

def moleRatio(tempVP, pressure):
    return(tempVP/(pressure-tempVP)) 

def saturatedWaterFlow(flow,ratio):
    return((ratio*flow*18*60)/idealConst)
    
def relativeHumidity(percent,temp,flow, pressure):
    rh=(percent*satVaporPressure(temp, pressure))/100
    rhMoleRatio=moleRatio(rh)
    return(saturatedWaterFlow(flow,rhMoleRatio))
    
#here we will begin to configure the MFC
def intiateMFC(node):
    if isinstance(node, str) and len(node) == 2:
        cmd = [':', '0500', node, '000A49']
        cmdJoin = ''.join(cmd)
        return(cmdJoin)
    else:
        if len(node) != 2:
            print ('Please Send an approperiate node length,')
        print ('Please Send a String')

#this could be used if we want to use FLOW-bus protocols
def setNodeAddress(node, newAddress):
    if isinstance(node, str) and len(node) == 2 and len(newAddress) == 
2:
        cmd = [':', '05', node, '01', newAddress, '01']
        cmdJoin = ''.join(cmd)
        return(cmdJoin)
    else:
        if len(node) != 2:
            print ('Please Send an approperiate node length')
        if len(newAddress) != 2:
            print ('Please Send an approperiate address length')
        print('Please send a string')

#this is essential for being able to to control the MFC by RS232
def setToRs232(node):
   if isinstance(node, str) and len(node) == 2:
        cmd = [':', '05', node, '01010412']
        cmdJoin = ''.join(cmd)
        return(cmdJoin)
   else:
       print('Please send a string')

#set the setpoint(0 to 32000)
def setMFCSetPoint (node, setPoint):
    if isinstance(node, str) and len(node) == 2 and -1 < int(setPoint) and int(setPoint) <= 32000:
        cmd = [':', '06', node, '010121', format(int(setPoint), 'x')]
        cmdJoin = ''.join(cmd)
        return(cmdJoin)
    else:
        if len(node) != 2:
            print ('Please Send an approperiate node length')
        if (-1 > int(setPoint) or int(setPoint) > 32000):
            print('Bad setpoint operation, 32000 is max')
    print('Please send a string')
    
#the MFC uses IEEE-floating point conversion this is not the safest way 
#to generate that number
def setChainedParmeter(node, polyA, polyB, polyC, polyD):
    polyA= floatToHex(polyA)[2:]
    polyB= floatToHex(polyB)[2:]
    polyC= floatToHex(polyC)[2:]
    polyD= floatToHex(polyD)[2:]
    if isinstance(node, str):
        cmd = [':', '1D', node, '01800A4081C5',polyA, '',
                    'C6', polyB, 'C7', polyC, '48', polyD, '000A52']
        cmdJoin = ''.join(cmd)
        return(cmdJoin)
    print('Please send a string')

#awful way to make the ieee floating point in hex, 0 as an fp is to ugly
def floatToHex(f):
    ieee= hex(struct.unpack('<I', struct.pack('<f', f))[0])
    if ieee == '0x0':
        return ('0x00000000')
    else:
        return(ieee)
        
#command to retrieve setpoint
def requestSetPoint(node):
    if isinstance(node, str) and len(node) == 2:
        cmd = [':', '06', node, '0401210121']
        cmdJoin = ''.join(cmd)
        return(cmdJoin) def requestMeasure(node):
     if isinstance(node, str) and len(node) == 2:
         cmd = [':', '06', node, '04', '01', '21', '01', '20']
         cmdJoin = ''.join(cmd)
         return(cmdJoin) def parseMeasure(msg):
    msgValue = int(msg[-4:], 16)
    return(msgValue)

    
struct.unpack('!f', bytes.fromhex('3F800000'))
