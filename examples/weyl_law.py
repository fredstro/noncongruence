import json
import sys
from sage.all import QQ,real,Spline,RR,dumps,arg,loads,dumps,unit_step
from psage.modform.maass.maass_forms import MaassWaveForms
from psage.matrix.matrix_complex_dense import Matrix_complex_dense
from psage.modform.maass.eisenstein_series import scattering_determinant
from psage.modform.arithgroup.mysubgroup import MySubgroup
from noncong.subgroups.models import Subgroup
from noncong.maass.models import MaassEigenvalue,ScatteringDeterminant,DeltaArg, ScatteringMatrixHalfSigns
from noncong.maass.encoder import ExtendedDecoder
import pymongo
import logging

log = logging.getLogger(__name__)
class WeylsLaw(object):
    """
    Class for computing and representing the Weyl's law in Theorem 5.
     This is of the form
        N(T)+M(T)+N_exc + N_res = mu/12 T^2 - e_oo/pi Tlog(2T/2) + c_G +g(T) +S(T)

    where c_G = -mu/144 + e2/8 + e3*2/9 -e_oo /4 + C/2, C = 1/2Tr(1-Phi(1/2))
    and Phi is the scattering matrix.



    """
    def __init__(self,g,use_db=True,verbose=0):
        if not isinstance(g, Subgroup):
            raise ValueError, "Need an element of type Subgroup"
        self.group = g
        self._trace_scattering_matrix_one_minus_half = None
        self._constant = None
        self.two_over_e = 0.73575888234288464319104754032 # 2/e
        self._space = None
        self._verbose = verbose
        self._NT = None
        self._MT = None
        if use_db:
            self._connection = pymongo.MongoClient(host='localhost:27017', connect=True)

    def space(self):
        if self._space is None:
            G = MySubgroup(self.group.permS, self.group.permR)
            self._space = MaassWaveForms(G, verbose=0)
        return self._space

    def constant(self):
        r"""
        The constant term c_G in Weyl's law
        :return:
        """
        if self._constant is None:
            C = self._scattering_matrix_trace_at_one_half()
            self._constant =  -QQ(self.group.index) / QQ(144) + QQ(1) / QQ(8) * self.group.e2 + QQ(2) / QQ(9) * self.group.e3 \
                              - self.group.ncusps / QQ(4) + QQ(C) / 2.0
        return self._constant

    def bound_for_gT(self):
        return QQ(self.group.index) / QQ(8707) + QQ(1) / QQ(139) * self.group.e2 + QQ(2) / QQ(67) * self.group.e3 + \
                self.group.ncusps*QQ(26)/QQ(75)

    def _scattering_matrix_trace_at_one_half(self):
        r"""
        Compute Tr(1-Phi(s)) where Phi is the scattering matrix
        :param g:
        :return:
        """
        if self._trace_scattering_matrix_one_minus_half is  None:
            M = self.space()
            A = scattering_determinant(M, 0.5, 0.000, ret_matrix=True)
            B = Matrix_complex_dense(A.parent()).identity_matrix()
            self._scattering_matrix_trace_at_one_half = real((B - A).trace() / 2.)
        return self._scattering_matrix_trace_at_one_half

    def explicit_value(self,t):
        """
        The 'explicit' part of the right hand side :

            mu/12 T^2 - e_oo/pi Tlog(2T/2) + c_G

        :param t:
        :return:
        """
        if t < 0:
            raise ValueError,"Need t>=0!"
        c = self.constant()
        if t == 0:
            return c
        return t ** 2 * self.group.index / QQ(12) - self.group.ncusps / RR.pi() * t * RR(t * self.two_over_e).log() + c

    def function__explicit(self, T, h=0.01,verbose=0):
        """
        A spline of the Weyl's law up to height t, evaluated at a step size h.
        :param T:
        :return:
        """
        t_old = 0
        h = 0.1
        t = 0
        z_old = self.constant()
        l = [(t,z_old)]
        while t < T:
            t = t_old+h
            if t>T:
                t = T
            z = self.explicit_value(t)
            #print t,z,z_old
            if abs(z-z_old)>0.1:
                h = h*0.95
                t = t_old
                continue
            l.append((t,z))
            z_old = z
            t_old = t
            if verbose > 0:
                vstr="{0:0>13.10f}".format(float(t))
                sys.stdout.write("\r"+vstr)
            if t == T:
                break
        if t<=T:
            l.append((t+h,self.explicit_value(t+h)))
        if verbose > 0:
            sys.stdout.write("\n")
        return Spline(l)

    def function__counting_discrete_eigenvalues(self,insert_pts=[]):
        """

        :param insert_pts:
        :return:
        """
        evs = [(0,1)] # the constant function
        for ev in MaassEigenvalue.objects.filter(group=self.group):
            if ev.dim is None:
                dim = 1
            else:
                dim = ev.dim
            evs.append((ev.R, dim))
        evs = evs + insert_pts  ## we can insert 'fake' eigenvalues
        evs.sort()
        return lambda x: sum([y[1]*unit_step(x-y[0]) for y in evs])

    def scattering_determinant_single_value(self,t,use_db = True,insert_nonexisting=True,eps=1e-8):
        """
        Compute Phi(1/2+it) or find from the database.
        :param t:
        :return:
        """
        z = None
        if use_db:
            coll = self._connection['subgroups']['scattering_determinant']
            s = {'group': self.group.id, 'sigma': float(0.5)}
            s['t'] = {'$lt': float(t + float(eps)), '$gt': float(t - float(eps))}
            z = coll.find_one(s)
        if z is None:
            z = scattering_determinant(self.space(), 0.5, t)
            z = complex(z)
            if insert_nonexisting and use_db:
                zz = {'re': z.real, 'im': z.imag, '__type__': 'cplx'}
                data = {'group': self.group.id, 'sigma': float(0.5), 't': float(t), 'value': json.dumps(zz)}
                coll.insert_one(data)
        else:
            t = z['t'] # get the actual value of t which was used to compute phi(1/2+it). might differ (within eps) from the input t
            z = json.loads(z['value'], cls=ExtendedDecoder)
        return t, z

    def function__winding_number(self, T=10, T0=0, insert_nonexisting=True, use_existing=False, h0=0.1, redo=False,
                                      use_db=True,adaptive=True,
                                    verbose=0):

        """
        Compute M(t)/2pi for 0<=t <=T
        :param T:
        :param T0:
        :param insert_nonexisting:
        :param use_existing:
        :param h0:
        :param redo:
        :param verbose:
        :return:
        """
        h = h0
        t_old = T0
        #conn = pymongo.MongoClient(host='localhost:27017', connect=True)
        #dbb = conn['subgroups']
        #coll = dbb['scattering_determinant']
        # If we want to use the existing values
        #if use_existing:
        #    return brute_force_arg_diff(g, T=T, ret_fun=True)
        twopi=2*RR.pi()
        verbose = self._verbose
        if not redo:
            coll1 = self._connection['subgroups']['delta_arg']
            M = coll1.find_one({'group': self.group.id})
            if M is not None:
                if M.get('maxT', 0) >= T:
                    return Spline(loads(M['pts']))
                    # coll = ScatteringDeterminant._get_collection()
        # pts = ScatteringDeterminant.objects.filter(group=g)
        s = {'group': self.group.id, 'sigma': float(0.5)}
        eps = float(1e-8)

        t = T0
        t, z_old = self.scattering_determinant_single_value(t,use_db=use_db,insert_nonexisting=insert_nonexisting)
        if T0 > 0:
            ## Get Delta arg at T0:
            M = DeltaArg.objects.filter(group=self.group).first()
            total_arg_change = M.spline()(T0)
        else:
            total_arg_change = 0
        l = [(t, total_arg_change/twopi)]
        dec = False
        i = 0
        while t < T:
            t = t_old + h
            t1, z = self.scattering_determinant_single_value(t,use_db=use_db,insert_nonexisting=insert_nonexisting)
            arg_diff = arg(z / z_old)
            if adaptive:
                if abs(arg_diff) > 0.05:
                    h = h * 0.995
                    t = t_old
                    dec = True
                    if verbose > 1:
                        print "decrease h at t={0} to h={1} arg_diff={2}".format(t, h, arg_diff)
                    continue
                elif abs(arg_diff) < 0.05 and not dec:  # we don't want to increase h after we decreased it
                    h = min(h / 0.995, h0)
                    if verbose > 1:
                        print "increase h at t={0} to h={1}".format(t, h)
                    t = t_old
                    dec = True
                    continue
            dec = False
            if abs(h) < 1e-16:
                raise ArithmeticError, "Step size too small for g={0} and t={1}".format(self.group.id, t)
            total_arg_change += arg_diff
            if verbose >1:
                print t, arg_diff, "\t", total_arg_change
            z_old = z
            t_old = t
            if verbose>0:
                vstr = "{0:0>13.10f}".format(float(t))
                sys.stdout.write("\r" + vstr)
            l.append((t, total_arg_change/twopi))
        if insert_nonexisting:
            coll1 = self._connection['subgroups']['delta_arg']
            M = coll1.find_one({'group': self.group.id})
            try:
                if M is not None:
                    if M.get('maxT', 0) <= T:
                        coll1.update_one({'_id':M['_id']},{"$set":{'pts': dumps(l),'maxT':float(t)}})
                else:
                    coll1.insert_one({'group': self.group.id, 'pts': dumps(l), 'maxT': float(t)})
            except Exception as e:
                log.debug("ERROR:{0}".format(e))
        return Spline(l)  # total_arg_change


    def _function__winding_number__use_all(self, T = 10, T0 = 0, start_value=0,ret_fun=True):
        """
        Use all values in the database to compute the change in argument.

        :param T:
        :param T0:
        :param start_value: Start the argument counting with this argument (to make it easier to work with partial counts)
        :param ret_fun:
        :return:
        """
        oldx = ScatteringDeterminant.objects.filter(group=self.group, sigma=0.5, t=T0).first()
        if oldx is None:
            raise ValueError,"Starting value at: {0} is not in the database!".format(T0)
        if abs(oldx.value + 1) < 1e-10:
            oldarg = -RR.pi()
        else:
            oldarg = arg(oldx.value)
        branch = 0
        xold = oldx.value
        totarg = 0
        told = 0
        maxdiff = 0
        pts = [(T0, start_value)]
        for x in ScatteringDeterminant.objects.filter(group=self.group, sigma=0.5, t__gt=T0,t__lt=T + 1e-10).order_by('t'):
            if self._verbose>1:
                vstr = "{0:0>13.10f}".format(float(x.t))
                sys.stdout.write("\r" + vstr)
            #if x.t <= T0:
            #    continue
            new_arg = arg(x.value)
            argdiff = new_arg - oldarg
            arg1 = new_arg + branch * 2 * RR.pi()
            arg2 = new_arg + branch * 2 * RR.pi() + 2 * RR.pi()
            arg3 = new_arg + branch * 2 * RR.pi() - 2 * RR.pi()
            t1 = abs(arg1 - oldarg);
            t2 = abs(arg2 - oldarg);
            t3 = abs(arg3 - oldarg)
            if min(t1, t2, t3) == t1:
                thisarg = arg1
            elif min(t1, t2, t3) == t2:
                branch += 1
                thisarg = arg2
            else:
                branch = branch - 1
                thisarg = arg3
            argdiff = thisarg - oldarg
            if abs(argdiff) > 0.1:
                print "t={0} new val={1} old val={2} argdiff={3} new_arg={4} oldarg={5}".format(x.t, x.value, xold,
                                                                                                argdiff, new_arg,
                                                                                                oldarg)
            totarg += argdiff
            if ret_fun:
                pts.append((x.t, totarg))

            oldarg = new_arg
            tmpt = abs(x.t - told)
            if tmpt > maxdiff:
                maxdiff = tmpt
                maxt = x.t
            xold = x.value
            told = x.t
        if self._verbose>0:
            print "max diff =",maxdiff
        if ret_fun:
            return Spline(pts)
        return totarg




    def E(self,T,h0=0.1,T0=0,insert_nonexisting=True, use_existing=False,use_db=True, use_all_from_db=False,redo=False,adaptive=True,starting_value=0):

        self._NT = self.function__counting_discrete_eigenvalues()
        if use_all_from_db:
            # We use the start value deduced from the start value for the E(T) function:
            if T0>0 and starting_value:
                starting_value_MT =  self._NT(T0) - self.explicit_value(T0) - starting_value
            self._MT = self._function__winding_number__use_all(T=T, T0=T0, start_value=starting_value_MT,ret_fun=True)
        else:
            self._MT = self.function__winding_number(T,h0=h0,insert_nonexisting=insert_nonexisting, use_existing=use_existing,
                                           use_db=use_db, redo=redo,adaptive=adaptive)
        pts = self._MT.list()

        Spts = [(x[0], -x[1] + self._NT(x[0]) - self.explicit_value((x[0]))) for x in pts]
        return Spline(Spts)




def scattering_determinant_signs(g,eps=1e-8):
    x = ScatteringMatrixHalfSigns.objects(group=g).first()
    if x is None:
        M = MaassWaveForms(MySubgroup(g.permS,g.permR))
        A = scattering_determinant(M,0.5,0.0,ret_matrix=True)
        n_plus = len(filter(lambda x: abs(x-1)<eps,A.diagonal()))
        n_minus = len(filter(lambda x: abs(x+1)<eps,A.diagonal()))
        x = ScatteringMatrixHalfSigns(group=g,plus_count=n_plus,minus_count=n_minus)
        x.save()
    return x.plus_count,x.minus_count


def average_int(fun,T0=0):
    """
    Compute  T**-1 * \int_0^T fun(t) dt as a function of T
    :param fun:
    :param T:
    :param T0:
    :return:
    """
    if isinstance(fun,Spline):
        intpts = [(x[0],fun.definite_integral(T0,x[0])/x[0]) for x in fun.list() if x[0]!=0]
    return Spline(intpts)