Upgrading Notes
+++++++++++++++
If installing a new version of MouseDB and not upgrading, none of this needs to be considered.  However if you are upgrading from a previous version, please follow these instructions.  Database schema upgrades will be attempted to be minimized, but when necessary **south** will be utilized.  When a schema upgrade is indicated follow these instructions from within the mousedb/bin directory::

    django schemamigration <INDICATED_APP> --auto
    django migrate <INDICATED_APP>

From 0.2 to 0.3
===============
* This marks the MouseDB release in which an upgrade is made to Django 1.3.  To upgrade from Django 1.2.x to 1.3.x two things must be done manually.  First re-run bin/buildout from the root directory or install Django 1.3.x from pip or source.  Second run **django sqlindexes sessions** to update the index for the sessions app.  
* Manually add the **STATIC_URL = '/static/'** line to the localsettings.py
* Add the following to your apache httpd.conf.  If using something other than apache or you want a different server structure, the key is to serve the static directory to wherever you pointed STATIC_URL::

  Alias /static/ /usr/src/mousedb/src/mousedb/static/  
  <Directory /usr/src/mousedb/src/mousedb/static>
       Order deny,allow
       Allow from all
  </Directory>  