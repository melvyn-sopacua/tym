from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^address$', views.AddressDetailView.as_view(), name='address_detail'),
]
