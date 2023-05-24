//Abandoned

var deviceID;
var connectedDevices;



function setup(){
    loadConfig();

}

function getReaderWriter(device){
    switch(device.config.type){
        case 'bool' : return [digitalRead,digitalWrite];
        case 'number' : return [analogRead,analogWrite];
        default : return [customRead,customWrite];
    }
}

function loadConfig(){    
    var jsonString = "";

    var file = FileSystem.open('/config.json', File.READ);
    while(file.available()){
        jsonString+=file.readln();
    }
    
    file.close();

    var jsonObject = JSON.parse(jsonString);

    deviceID = jsonObject.deviceID;

    for(var i in jsonObject.devices){
        var device = jsonObject.devices[i]
        var readWrite = getReaderWriter(device);
        device.read = readWrite[0];
        device.write = readWrite[1];
        
    }
}