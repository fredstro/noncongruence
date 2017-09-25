r"""

Examples of noncongruence subgroups with exceptional eigenvalues 

Copyright (c) 2017 Fredrik Stromberg

All data is made available under Open Database License whose full text can be found at http://opendatacommons.org/licenses/odbl/. Any rights in individual contents of the database are licensed under the Database Contents License whose text can be found http://opendatacommons.org/licenses/dbcl/


Prerequisite:

 You need SAGE and PSAGE (https://github.com/fredstro/psage) installed for this to work.

Usage:

Copy relevant statements into your SAGE prompt.

"""

## Data for Exceptional Eigenvalues ##

## Notes ##
# Note that the 'eigenvalue' here is not lambda, but r=i*sqrt(lambda-1/4)
#Note also tha thre 'genus' produced by the program is of the form (mu,h,e2,e3,g) where mu is the index, h is the number of cusps, e2 and e3 are the number of elliptic fixed points and g is the genus.


#
# Index 96 Groups and tests for the given small eigenvalues: #
#

sage: s='(1)(2)(3 4)(5 6)(7 8)(9 10)(11 12)(13 14)(15 16)(17 18)(19 20)(21 22)(23 24)(25 26)(27 28)(29 30)(31 32)(33 34)(35 36)(37 38)(39 40)(41 42)(43 44)(45 46)(47 48)(49 50)(51 52)(53 54)(55 56)(57 58)(59 60)(61 62)(63 64)(65 66)(67 68)(69 70)(71 72)(73 74)(75 76)(77 78)(79 80)(81 82)(83 84)(85 86)(87 88)(89 90)(91 92)(93 94)(95 96)'
sage: r ='(1 51 50)(2 53 52)(3)(4 55 54)(5)(6 57 56)(7)(8 59 58)(9)(10 61 60)(11)(12 63 62)(13)(14 65 64)(15)(16 67 66)(17)(18 69 68)(19)(20 71 70)(21)(22 73 72)(23)(24 75 74)(25)(26 77 76)(27)(28 79 78)(29)(30 81 80)(31)(32 83 82)(33)(34 85 84)(35)(36 87 86)(37)(38 89 88)(39)(40 91 90)(41)(42 93 92)(43)(44 95 94)(45)(46 96 48)(47)(49)'
sage: G1=psage.modform.arithgroup.all.MySubgroup(o2=s,o3=r)
age: G1.signature()
(96, 0, 1, 2, 24)
sage: s='(1)(2)(3)(4)(5)(6)(7 8)(9 10)(11 12)(13 14)(15 16)(17 18)(19 20)(21 22)(23 24)(25 26)(27 28)(29 30)(31 32)(33 34)(35 36)(37 38)(39 40)(41 42)(43 44)(45 46)(47 48)(49 50)(51 52)(53 54)(55 56)(57 58)(59 60)(61 62)(63 64)(65 66)(67 68)(69 70)(71 72)(73 74)(75 76)(77 78)(79 80)(81 82)(83 84)(85 86)(87 88)(89 90)(91 92)(93 94)(95 96)'
sage: r='(1 49 48)(2 51 50)(3 53 52)(4 55 54)(5 57 56)(6 59 58)(7)(8 61 60)(9)(10 63 62)(11)(12 65 64)(13)(14 67 66)(15)(16 69 68)(17)(18 71 70)(19)(20 73 72)(21)(22 75 74)(23)(24 77 76)(25)(26 79 78)(27)(28 81 80)(29)(30 83 82)(31)(32 85 84)(33)(34 87 86)(35)(36 89 88)(37)(38 91 90)(39)(40 93 92)(41)(42 95 94)(43)(44 96 46)(45)(47)'
sage: G2=psage.modform.arithgroup.all.MySubgroup(o2=s,o3=r)
sage: G2.signature()
(96, 0,1, 6, 21)
sage: s='(1)(2)(3)(4)(5)(6)(7)(8)(9)(10)(11 12)(13 14)(15 16)(17 18)(19 20)(21 22)(23 24)(25 26)(27 28)(29 30)(31 32)(33 34)(35 36)(37 38)(39 40)(41 42)(43 44)(45 46)(47 48)(49 50)(51 52)(53 54)(55 56)(57 58)(59 60)(61 62)(63 64)(65 66)(67 68)(69 70)(71 72)(73 74)(75 76)(77 78)(79 80)(81 82)(83 84)(85 86)(87 88)(89 90)(91 92)(93 94)(95 96)'
sage: r='(1 47 46)(2 49 48)(3 51 50)(4 53 52)(5 55 54)(6 57 56)(7 59 58)(8 61 60)(9 63 62)(10 65 64)(11)(12 67 66)(13)(14 69 68)(15)(16 71 70)(17)(18 73 72)(19)(20 75 74)(21)(22 77 76)(23)(24 79 78)(25)(26 81 80)(27)(28 83 82)(29)(30 85 84)(31)(32 87 86)(33)(34 89 88)(35)(36 91 90)(37)(38 93 92)(39)(40 95 94)(41)(42 96 44)(43)(45)'
sage: G3=psage.modform.arithgroup.all.MySubgroup(o2=s,o3=r)
sage: G3.signature()
(96, 0,1, 10, 18)
sage: s='(1)(2)(3)(4)(5)(6)(7)(8)(9)(10)(11)(12)(13)(14)(15 16)(17 18)(19 20)(21 22)(23 24)(25 26)(27 28)(29 30)(31 32)(33 34)(35 36)(37 38)(39 40)(41 42)(43 44)(45 46)(47 48)(49 50)(51 52)(53 54)(55 56)(57 58)(59 60)(61 62)(63 64)(65 66)(67 68)(69 70)(71 72)(73 74)(75 76)(77 78)(79 80)(81 82)(83 84)(85 86)(87 88)(89 90)(91 92)(93 94)(95 96)'
sage: r='(1 45 44)(2 47 46)(3 49 48)(4 51 50)(5 53 52)(6 55 54)(7 57 56)(8 59 58)(9 61 60)(10 63 62)(11 65 64)(12 67 66)(13 69 68)(14 71 70)(15)(16 73 72)(17)(18 75 74)(19)(20 77 76)(21)(22 79 78)(23)(24 81 80)(25)(26 83 82)(27)(28 85 84)(29)(30 87 86)(31)(32 89 88)(33)(34 91 90)(35)(36 93 92)(37)(38 95 94)(39)(40 96 42)(41)(43)'
sage: G4=psage.modform.arithgroup.all.MySubgroup(o2=s,o3=r)
(96, 0,1, 14, 15)
sage: s='(1)(2)(3)(4)(5)(6)(7)(8)(9)(10)(11)(12)(13)(14)(15)(16)(17)(18)(19 20)(21 22)(23 24)(25 26)(27 28)(29 30)(31 32)(33 34)(35 36)(37 38)(39 40)(41 42)(43 44)(45 46)(47 48)(49 50)(51 52)(53 54)(55 56)(57 58)(59 60)(61 62)(63 64)(65 66)(67 68)(69 70)(71 72)(73 74)(75 76)(77 78)(79 80)(81 82)(83 84)(85 86)(87 88)(89 90)(91 92)(93 94)(95 96)'
sage: r='(1 43 42)(2 45 44)(3 47 46)(4 49 48)(5 51 50)(6 53 52)(7 55 54)(8 57 56)(9 59 58)(10 61 60)(11 63 62)(12 65 64)(13 67 66)(14 69 68)(15 71 70)(16 73 72)(17 75 74)(18 77 76)(19)(20 79 78)(21)(22 81 80)(23)(24 83 82)(25)(26 85 84)(27)(28 87 86)(29)(30 89 88)(31)(32 91 90)(33)(34 93 92)(35)(36 95 94)(37)(38 96 40)(39)(41)'
G5=psage.modform.arithgroup.all.MySubgroup(o2=s,o3=r)
sage: G5.signature()
(96, 0,1, 18, 12)
sage: G96=[G1,G2,G3,G4,G5]

