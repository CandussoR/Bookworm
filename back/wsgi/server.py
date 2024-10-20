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
        headers = MyHTTPService.get_headers(splitted_request)

        if headers["method"] == 'OPTIONS':
            return {"headers" : {"method" : "OPTIONS"}, "data" : ""}

        if headers["method"] in ["GET", "DELETE"] :
            endpoint = ""
            if '?' in headers["uri"]:
                # With query params
                endpoint, params = headers["uri"].rsplit("?", 1)
                if '&' in params:
                    params = params.split('&')
                    data = [p.split('=') for p in params]
                else:
                    data = params.split('=')
            # Without query params
            elif headers["uri"].count('/') > 2:
                # TODO : Correct this if we ever use and endpoint with more then 3 slashes
                endpoint,*data = headers["uri"].rsplit("/", 1)
            else:
                endpoint = headers["uri"]
                data = []

        else:
            # No post or put without a json body, so no query in uri
            # Breaks with Value Error if no body but POST or PUT
            separator = splitted_request.index('')
            data = "\r\n".join(splitted_request[separator+1:])

        if not data:
            data = None
        elif data and '+' in data:
            # Cleans query params
            data = [d.replace('+', ' ') for d in data]
        
        if endpoint:
            headers["uri"] = endpoint
        
        return {"headers" : headers, "data" : data}

    @staticmethod
    def create_response_from(code, content_type, message):
        status = {
            200: "OK",
            201: "Resource created",
            204: "No content",
            400: "Bad Request",
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
