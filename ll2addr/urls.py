from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'address/', views.AddressDetail.as_view(), name='address_detail'),
]
