r"""

Classes for representing subgroups of the modular group as mongoengine documents.

"""
import pymongo
from ..extensions import mongoeng as db
from mongoengine import queryset_manager
from ..backend.utils import list_of_tuples_to_json,string_of_list_to_cycles,mygetattr,lcm
from flask import json
import logging

log = logging.getLogger(__name__)



class Signature(db.Document):
    r"""
    Represents the signature of a subgroup G of the (projective) modular group.
    Given by a tuple (index; g, ncusps, e2,e3) where

    index = the index of G in PSL(2,Z)
    g     = the genus of G
    ncusps= the number of cusp classes of G
    e2    = the number of elliptic classes of order 2
    e3    = the number of elliptic classes of order 3
    
    """
    index = db.IntField(required=True)
    genus = db.IntField(required=True)
    e2    = db.IntField(required=True)
    e3    = db.IntField(required=True)
    ncusps= db.IntField(required=True)    
    name = db.StringField()
    meta = {
        'indexes': [
            {'fields': ('index',), 'unique': False},
            {'fields': ('genus',), 'unique': False},
            {'fields': ('e2',), 'unique': False},
            {'fields': ('e3',), 'unique': False},
            {'fields': ('ncusps',), 'unique': False},
            {'fields': ('index','genus','e2','e3','ncusps'),'unique':True}
            ]
    }
    def __init__(self,**kwds):
        super(Signature,self).__init__(**kwds)
        
    def __str__(self):
        return "({index};{genus},{ncusps},{e2},{e3})".format(index=self.index,
            genus=self.genus,e2=self.e2,e3=self.e3,ncusps=self.ncusps)
    def __repr__(self):
        return str(self)
    def save(self,**kwds):
        if self.name is None:
            self.name = str(self)
        super(Signature,self).save(**kwds)
        
