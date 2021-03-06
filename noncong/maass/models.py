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
        if isinstance(value,basestring):
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
            {'fields':('group','t','sigma'),'unique':True}
            ],
        'db_alias': 'scattering-determinant'
    }
    group = db.ReferenceField(Subgroup,required=True)
    sigma = db.FloatField()
    t = db.FloatField()
    value = ComplexNumberField()
    is_zero=db.BooleanField()  ## Set to true to indicate that this is one of the located zeros 

class ScatteringMatrixHalfSigns(db.Document):
    """
    Stores the number of +1 and -1 on the diagonal of \Phi(1/2)
    """
    group = db.ReferenceField(Subgroup,required=True)
    plus_count = db.IntField()
    minus_count = db.IntField()
    meta = {
        'indexes': [
            {'fields': ('group',), 'unique': True}
        ]
    }
    def __unicode__(self):
        return u"({1},{2}) : {0}".format(self.group
                                         ,self.plus_count,self.minus_count)
        
class MaassEigenvalue(db.Document):
    r"""
    Class to represent Maass form eigenvalues
    """
    meta = {
          'indexes': [
            {'fields': ('group','R'), 'unique': True},
            {'fields': ('R',), 'unique': False},
        ]
    }
    group = db.ReferenceField(Subgroup,required=True)
    R = db.FloatField(required=True)
    err=db.FloatField()
    Y=db.FloatField()
    M=db.IntField()
    dim=db.IntField()
    C2=ComplexNumberField() # C(2)  mainly here to help detect multiple eigenvalues.
    Cm1=ComplexNumberField()# C(-1) and to estimate errors
    new=db.BooleanField()
    
class DeltaArg(db.Document):
    r"""
    Class containing spline points which represent the function M(T)=DeltaArg phi(1/2+it)
    Requires: Sage
    """
    group = db.ReferenceField(Subgroup,required=True)
    pts = db.BinaryField() ## json string
    maxT=db.FloatField()
    meta = {
          'indexes': [
            {'fields': ('group',), 'unique': True}
        ]
    }
    def save(self,**kwds):
        from sage.all import dumps
        ## 
        if isinstance(self.pts,list):
            self.maxT=max(self.pts)[0]
            ## We can't make a Spline if we have duplicate x-coords
            d = dict(self.pts)
            self.pts = zip(d.keys(),d.values())
            self.pts = dumps(self.pts)
            
        super(DeltaArg,self).save(**kwds)
        
    def spline(self):
        from sage.all import Spline,loads
        return Spline(loads(self.pts))

    
