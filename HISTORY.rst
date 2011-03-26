Version 0.2.1dev
================
* Upgraded to Django 1.3.  
* Moved static files to be served from a separate location and from a separate folder.  
* Added units tests for data and timed_mating apps.  
* Added south, mysql-python and django-ajax-selects dependencies to setup.py.  There is a problem with installing mysql-python on windows that needs to be addressed (see http://stackoverflow.com/questions/1972259/mysql-python-install-problem-using-virtualenv-windows-pip and https://sourceforge.net/tracker/?func=detail&aid=3153396&group_id=22307&atid=374932)
* Removed all references to "mousedb" in urls.  This allows for separate installations to use different server locations (ie /mousedb-dave and /mousedb-nicole.  Checked that all templates use get_absolute_url or {% url url-name %} tags.
* Set inactive breeding cages to be marked as red.  Put an inactive cage message on the detail page for inactive breeding cages.
* Added an annual archive of mouse births using the url archive-home
* Updated documentation for installation using pip and buildout

Upgrading Notes
+++++++++++++++
* To upgrade from Django 1.2.x to 1.3.x two things must be done manually.  First re-run bin/buildout from the root directory.  Second run **django sqlindexes sessions** to update the index for the sessions app.  
* Manually add the **STATIC_URL = '/static/'** line to their localsettings.py
* Add the following to your apache httpd.conf.  If using something other than apache or you want a different server structure, the key is to serve the static directory to wherever you pointed STATIC_URL::

  Alias /static/ /usr/src/mousedb/src/mousedb/static/  
  <Directory /usr/src/mousedb/src/mousedb/static>
       Order deny,allow
       Allow from all
  </Directory>  
    
 

Stuff To Do
+++++++++++
* Migrate views to class based generic views and added docstrings.  See http://docs.djangoproject.com/en/dev/topics/class-based-views/ and http://docs.djangoproject.com/en/dev/topics/generic-views-migration/
* Check for non-cascading deletes on foreignkey models.  See http://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ForeignKey.on_delete
* Look into logging as potentially useful.  See http://docs.djangoproject.com/en/dev/topics/logging/
* Examine potential of using transaction managers.  See http://docs.djangoproject.com/en/dev/topics/db/transactions/#transaction-management-functions
* Check for use of RequestFactory objects in testing.  See http://docs.djangoproject.com/en/dev/topics/testing/#django.test.client.RequestFactory
* The MEDIA_URL and LOGIN_URL are hardcoded, this should be fixed.
* Need to update get_absolute_url for all models
* Still need the following tests
 * ModelTests: animal.Strain, data.Treatment, data.Assay, data.Diet, data.Environment, data.Experiment, data.Implantation, data.Measurement, data.Pharmaceutical, data.Researcher, data.Transplantation, data.Vendor
 * ViewTests: 
   * **root App**: logout-view
   * **data App**: treatment-list,treatment-new, treatment-detail, treatment-edit, treatment-delete, experiment-list, experiment-detail, experiment-detail-csv, data-entry, experiment-new, measurement-list, pharmaceutical-list, diet-list, study-experiment-new
   * **animals app**: breeding-pups, breeding-pups-wean, breeding-pups-change, animal-multiple-pups-new, breeding-list-timed-matings, todo-eartags, todo-genotype, todo-weaning, todo-eartags, todo-no-cage, todo-no-rack, strain-list, strain-new, strain-edit, strain-delete, strain-detail, strain-detail-all, animal-list, animal-list-all, animal-new, animal-update, animal-delete, animal-multiple-new
* Write a view and template for archive-home.  Update unit test
* Used jquery-ui buttons in timed_mating app.
* Change version number in setup.py and Docs/source/conf.py Update Documentation and move to root directory

Version 0.2.1
=============

* Fixed errors in buildout and updated documentation

Version 0.2
===========

* Incorporated buildout for easier deployment


