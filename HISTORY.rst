Version 0.2.1dev
================
* Added units tests for data and timed_mating apps.  
* Added south, mysql-python and django-ajax-selects dependencies to setup.py
* Removed all references to "mousedb" in urls.  This allows for separate installations to use different server locations (ie /mousedb-dave and /mousedb-nicole.  Checked that all templates use get_absolute_url or {% url url-name %} tags.
* Fixed error in todo/wean page to show only animals >21 days old which have not been weaned.
* Added logout button
* Adjusted filters for genotyping and weaning.  Updated localsettings_empty.py with default values.
* Updated documentation for installation using pip and buildout

Stuff To Do
+++++++++++
* Add researcher/new page
* Make experiment_add into a form without the experiment field where that is saved automatically.
* The MEDIA_URL and LOGIN_URL are hardcoded, this should be fixed.
* Need to update get_absolute_url for all models
* Set a post-save-redirect for measurement-new and measurement-edit
* Still need the following tests
 * ModelTests: animal.Strain, data.Treatment, data.Assay, data.Diet, data.Environment, data.Experiment, data.Implantation, data.Measurement, data.Pharmaceutical, data.Researcher, data.Transplantation, data.Vendor
 * ViewTests: logout-view,treatment-list,treatment-new, treatment-edit, treatment-delete, experiment-list, experiment-detail, experiment-detail-csv, data-entry, experiment-new, measurement-list, experiemnt-edit, measurement-edit, measurement-delete, pharmaceutical-list, diet-list, study-experiment-new
* Change version number in setup.py and Docs/source/conf.py Update Documentation and move to root directory


Version 0.2.1
=============

* Fixed errors in buildout and updated documentation

Version 0.2
===========

* Incorporated buildout for easier deployment


