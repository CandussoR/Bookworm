from typing import Callable
from uuid import UUID


class BaseRequest:
    def from_json(self, a_dict):
        for key in self.__dict__.keys():
            for k,v in a_dict.items():
                if k in key:
                    if '_guid' in k:
                        self.__dict__[k] = UUID(v)
                    else :
                        self.__dict__[k] = v
                    break
        self.validate()
        return self
    
    def validate(self):
        raise NotImplementedError("This method needs implementation")