sage: M1=psage.modform.maass.all.MaassWaveForms(G1,exceptional=True)
sage: ev=0.25993245233974344
sage: ev=0.4033819068346995
sage: F1=M1.get_element(ev,compute=True)
sage: F1.C(-1)
0.290325721699923 + 0.956927884053285*I
sage: abs(F1.C(-1))-1
-2.03608241378106e-11


sage: M2=psage.modform.maass.all.MaassWaveForms(G2,exceptional=True)
sage: ev=0.26298061494325109
sage: F2=M2.get_element(ev,compute=True)
sage: F2.C(-1)
-0.433509032349625 - 0.901149221155274*I
sage: abs(F2.C(-1))-1
-4.12676559591318e-11

sage: M3=psage.modform.maass.all.MaassWaveForms(G3,exceptional=True)
sage: ev=0.26707928772711864
sage: F3=M3.get_element(ev,compute=True)
sage: F.C(-1)
-0.576297458202358 - 0.817240013498072*I
sage: abs(F.C(-1))-1
-3.58635343644664e-12
sage: ev=0.40450173030846004
sage: F3=M3.get_element(ev,compute=True)
sage: F3.C(-1)
0.540882479332576 + 0.841098177126570*I
sage: abs(F3.C(-1))-1
7.29660776244145e-12

