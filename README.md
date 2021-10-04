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
(This was created using `mongodump -d 

# Docker #
If you can't install mongodb on your machine but have docker installed you can 
install it and recreate the database by the following steps:
1. follow the steps above and untar the `subgroups` directory in /tmp (otherwise change /tmp below)) 
2. >docker pull mongo
3. >docker run --name mongo-503 -p 27017:27017 -v /tmp:/data/ -d mongo
4. >docker exec mongo-503 sh -c 'mongorestore -d subgroups /data/subgroups'

You will now have a running mongodb at port 27017

# Use without Sage

It is generally considered best to setup and run python modules in a virtual environment of some kind.
Which version you use depends on your preferences. You can use either of
1. virtualenv wrapper: https://virtualenvwrapper.readthedocs.io/ 
2. venv
3. conda

**venvwrapper**
1. Install virtualenv wrapper: https://virtualenvwrapper.readthedocs.io/
2. Make a virtual environment
> mkvirtualenv noncong
This also activates the environment.

**venv**
1. python3 -m venv /path/to/new/virtual/environment
2. source /path/to/new/virtual/environment/bin/activate

**conda**
1conda create -n noncong python=3

After this you just need to install the requirements:
> pip install -r requirements.txt

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
