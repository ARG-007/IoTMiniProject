from json import loads,dumps
from gpio import *
from time import *
from file import *
from ioeclient import *
from HttpServer import initHttp
from physical import *
from networking import localIP

pinSlots = {"A0":A0, "A1":A1,"A2":A2, "A3":A3}

ConnectedDevices = {}

ip = localIP()

class Device:
    def __init__(self, device):
        global pinSlots
        self.name = device['config']['name']
        self.defaultState = device['defaultState']
        self.pin = device['pin'] if device['pin'] not in pinSlots else pinSlots[device['pin']]
        self.config = device['config']
        self.currentState = None

        self.readable = device['readable']
        self.writable = device['config']['controllable']


        self.read ,self.write = getReadWrite(self.config["type"])
        self.setState(self.defaultState)
        if(self.readable):
            add_event_detect(self.pin, lambda : self.getState())
            self.getState()

    def getState(self):
        if not self.readable:
            return
        self.currentState = self.read(self.pin)
        reportState()

    def setState(self, value):
        if not self.writable:
            return
        self.currentState = value
        if self.config["type"] == "bool":
            self.write(self.pin, HIGH if value!="0" else LOW)
        else:
            self.write(self.pin,value)

def init():
    loadConfig()
    setupIoE()

def main():
    init()
    initHttp(onConfigUpdate)
    while True:
        checkForIPChange()
        reportState()
        sleep(100)

def setupIoE():
    global ConnectedDevices
    global ip
    IoEClient.setup({
        "type":ip,
        "states": [i.config for i in ConnectedDevices.values()]
    })
    
    IoEClient.onStateSet(setDeviceState)


def setDeviceState(device, state):
    ConnectedDevices[device].setState(state)
    reportState()


def reportState():
    try:
        states = ",".join([str(ConnectedDevices[i].currentState) for i in ConnectedDevices])
        print(states)
        IoEClient.reportStates(states)
    except Exception as e:
        print(e)


def checkForIPChange():
    global ip
    if ip!=localIP():
        ip = localIP()
        setupIoE()

def loadConfig():
    global ConnectedDevices
    global SBC_Name

    json = ""

    jsonFile =open("/config.json","r")

    line = jsonFile.readline()
    while(line!=''):
        json+=line.strip('\n')
        line = jsonFile.readline()
    jsonFile.close()

    json = loads(json)

    setDeviceProperty(getName(),"name",json['deviceID'])

    for i in json['devices'].values():
        device = Device(i)
        ConnectedDevices[device.name] = device

def onConfigUpdate(configJSON):
    global ConnectedDevices
    configFile = open("/config.json","w")
    for i in configJSON:
        configFile.write(i)
    configFile.close()
    ConnectedDevices = {}
    init()

def getReadWrite(type):
        if(type == 'bool'):
            return (digitalRead, digitalWrite)
        elif(type == 'number'):
            return (analogRead, analogWrite)
        else:
            return (customRead, customWrite)



if __name__ == "__main__":
    main()