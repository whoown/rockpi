import tornado.ioloop
import tornado.web

PORT = 5000

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello world")
        print "MainHandler - get"

class TestHandler1(tornado.web.RequestHandler):
    def get(self, id):
        self.write("The test1 id = "+id)
        print "TestHandler - get"

class TestHandler2(tornado.web.RequestHandler):
    def get(self):
        self.write('<html><body><form action="/" method="post">'
                   '<input type="text" name="message">'
                   '<input type="submit" value="Submit">'
                   '</form></body></html>')
        print "MainHandler - get"
    
    def post(self):
        self.set_header("Content-Type", "text/plain")
        self.write("Test2 write "+self.get_argument("message"))
        print "MainHandler - post"


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/test1/([0-9]+)", TestHandler1),
    (r"/test2/", TestHandler2),
])


if __name__ == '__main__':
    application.listen(PORT)