sage: M4=psage.modform.maass.all.MaassWaveForms(G4,exceptional=True)
sage: ev=0.2638365272575325
sage: F4=M4.get_element(ev,compute=True)
sage: F4.C(-1)
-0.674042684512656 - 0.738692398176520*I
sage: abs(F4.C(-1))-1
-1.65597202617107e-10
sage: ev=0.40620684042273258
sage: F4_1=M4.get_element(ev,compute=True)
sage: F4_1.C(-1)
0.628289200748876 + 0.777979871324950*I
sage: abs(F4_1.C(-1))-1
-1.77764469810882e-11


sage: M5=psage.modform.maass.all.MaassWaveForms(G5,exceptional=True)
sage: ev=0.25732068034063121
sage: F5=M5.get_element(ev,compute=True)
sage: F5.C(-1)
-0.719011587442541 - 0.694998084138351*I
sage: abs(F5.C(-1))-1
-8.36894997746640e-11
sage: ev=0.40801114034103469
sage: F5_1=M5.get_element(ev,compute=True)
sage: F5_1.C(-1)
0.670044016537574 + 0.742321369702485*I
sage: abs(F5_1.C(-1))-1
7.38875627348534e-12


# Subgroups of Index 48 #

sage: s='(1)(2)(3 4)(5 6)(7 8)(9 10)(11 12)(13 14)(15 16)(17 18)(19 20)(21 22)(23 24)(25 26)(27 28)(29 30)(31 32)(33 34)(35 36)(37 38)(39 40)(41 42)(43 44)(45 46)(47 48)'
sage: r='(1 27 26)(2 29 28)(3)(4 31 30)(5)(6 33 32)(7)(8 35 34)(9)(10 37 36)(11)(12 39 38)(13)(14 41 40)(15)(16 43 42)(17)(18 45 44)(19)(20 47 46)(21)(22 48 24)(23)(25)'
sage: G1=psage.modform.arithgroup.all.MySubgroup(o2=s,o3=r)
sage: G1.signature()
(48, 1, 2, 12, 0)
sage: s='(1)(2)(3)(4)(5)(6)(7 8)(9 10)(11 12)(13 14)(15 16)(17 18)(19 20)(21 22)(23 24)(25 26)(27 28)(29 30)(31 32)(33 34)(35 36)(37 38)(39 40)(41 42)(43 44)(45 46)(47 48)'
sage: r='(1 25 24)(2 27 26)(3 29 28)(4 31 30)(5 33 32)(6 35 34)(7)(8 37 36)(9)(10 39 38)(11)(12 41 40)(13)(14 43 42)(15)(16 45 44)(17)(18 47 46)(19)(20 48 22)(21)(23)'
sage: G2=psage.modform.arithgroup.all.MySubgroup(o2=s,o3=r)
sage: G2.signature()
(48, 1, 6, 9, 0)
sage: s='(1)(2)(3)(4)(5)(6)(7)(8)(9)(10)(11 12)(13 14)(15 16)(17 18)(19 20)(21 22)(23 24)(25 26)(27 28)(29 30)(31 32)(33 34)(35 36)(37 38)(39 40)(41 42)(43 44)(45 46)(47 48)'
sage: r='(1 23 22)(2 25 24)(3 27 26)(4 29 28)(5 31 30)(6 33 32)(7 35 34)(8 37 36)(9 39 38)(10 41 40)(11)(12 43 42)(13)(14 45 44)(15)(16 47 46)(17)(18 48 20)(19)(21)'
sage: G3=psage.modform.arithgroup.all.MySubgroup(o2=s,o3=r)
sage: G3.signature()
(48, 1, 10, 6, 0)
sage: G48=[G1,G2,G3]


sage: M1=psage.modform.maass.all.MaassWaveForms(G1,exceptional=True)
sage: ev=0.2245365560238645
sage:  F1=M1.get_element(ev,compute=True)
sage: F1.C(-1)
0.557382098772570 + 0.830256102643485*I
sage: abs(F1.C(-1))-1
4.43245440351347e-12

sage: M2=psage.modform.maass.all.MaassWaveForms(G2,exceptional=True)
sage: ev=0.23342157067877212
sage: F2=M2.get_element(ev,compute=True)
sage: F2.C(-1)
0.761233264784584 + 0.648478154295867*I
sage: abs(F2.C(-1))-1
6.78501699269418e-12


sage: M3=psage.modform.maass.all.MaassWaveForms(G3,exceptional=True)
sage: ev=0.24814349315349024
sage: F3=M3.get_element(ev,compute=True)
sage: F3.C(-1)
0.823802234041514 + 0.566877305246636*I
sage: abs(F3.C(-1))-1
7.73825448163734e-12



