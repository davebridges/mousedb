'''This package controls API access to the :mod:`~mousedb.data` app.

Overview
--------

The API for the :mod:`~mousedb.models.data` application provides data on measurements. 
There are four access points, each of which is available using GET requests only:

* measurements available at the endpoint **http://yourserver.org/api/v1/data/**
* assays available at the endpoint **http://yourserver.org/api/v1/assay/**
* experiments available at the endpoint **http://yourserver.org/api/v1/experiment/**
* studies available at the endpoint **http://yourserver.org/api/v1/study/**

The data can be provided as either a group of objects or as a single object. 
Currently for all requests, no authentication is required.  The entire API schema is available from each endpoint at::

    /schema/?format=xml
    /schema/?format=json
    

Sample Code
-----------

Either group requests or single object requests can be served depending on if the primary key is provided.  
The request URI has several parts including the servername, the api version (currently v1) then the item type (data, assay, experiment or study).  
There must be a trailing slash before the request parameters (which are after a **?** sign and separated by a **&** sign).

For a collection of objects
```````````````````````````

For a collection of measurements you can request::

    http://yourserver.org/api/v1/data/?format=json 
    
This would return all measurements in the database.  This would return the following json response with two JSON objects, meta and objects.
The meta object contains fields for the limit, next, offset, previous and total_count for the series of objects requested.  
The objects portion is an array of the returned measurements.  
Note the id field of a measurement.  This is used for retrieving a single datum.  
Collections can also be filtered based on assay or year::

    http://yourserver.org/api/v1/data/?format=json&year=2012     
    http://yourserver.org/api/v1/data/?format=json&assay=body-weight 
    http://yourserver.org/api/v1/data/?format=json&assay=body-weight&year=2012
    http://yourserver.org/api/v1/data/set/1;3/?format=json 
    
The last example requests the measurements with id numbers 1 and 3.                    

For a single object
```````````````````

To retrieve a single item you need to know the primary key of the object.  
This can be found from the id parameter of a collection (see above) or from the actual object page.  
You can retrieve details about a single assay with a call such as::

    http://yourserver.org/api/v1/assay/2/?format=json  
    
In this case **2** is the primary key (or id field) of the assay in question.


Reference for Measurement API
-----------------------------

Request Parameters
``````````````````

The following are the potential request variables, all of which are optional.  
The default format is json, but this can be set as json if required.
If viewing by web browser ?format=json must be specified  
By default 20 items are returned but you can increase this to all by setting limit=0.

+------------------+-----------------------------------------+
| Parameter        | Potential Values                        |
+==================+=========================================+
| format           | **json** or **xml**                     |
+------------------+-----------------------------------------+
| limit            | **0** for all, any other number         |
+------------------|-----------------------------------------+

Response Values
```````````````

The response (in either json or xml) provides the following fields for each object (or for the only object in the case of a single object request).

+--------------------+-----------------------------------------------------+-------------------------------------------------------------+
|      Field         |              Explanation                            |                         Sample Value                        |
+====================+=====================================================+=============================================================+
| id                 | the id of the measurement                           | 1                                                           |
+--------------------+-----------------------------------------------------+-------------------------------------------------------------+ 
| resource_uri       | the URI to request details about a measurement      | /api/v1/data/3/                                             |
+--------------------+-----------------------------------------------------+-------------------------------------------------------------+ 
| values             | the measurement, or measurement(s)                  | 423                                                         |
+--------------------+-----------------------------------------------------+-------------------------------------------------------------+ 


Reference for the Assay API
---------------------------

Request Parameters
``````````````````

The following are the potential request variables, all of which are optional.  
The default format is json, but this can be set as json if required.
If viewing by web browser ?format=json must be specified  
By default 20 items are returned but you can increase this to all by setting limit=0.

+------------------+-----------------------------------------+
| Parameter        | Potential Values                        |
+==================+=========================================+
| format           | **json** or **xml**                     |
+------------------+-----------------------------------------+
| limit            | **0** for all, any other number         |
+------------------|-----------------------------------------+

Response Values
```````````````

The response (in either json or xml) provides the following fields for each object (or for the only object in the case of a single object request).

+--------------------+-------------------------------------------------------------+-------------------------------------------------------------+
|      Field         |              Explanation                                    |                         Sample Value                        |
+====================+=============================================================+=============================================================+
| id                 | the id of the measurement                                   | 1                                                           |
+--------------------+-------------------------------------------------------------+-------------------------------------------------------------+ 
| resource_uri       | the URI to request details about a measurement              | /api/v1/data/3/                                             |
+--------------------+-------------------------------------------------------------+-------------------------------------------------------------+ 
| assay              | the name of the assay                                       | Body Weight                                                 |
+--------------------+-------------------------------------------------------------+-------------------------------------------------------------+ 
| assay_slug         | the slugified name of the assay (can be used for filtering) | body_weight                                                 |
+--------------------+-------------------------------------------------------------+-------------------------------------------------------------+
| measurement_units  | the units for the measurment                                | mg/dL                                                       |
+--------------------+-------------------------------------------------------------+-------------------------------------------------------------+
| notes              | notes regarding this assay                                  | Some text values                                            |
+--------------------+-------------------------------------------------------------+-------------------------------------------------------------+

'''

from tastypie.resources import ModelResource

from mousedb.data.models import Measurement, Assay

class MeasurementResource(ModelResource):
    '''This generates the API resource for :class:`~mousedb.data.models.Measurement` objects.
    
    It returns all measurements in the database.
    '''
    
    class Meta:
        '''The API serves all :class:`~mousedb.data.models.Measurement` objects in the database..'''

        queryset = Measurement.objects.all()
        resource_name = 'data'
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']   
               
class AssayResource(ModelResource):
    '''This generates the API resource for :class:`~mousedb.data.models.Assay` objects.
    
    It returns all assays in the database.
    '''
    
    class Meta:
        '''The API serves all :class:`~mousedb.data.models.Assat` objects in the database..'''

        queryset = Assay.objects.all()
        resource_name = 'assay'
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']         
        
        