class Subgroup(db.Document):
    signature = db.ReferenceField(Signature)
    ## We also list the individual properties of the signature to be able to search more efficient.
    index = db.IntField()
    e2 = db.IntField()
    e3 = db.IntField()
    genus = db.IntField()
    ncusps = db.IntField()

    ## Represent a list of element in SL2Z by a json string of the form:
    ## '[[a1,b1,c1,d1],[a2,b2,c2,d2],...[an,bn,cn,dn]]'

    coset_representatives = db.StringField(required=True) 
    generators            = db.StringField()
    # Permutations are stored as strings of lists, e.g. '[1,2,3]'
    # 
    permS                 = db.StringField(required=True) # permutation representing S   =[0,-1,1,0]
    permR                 = db.StringField(required=True) # permutation representing R=ST=[0,-1,1,1]
    permT                 = db.StringField(required=True) # permutation representing T   =[1,1,0,1]
    # A combined field which is hashed to a unique index.
    permS_permR           = db.StringField()
    ## Because the map between groups and permutations is *homomorphism*: permS*permT=permR
    label      = db.StringField() 
    name       = db.StringField()
    common_name= db.StringField()
    latex_name = db.StringField()

    # properties
    congruence = db.BooleanField() # if self is a congruence group
    psl_rep    = db.BooleanField(default=False) # if self is a representative of its PSL(2,Z)-conjugacy class
    pgl_rep    = db.BooleanField(default=False) # if self is a representative of its PSL(2,Z)-conjugacy class

    # symmetry information
    symmetric       = db.BooleanField(default=False) ## Does self have a reflectional symmetry
    reflected_group = db.ReferenceField('Subgroup')
    reflection_info = db.StringField()

    # modular correspondences = same as symmetries?
    #modular_correspondence = db.ReferenceField(ModularCorrespondence)
    cusp_representatives = db.StringField()

    ## The group congruence cover (self) / self =~ <permS,permR> =~ Image(mod N)?
    permutation_group = db.StringField()

    generalized_level = db.IntField()

    supergroups = db.ListField(db.ReferenceField('Subgroup'))

    gamma0n_cover = db.IntField() # largest N for which self is a subgroup of Gamma0(N)
    meta = {
        'indexes' : [
            {'fields':('index',),'unique':False},
            {'fields':('e2',),'unique':False},
            {'fields':('e3',),'unique':False},
            {'fields':('genus',),'unique':False},
            {'fields':('ncusps',),'unique':False},                        
            {'fields':[('permS_permR',pymongo.HASHED)]},
            {'fields':('generators',),'unique':True},
        ],
        'strict': False
    }
    # Note that it is very hard to define a unique index here since the same group can be represented by many different
    # permutations.
    # We can try to find  a unique representative by using the "smallest" in some lexicographical sense, but
    # we can't guarantee that this is the representation in the database.
    #
    def save(self,**kwds):
        if self.signature is None:
            sig = Signature(e2=self.e2,e3=self.e3,ncusps=self.ncusps,genus=self.genus,index=self.index)
            sig.save()
            self.signature=sig
      
        if isinstance(kwds.get('signature'),dict):
            sig = Signature(**kwds['signature'])
            sig.save()
            self.signature=sig
        
        if self.e2 is None and not self.signature is None:
            self.e2     = self.signature.e2
            self.e3     = self.signature.e3
            self.genus  = self.signature.genus
            self.ncusps = self.signature.ncusps
            self.index  = self.signature.index

        if self.latex_name == '' or self.latex_name is None:
            s = "Subgroup of $\mathrm{{PSL}}(2,\mathbb{{Z}})$ of signature ${0}$ ".format(self.signature)
            s+= " with perm(T)= ${0}$ ".format(string_of_list_to_cycles(self.permT))
            self.latex_name = s
        if self.name == '' or self.name is None:
            s = "Subgroup of PS(2,Z) of signature {0} ".format(self.signature)
            s+= " with perm(T)= {0} ".format(string_of_list_to_cycles(self.permT))
            self.latex_name = s
        if self.congruence is None:
            try:
                self.congruence = self._to_sage().is_congruence()
            except ImportError:
                pass
        self.generalized_level = self.get_generalized_level()
        ## Now check if this exists
        self.permS_permR=self.permS+self.permR
        # Try harder to find self.
        g = type(self).find_group(self)
        if g is not None:
            self.id = g.id
        super(Subgroup,self).save(**kwds)
    
    def __init__(self,**kwds):
        #sig = kwds.get('signature')
        #if isinstance(sig,(tuple,list)):
        #    sig =
        super(Subgroup,self).__init__(**kwds)
            
    @queryset_manager
    def find_group(doc_cls, queryset,G):
        """
        Find a group in the database which is the same as the group G which is an instance of Subgroup.
        :param G:
        :return:
        """
        if not isinstance(G,Subgroup):
            raise NotImplementedError
        group = queryset.filter(permS_permR=G.permS_permR).first()
        if group is not None:
            return group
        signature = G.signature
        G = G._to_psage()
        for group in queryset.filter(signature=signature):
            try:
                for gen in group.gens():
                    if gen not in G:
                        raise StopIteration
                # If here then group is a subgroup of G and since the index is the same they must be equal
                return group
            except StopIteration:
                pass
        return None

    def __repr__(self):
        return str(self)
    def __unicode__(self):
        if self.name != '' and not self.name is None:
            return u'{0}'.format(self.name)
        elif self.latex_name:
            return u'{0}'.format(self.latex_name)
        else:
            return u'Subgroup of PSL(2,Z) with signature {0}, s(S)={1}, s(R)={2}'.format(
                self.signature,string_of_list_to_cycles(self.permS),string_of_list_to_cycles(self.permR))
    
        
    def coset_representatives_as_tuples(self):
        return json.loads(self.coset_representatives)

    def coset_representative_from_tuples(self,tuples):
        self.coset_representatives = list_of_tuples_to_json(tuples)
        return self.coset_representatives

    def S(self):
        return string_of_list_to_cycles(self.permS)
    def R(self):
        return string_of_list_to_cycles(self.permR)
    def T(self):
        return string_of_list_to_cycles(self.permT)
    def get_generalized_level(self):
        return lcm(map(lambda x: len(x),self.T()))
    
    def _to_psage(self):
        try:
            from psage.all import MySubgroup
        except ImportError as e:
            raise e
        return MySubgroup(s2=self.permS,s3=self.permR)
    def _to_sage(self):
        G = self._to_psage()
        return G.as_permutation_group()
    def is_congruence(self):
        if self.congruence is None:
            self.congruence = self._to_sage().is_congruence()
        return self.congruence

    def _get_canonical_labels(self):
        try:
            from psage.all import MySubgroup
        except ImportError as e:
            raise e
        G = self._to_psage()
        mapping = G._canonical_rooted_labels()
        s = [None]*G.index()
        r = [None]*G.index()
        t = [None]*G.index()
        for  i in range(G.index()):
            s[ mapping[i]] = mapping[G.permS(i+1)-1]+1 
            r[ mapping[i]] = mapping[G.permR(i+1)-1]+1 
            t[ mapping[i]] = mapping[G.permT(i+1)-1]+1 
        s = str(s).replace(" ","")
        r = str(r).replace(" ","")
        t = str(t).replace(" ","")
        return s,r,t

    def conjugacy_class(self):
        return ConjugacyClassPSL.objects.filter(elements=self).first()

    def gens(self):
        """
        Return the generators of self as a list of tuples
        :return:
        """
        # Check first that no one stored something malicious in our field.
        if len(filter(lambda x: x.isalpha(),self.generators)) > 0:
            raise ValueError,'Generator field contaains letters!: self.generators'.format(self.generators)
        return eval(self.generators)

