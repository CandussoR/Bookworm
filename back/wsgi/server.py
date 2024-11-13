from dataclasses import dataclass
import json
import socketserver
from typing import Optional
from back.services.draggedService import DraggedController
from back.services.ebookService import EbookController
from back.services.libraryService import LibraryController
from back.db import sqlite_db
from back.services.authorService import AuthorController
from back.services.countriesService import CountryController
from back.services.readingListService import ReadingListController
from back.services.readingsService import ReadingsController
from operator import itemgetter

from back.services.searchService import SearchController

NEW_LINE = "\r\n"
BODY = b"\r\n\r\n"

class MyHTTPService():
    @staticmethod
    def get_headers_from_bytes(request : bytes) -> dict:
        splitted_request = request.decode().split(NEW_LINE)
        headers = {}
        [headers["method"], headers["uri"], _] = splitted_request[0].split(" ")
        for line in splitted_request[1:]:
            # Distinction between the headers and body since request split on new_line
            if line == "":
                break
            k, v = line.split(': ')
            headers[k] = v
        return headers

    @staticmethod
    def parse_request(headers : dict) -> str | None :
        data = None

        if headers["method"] not in ["GET", "DELETE"]:
            return data

        # With query params
        if '?' in headers["uri"]:
            params = headers["uri"].rsplit("?", 1).pop()
            if '&' in params:
                params = params.split('&')
                data = [p.split('=') for p in params]
            else:
                data = params.split('=')
            # Cleans query params
            # TODO : remember why this is only in a matrix and not a dict
            data = [d.replace('+', ' ') for d in data]

        # Without query params, 
        # /api/sth -> two slashes, if we need one more, up until now it's a guid
        if headers["uri"].count('/') > 2: 
            # TODO : Correct this if we ever use and endpoint with more then 3 slashes
            data = headers["uri"].rsplit("/", 1).pop()

        return data


    @staticmethod
    def parse_uri(uri : str) -> str:
        if '?' in uri:
            return uri.rsplit("?", 1)[0]
        elif uri.count('/') > 2:
            return uri.rsplit("/", 1)[0]
        return uri
        

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
        return "".join(response).encode()


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
                return DraggedController('./dragged.json', method, data)
            case '/api/search':
                return SearchController(db, "GET", data)
            case _:
                raise Exception("err... what did you want again ?")

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = None

        headers, body = self.request.recv(4096).split(BODY)
        print("ENTERING REQUEST", BODY.join([headers, body]))
        parsed_headers = MyHTTPService.get_headers_from_bytes(headers)

        if parsed_headers["method"] == "OPTIONS":
            http_response = MyHTTPService.create_response_from(200, "application/json", str(''))
            self.request.sendall(http_response)
            return

        # Axios always send Content-Length with a body
        if body and parsed_headers.get("Content-Length"):
            while len(body) < int(parsed_headers["Content-Length"]):
                new_chunk = self.request.recv(4096)
                if not new_chunk:
                    break
                body += new_chunk

        # If data not in body but in request (params)
        # No slug in this app for now so no worries about data both in uri and body
        elif not body:
            if parsed_headers["method"] in ["POST", "PUT"]:
                raise Exception("POST or PUT MUST have a body.")
            data = MyHTTPService.parse_request(parsed_headers)

        # Ensuring we forward the good uri
        parsed_headers["uri"] = MyHTTPService.parse_uri(parsed_headers["uri"])

        env = json.loads(open('back/env.json', 'r').read())
        with sqlite_db.connect(env["database_test"]) as conn:
            service = RouterService.call_service(
                    parsed_headers["uri"],
                    parsed_headers["method"],
                    conn,
                    data if data else body.decode()
                )
            # Ignoring type because all the methods have to be implemented
            # in child classes or app should break.
            code, message = service.do() #type: ignore
            print("code", code, "\nmessage", message)
            http_response = MyHTTPService.create_response_from(code, "application/json", str(message))
            print("sending this response", http_response)
            self.request.sendall(http_response)