class LibraryController():
    '''Superclass for all the services.'''

    def __init__(self, db, method, data):
        self.db = db
        self.method = method
        self.data = data
    
    def do(self):
        match self.method:
            case "GET":
                return self.do_GET()
            case "POST":
                return self.do_POST()
            case "PUT":
                return self.do_PUT()
            case "DELETE":
                return self.do_DELETE()
    
    def do_GET(self):
        raise NotImplemented("Method must be implemented in child class.")

    def do_POST(self):
        raise NotImplemented("Method must be implemented in child class.")

    def do_PUT(self):
        raise NotImplemented("Method must be implemented in child class.")

    def do_DELETE(self):
        raise NotImplemented("Method must be implemented in child class.")
