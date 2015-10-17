from provider.demo import main
from wsgiref.simple_server import make_server

if __name__ == '__main__':
    wsgi = main()
    server = make_server('0.0.0.0', 8888, wsgi)
    print 'listening 8888'
    server.serve_forever()


