from dataclasses import dataclass
import json
import socketserver
from back.services.ebookService import EbookController
from back.services.libraryService import LibraryController
from back.db import sqlite_db
from back.services.authorService import AuthorController
from back.services.countriesService import CountryController
from back.services.readingListService import ReadingListController
from back.services.readingsService import ReadingsController

NEW_LINE = "\r\n"

class MyHTTPService():
    @staticmethod
    def parse_request(request : bytes) -> dict:
        splitted_request = request.decode().split(NEW_LINE)
        [method, uri, _] = splitted_request[0].split(" ")
        # Always creates at least an empty list for data, avoids unpacking errors
        endpoint = ""
        if method in ["GET", "DELETE"] :
            if '?' in uri:
                # With query params
                endpoint, params = uri.rsplit("?", 1)
                if '&' in params:
                    params = params.split('&')
                    data = [p.split('=') for p in params]
                else:
                    data = params.split('=')
            # Without query params
            elif uri.count('/') > 2:
                endpoint,*data = uri.rsplit("/", 1)
            else:
                endpoint = uri
                data = []

        else:
            # No post or put without a json body, so no query in uri
            # Breaks with Value Error if no body but POST or PUT
            separator = splitted_request.index('')
            data = "\r\n".join(splitted_request[separator+1:])

        if not data:
            data = None
        else :
            data = [d.replace('+', ' ') for d in data]
            
        return {"method" : method, "uri" : endpoint if endpoint else uri, "data" : data}
    

    @staticmethod
    def create_response_from(code, content_type, message):
        status = {200 : "OK",
                  201 : "Resource created",
                  204 : "No content",
                  400 : "Bad Request",
                  404 : "Not found",
                  500 : "Internal Server Error",
                  501 : "Not Implemented"}
        response = []
        response.append(f'HTTP/1.1 {code} {status[code]}{NEW_LINE}')
        response.append(f'Content-Type : {content_type}; charset=utf-8{NEW_LINE}')
        response.append(f'Access-Control-Allow-Origin: http://localhost:5173{NEW_LINE}')
        response.append(f'{NEW_LINE}')
        response.append(message)
        return "".join(response)


class RouterService():
    @staticmethod
    def call_service(uri, method, db, data) -> LibraryController:
        # print("uri is ", uri, uri == 'api/authors', list(enumerate(uri)), list(enumerate('api/authors')))

        if not method in ['GET', 'POST', 'PUT', 'DELETE']:
            raise Exception("How the hell did you miss that?")
        
        match uri:
            case '/api/authors':
                return AuthorController(db, method, data)
            case '/api/ebooks':
                return EbookController(db, method, data)
            case '/api/countries':
                return CountryController(db, method, data)
            case '/api/readings':
                return ReadingsController(db, method, data)
            case 'api/reading_lists':
                return ReadingListController(db, method, data)
            # case '/api/search':
            case _:
                raise Exception("err... what did you want again ?")


class MyTCPHandler(socketserver.BaseRequestHandler): 
    def handle(self):
        request = self.request.recv(1024).strip()
        print(request)
        decoded_request = MyHTTPService.parse_request(request)
        print(decoded_request)
        env = json.loads(open('back/env.json', 'r').read())
        with sqlite_db.connect(env["database_test"]) as conn:
            code, message = RouterService.call_service(decoded_request["uri"], decoded_request["method"], conn, decoded_request["data"]).do()
            http_response = MyHTTPService.create_response_from(code, "application/json", str(message))
            encoded_response = http_response.encode()
            self.request.sendall(encoded_response)
