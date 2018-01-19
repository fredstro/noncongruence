r"""

Extended JSOn Encoder

"""
import json
from collections import Iterable,Sequence
from bson import ObjectId
from datetime import datetime

class ExtendedEncoder(json.JSONEncoder):
    """
    Extended JSON Encoder to recursively encode dates and complex numbers.
    """
    def default(self, obj):
        if isinstance(obj,Sequence):
            return [self.default(x) for x in obj]
        if isinstance(obj, Iterable):
            return {unicode(key) : getattr(obj, key) for key in obj}
        if isinstance(obj, ObjectId):
            return unicode(obj)
        if isinstance(obj, datetime):
            return datetime.strftime(obj,"%Y-%m-%d %T")
        if isinstance(obj,complex):
            return {"__type__":"cplx","re":obj.real,"im":obj.imag}
        elif hasattr(obj,'real'):
            return {"re":float(obj.real()),"im":float(obj.imag()),"__type__":"cplx"}
        return json.JSONEncoder.default(self, obj)

    
class ExtendedDecoder(json.JSONDecoder):
    def __init__(self,**kwds):
        json.JSONDecoder.__init__(self, object_hook=self.dict_to_object)

    def dict_to_object(self, d):
        if d.get('__type__')=='cplx':
            return complex(d['re'],d['im'])
        else:
            inst = d
        return inst
