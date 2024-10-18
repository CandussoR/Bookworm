import json
import os
from typing import Literal
import pypdf
import epub_metadata

from back.services.libraryService import LibraryController

class DraggedService():
    def init_or_add_to_file(self, json_path : str, flag : Literal['init', 'add'], filepaths : list[str]):
        d = {}
        for f in filepaths:
            metadata = self._get_file_metadata(f)
            d[f] = metadata
        with open(json_path, 'w' if flag == 'init' else 'w+', encoding="utf-8") as fw:
            json.dump(d, fw, indent = 4, separators=(',', ': '))


    def update_json_file(self, json_path : str, book_path : str, updated_book_metadata : dict):
        with open(json_path, 'r', encoding="utf-8") as fr:
            data_json = json.loads(fr.read())
        data_json[book_path] = updated_book_metadata
        with open(json_path, 'w', encoding="utf-8") as fw:
            json.dump(data_json, fw, indent=4, separators=(',', ': '))


    def _get_file_metadata(self, filepath : str):
        _, ext = os.path.splitext(filepath)
        if ext not in ['.pdf', '.epub']:
            raise TypeError("File is not supported (only pdf and epub).")
        
        if ext == '.pdf':
            with open(filepath, 'rb') as fr:
                reader = pypdf.PdfReader(fr)
                metadata = self._convert_pdf_metadata(reader.metadata)

        elif ext == '.epub':
            epub = epub_metadata.epub(filepath)
            metadata = epub.metadata

        return metadata
    
    def _convert_pdf_metadata(self, metadata):
        m = dict()
        for k, v in metadata.items():
            m[k[1:].lower()] = v
        return m
        
class DraggedController(LibraryController):
    def __init__(self, _, method, data):
        self.file = './dragged.json'
        self.data = data


    def do_GET(self):
        if not (self.file):
            return 200, {}
        return 200, json.loads(self.file)
    

    def do_POST(self):
        assert("filepaths" in self.data and isinstance(self.data.filepaths, list))
        try:
            if not os.path.isfile(self.file):
                DraggedService().init_or_add_to_file(self.file, 'init', self.data.filepaths)  
            else:
                DraggedService().init_or_add_to_file(self.file, 'add', self.data.filepaths)
            assert(os.path.isfile(self.file))
            return 200, ''
        except Exception as e:
            return 500, 'Error during the writing of the json file : ' + str(e)


    def do_PUT(self):
        assert(len(self.data.keys()) == 2 and 'filepath' in self.data and 'metadata' in self.data) 
        try:
            DraggedService().update_json_file(self.file, self.data.filepath, self.data.metadata)
            return 200, ''
        except Exception as e:
            return 500, 'Error during the update of the json file : ' + str(e)
        

    def do_DELETE(self):
        with open(self.file, 'r', encoding="utf-8") as fr:
            data_json = json.loads(fr.read())
        del data_json[self.data.filepath]
        with open(self.file, 'w', encoding="utf-8") as fw:
            json.dump(data_json, fw, indent=4, separators=(',', ': '))
        return 200, 'Deleted.'

        