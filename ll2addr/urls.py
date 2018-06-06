from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^address$', views.OSMAddressView.as_view(), name='address_detail'),
]
