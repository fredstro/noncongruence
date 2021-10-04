r"""

Examples of noncongruence subgroups with Maass form eigenvalues corresponding to tables in the paper "Noncongruence subgroups and Maass waveforms". This file allow you to for instance test accuraccy and/or plot Maassforms appearing in the paper.

Copyright (c) 2017 Fredrik Stromberg

All data is made available under Open Database License whose full text can be found at http://opendatacommons.org/licenses/odbl/. Any rights in individual contents of the database are licensed under the Database Contents License whose text can be found http://opendatacommons.org/licenses/dbcl/


Prerequisite:

 You need SAGE and PSAGE (https://github.com/fredstro/psage) installed for this to work.

Usage:

Copy relevant statements into your SAGE prompt.

"""


sage: r='(1 2 5)(3)(4 7 9)(6 10 8)'
sage: s='(1)(2)(3 4)(5 6)(7 8)(9 10)'
sage: G=psage.modform.arithgroup.all.MySubgroup(o2=s,o3=r)
sage: G.signature()
(10, 2, 2, 1, 0)
sage: GG = G.reflected_group()
sage: check_conjugate_subgroup(GG,G)
1
# Shows that T (G^*) T^-1 = G
sage: M=psage.modform.maass.all.MaassWaveForms(G)
sage: ev=2.40931877484576
sage: F=M.get_element(ev,compute=True)

## Example of how to to make figures

### Index 7 ###
sage: 
sage: s='(1)(2 3)(4 5)(6 7)'
sage: r='(1 4 6)(2)(3 7 5)'
sage: G=psage.modform.arithgroup.all.MySubgroup(o2=s,o3=r)
sage: M=psage.modform.maass.all.MaassWaveForms(G)
sage: ev = 2.98380890177954
sage: F1 = M.get_element(ev,compute=True)
sage: ev = 9.67736151045037
sage: F2 = M.get_element(ev,compute=True)
sage: g1=F1.plot(num_pts=1000)
sage: g1.savefig('F_ix7G1_R298.png',dpi=600)
sage: g11=F1.plot(num_pts=1000,cmap='bone')
sage: g11.savefig('F_ix7G1_R298_bone.png',dpi=600)
sage: g2=F2.plot(num_pts=1000)
sage: g2.savefig('F_ix7G1_R9677.png',dpi=600)
sage: g22=F2.plot(num_pts=1000,cmap='bone')
sage: g22.savefig('F_ix9G1_R9677_bone.png',dpi=600)


### Index 9 ###
sage: r='(1 4 6)(2 5 8)(3 7 9)'
sage: s='(1)(2)(3)(4 5)(6 7)(8 9)'
sage: G=psage.modform.arithgroup.all.MySubgroup(o2=s,o3=r)
sage: M=psage.modform.maass.all.MaassWaveForms(G,exceptional=False)
sage: ev=9.66113248208174
sage: F=M.get_element(ev,compute=True)
sage: g=F.plot(num_pts=1000)
sage: g.savefig('F_ix9G1_R966.png',dpi=600)
sage: g1=F.plot(num_pts=1000,cmap='bone')
sage: g1.savefig('F_ix9G1_R966_bone.png',dpi=600)
sage: r='(1 4 6)(2 5 8)(3 7 9)'
sage: s='(1)(2)(3)(4 5)(6 7)(8 9)'
sage: G=psage.modform.arithgroup.all.MySubgroup(o2=s,o3=r)
sage: M=psage.modform.maass.all.MaassWaveForms(G,exceptional=False)
sage: ev=9.50035839336283
sage: F=M.get_element(ev,compute=True)
sage: g=F.plot(num_pts=1000)
sage: g.savefig('F_ix9G1_R9500.png',dpi=600)
sage: g2=F.plot(num_pts=1000,cmap='bone')
sage: g2.savefig('F_ix9G1_R9500_bone.png',dpi=600)


