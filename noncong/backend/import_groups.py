# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
r"""
Routines to import subgroups into the database.

"""

from ..subgroups.models import Signature,Subgroup,ConjugacyClassPSL
import logging
import mongoengine
log = logging.getLogger(__name__)

def signature_from_G(G):
    r"""
    The .signature() method of the MySubgroup instance G contains
    (index,h,nu2,nu3,g)
    """
    s = dict(index=G.index(),ncusps=G.ncusps(),genus=G.genus(),
        e2=G.nu2(),e3=G.nu3())
    sig = Signature.objects.filter(**s).first()
    if not sig is None:
        return sig
    sig = Signature(**s)
    sig.save()
    return sig

def sage_subgroup_to_db(G,update=True,**kwds):
    r"""
    A simple class which just represents a sage group in a way that we can convert 
    """
    from sage.all import Gamma0,Gamma,Gamma1
    d = {}
    GP = G.as_permutation_group()
    tS = GP.permutation_action([0,-1,1,0])
    d['permS'] = str([tS(i) for i in range(1,G.index()+1)]).replace(' ','')
    tR = GP.permutation_action([0,-1,1,1])  ## R = ST
    d['permR'] = str([tR(i) for i in range(1,G.index()+1)]).replace(' ','')
    if not update:
        obj =  Subgroup.objects.filter(permS=d['permS']).filter(permR=d['permR']).first()
        if not obj is None:
            return obj
        return None
    d['index'] = G.index()
    d['signature'] = signature_from_G(G)
    d['coset_representatives'] = str([[x[0][0],x[0][1],x[1][0],x[1][1]] for x in G.coset_reps()])
    d['generators']             = str([[x[0][0],x[0][1],x[1][0],x[1][1]] for x in G.gens()])

    tT = GP.permutation_action([1,1,0,1])
    d['permT'] = str([tT(i) for i in range(1,G.index()+1)])
    d['congruence'] = G.is_congruence()
    if G.is_congruence():
        d['symmetric'] = True
        d['reflection_info']=str([[-1, 0, 0, 1]])
    else:
        pass ## It takes too long to do that computation for a sage group... 
    s = []
    for c in G.cusps():
        s.append( [c.numerator(),c.denominator()])
    d['cusp_representatives'] = str(s)
    if kwds.get('name','') != '':
        d['name'] = kwds.get('name')
    else:
        if G.is_congruence():
            N = G.generalised_level()
            if G == Gamma0(N):
                d['name'] = 'Gamma0({0})'.format(N)
            elif G == Gamma1(N):
                d['name'] = 'Gamma1({0})'.format(N)
            elif  G == Gamma(N):
                d['name'] = 'Gamma({0})'.format(N)
    G = Subgroup(**d)
    try:
        G.save()
    except mongoengine.errors.NotUniqueError as e:
        G = Subgroup.objects(permS=d['permS'],permR=d['permR']).first()
        if update:
            if not G is None:
                G.update(**d)
    return G                
            
