'''This package controls API access to the :mod:`~mousedb.data` app.

Overview
--------

The API for the :mod:`papers` application provides data on publications.  The data can be provided as either a group of publications or as a single publication.  Only GET requests are accepted.
These urls are served at the endpoint **/api/v1/publications/**, and depends on your server url.  For these examples we will presume that you can reach this endpoint at **http://yourserver.org/api/v1/publications/**.  Currently for all requests, no authentication is required.  The entire API schema is available at::

    http://yourserver.org/api/v1/data/schema/?format=xml
    http://yourserver.org/api/v1/data/schema/?format=json
    

Sample Code
-----------

Either group requests or single publication requests can be served depending on if the primary key is provided.  The request URI has several parts including the servername, the api version (currently v1) then the item type (publications).  There must be a trailing slash before the request parameters (which are after a **?** sign and separated by a **&** sign).

For a collection of publications
````````````````````````````````

For a collection of publications you can request::

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

For a single measurement
````````````````````````

To retrieve a single measurement you need to know the primary key of the object.  
This can be found from the id parameter of a collection (see above) or from the actual object page.  
You can retrieve details about a single measurment with a call such as::

    http://yourserver.org/api/v1/publications/2/?format=json  
    
In this case **2** is the primary key (or id field) of the measurement in question.


Reference
---------

Request Parameters
``````````````````

The following are the potential request variables.  
You must supply a format, but can also filter based on other parameters.  
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


'''

from tastypie.resources import ModelResource

from mousedb.data.models import Measurement

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
               