from http import *

def urlDecode(url):
    url = url.replace("%22",'"')
    url = url.replace("%7B",'{')
    url = url.replace("%7D",'}')
    url = url.replace("%20",' ')
    return url

def initHttp(callback):
    HTTPServer.start(80)
    HTTPServer.route('/*',sendFile)
    HTTPServer.route('/setConfig/*', lambda u,r : setConfig(u,r,callback))
    
def sendFile(url,response):
    print("Requested : "+url)
    if(url == "/"):
        response.sendFile("/index.html")
    else:
        response.sendFile(url)

def setConfig(url,response,callback):
    callback(urlDecode(url.strip("/setConfig/")))

def call(string):
    print(string)

if __name__ == "__main__":
    from time import *
    initHttp(call)
    while True:
        sleep(100)