### Examples for Index 10 Eigenvalues ###

# Table 4
sage: s='(1 2)(3 4)(5 6)(7 8)(9 10)'
sage: r='(1)(2 3 5)(4 7 9)(6 8 10)'
sage: G=psage.modform.arithgroup.all.MySubgroup(o2=s,o3=r)
sage: M=psage.modform.maass.all.MaassWaveForms(G,exceptional=False)
sage: k = G.has_translational_symmetry()

sage: assert(k==9)
sage: n = G.cusp_width(Infinity)
sage: assert(n==10)
sage: z = CC(0,2*RR.pi()*k/n).exp()
sage: for ev in [1.56460530796110,2.11939343023923,2.50414532509967,2.91592762476298,3.00023468927910,3.10845111145684,3.56237482722476,3.65766022871834,3.88274850431287,4.10694094068138,4.55947270613401,4.74782424736486,4.76752492536872,4.84953817531720]:
    F1 = M.get_element(ev,compute=True)
    er1 =  abs(F1.C(-1)-z)  
    er2 = abs(F1.C(-1)+z)
    if er1 < 6e-10:
        print("{0} \t {1:.0e} \t even".format(ev,float(er1)))
    elif er2 < 6e-10:
        print("{0} \t {1:.0e} \t odd".format(ev,float(er2)))
    else:
        raise ArithmeticError
# Table 5a
sage: s='(1)(2)(3 4)(5 6)(7 8)(9 10)'
sage: r='(1 2 5)(3)(4 7 9)(6 8 10)'
sage: G1=psage.modform.arithgroup.all.MySubgroup(o2=s,o3=r)
sage: assert G1.signature()==(10,0,2,2,1)
sage: assert G1.generalised_level()==12
sage: M1=psage.modform.maass.all.MaassWaveForms(G1)
sage: k = G1.has_translational_symmetry(); assert(k==1)
sage: n = G1.cusp_width(Infinity); assert(n==6)
sage: z = CC(0,2*RR.pi()*k/n).exp()
#sage: z = CC(0,2*RR.pi()*1/6).exp()
sage: for ev in [2.7818731828528, 3.3718432084177,3.7603510695428, 4.2298571733650, 4.8535236823625]:
     F1 = M1.get_element(ev,compute=True)
     er = abs(F1.C(-1)+z)
     print("{0} \t {1:.0e} ".format(ev,float(er)))
     assert er < 6e-11
# Table 5b
sage: s='(1)(2)(3 4)(5 6)(7 8)(9 10)'
sage: r='(1 2 5)(3)(4 7 9)(6 10 8)'
sage: G2=psage.modform.arithgroup.all.MySubgroup(o2=s,o3=r)
sage: assert G2.signature()==(10,0, 2, 2, 1)
sage: assert G2.generalised_level()==8
sage: k = G2.has_translational_symmetry(); assert(k==1)
sage: n = G2.cusp_width(Infinity); assert(n==8)
sage: z = CC(0,2*RR.pi()*k/n).exp()
sage: M2=psage.modform.maass.all.MaassWaveForms(G2)
sage: for ev in [2.4093187748458, 3.2980390023681, 3.7095318601808, 4.2745965949785, 4.5864668030104]:
     F2 = M2.get_element(ev,compute=True)
     er = abs(F2.C(-1)+z)
     print("{0} \t {1:.0e} ".format(ev,float(er)))
     assert er < 3e-8

# Table 5c
sage: s='(1)(2)(3 4)(5 6)(7 8)(9 10)'
sage: r='(1 5 7)(2 8 9)(3)(4 10 6)'
sage: G3=psage.modform.arithgroup.all.MySubgroup(o2=s,o3=r)
sage: assert G3.signature()==(10,0, 2, 2, 1)
sage: assert G3.generalised_level()==21
sage: k = G3.has_translational_symmetry(); assert(k==5)
sage: n = G3.cusp_width(Infinity); assert(n==7)
sage: M3=psage.modform.maass.all.MaassWaveForms(G3)
sage: z = CC(0,2*RR.pi()*k/n).exp()
sage: for ev in [1.9099559058915, 3.2045604949759, 3.5047586985069, 4.2075358132024, 4.7774437178153]:
     F3 = M3.get_element(ev,compute=True)
     er = abs(F3.C(-1)+z)
     print("{0} \t {1:.0e} ".format(ev,float(er)))
     assert er < 4e-8