class ConjugacyClassPSL(db.Document):
    """
    A conjugacy class of subgroups of PSL(2,Z)
    """
    representative = db.ReferenceField(Subgroup,required=True,unique=True)
    reflected_class = db.ReferenceField('self')
    elements = db.ListField(db.ReferenceField(Subgroup))
    signature = db.ReferenceField(Signature)
    is_representative_class=db.BooleanField(default=True)
    length = db.IntField()
    meta = {
        'collection':'conjugacy_class_psl'
        }    
    def save(self,**kwds):
        if self.reflected_class is None:
            self.reflected_class=self.find_reflected_class()
        if self.length is None:
            self.length = len(self.elements)
        super(ConjugacyClassPSL,self).save(**kwds)
        
    def find_reflected_class(self):
        reflected = self
        try:
            from psage.all import MySubgroup
        except ImportError as e:
            raise e
        for c in ConjugacyClassPSL.objects.filter(signature=self.signature):
            if c == self:
                continue
            ## We need to identify groups which we can only do using Psage (or Sage)
            reflected_rep = self.representative._to_psage().reflected_group()
            reflected_rep.relabel()
            d = {}
            d['permR'] = str(reflected_rep.permR.list()).replace(" ","")
            d['permS'] = str(reflected_rep.permS.list()).replace(" ","")
            g = Subgroup.objects.filter(permS=d['permS']).filter(permR=d['permR']).first()
            if g is None: ## In case we haven't the normalized groups in the database...
               if reflected_rep in map(lambda x:x._to_psage(),c.elements):
                   reflected = c
                   break
            else:
                if g in c.elements:
                    #if self.representative in c.elements:
                    reflected = c
                    break
        return reflected
    def length(self):
        return len(self.elements)
    def __unicode__(self):
        s = u"PSL2Z conjugacy class of {0} groups with signature {1}".format(self.length(),self.signature)
        return s

class OldFormMap(db.Document):
    """
    Elements A in PGL(2,Z) that maps modular forms on a group G1 to forms on a subgroup G2
    In other words, A G2 A^{-1} \leqslant G1
    The map, A, is given as a string of the form [a,b,c,d] and satisfy

    """
    supergroup = db.ReferenceField(Subgroup)
    subgroup = db.ReferenceField(Subgroup)
    map = db.StringField()

    def __unicode__(self):
        return "{0}: {1} --> {2}".format(self.map,self.supergroup,self.subgroup)

# class ConjugacyClassPGL(db.Document):
#     representative = db.ReferenceField(Subgroup,required=True,unique=True)
#     reflected_class = db.ReferenceField('self')
#     elements = db.ListField(db.ReferenceField(Subgroup))
#     signature = db.ReferenceField(Signature)
#     meta = {
#         'collection':'conjugacy_class_pgl'
#         }
#     def length(self):
#         return len(self.elements)
