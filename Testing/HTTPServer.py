from realhttp import *

def initHttp(callback):
    HTTPServer = RealHTTPServer()
    HTTPServer.start(8012)
    print(HTTPServer.isListening())
    HTTPServer.route('/*',[],sendFile)
    HTTPServer.route('/setConfig/*',[], lambda u,req,res : setConfig(u,req,callback))
    
def sendFile(u,re,response):
    url = re.url()
    response.setHeaders({'Access-Control-Allow-Origin':"*"})
    if(url == "/"):
        response.sendFile("/index.html")
    else:
        response.sendFile(url)

def sendConfigHTML(url,re,response):
    response.sendFile('/index.html')
    
def sendConfigFile(url,re,response):
    response.setContentType('text/json')
    response.sendFile('/config.json')

def setConfig(url,request,callback):
    callback(request.url().strip("/setConfig/"))

def call(string):
    print(string.replace("%22",'"').replace("%7B","{").replace("%7D","}"))

if __name__ == "__main__":
    from time import *
    while True:
        sleep(100)