# Table 5d
sage: s='(1 2)(3 4)(5 6)(7 8)(9 10)'
sage: r='(1)(2 3 5)(4 7 9)(6 10 8)'
sage: G4=psage.modform.arithgroup.all.MySubgroup(o2=s,o3=r)
sage: assert G4.signature()==(10, 0,3, 0, 1)
sage: assert G4.generalised_level()==30
sage: k = G4.has_translational_symmetry(); assert(k==4)
sage: n = G4.cusp_width(Infinity); assert(n==5)
sage: M4=psage.modform.maass.all.MaassWaveForms(G4)
sage: z = CC(0,2*RR.pi()*k/n).exp()
sage: for ev in [2.6817198332904, 3.5645125659019, 4.4420512498009, 4.7018937088526 , 4.9743710668935]:
     F4 = M4.get_element(ev,compute=True)
     er = abs(F4.C(-1)+z)
     print("{0} \t {1:.0e} ".format(ev,float(er)))
     assert er < 8e-9

# Table 5e
sage: s='(1 2)(3 4)(5 6)(7 8)(9 10)'
sage: r='(1)(2 3 5)(4 6 7)(8 9 10)'
sage: G5=psage.modform.arithgroup.all.MySubgroup(o2=s,o3=r)
sage: assert G5.signature()==(10, 0,3, 0, 1)
sage: assert G5.generalised_level()==20
sage: k = G5.has_translational_symmetry(); assert(k==3)
sage: n = G5.cusp_width(Infinity); assert(n==4)
sage: M5=psage.modform.maass.all.MaassWaveForms(G5)
sage: z = CC(0,2*RR.pi()*k/n).exp()
sage: for ev in [3.0877339408933,3.5070902176928,4.3456594421154]:
    F5 = M5.get_element(ev,compute=True)
    er = abs(F5.C(-1)+z)
    print("{0} \t {1:.0e} ".format(ev,float(er)))
    assert er < 8e-9

sage: s='(1 2)(3 4)(5 6)(7 8)(9 10)'
sage: r='(1)(2 3 5)(4 7 6)(8 9 10)'
sage: G6=psage.modform.arithgroup.all.MySubgroup(o2=s,o3=r)
sage: assert G6.signature()==(10, 0,3, 0, 1)
sage: assert G6.generalised_level()==14
sage: k = G6.has_translational_symmetry(); assert(k==6)
sage: n = G6.cusp_width(Infinity); assert(n==7)
sage: M6=psage.modform.maass.all.MaassWaveForms(G6)
sage: z = CC(0,2*RR.pi()*k/n).exp()
sage: for ev in [2.5744038863311,3.7941339745816,4.0617322627988,4.6861370442514]:
    F6 = M6.get_element(ev,compute=True)
    er = abs(F6.C(-1)+z)
    print("{0} \t {1:.0e} ".format(ev,float(er)))
    assert er < 8e-9

##
## Example without symmetry
## G(10;0,3,0,1;8,1)
sage: s='(1 2)(3 4)(5 6)(7 8)(9 10)'
sage: r='(1)(2 3 5)(4 7 8)(6 9 10)'
sage: G=psage.modform.arithgroup.all.MySubgroup(o2=s,o3=r)
sage: assert G.signature()==(10, 0,3, 0, 1)
sage: assert G.generalised_level()==8
sage: assert G.has_translational_symmetry(return_k=False,check_preserve_cusp=True)
