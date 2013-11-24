'''This package controls API access to the :mod:`~mousedb.data` app.

Overview
--------

The API for the :mod:`~mousedb.models.data` application provides data on measurements and their associated data types.
A list of all endpoints and links to their schemas are available at **http://yourserver.org/api/v1/** where yourserver is specific to your installation.
There are four access points, each of which is available using GET requests only:

* measurements are available at the endpoint **http://yourserver.org/api/v1/data/**
* assays are available at the endpoint **http://yourserver.org/api/v1/assay/**
* experiments are available at the endpoint **http://yourserver.org/api/v1/experiment/**
* studies are available at the endpoint **http://yourserver.org/api/v1/study/**

The data can be provided as either a group of objects or as a single object. 
Currently for all requests, no authentication is required.  

The entire API schema is available from each endpoint at::

    /schema/?format=xml
    /schema/?format=json

For example **http://yourserver.org/api/v1/study/schema/?format=json**.
    

Sample Code
-----------

Either group requests or single object requests can be served depending on if the primary key is provided.  
The request URI has several parts including the servername, the api version (currently v1) then the item type (data, assay, experiment or study).  
There must be a trailing slash before the request parameters (which are after a **?** sign and separated by a **&** sign).

For a collection of objects
```````````````````````````

For a collection of measurements you can request::

    http://yourserver.org/api/v1/data/?format=json 
    
This would return all measurements in the database.  
This would return the response with two JSON objects, **meta** and **objects**.
The **format=json** parameter is default for curl and not required but is necessary for browser requests.
The meta object contains fields for the **limit**, **next**, **offset**, **previous** and **total_count** for the series of objects requested.  
The objects portion is an array of the returned object fields (see the details below for each API).  
Note the id field of an object.  This is used for retrieving a single object.  
Collections can also be filtered based on several request parameters (see below for details for each API)::

    http://yourserver.org/api/v1/data/ #returns all data in JSON format 
    http://yourserver.org/api/v1/experiment/set/1;3/?format=json #returns the experiments with id numbers 1 and 3 in XML format.                    

For a single object
```````````````````

To retrieve a single item you need to know the primary key of the object.  
This can be found from the id parameter of a collection (see above) or from the actual object page.  
You can retrieve details about a single assay with a call such as::

    http://yourserver.org/api/v1/assay/2/?format=json  
    
In this case **2** is the primary key (or id field) of the assay in question.


Reference for Measurement API
-----------------------------

The measurement API is available at the endpoint **/api/v1/data/**

Request Parameters
``````````````````

The following are the potential request variables, all of which are optional.  
The default format is JSON, but this can be set as XML if required.
If viewing by web browser ?format=json must be specified  
By default 20 items are returned but you can increase this to all by setting limit=0.

+------------------+-----------------------------------------+
| Parameter        | Potential Values                        |
+==================+=========================================+
| format           | **json** or **xml**                     |
+------------------+-----------------------------------------+
| limit            | **0** for all, any other number         |
+------------------+-----------------------------------------+


Response Values
```````````````

The response (in either JSON or XML) provides the following fields for each object (or for the only object in the case of a single object request).

+--------------------+-----------------------------------------------------+-------------------------------------------------------------+
|      Field         |              Explanation                            |                         Sample Value                        |
+====================+=====================================================+=============================================================+
| id                 | the id of the measurement                           | 1                                                           |
+--------------------+-----------------------------------------------------+-------------------------------------------------------------+ 
| resource_uri       | the URI to request details about a measurement      | /api/v1/data/1/                                             |
+--------------------+-----------------------------------------------------+-------------------------------------------------------------+ 
| values             | the measurement, or measurement(s)                  | 423                                                         |
+--------------------+-----------------------------------------------------+-------------------------------------------------------------+ 


Reference for the Assay API
---------------------------

The assay API is available at the endpoint **/api/v1/assay/**

Request Parameters
``````````````````

The following are the potential request variables, all of which are optional.  
The default format is JSON, but this can be set as XML if required.
If viewing by web browser ?format=json must be specified  
By default 20 items are returned but you can increase this to all by setting limit=0.

+------------------+-----------------------------------------+
| Parameter        | Potential Values                        |
+==================+=========================================+
| format           | **json** or **xml**                     |
+------------------+-----------------------------------------+
| limit            | **0** for all, any other number         |
+------------------+-----------------------------------------+

Response Values
```````````````

The response (in either JSON or XML) provides the following fields for each object (or for the only object in the case of a single object request).

+--------------------+-------------------------------------------------------------+-------------------------------------------------------------+
|      Field         |              Explanation                                    |                         Sample Value                        |
+====================+=============================================================+=============================================================+
| id                 | the id of the measurement                                   | 3                                                           |
+--------------------+-------------------------------------------------------------+-------------------------------------------------------------+ 
| resource_uri       | the URI to request details about a measurement              | /api/v1/assay/3/                                            |
+--------------------+-------------------------------------------------------------+-------------------------------------------------------------+ 
| assay              | the name of the assay                                       | Body Weight                                                 |
+--------------------+-------------------------------------------------------------+-------------------------------------------------------------+ 
| assay_slug         | the slugified name of the assay (can be used for filtering) | body_weight                                                 |
+--------------------+-------------------------------------------------------------+-------------------------------------------------------------+
| measurement_units  | the units for the measurment                                | mg/dL                                                       |
+--------------------+-------------------------------------------------------------+-------------------------------------------------------------+
| notes              | notes regarding this assay                                  | Some text values                                            |
+--------------------+-------------------------------------------------------------+-------------------------------------------------------------+

Reference for the Experiment API
--------------------------------

The experiment API is available at the endpoint **/api/v1/experiment/**

Request Parameters
``````````````````

The following are the potential request variables, all of which are optional.  
The default format is JSON, but this can be set as XML if required.
If viewing by web browser ?format=json must be specified  
By default 20 items are returned but you can increase this to all by setting limit=0.

+------------------+-----------------------------------------+
| Parameter        | Potential Values                        |
+==================+=========================================+
| format           | **json** or **xml**                     |
+------------------+-----------------------------------------+
| limit            | **0** for all, any other number         |
+------------------+-----------------------------------------+


Response Values
```````````````

The response (in either JSON or XML) provides the following fields for each object (or for the only object in the case of a single object request).

+--------------------+-------------------------------------------------------------+-------------------------------------------------------------+
|      Field         |              Explanation                                    |                         Sample Value                        |
+====================+=============================================================+=============================================================+
| id                 | the id of the measurement                                   | 5                                                           |
+--------------------+-------------------------------------------------------------+-------------------------------------------------------------+ 
| resource_uri       | the URI to request details about a measurement              | /api/v1/experiment/5/                                       |
+--------------------+-------------------------------------------------------------+-------------------------------------------------------------+ 
| concentration      | the concentration of the injection (if done)                | 1mU/kg                                                      |
+--------------------+-------------------------------------------------------------+-------------------------------------------------------------+ 
| date               | the date of the experiment                                  | 2012-09-28                                                  |
+--------------------+-------------------------------------------------------------+-------------------------------------------------------------+ 
| experimentID       | the optional experimentID number                            | DB-2012-09-28                                               |
+--------------------+-------------------------------------------------------------+-------------------------------------------------------------+ 
| fasting_time       | the duration of the animal fast (if done) in hours          | 16                                                          |
+--------------------+-------------------------------------------------------------+-------------------------------------------------------------+ 
| feeding_state      | whether the animals were fed or fasted                      | fed OR fasted                                               |
+--------------------+-------------------------------------------------------------+-------------------------------------------------------------+ 
| injection          | the injection (if done)                                     | Insulin, Glucose, Pyruvate or Glucagon                      |
+--------------------+-------------------------------------------------------------+-------------------------------------------------------------+
| notes              | notes regarding this experiment                             | Some text values                                            |
+--------------------+-------------------------------------------------------------+-------------------------------------------------------------+
| time               | the time of day the assay was done (24h format)             | 16:00                                                       |
+--------------------+-------------------------------------------------------------+-------------------------------------------------------------+

Reference for the Study API
---------------------------

The study API is available at the endpoint **/api/v1/study/**

Request Parameters
``````````````````

The following are the potential request variables, all of which are optional.  
The default format is JSON but this can be set as XML if required.
If viewing by web browser ?format=json must be specified  
By default 20 items are returned but you can increase this to all by setting limit=0.

+------------------+-----------------------------------------+
| Parameter        | Potential Values                        |
+==================+=========================================+
| format           | **json** or **xml**                     |
+------------------+-----------------------------------------+
| limit            | **0** for all, any other number         |
+------------------+-----------------------------------------+

Response Values
```````````````

The response (in either JSON or XML) provides the following fields for each object (or for the only object in the case of a single object request).

+--------------------+-------------------------------------------------------------+-------------------------------------------------------------+
|      Field         |              Explanation                                    |                         Sample Value                        |
+====================+=============================================================+=============================================================+
| id                 | the id of the measurement                                   | 6                                                           |
+--------------------+-------------------------------------------------------------+-------------------------------------------------------------+ 
| resource_uri       | the URI to request details about a measurement              | /api/v1/study/6/                                            |
+--------------------+-------------------------------------------------------------+-------------------------------------------------------------+ 
| description        | the description of the study                                | some text                                                   |
+--------------------+-------------------------------------------------------------+-------------------------------------------------------------+ 
| notes              | some notes about the study                                  | some text                                                   |
+--------------------+-------------------------------------------------------------+-------------------------------------------------------------+ 
| start_date         | the optional starting date of the study                     | 2012-07-23                                                  |
+--------------------+-------------------------------------------------------------+-------------------------------------------------------------+ 
| stop _date         | the optional end date of the study                          | 2012-09-27                                                  |
+--------------------+-------------------------------------------------------------+-------------------------------------------------------------+ 

'''

