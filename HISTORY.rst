Version 0.2.1dev
================
<<<<<<< HEAD
*Added units tests for Study objects
*Added model and view tests for the timed_mating app
*Added south, mysql-python and django-ajax-selects dependencies to setup.py
*Updated documentation for installation using pip and buildout
*Removed all references to "mousedb" in urls.  This allows for separate installations to use different server locations (ie /mousedb-dave and /mousedb-nicole.  Checked that all templates use get_absolute_url or {% url url-name %} tags.
-Removed cage-detail links
-The MEDIA_URL and LOGIN_URL are hardcoded, this should be fixed.
-Need to update get_absolute_url for all models


Version 0.2.1
=============

*Fixed errors in buildout and updated documentation

Version 0.2
===========

*Incorporated buildout for easier deployment


