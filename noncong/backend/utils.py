from functools import reduce
import six

def string_of_list_to_cycles(s):
    r"""
    INPUT : permutation in tuple/list format:
    OUTPUT: string of cycles. 
    """
    if not isinstance(s,six.text_type):
        raise ValueError("need a string as input!")
    #l = json.loads(s)
    for x in ["(", ")","[","]"]:
        s = s.replace(x,"") 
    try:
        l = map(int,s.split(","))
    except ValueError as e:
        raise e
    x = 1
    cy = []
    cycles =[]; seen =[]
    unseen = range(1,len(l)+1)
    for i in range(len(l)):
        x = l[x-1]
        if x in unseen:
            cy.append(x)
        else:
            ## Permute the cycle so that the smallest element is first
            minx = cy.index(min(cy))
            if minx != 0:
                n = len(cy)
                cy = [cy[i % n] for i in range(0+minx,n+minx)]
            cycles.append(tuple(cy))
            if unseen != []:
                x = min(unseen)
                cy = [x]
            else:
                break
        unseen.remove(x)
        if unseen == []:
            ## Permute the cycle so that the smallest element is first
            minx = cy.index(min(cy))
            if minx != 0:
                n = len(cy)
                cy = [cy[i % n] for i in range(0+minx,n+minx)]
            cycles.append(tuple(cy))
            break
    return tuple(cycles)
            

def list_of_tuples_to_json(tuples):
    r"""
    Convert a list of lists (or tuples) of integers into a json string.
    """
    ## make a sanity check first in case we call it with a list of sage Integers or something.
    if not isinstance(tuples,(list,tuple)):
        raise ValueError("Need a list to convert! got:{0}".format(type(tuples)))
    if len(tuples)==0:
        raise ValueError("Need a non-empty list!")
    if not isinstance(tuples[0],(list,tuple)):
        raise ValueError("Need a list of lists to convert! got:{0}".format(type(tuples)))
    if not isinstance(tuples[0][0],int):
        tuples = [map(int,m) for m in tuples]
    return json.dumps(tuples)
        
    
def mygetattr(obj,prop):
    try:
        return getattr(obj,prop)
    except:
        pass
    try:
        return obj[prop]
    except:
        raise ValueError('object {0} does not have proprty {1}'.format(obj,prop))
            
def gcd(*numbers):
    """Return the greatest common divisor of the given integers"""
    from fractions import gcd
    return reduce(gcd, numbers)


def lcm(*numbers):
    """Return least common multiple."""
    if isinstance(numbers[0],list):
        numbers = numbers[0]
    def lcm(a, b):
        return (a * b) // gcd(a, b)
    return reduce(lcm, numbers, 1)