from tastypie.resources import ModelResource
from tastypie.authentication import ApiKeyAuthentication
from tastypie import fields
from tastypie.constants import ALL, ALL_WITH_RELATIONS

from mousedb.data.models import Measurement, Assay, Experiment, Study

class MeasurementResource(ModelResource):
    '''This generates the API resource for :class:`~mousedb.data.models.Measurement` objects.
    
    It returns all measurements in the database.
    '''
    animal = fields.ForeignKey('mousedb.animal.api.AnimalResource','animal',full=True)
    assay = fields.ForeignKey('mousedb.data.api.MeasurementAssayResource', 'assay', full=True)
    experiment = fields.ForeignKey('mousedb.data.api.MeasurementExperimentResource', 'experiment', full=True)
    age = fields.IntegerField(attribute='age', null=True)   
 
    class Meta:
        '''The API serves all :class:`~mousedb.data.models.Measurement` objects in the database..'''

        queryset = Measurement.objects.all()
        resource_name = 'data'
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        include_resource_uri = False
        authentication = ApiKeyAuthentication()  
        filtering = {"assay":ALL_WITH_RELATIONS,
                     "animal":ALL_WITH_RELATIONS}

           
class AssayResource(ModelResource):
    '''This generates the API resource for :class:`~mousedb.data.models.Assay` objects.
    
    It returns all assays in the database.
    '''
    
    class Meta:
        '''The API serves all :class:`~mousedb.data.models.Assay` objects in the database..'''

        queryset = Assay.objects.all()
        resource_name = 'assay'
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        authentication = ApiKeyAuthentication()
        filtering = {"assay":ALL}


