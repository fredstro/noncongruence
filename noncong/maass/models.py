r"""

Classes for representing Maass forms and related objects for subgroups of the 
modular group.

"""
from mongoengine.fields import BaseField
from ..extensions import mongoeng as db
from ..backend.utils import list_of_tuples_to_json,string_of_list_to_cycles,mygetattr,lcm
from ..subgroups.models import Subgroup
from flask import json
from encoder import ExtendedEncoder,ExtendedDecoder
#from flask.ext.mongoengine import Document
import logging

log = logging.getLogger(__name__)

class ComplexNumberField(BaseField):
    def to_python(self,value):
        if not isinstance(value,dict):
            return json.loads(value,cls=ExtendedDecoder)
        else:
            return value
    def to_mongo(self, value):
        return json.dumps(value,cls=ExtendedEncoder)


class ScatteringDeterminant(db.Document):
    r"""
    Class to represent phi(s) - values of the scattering determinant for 
    subgroups of the modular group.
    """
    meta = {
        'indexes' : [
            {'fields':('group','t'),'unique':True}
            ]
    }
    group = db.ReferenceField(Subgroup,required=True)
    sigma = db.FloatField()
    t = db.FloatField()
    value = ComplexNumberField()
    
    
class MaassEigenvalue(db.Document):
    r"""
    Class to represent Maass form eigenvalues
    """
    group = db.ReferenceField(Subgroup,required=True)
    R = db.FloatField(required=True)
    err=db.FloatField()
    Y=db.FloatField()
    M=db.IntField()
    
class DeltaArgument(db.Document):
    r"""
    Class containing spline points which represent the function M(T)=DeltaArg phi(1/2+it)
    Requires: Sage
    """
    group = db.ReferenceField(Subgroup,required=True)
    pts = db.BinaryField() ## json string
    maxT=db.FloatField()
    def save(self,**kwds):
        from sage.all import dumps
        if isinstance(self.pts,list):
            self.pts = dumps(self.pts)
        super(DeltaArg,self).save(**kwds)
    def spline(self):
        from sage.all import Spline,loads
        return Spline(loads(self.pts))

    
