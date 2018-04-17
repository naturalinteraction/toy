from twisted.web import server, resource
from twisted.internet import reactor

global log
log = ''

def Page():
    return log

class WebPage(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        if not 'pump' in str(request):
            return ''
        return '<head><link rel="icon" href="http://naturalinteraction.org/favicon.ico">' + '' + '</head><body><font face="Arial">' + Page() + '</font></body>'

def UpdateWeb(text):
    global log
    log = text

def StartWebServer():
    site = server.Site(WebPage())
    reactor.listenTCP(40000, site)
    reactor.startRunning(False)

def WebServerIterate():
    reactor.iterate()
