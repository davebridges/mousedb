Version 0.2.1dev
================
* Upgraded to Django 1.3.  
* Moved static files to be served from a separate location and from a separate folder.  
* Added units tests for data and timed_mating apps.  
* Added south, mysql-python and django-ajax-selects dependencies to setup.py.  There is a problem with installing mysql-python on windows that needs to be addressed (see http://stackoverflow.com/questions/1972259/mysql-python-install-problem-using-virtualenv-windows-pip and https://sourceforge.net/tracker/?func=detail&aid=3153396&group_id=22307&atid=374932)
* Removed all references to "mousedb" in urls.  This allows for separate installations to use different server locations (ie /mousedb-dave and /mousedb-nicole.  Checked that all templates use get_absolute_url or {% url url-name %} tags.
* Set inactive breeding cages to be marked as red.  Put an inactive cage message on the detail page for inactive breeding cages.
* Animals are no longer defined at the Experiment object level, but are defined in Treatment and Measurement objects.  These are then introspected at the Study and Experiment level.  **This requires a migration of the data app.**
* Factored out the background from a hardcoded list of choices to a separate set of objects defined by a Background object.  **This requires a migration of the animal app.**.  The old Background field is still functional, but wll be deprecated 
* Added an annual archive of mouse births using the url archive-home
* Added a new view for exporting animal survival data
* Updated documentation for installation using pip and buildout

  
 

Stuff To Do
+++++++++++
* Migrate views to class based generic views and added docstrings.  See http://docs.djangoproject.com/en/dev/topics/class-based-views/ and http://docs.djangoproject.com/en/dev/topics/generic-views-migration/
* Check for non-cascading deletes on foreignkey models.  See http://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ForeignKey.on_delete
* Look into logging as potentially useful.  See http://docs.djangoproject.com/en/dev/topics/logging/
* Check for use of RequestFactory objects in testing.  See http://docs.djangoproject.com/en/dev/topics/testing/#django.test.client.RequestFactory
* The MEDIA_URL and LOGIN_URL are hardcoded, this should be fixed.
* Need to update get_absolute_url for all models
* Still need the following tests
 * ModelTests: data.Treatment, data.Assay, data.Diet, data.Environment, data.Experiment, data.Implantation, data.Measurement, data.Pharmaceutical, data.Researcher, data.Transplantation, data.Vendor
 * ViewTests: 
   * **data App**: treatment-list,treatment-new, treatment-detail, treatment-edit, treatment-delete, experiment-list, experiment-detail, experiment-detail-csv, data-entry, experiment-new, measurement-list, pharmaceutical-list, diet-list, study-experiment-new
   * **animals app**: breeding-pups, breeding-pups-wean, breeding-pups-change, ,animal-multiple-pups-new, todo-eartags, todo-genotype, todo-weaning, todo-eartags, todo-no-cage, todo-no-rack, animal-list, animal-list-all, animal-new, animal-update, animal-delete, animal-multiple-new
   * POST tests.  See http://toastdriven.com/blog/2011/apr/17/guide-to-testing-in-django-2/
   * Add named urls to tests?  See http://toastdriven.com/blog/2011/apr/17/guide-to-testing-in-django-2/
* Check ModelTests
* Write a view and template for archive-home.  Update unit test.
* Use jquery-ui buttons in timed_mating app.
* Update usage document.
* Change version number in setup.py and Docs/source/conf.py Update Documentation and move to root directory
* Migrate breeding-pups, breeding-pups-wean, breeding-pups-change, and animal-multiple-pups-new to class based generic views.
* Remove older Background field from animal models and write a SQL script to transfer data from previous field to new objects.
* Check documentation so that the use of the Background field is described appropriately.  Write initial Mixed and C57BL/6J Background objects in initial_data.json.  Add this information to installation instructions.

Version 0.2.1
=============

* Fixed errors in buildout and updated documentation

Version 0.2
===========

* Incorporated buildout for easier deployment