def psage_subgroup_to_db(G,update=True,**kwds):
    r"""
    Convert a subgroup of type MySubgroup to the database format in a canonical way.
    """

    d = kwds
    G.relabel() ## make the permutations canonical
    d['index'] = G.index()
    d['permS'] = str(G.permS.list()).replace(" ","")
    d['permR'] = str(G.permR.list()).replace(" ","")
    d['permT'] = str(G.permT.list()).replace(" ","")
    if not update:
        obj =  Subgroup.objects.filter(permS=d['permS']).filter(permR=d['permR']).first()
        if obj is not None:
            return obj
        # Else do a more complicated search...
        for g in Subgroup.objects.filter(index=G.index(),permS=d['permS']):
            gg = g._to_psage()
            # check if the group is identical by a falll-back algorithm,
            equal = True
            for A in g.gens():
                if A not in G:
                    equal = False
                    break
            if equal:
                return g
        log.warning("Could not find this group in the database!")
    d['signature'] = signature_from_G(G)
    d['coset_representatives'] = str(G.coset_reps())
    d['generators'] = str(G.generators_as_slz_elts())

    
    d['congruence'] = G.is_congruence()
    # We need to check if
    # a) G has a symmetry
    # b) if this symmetry preserve cusp classes
    d['symmetric']  = False
    if G.is_symmetric():
        tmp = {}
        if G.has_modular_correspondence():
            for t in G._modular_correspondences:
                val = G._modular_correspondences[t]
                if val != []:
                    tmp[t] = val
            d['reflection_info'] = str(tmp)
            d['symmetric'] = True
    s = []
    for c in G.cusps():
        s.append( [c.numerator(),c.denominator()])
    d['cusp_representatives'] = str(s)
    if G.find_name() != '':
        d['name'] = G.find_name()
    G = Subgroup(**d)
    try:
        G.save()
    except mongoengine.errors.NotUniqueError as e:
        G = Subgroup.objects(permS=d['permS'],permR=d['permR']).first()
        if update:
            if not G is None:
                G.update(**d)
    return G

def import_from_dict(l,index_min=1,index_max=0):
    from psage import MySubgroup
    for ix in l:
        if index_min >0 and ix < index_min:
            continue
        if index_max >0 and ix > index_max:
            continue        
        signatures = l[ix]
        for sig in signatures:
            print sig
            d = l[ix][sig]
            for s,r in d['conjugates']:
                #print s,r,s.order(),r.order()
                G = MySubgroup(s,r)
                quotient_group = d['quotient_groups'].get((s,r),'')
                g = psage_subgroup_to_db(G,psl_rep=True,pgl_rep=True,quotient_group=quotient_group)
                g.save()
                cc = ConjugacyClassPSL.objects.filter(representative=g).first()
                if cc is None:
                    cc = ConjugacyClassPSL(representative=g,signature=g.signature)
                    cc.save()            
                for s1,r1 in d['conjugates'][(s,r)]['psl']:
                    G1 = MySubgroup(s1,r1)
                    g1 = psage_subgroup_to_db(G1,psl_rep=True,pgl_rep=True)
                    cc.elements.append(g1)
                cc.save()
            ## We can now add the reflected classes as well...
            for s,r in d['conjugates']:
                if len(d['conjugates'][(s,r)]['pgl'])==0:
                    continue
                s1,r1 = d['conjugates'][(s,r)]['pgl'][0]
                if len(d['conjugates'][(s,r)]['pgl'])>1:
                    print "conjugates mod pgl=",d['conjugates'][(s,r)]['pgl']
                if s1 != s or r1 != r:
                    G = MySubgroup(s,r)
                    g = psage_subgroup_to_db(G,psl_rep=True,pgl_rep=True)
                    G1 = MySubgroup(s1,r1)
                    g1 = psage_subgroup_to_db(G1,psl_rep=True,pgl_rep=True)
                    cc = ConjugacyClassPSL.objects.filter(representative=g).first()
                    cc1 = ConjugacyClassPSL.objects.filter(elements=g1).first()
                    cc.reflected_class = cc1
                    cc1.reflected_class = cc
                    cc.save()
                    cc1.save()
                # cc = ConjugacyClassPGL.objects.filter(representative=g).first()

                # for rr in d['groups'][(s,r)]['pgl_conj']:
                #     if rr != r:
                #         G1 = MySubgroup(s,rr)
                #         g1 = psage_subgroup_to_db(G1)
                #         cc.elements.append(g1)
                # cc.save()
                # cc = ConjugacyClassPSL.objects.filter(representative=g).first()
                # if cc is None:
                #     cc = ConjugacyClassPSL(representative=g,signature=g.signature)
                #     cc.save()
                # for rr in d['groups'][(s,r)]['psl_conj']:
                #     if rr != r:
                #         G1 = MySubgroup(s,rr)
                #         g1 = psage_subgroup_to_db(G1)
                #         cc.elements.append(g1)
                # cc.save()
