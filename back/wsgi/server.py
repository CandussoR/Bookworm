from dataclasses import dataclass
import json
import socketserver
from back.services.draggedService import DraggedController
from back.services.ebookService import EbookController
from back.services.libraryService import LibraryController
from back.db import sqlite_db
from back.services.authorService import AuthorController
from back.services.countriesService import CountryController
from back.services.readingListService import ReadingListController
from back.services.readingsService import ReadingsController
from operator import itemgetter

NEW_LINE = "\r\n"

class MyHTTPService():
    @staticmethod
    def get_headers(request : list[str]) -> dict:
        headers = {}
        [headers["method"], headers["uri"], _] = request[0].split(" ")
        for line in request[1:]:
            # Distinction between the headers and body since request split on new_line
            if line == "":
                break
            k, v = line.split(': ')
            headers[k] = v
        return headers


    @staticmethod
    def parse_request(request : bytes) -> dict:
        splitted_request = request.decode().split(NEW_LINE)
        print("REQUEST CAME IN, FIRST BUFFER", splitted_request)
        headers = MyHTTPService.get_headers(splitted_request)
        endpoint = headers["uri"]

        # Preflight, it's about sending a message
        if headers["method"] == 'OPTIONS':
            return {"headers" : {"method" : "OPTIONS"}, "data" : ""}

        # With query params
        if headers["method"] in ["GET", "DELETE"] and '?' in headers["uri"]:
            endpoint, params = headers["uri"].rsplit("?", 1)
            if '&' in params:
                params = params.split('&')
                data = [p.split('=') for p in params]
            else:
                data = params.split('=')
            # Cleans query params
            data = [d.replace('+', ' ') for d in data]
            # Gets the uri without its params
            headers["uri"] = endpoint

        # Without query params, 
        # /api/sth -> two slashes, if we need one more, up until now it's a guid
        elif headers["method"] in ["GET", "DELETE"] and headers["uri"].count('/') > 2: 
            # TODO : Correct this if we ever use and endpoint with more then 3 slashes
            headers["uri"],*data = headers["uri"].rsplit("/", 1)

        # We only get a request without data if it's a get, so we can check it at this point
        elif headers["method"] == "GET":
            data = None

        else:
            # If we came this far, the request MUST have a body.
            # This has to break and does so with Value Error.
            separator = splitted_request.index('')
            data = "\r\n".join(splitted_request[separator+1:])
        
        return {"headers" : headers, "data" : data}


    @staticmethod
    def create_response_from(code, content_type, message):
        status = {
            200: "OK",
            201: "Resource created",
            204: "No content", 400: "Bad Request",
            404: "Not found",
            500: "Internal Server Error",
            501: "Not Implemented",
        }
        response = [
            f"HTTP/1.1 {code} {status[code]}{NEW_LINE}",
            f"Content-Type : {content_type}; charset=utf-8{NEW_LINE}",
            f"Content-Length: {len(message.encode())}{NEW_LINE}",
            f"Connection: keep-alive{NEW_LINE}",
            f"Access-Control-Allow-Origin: http://localhost:5173{NEW_LINE}",
            f"Access-Control-Allow-Methods: POST, PUT, DELETE, GET, OPTIONS{NEW_LINE}",
            f"Access-Control-Allow-Headers: content-type{NEW_LINE}",
            f"{NEW_LINE}",
            message,
        ]
        return "".join(response)


class RouterService():
    @staticmethod
    def call_service(uri, method, db, data) -> LibraryController:

        if not method in ['GET', 'POST', 'PUT', 'DELETE']:
            raise Exception("How the hell did you miss that?")

        match uri:
            case '/api/ebooks':
                return EbookController(db, method, data)
            case '/api/authors':
                return AuthorController(db, method, data)
            case '/api/countries':
                return CountryController(db, method, data)
            case '/api/readings':
                return ReadingsController(db, method, data)
            case '/api/reading_lists':
                return ReadingListController(db, method, data)
            case '/api/dragged':
                return DraggedController(db, method, data)
            case _:
                raise Exception("err... what did you want again ?")


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        request = self.request.recv(1024).strip()
        headers, data = MyHTTPService.parse_request(request).values()

        if headers["method"] == "OPTIONS":
            code, message = 200, data
        else:
            # Axios always send Content-Length with a body
            if headers.get("Content-Length") and data:
                while len(data) < int(headers["Content-Length"]):
                    new_chunk = self.request.recv(1024)
                    if not new_chunk:
                        break
                    data += new_chunk.decode()
                    print(len(data), int(headers["Content-Length"]))

            env = json.loads(open('back/env.json', 'r').read())
            with sqlite_db.connect(env["database_test"]) as conn:
                service = RouterService.call_service(
                    headers["uri"],
                    headers["method"],
                    conn,
                    data
                )
                # Ignoring type because all the methods have to be implemented
                # in child classes or app should break.
                code, message = service.do() #type: ignore
                print("code", code, "\nmessage", message)
        http_response = MyHTTPService.create_response_from(code, "application/json", str(message))
        encoded_response = http_response.encode()
        print("encoded response\n", encoded_response)
        self.request.sendall(encoded_response)
