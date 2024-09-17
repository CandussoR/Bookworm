import socketserver
from back.wsgi.server import MyTCPHandler

if __name__ == '__main__':
    server = socketserver.TCPServer(("127.0.0.1", 9999), MyTCPHandler)
    server.serve_forever()