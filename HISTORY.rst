Version 0.2.1dev
================
* Added units tests for data and timed_mating apps.  
* Added south, mysql-python and django-ajax-selects dependencies to setup.py.  There is a problem with installing mysql-python on windows that needs to be addressed (see http://stackoverflow.com/questions/1972259/mysql-python-install-problem-using-virtualenv-windows-pip and https://sourceforge.net/tracker/?func=detail&aid=3153396&group_id=22307&atid=374932)
* Removed all references to "mousedb" in urls.  This allows for separate installations to use different server locations (ie /mousedb-dave and /mousedb-nicole.  Checked that all templates use get_absolute_url or {% url url-name %} tags.
* Set inactive breeding cages to be marked as red.  Put an inactive cage message on the detail page for inactive breeding cages.
* Added an annual archive of mouse births using the url archive-home
* Updated documentation for installation using pip and buildout

Stuff To Do
+++++++++++
* The MEDIA_URL and LOGIN_URL are hardcoded, this should be fixed.
* Need to update get_absolute_url for all models
* Still need the following tests
 * ModelTests: animal.Strain, data.Treatment, data.Assay, data.Diet, data.Environment, data.Experiment, data.Implantation, data.Measurement, data.Pharmaceutical, data.Researcher, data.Transplantation, data.Vendor
 * ViewTests: 
   * **root App**: logout-view
   * **data App**: treatment-list,treatment-new, treatment-detail, treatment-edit, treatment-delete, experiment-list, experiment-detail, experiment-detail-csv, data-entry, experiment-new, measurement-list, pharmaceutical-list, diet-list, study-experiment-new
   * **animals app**: breeding-pups, breeding-pups-wean, breeding-pups-change, animal-multiple-pups-new, breeding-list-timed-matings, todo-eartags, todo-genotype, todo-weaning, todo-eartags, todo-no-cage, todo-no-rack, strain-list, strain-new, strain-edit, strain-delete, strain-detail, strain-detail-all, animal-list, animal-list-all, animal-new, animal-update, animal-delete, animal-multiple-new
* Write a view and template for archive-home.  Update unit test
* Change version number in setup.py and Docs/source/conf.py Update Documentation and move to root directory

Version 0.2.1
=============

* Fixed errors in buildout and updated documentation

Version 0.2
===========

* Incorporated buildout for easier deployment


