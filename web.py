from twisted.web import server, resource
from twisted.internet import reactor

def Page():
    return ('page')

class WebPage(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        if not 'pump' in str(request):
            return ''
        refresh = ''
        return '<head><link rel="icon" href="http://naturalinteraction.org/favicon.ico">' + refresh + '</head><body><font face="Arial">' + Page() + '</font></body>'

def StartWebServer():
    site = server.Site(WebPage())
    reactor.listenTCP(50000, site)
    reactor.startRunning(False)

def WebServerIterate():
    reactor.iterate()
