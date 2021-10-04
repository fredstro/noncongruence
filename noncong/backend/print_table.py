r"""
Routines to produce tables of subgroups in HTML or LaTeX format.

If the subgroup module and database exists then you need only write: 

[1]: s = print_table_of_groups(format='html',index_max=10)
[2]: fp = open('test.html') 
[3]: fp.writelines(s)
[4]: fp.close()


"""

import re

def print_table_of_groups(reps_only=0,index_max=7,format='latex',**kwds):
    r"""
    The main function that generates the table of subgroups using the database.
    """
    from ..subgroups.models import Subgroup,ConjugacyClassPSL,Signature
    verify = kwds.get('verify',False)
    s = " ----- Table of subgroups of SL(2,Z) ------- \n"
    if format=='latex':
        s = r"""
        \begin{longtable}{lllccccccl}
        \caption[]{Conjugacy classes of subgroups of $\PSLZ$ with index at most $"""
        s+=str(index_max)
        s+=r"""$ } \\\\
        \toprule
        $\mu$ & $ (\mu; g,\kappa,e_2,e_3)$  &  \multicolumn{6}{l}{$\sigma_S$}  \\\\
        & \multicolumn{1}{l}{$\sigma_R$} & $\sigma_T$ & $N$ & $\#(G)$ & $h_G$ & $k_{G}$ & $C$ & $n_{\textrm{sup}}$ & $\langle \sigma_S,\sigma_R \rangle$  \\\\        \toprule 
        \endhead 
        """
    else:
        s = '<table border=1><th colspan="10">Conjugacy classes of subgroups of PSL(2,Z) with index at most '
        s+=str(index_max)
        s+="</th></tr></th>\n"
        s+=r"""
        <tr><th style="width:56px">&mu;</th>
        <th style="width:256px">(&mu; g,&kappa;,e<sub>2</sub>,e<sub>3</sub>)</th><th colspan="6" style="text-align:left">&sigma;<sub>S</sub></th><tr>
        <tr><th></th><th>&sigma;<sub>R</sub></th>
        <th style="width:256px">&sigma;<sub>T<sub></th>
        <!-- th style="width:56px">&nbsp;</th-->
        <th style="width:56px">N</th><th style="width:56px">#(G)</th>
        <th style="width:56px">h<sub>G</sub></th>
        <th style="width:56px">k<sub>&alpha;</sub></th>
        <th style="width:56px">C</th>
        <th style="width:56px">Supg.</th>
        <th style="width:56px">G/G<sup>N<sup></th></tr>"""    
    index_old=1
    
    for sig in Signature.objects.filter(index__lt=index_max+1).order_by('index','ncusps'):
        if ConjugacyClassPSL.objects.filter(signature = sig).count()==0:
            continue
        g = ConjugacyClassPSL.objects.filter(signature = sig).order_by('representative').first().representative
        if format=='latex':
            S = ''.join(map(str,g.S())).replace(',','').replace(' ','\\ ')
        else:
            S = ''.join(map(str,g.S())).replace(',','')
        l = ['',str(sig),S,'','','','','','']
        if index_old != g.index:
            l[0]=str(g.index)
            ix = g.index
            index_old = g.index
        else:
            ix =''
        if format == 'latex':
            if ix != '':
                row = '\midrule \n'
            else:
                row = '\cmidrule{2-10}'
            row +=  '${0}$ & ${1}$ &'.format(ix,sig)+'\multicolumn{8}{l}{'+str(S)+'} \\\\ \n'
        else:
            if ix != '':
                row = '<tr><td STYLE="font-weight:bold">{0}</td>'.format(ix)
                row += '<td colspan="9" style="border-width:1px solid black">&nbsp</td></tr>'
            else:
                row = ''            
            row +=  '<tr><td></td><td>{0}</td><td colspan="7">{1}</td></tr>'.format(sig,S)
        s+=row+'\n'
        ##
        ## We now sort the conjugacy classes lexicographically by representative R
        def c_sort(x,y):
            return cmp(x.representative.permR,y.representative.permR)
        cc_list = list(ConjugacyClassPSL.objects.filter(signature = sig,is_representative_class=True))
        cc_list.sort(cmp=c_sort) 
        for c in cc_list:
#            print(c)
            s+=conjugacy_class_table_row(c,format=format,verify=verify)+"\n"
            #
            #s+="{0}\n".format(c.representative)
    if format == 'latex':
        s+=r"""
        \bottomrule
        \end{longtable}
        """
    else:
        s+="</table>"
    return s


def conjugacy_class_table_row(c,format='latex',verify=False):
    r"""
    Subroutine that prints one row in the table. 
    """
    import json
    g = c.representative
    if c.reflected_class == c:
        h = 1
    else:
        h = 2
    if g.is_congruence():
        cong='C'
    else:
        cong=''
    if format=='latex':
        R = ''.join(map(str,g.R())).replace(',','').replace(' ','\\ ')   
        T = ''.join(map(str,g.T())).replace(',','').replace(' ','\\ ')
    else:
        R = ''.join(map(str,g.R())).replace(',','')
        T = ''.join(map(str,g.T())).replace(',','')
        
    k = -1
    if g.reflection_info != None:
        symms = json.loads(g.reflection_info)
        A = symms.get('tIIa',[])
        if len(A)>0:
            k = A[0][1]
        else:
            B = symms.get('tIIb',[])
            if B != []:
                k = "tIIb: {B}".format(B=B)
                print(k)
    if verify:
        try:
            G = g._to_psage()
            kk = G.has_translational_symmetry()
            ## Assert that the databsse values are ok...
            if kk != k:
                raise ValueError
        except ImportError:
            pass
    if k==-1:
        k=''
    ng = len(g.supergroups)
    permg = g.permutation_group
    if len(permg.split('~'))>1:
        gap,grp = permg.split('~')
        if grp.count('times') > 1:
            permg = gap
        else:
            permg = grp
    if format=='latex':
        permg = re.sub('GL\((\d+),','\GL_{\\1}(',permg)            
        permg = re.sub('PSL\((\d+),','\PSL_{\\1}(',permg)
        permg = re.sub(r'Gap',r'\\textrm{Gap}',permg)
        return '& ${R}$ & ${T}$ & ${N}$ & ${l}$ & ${h}$ & ${k}$ &  ${C}$ & ${ng}$ & ${G}$ \\\\'.format(R=R,T=T,N=g.generalized_level,l=c.length(),h=h,C=cong,G=permg,k=k,ng=ng)
    else:
        permg = permg.replace('_{','<sub>')
        permg = permg.replace('}','</sub>')
        l = map(str,['',R,T,g.generalized_level,c.length(),h,k,cong,ng,permg])
        s =  '<tr>'+''.join(map(lambda x:'<td>{0}</td>'.format(x),l))+'</tr>'
        return s
    
