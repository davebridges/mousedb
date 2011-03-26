MouseDB Installation
====================

Configuration
-------------
MouseDB requires both a database and a webserver to be set up.  Ideally, the database should be hosted separately from the webserver and MouseDB installation, but this is not necessary, as both can be used from the same server.  If you are using a remote server for the database, it is best to set up a user for this database that can only be accessed from the webserver.  If you want to set up several installations (ie for different users or different laboratories), you need separate databases and MouseDB installations for each.  You will also need to set up the webserver with different addresses for each installation.

Software Dependencies
---------------------

1. **Python**.  Requires Version 2.6, is not yet compatible with Python 3.0.  Download from http://www.python.org/download/.
2. **MouseDB source code**.  Download from one of the following:  

  a. Using **pip or easy_install**.  If setuptools (available at http://pypi.python.org/pypi/setuptools) is installed type **pip install mousedb** at a command prompt.
  b. http://github.com/davebridges/mousedb/downloads for the current release.  If you will not be contributing to the code, download from here.
  c. http://github.com/davebridges/mousedb for the source code via Git.  If you might contribute code to the project use the source code.

Downloading and/or unzipping will create a directory named mousedb.  You can update to the newest revision at any time either using git or downloading and re-installing the newer version.  Changing or updating software versions will not alter any saved data, but you will have to update the localsettings.py file (described below).

3. **Database software**.  Recommended to use mysql, available at http://dev.mysql.com/downloads/mysql/ .  It is also possible to use SQLite, PostgreSQL, MySQL, or Oracle.  See http://docs.djangoproject.com/en/1.2/topics/install/#database-installation for more information.  You will also need the python bindings for your database.  If using MySQL python-mysql will be installed below.
4. **Webserver**.  Apache is recommended, available at http://www.apache.org/dyn/closer.cgi .  It is also possible to use FastCGI, SCGI, or AJP.  See http://docs.djangoproject.com/en/1.2/howto/deployment/ for more details.  The recommended way to use Apache is to download and enable mod_wsgi.  See http://code.google.com/p/modwsgi/ for more details.

Installation
------------
1. Navigate into mousedb folder
2. Run **python setup.py install** to get dependencies.  If you installed via pip, this step is not necessary (but wont hurt).  This will install the dependencies South, mysql-python and django-ajax-selects.
3. Run **python bootstrap.py** to get the correct version of Django and to set up an isolated environment.  This step may take a few minutes.
4. Run **bin\\buildout** to generate django, test and wsgi scripts.  This step may take a few minutes.

Database Setup
--------------
1. Create a new database.  Check the documentation for your database software for the appropriate syntax for this step.  You need to record the user, password, host and database name.  If you are using SQLite this step is not required.
2. Go to \mousedb\src\mousedb\localsettings_empty.py and edit the settings:

  * ENGINE: Choose one of 'django.db.backends.postgresql_psycopg2','django.db.backends.postgresql', 'django.db.backends.mysql', 'django.db.backends.sqlite3', 'django.db.backends.oracle' depending on the database software used.
  * NAME: database name
  * USER: database user
  * PASSWORD: database password
  * HOST: database host

3. Save this file as **localsettings.py** in the same folder as localsettings_empty.py
4. Migrate into first mousedb directory and enter *django syncdb*.  When prompted create a superuser (who will have all availabler permissions) and a password for this user.

Web Server Setup
----------------
You need to set up a server to serve both the django installation and saved files.  For the saved files.  I recommend using apache for both.  The preferred setup is to use Apache2 with mod_wsgi.  See http://code.google.com/p/modwsgi/wiki/InstallationInstructions for instructions on using mod_wsgi.  The following is a httpd.conf example where the code is placed in **/usr/src/mousedb**::

  Alias /robots.txt /usr/src/mousedb/src/mousedb/media/robots.txt 
  Alias /favicon.ico /usr/src/mousedb/src/mousedb/media/favicon.ico

  Alias /mousedb-media/ /usr/src/mousedb/src/mousedb/media/  
  <Directory /usr/src/mousedb/src/mousedb/media>
       Order deny,allow
       Allow from all
  </Directory>

  <Directory /usr/src/mousedb/bin>
       Order deny,allow
       Allow from all
  </Directory>
  WSGIScriptAlias /mousedb /usr/src/mousedb/bin/django.wsgi

If you want to restrict access to these files, change the Allow from all directive to specific domains or ip addresses (for example Allow from 192.168.0.0/99 would allow from 192.168.0.0 to 192.168.0.99)

Final Configuration and User Setup
----------------------------------
* Go to *servername/mousedb/admin/groups/group/1* and name your research group and select a license if desired
* Go to *servername/mousedb/admin/auth/users/* and create users, selecting usernames, full names, password (or have the user set the password) and then choose group permissions.

Testing
-------
From the mousedb directory run **bin\\test** or **bin\\django test** to run the test suite.  See https://github.com/davebridges/mousedb/wiki/Known-Issues---Test-Suite for known issues.  Report any additional errors at the issue page at https://github.com/davebridges/mousedb/issues.