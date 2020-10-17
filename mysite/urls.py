"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from cars import urls
from cars.views import carview
from cars.views import rateview
from cars.views import popularview

# urlpatterns = [
#      path('admin/', admin.site.urls),
#      path('hello', include('cars.urls')),
#      path('cars/', include('cars.urls')),
#      path('rate/', include('cars.urls')),
# ]


urlpatterns = [
    url('', csrf_exempt(carview.cars.as_view()), name='cars'),
    url('/favicon.ico', csrf_exempt(carview.cars.as_view()), name='cars'),
    url('cars', csrf_exempt(carview.cars.as_view()), name='cars'),
    url('rate', csrf_exempt(rateview.rate.as_view()), name='rate'), # popular
    url('popular/(?P<number>\w+)', csrf_exempt(popularview.popular.as_view()), name='popular'),
    url('popular', csrf_exempt(popularview.popular.as_view()), name='popular'),
    
]