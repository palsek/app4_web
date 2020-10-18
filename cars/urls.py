from django.urls import path
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
#from . import views

from .views import carview
from .views import rateview


urlpatterns = [
    #path('', views.hello, name='hello'),
    #path('', csrf_exempt(views.cars.as_view()), name='cars'),

    # url('', csrf_exempt(views.rate.as_view()), name='rate'),
    # url('', csrf_exempt(views.cars.as_view()), name='cars'),

    url('', csrf_exempt(carview.cars.as_view()), name='cars'),
    url('', csrf_exempt(rateview.rate.as_view()), name='rate'),
    

    #url('', csrf_exempt(xviews.rate.as_view()), name='rate'),
    #url('', csrf_exempt(xviews.cars.as_view()), name='cars'),    
    
    #url('', csrf_exempt(views.carview.cars.as_view()), name='cars'),
    #url('', csrf_exempt(views.rateview.rate.as_view()), name='rate'),
]