class MeasurementAssayResource(AssayResource):
    '''This generates serves :class:`~mousedb.data.models.Assay` objects.
    
    This is a limited dataset for use in MeasurementResource calls.
    '''
    
    class Meta:
        '''The API serves all :class:`~mousedb.data.models.Assay` objects in the database..'''

        include_resource_uri = False
        fields = ['assay',]         
        filtering  = {"assay":ALL}    
    
class ExperimentResource(ModelResource):
    '''This generates the API resource for :class:`~mousedb.data.models.Experiment` objects.
    
    It returns all experiments in the database.
    '''

    class Meta:
        '''The API serves all :class:`~mousedb.data.models.Experiment` objects in the database..'''

        queryset = Experiment.objects.all()
        resource_name = 'experiment'
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        authentication = ApiKeyAuthentication()

class MeasurementExperimentResource(ExperimentResource): 

    class Meta:
        '''The API serves :class:`~mousedb.data.models.Experiment` objects.
        
        This is a limited dataset for use in MeasurementResource calls.
        '''

        fields = ['date',]
        include_resource_uri = False           
        
class StudyResource(ModelResource):
    '''This generates the API resource for :class:`~mousedb.data.models.Study` objects.
    
    It returns all studies in the database.
    '''
    
    class Meta:
        '''The API serves all :class:`~mousedb.data.models.Study` objects in the database..'''

        queryset = Study.objects.all()
        resource_name = 'study'
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        authentication = ApiKeyAuthentication()        
