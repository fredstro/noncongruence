"""

Programs to compute the counting functions in Example XXX
using the data provided in the mongodb.

"""


# Make plots from existing data:

colors = ['blue','green']
ymax = 2
ymin = -2

file_name_complete = 'E_g7211_10__T20_ok_to_18_high_res.txt'

def make_spline(filename):
    fp=open(filename,'r')
    l=json.load(fp)
    fp.close()
    return Spline(l)

def make_plots(filename,xmin=None,xmax=None,ymin=-2,ymax=2,do_int=True,label=""):
  

    # Complete plots
    fp=open(filename,'r')
    l=json.load(fp)
    F=Spline(l)
    IF=average_int(F)
    if not xmax:
        xmax = 20
    if do_int:
        return plot([F,IF],0,xmax,color=colors,legend_label=['$E(T)$','$\langle E(T)\\rangle $'],ymin=ymin,ymax=ymax)
    else:
        return plot([F],xmin,xmax,color=colors,legend_label=['$M_{\text{exp}}(T)$'],ymin=ymin,ymax=ymax)        

    # Incomplete plot
