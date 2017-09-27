# Noncongruence subgroups and Maass Waveforms.

This repository contains Examples, code and Data for the paper "Noncongruence Subgroups and Maass waveforms" 

You can make basic queries etc. against the database of subgroups without having SAGE (http://www.sagemath.org) or PSAGE  (https://github.com/fredstro/psage) installed but certain extra features will only be available through PSAGE.

Examples of Maass forms and eigenvalues are available in the `/examples` directory:

* `examples/examples_eigenvalue_tables.py` -- data corresponding to Tables of non-exceptional eigenvalues
* `examples/examples_exceptional.py`   -- data for Tables of exceptional eigenvalues.



# Database of subgroups #

The database of subgroups is available through MongoDB
and to interact with it you need access to the following:.
1) MongoDB
2) Python

# Setup database: #
1. Install mongodb: See e.g. http://www.hongkiat.com/blog/webdev-with-mongodb-part1/ for installation in various systems.
2. Untar the database files in subgroupsdb.tar:
> cd data
> tar -xvf subgroupsdb.tar
this creates a directory 'subgroups'  and you can now:
3. Insert all data into your local mongo database:
> mongorestore -d subgroups data/subgroups/

# If you want to use python without Sage

It is generally considered best to setup and run python modulesin a virtual environment

1. Instal virtualenv wrapper: https://virtualenvwrapper.readthedocs.io/
2. Make a virtual environment
> mkvirtualenv noncong
This also activates the environment.
3. Install requirements
> pip install flask-mongoengine
> pip install ipython==5.0

# Access the database 

See the mongoengine docs: http://mongoengine.org/ for information on how to query the database through the models.
Available models:

subgroups.models.Signatures                    --> Valid signatures of groups in the database
subgroups.models.ConjugacyClassesPSL  -->  Conjugacy classes (where we have complete information)
subgroups.models.Subgroups                  -->   Subgroups


>ipython
In [1]: import noncong

In [2]: noncong.subgroups.models.Subgroup.objects.filter(genus=0,index=10).count()
255

In [3]: g=noncong.subgroups.models.Subgroup.objects.filter(index=10).first();g

Out[4]: Subgroup of PS(2,Z) of signature (10;0,2,2,1)  with perm(T)= ((1, 2, 5, 4, 3, 7, 9, 8, 6), (10,))

In [5]: g.generators

Out[6]: u'[[0, -1, 1, 0], [4, -1, 9, -2], [-4, 3, -7, 5], [1, -2, 1, -1]]'


# Print tables #:
>ipython
In[1]: import noncong.subgroups.models
In[2]: fp=open('table.html','w')
In[3]: s=noncong.backend.print_table.print_table_of_groups(index_max=17,format='html')
In[4]: fp.writelines(s)
In[5]: fp.close()
In[2]: fp=open('table.tex','w')
In[3]: s=noncong.backend.print_table.print_table_of_groups(index_max=17,format='latex')
In[4]: fp.writelines(s)
In[5]: fp.close()
