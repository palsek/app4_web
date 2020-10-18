#from django.shortcuts import render
#from django.http import HttpResponse

from rest_framework import status
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

import requests
import json

from cars.models import *
from cars.serializers import TheCarSerializer
from cars.facades import CarsDbFacade


class rate(APIView):

    def get(self, request, format=None):
        """Return error because this operation is forbidden
        """

        error_detail = 'This method is unsupported'
        return Response(error_detail, status=status.HTTP_404_NOT_FOUND)


    def post(self, request, format=None):
        """Add a rate for a car from 1 to 5
        """

        try:
            wanted_car_make = request.data['car_make']
            wanted_car_name = request.data['model_name']
            wanted_car_rate = request.data['rate']
        except KeyError as e:
            content = {
                'Not found key in request body: ': str(e),
                'proper request example' : {
                    "car_make" : "Honda",
                    "model_name": "civic",
                    "rate" : 5
                    }                
                }
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        if int(wanted_car_rate) < 1 or int(wanted_car_rate) > 5:
            return Response('Rate need to be between 1 and 5', status=status.HTTP_404_NOT_FOUND)

        cars_db = CarsDbFacade()
        if cars_db.rate_car(wanted_car_make, wanted_car_name, wanted_car_rate):
            return Response('', status=status.HTTP_200_OK)
        else:
            error_detail = 'Error during rating, probably no such car exists'
            return Response(error_detail, status=status.HTTP_404_NOT_FOUND)