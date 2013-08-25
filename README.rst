.. image:: https://travis-ci.org/davebridges/mousedb.png?branch=master   :target: https://travis-ci.org/davebridges/mousedb
.. image:: https://coveralls.io/repos/davebridges/mousedb/badge.png  :target: https//coveralls.io/repos/davebridges/mousedb

=======
MouseDB
=======

MouseDB is a data management and analysis system for experimental animals.  Source code is freely available via Github (through the BSD License please see LICENSE file or http://www.opensource.org/licenses/bsd-license.php), and collaboration is encouraged.  For specific details please contact Dave Bridges via Github.  MouseDB uses a web interface and a database server to store information and a web interface to access and analyse this information.  The standard setup is to use MySQL as the database and Apache as the webserver, but this can be modified if necessary.  The software was written using Django, which itself is based on the Python programming language.  Please see www.djangoproject.com and www.python.org for more information.  Documentation for this project is available at http://packages.python.org/mousedb/ or within this repository (in the Docs folder).

MouseDB Installation
''''''''''''''''''''

Configuration
-------------
MouseDB requires both a database and a webserver to be set up.  Ideally, the database should be hosted separately from the webserver and MouseDB installation, but this is not necessary, as both can be used from the same server.  If you are using a remote server for the database, it is best to set up a user for this database that can only be accessed from the webserver.  If you want to set up several installations (ie for different users or different laboratories), you need separate databases and MouseDB installations for each.  You will also need to set up the webserver with different addresses for each installation.

Software Dependencies
---------------------

1. **Python**.  Requires Version 2.6+ but preferably 2.7.3, Django is not yet compatible with Python 3.0.  Download from http://www.python.org/download/.
2. **pip**.  The python package manager, this will assist in the installation of dependencies.  See http://stackoverflow.com/questions/4750806/how-to-install-pip-on-windows#answer-4921215 for installation instructions.
3. **MouseDB source code**.  Download from one of the following and place in a folder on your computer.  Downloading and/or unzipping will create a directory named mousedb.  You can update to the newest revision at any time either using git or downloading and re-installing the newer version and copying over the existing version.  Changing or updating software versions will not alter any saved data, but you should back up your database prior to this just in case:  

  a. If you plan on developing the software,  Make your own fork of https://github.com/davebridges/mousedb and clone via git. 
  b. If you do not plan on developing the software, but want to be able to upgrate it via git, clone it from git://github.com/davebridges/mousedb.git
  c. If you do not plan on developing the software, and only want a specific version download and unzip the source code from  https://github.com/davebridges/mousedb/archive/master.zip or a particular version from https://github.com/davebridges/mousedb/tags.  Unzip/extract the package into your destination folder

4. **Other Python Packages**.  Several other python packages are also required.  These are listed in the requirements.txt file.  To install these, open a command line and move into the mousedb directory.  You may need administrative priviledges to install these.  Do get the required python packages enter::

    pip install -r requirements.txt

5. **Database software**.  Recommended to use mysql, available at http://dev.mysql.com/downloads/mysql/ .  It is also possible to use SQLite, PostgreSQL, MySQL, or Oracle.  See https://docs.djangoproject.com/en/1.4/topics/install/#get-your-database-running for more information.
6. **Webserver**.  Apache is recommended, available at http://www.apache.org/dyn/closer.cgi .  It is also possible to use FastCGI, SCGI, or AJP.  See https://docs.djangoproject.com/en/1.4/topics/install/#install-apache-and-mod-wsgi for more details.  The recommended way to use Apache is to download and enable mod_wsgi.  See http://code.google.com/p/modwsgi/ for more details.


Database Setup
--------------
1. Create a new database.  Check the documentation for your database software for the appropriate syntax for this step.  You need to record the user, password, host and database name.  If you are using SQLite this step is not required.
2. Go to localsettings_empty.py and edit the settings:

  * ENGINE: Choose one of 'django.db.backends.postgresql_psycopg2','django.db.backends.postgresql', 'django.db.backends.mysql', 'django.db.backends.sqlite3', 'django.db.backends.oracle' depending on the database software used.
  * NAME: database name
  * USER: database user
  * PASSWORD: database password
  * HOST: database host

3. Save this file as **localsettings.py** in the same folder as localsettings_empty.py

Web Server Setup
----------------
You need to set up a server to serve both the django installation and saved files.  The preferred setup is to use Apache2 with mod_wsgi to serve the project files and a separate webserver to serve media and static files.
Static files are website files such as javascript, images and css files.  Media files are user-specific files such as images.  As of this version there are no media files in this project.  These can both be served from a separate webserver but below is an example where Apache is used for both.
The default is to serve static files from **mousedb/static** to the url **/mousedb-static**.  These locations can be altered in the localsettings.py file using STATIC_ROOT and STATIC_URL respectively.
The following is a httpd.conf example where the code is placed in **/usr/src/mousedb**::

  Alias /robots.txt /usr/src/mousedb/mousedb/static/robots.txt 
  Alias /favicon.ico /usr/src/mousedb/mousedb/static/favicon.ico

  Alias /mousedb-media/ /usr/src/mousedb/mousedb/media/  
  <Directory /usr/src/mousedb/mousedb/media>
       Order deny,allow
       Allow from all
  </Directory>
  
  Alias /mousedb-static/ /usr/src/mousedb/mousedb/static/  
  <Directory /usr/src/mousedb/mousedb/static>
       Order deny,allow
       Allow from all
  </Directory>    

  <Directory /usr/src/mousedb/mousedb/apache/django.wsgi>
       Order deny,allow
       Allow from all
  </Directory>
  WSGIScriptAlias /mousedb /usr/src/mousedb/mousedb/apache/django.wsgi

If you want to restrict access to these files, change the Allow from all directive to specific domains or ip addresses (for example Allow from 192.168.0.0/99 would allow from 192.168.0.0 to 192.168.0.99)
If you want to restrict access to these files, change the Allow from all directive to specific domains or ip addresses (for example Allow from 192.168.0.0/99 would allow from 192.168.0.0 to 192.168.0.99).

To move all static files (css/javascript/images) to the directory from which static media will be served run the following command.  This will move the files to the directory defined in STATIC_ROOT::

    python manage.py collectstatic


Enabling of South for Future Migrations
---------------------------------------
Schema updates will utilize south as a way to alter database tables.  This must be enabled initially by entering the following commands from /mousedb/bin::

    python manage.py schemamigration animal --initial
    python manage.py schemamigration data --initial
    python manage.py schemamigration groups --initial
    python manage.py schemamigration timed_mating --initial
    python manage.py syncdb
    python manage.py migrate
    
Future schema changes (se the UPGRADE_NOTES.rst file for whether this is necessary) are accomplished by entering::

    python manage.py schemamigration schemamigration <INDICATED_APP> --auto
    python manage.py schemamigration migrate <INDICATED_APP>

Final Configuration and User Setup
----------------------------------
Go to a command prompt, navigate to inside the mousedb/src directory and enter the following to get to a python prompt::

  python manage.py shell
  
Go to servername/mousedb/admin/groups/group/1 and name your research group and select a license if desired
  
Go to servername/mousedb/admin/auth/users/ and create users, selecting usernames, full names, password (or have the user set the password) and then choose group permissions.

Testing
-------
From the mousedb directory run **python manage.py test** to run the test suite.  See https://github.com/davebridges/mousedb/wiki/Known-Issues---Test-Suite for known issues.  Report any additional errors at the issue page at https://github.com/davebridges/mousedb/issues.

Concepts
''''''''
Data storage for MouseDB is separated into packages which contain information about animals, and information collected about animals.  There is also a separate module for timed matings of animals.  This document will describe the basics of how data is stored in each of these modules.

Animal Module
-------------
Animals are tracked as individual entities, and given associations to breeding cages to follow ancestry, and strains.

Animal
++++++
Most parameters about an animal are set within the animal object.  Here is where the animals strain, breeding, parentage and many other parameters are included.  Animals have foreignkey relationships with both Strain and Breeding, so an animal may only belong to one of each of those.  As an example, a mouse cannot come from more than one Breeding set, and cannot belong to more than one strain.

Backcrosses and Generations
...........................
For this software, optional tracking of backcrosses and generations is available and is stored as an attribute of an animal.  When an inbred cross is made against a pure background, the backcross increases by 1.  When a heterozygote cross is made, the generation increases by one.  As an example, for every time a mouse in a C57/BL6 background is crossed against a wildtype C57/B6 mouse, the backcross (but not the generation) increases by one.  For every time a mutant strain is crosses against itself (either vs a heterozygote or homozygote of that strain), the generation will increase by one.  Backcrosses should typically be performed against a separate colony of purebred mouse, rather than against wild-type alleles of the mutant strain.

Breeding Cages
++++++++++++++
A breeding cage is defined as a set of one or more male and one or more female mice.  Because of this, it is not always clear who the precise parentage of an animal is.  If the parentage is known, then the Mother and Father fields can be set for a particular animal.

Strains
+++++++
A strain is a set of mice with a similar genetics.  Importantly strains are separated from Backgrounds.  For example, one might have mice with the genotype ob/ob but these mice may be in either a C57-Black6 or a mixed background.  This difference is set at the individual animal level.  
The result of this is that a query for a particular strain may then need to be filtered to a specific background.


Data Module
-----------
Data (or measurements) can be stored for any type of measurement.  Conceptually, several pieces of data belong to an experiment (for example several mice are measured at some time) and several experiments belong to a study.  Measurements can be stored independent of experiments and experiments can be performed outside of the context of a study.  It is however, perfered that measurements are stored within an experiment and experiments are stored within studies as this will greatly facilitate the organization of the data.

Studies
+++++++
In general studies are a collection of experiments.  These can be grouped together on the basis of animals and/or treatment groups.  A study must have at least one treatment group, which defines the animals and their conditions.

Experiments
+++++++++++
An experiment is a collection of measurements for a given set of animals.  In general, an experiment is defined as a number of measurements take in a given day.

Measurements
++++++++++++
A measurement is an animal, an assay and a measurement value.  It can be associated with an experiment, or can stand alone as an individual value.  Measurements can be viewed in the context of a study, an experiment, a treatment group or an animal by going to the appropriate page.

Timed Matings Module
--------------------
Timed matings are a specific type of breeding set.  Generally, for these experiments a mating cage is set up and pregnancy is defined by a plug event.  Based on this information, the age of an embryo can be estimated.  When a breeding cage is defined, one option is to set this cage as a timed mating cage (ie Timed_Mating=True).  If this is the case, then a plug event can be registered and recorded for this mating set.  If the mother gives birth then this cage is implicitly set as a normal breeding cage.

Groups Module
-------------
This app defines generic Group and License information for a particular installation of MouseDB.  Because every page on this site identifies both the Group and data restrictions, at a minimum, group information must be provided upon installation (see installation instructions).



