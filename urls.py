from django.conf.urls import url
from payu import views

urlpatterns = [
    url(r'^paymentpage$', views.index, name='index'),
    url(r'^success', views.success, name='success'),
    url(r'^fail', views.fail, name='fail'),
]
