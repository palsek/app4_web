from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import status
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

import requests
import json # loads str --> json; dumps json --> str

from cars.models import *
from cars.serializers import TheCarSerializer
from cars.facades import CarsDbFacade


class popular(APIView):

    def get(self, request, number=3, format=None):

        print("popular / get / number: " + str(number))

        cars_db = CarsDbFacade()
        most_popular_cars = cars_db.get_most_popular_car(number)

        
        serializer = TheCarSerializer(most_popular_cars, many=True)
        return Response(serializer.data)
 