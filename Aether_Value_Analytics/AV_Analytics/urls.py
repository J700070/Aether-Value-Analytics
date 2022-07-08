from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('data_collection', views.data_collection, name='data_collection'),
    path('data_collection/<str:message>', views.data_collection, name='data_collection'),
    path('data_analysis', views.data_analysis, name='data_analysis'),
    path('company/<str:company_id>', views.company, name='company'),
    path('get_company_data', views.get_company_data, name='get_company_data'),
    path('search', views.search, name='search'),
]