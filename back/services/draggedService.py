import json
import os
import traceback
from typing import Literal
import pypdf
import ebookmeta

from back.services.libraryService import LibraryController

class DraggedService():
    def init_or_add_to_file(
        self, json_path: str, flag: Literal["init", "add"], filepaths: list[str]
    ) -> dict:
        '''Creates or adds to the dragged elements file and return what has been
        added in order to add those elements in the front.'''

        print("ENTER INIT OR ADD", flag, filepaths)
        data = {}
        added = {}

        if os.path.isfile(json_path):
            with open(json_path, 'r', encoding="utf-8") as fr:
                data = json.loads(fr.read())

        self.enrich_data(filepaths, data, added)

        with open(json_path, 'w', encoding="utf-8") as fw:
            json.dump(data, fw, indent = 4, separators=(',', ': '))

        return added

    def enrich_data(self, filepaths, data, added) :
        '''This mutates the data to insert in the dragged file and the added list.'''
        for f in filepaths:
            # We shall walk a whole directory if we drop one in there
            if os.path.isdir(f):
                paths  =[os.path.join(f, file) for file in os.listdir(f) if os.path.isfile(os.path.join(f, file))]
                self.enrich_data(paths, data, added)
                continue

            if f in data:
                continue

            metadata = self._get_file_metadata(f)
            # filtered_metadata = self._filter_metadata(metadata)

            data[f] = added[f] = metadata

    def update_json_file(
        self, json_path: str, book_path: str|list[str], updated_book_metadata: dict
    ) -> dict:

        updated = {}

        with open(json_path, 'r', encoding="utf-8") as fr:
            data_json = json.loads(fr.read())

        if isinstance(book_path, list):
            for b in book_path:
                assert b in data_json, f"Error in update_json_file (Dragged Service line 39) : {b} is not a key."
                data_json[b] = data_json[b] | updated_book_metadata
                updated[b] = data_json[b]
        else:
            assert book_path in data_json, f"Error in update_json_file (Dragged Service line 39) : {book_path} is not a key."
            data_json[book_path] = data_json[book_path] | updated_book_metadata
            updated[book_path] = data_json[book_path]

        with open(json_path, 'w', encoding="utf-8") as fw:
            json.dump(data_json, fw, indent=4, separators=(',', ': '))
        
        return updated
    

    def delete_from_file(self, json_path : str, data : str | list[str]):
        with open(json_path, 'r', encoding="utf-8") as fr:
            data_json = json.loads(fr.read())

        if isinstance(data, str):
            del data_json[data]
        elif isinstance(data, list):
            for f in data:
                del data_json[f]

        with open(json_path, 'w', encoding="utf-8") as fw:
            # json.dump(data_json, fw, indent=4, separators=(',', ': '))
            json.dump(data_json, fw)

    def _get_file_metadata(self, filepath : str):
        _, ext = os.path.splitext(filepath)
        if ext not in ['.pdf', '.epub']:
            raise TypeError(f"File is not supported (only pdf and epub) : {ext}")

        md = {
            "title": "",
            "author": [],
            "publisher": "",
            "year_of_publication": "",
            "theme": [],
            "genre": [],
        }

        if ext == '.pdf':
            with open(filepath, 'rb') as fr:
                reader = pypdf.PdfReader(fr)
                metadata = self._convert_pdf_metadata(reader.metadata)

        elif ext == '.epub':
            epub = ebookmeta.get_metadata(filepath)
            metadata = self._convert_epub_metadata(epub)

        md = md | metadata
        if not md["title"]:
            md["title"] = os.path.basename(filepath)
        return metadata


    def _filter_metadata(self, metadata) -> dict:
        filtered = {}

        for k,v in metadata.items():
            if k in ["author", "title"]:
                filtered[k] = v
            elif k in ["publisher", "ebx_publisher"]:
                filtered["publisher"] = v
        return filtered

    def _convert_pdf_metadata(self, metadata):
        m = dict()
        for k, v in metadata.items():
            # Translates /Author as author, for ex.
            k = k[1:].lower()
            if k == "author":
                m[k] = v.split(',') if ',' in v else [v]
                continue
            m[k] = v
        if not "author" in m:
            m["author"] = []
        return m

    def _convert_epub_metadata(self, metadata) -> dict:
        m = dict()
        m["author"] = metadata.author_list
        m["title"] = metadata.title
        m["tags"] = metadata.tag_list
        m["publisher"] = metadata.publish_info.publisher
        m["year_of_publication"] = metadata.publish_info.year
        m["genre"] = []
        m["theme"] = []
        return m


class DraggedController(LibraryController):
    def __init__(self, filepath, method, data):
        self.file = filepath
        self.method = method
        self.data = json.loads(data) if data else {}

    def do_GET(self):
        if not (self.file):
            return 200, {}
        assert(os.path.isfile(self.file))
        with open(self.file, 'r', encoding="utf-8") as fr:
            file = fr.read()
        return 200, file

    def do_POST(self):
        assert("filepaths" in self.data and isinstance(self.data["filepaths"], list))
        try:
            operation = 'init' if not os.path.isfile(self.file) else 'add'
            added = DraggedService().init_or_add_to_file(self.file, operation, self.data["filepaths"])  
            assert(os.path.isfile(self.file))
            return 200, json.dumps(added)
        except Exception as e:
            print(traceback.format_exc())
            return 500, 'Error during the writing of the json file : ' + str(e)

    def do_PUT(self):
        assert(len(self.data.keys()) == 2 and 'filepath' in self.data and 'metadata' in self.data) 
        try:
            updated = DraggedService().update_json_file(self.file, self.data["filepath"], self.data["metadata"])
            return 200, json.dumps(updated)
        except Exception as e:
            return 500, 'Error during the update of the json file : ' + str(e)

    def do_DELETE(self):
        assert "filepath" in self.data and (
            isinstance(self.data["filepath"], str)
            or isinstance(self.data["filepath"], list)
        )

        try:
            DraggedService().delete_from_file(self.file, self.data["filepath"])
            return 200, 'Successfully deleted.'
        except Exception as e:
            return 500, str(e)


