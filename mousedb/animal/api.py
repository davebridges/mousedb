'''This package controls API access to the :mod:`~mousedb.animal` app.

Overview
--------

The API for the :mod:`~mousedb.models.animal` application provides data on experimental animals.
A list of all endpoints and links to their schemas are available at **http://yourserver.org/api/v1/** where yourserver is specific to your installation.
There is one access point for animals,which is available using GET requests only:

    measurements are available at the endpoint **http://yourserver.org/api/v1/animal/**

The data can be provided as either a group of objects or as a single object. 
Currently for all requests, no authentication is required.  

The entire API schema is available from each endpoint at::

    /schema/?format=xml
    /schema/?format=json

For example **http://yourserver.org/api/v1/animal/schema/?format=json**.
    

Sample Code
-----------

Either group requests or single object requests can be served depending on if the primary key is provided.  
The request URI has several parts including the servername, the api version (currently v1) then the item type (animal).  
There must be a trailing slash before the request parameters (which are after a **?** sign and separated by a **&** sign).

For a collection of objects
```````````````````````````

For a collection of animals you can request::

    http://yourserver.org/api/v1/animal/?format=json 
    
This would return all animals in the database.  
This would return the response with two JSON objects, **meta** and **objects**.
The **format=json** parameter is default for curl and not required but is necessary for browser requests.
The meta object contains fields for the **limit**, **next**, **offset**, **previous** and **total_count** for the series of objects requested.  
The objects portion is an array of the returned object fields (see the details below for each API).  
Note the id field of an object.  This is used for retrieving a single object.  
Collections can also be filtered based on several request parameters (see below for details for each API)::

    http://yourserver.org/api/v1/animal/ #returns all data in JSON format 
    http://yourserver.org/api/v1/animal/set/1;3/?format=json #returns the animals with the internal id numbers 1 and 3 in XML format.                    

For a single object
```````````````````

To retrieve a single item you need to know the primary key of the object.  
This can be found from the id parameter of a collection (see above) or from the actual object page.  
You can retrieve details about a single assay with a call such as::

    http://yourserver.org/api/v1/animal/2/?format=json  
    
In this case **2** is the primary key (or id field) of the animal in question, but notably is **NOT** the ear tag.


Reference for Animal API
-----------------------------

The measurement API is available at the endpoint **/api/v1/animal/**

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

'''

from tastypie.resources import ModelResource
from tastypie.authentication import ApiKeyAuthentication
from tastypie import fields
from tastypie.constants import ALL, ALL_WITH_RELATIONS

from mousedb.animal.models import Animal, Strain

class AnimalResource(ModelResource):
    '''This generates the API resource for :class:`~mousedb.animal.models.Animal` objects.
    
    It returns all animals in the database.
    '''
    strain = fields.ForeignKey('mousedb.animal.api.StrainResource', 'Strain', full=True)
    age = fields.IntegerField(attribute='age')

    class Meta:
        '''The API serves all :class:`~mousedb.animal.models.Animal` objects in the database..'''

        queryset = Animal.objects.all()
        resource_name = 'animal'
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        fields = ['MouseID','Genotype','Gender','Background','Alive']
        filtering = {"Cage":'exact',
                     "Gender":('exact','startswith'),
                     "Genotype":ALL,
                     "Background":ALL,
                     "Born":ALL,
                     "Weaned":ALL,
                     "Death":ALL,
                     "Cause_of_Death":ALL,
                     "Alive":ALL,
                     "MouseID":ALL,
                     "strain":ALL_WITH_RELATIONS}
        include_resource_uri = False
        authentication = ApiKeyAuthentication()  
        
class StrainResource(ModelResource):  
    '''This generates the API resource for :class:`~mousedb.animal.models.Strain` objects.
    This API is not visible, but instead is used by the AnimalResource
    
    It returns all strains in the database.
    '''
    
    class Meta:
        '''The API serves all :class:`~mousedb.animal.models.Strain` objects in the database..'''

        queryset = Strain.objects.all()
        resource_name = 'strain'
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        fields = ['Strain',]
        include_resource_uri = False
        authentication = ApiKeyAuthentication()
        filtering = {"Strain":ALL}       
