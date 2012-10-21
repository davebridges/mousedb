from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.contrib.auth.decorators import login_required

from mousedb.data.models import Pharmaceutical, Diet
from mousedb.data import views

@login_required
def limited_object_list(*args, **kwargs):
	return object_list(*args, **kwargs)

@login_required
def limited_object_detail(*args, **kwargs):
	return object_detail(*args, **kwargs)

urlpatterns = patterns('',
    url(r'^pharmaceuticals?/?$', views.PharmaceuticalList.as_view(), name="pharmaceutical-list"),
	url(r'^pharmaceuticals?/new/?$', views.PharmaceuticalCreate.as_view(), name="pharmaceutical-new"),    
	url(r'^pharmaceuticals?/(?P<pk>\d*)/?$', views.PharmaceuticalDetail.as_view(), name="pharmaceutical-detail"),
	url(r'^pharmaceuticals?/(?P<pk>\d*)/edit/?$', views.PharmaceuticalUpdate.as_view(), name="pharmaceutical-edit"),
	url(r'^pharmaceuticals?/(?P<pk>\d*)/delete/?$', views.PharmaceuticalDelete.as_view(), name="pharmaceutical-delete"),
			
	url(r'^diets?/(?P<object_id>\d*)', limited_object_detail, {
		'queryset': Diet.objects.all(),
		'template_name': 'diet_detail.html',
		'template_object_name': 'diet',
		}, name="diet-list"),
)
