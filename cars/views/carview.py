from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import status
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

import requests
#import json
import json # loads str --> json; dumps json --> str

from cars.models import *
from cars.serializers import TheCarSerializer
from cars.facades import CarsDbFacade



class cars(APIView):

    def get(self, request, format=None):
        print('cars / get')
        cars_db = CarsDbFacade()
        all_cars = cars_db.get_all_cars()

        serializer = TheCarSerializer(all_cars, many=True)
        return Response(serializer.data)
        

    def post(self, request, format=None):

        try:
            wanted_car_make = request.data['car_make']
            wanted_car_name = request.data['model_name']
        except KeyError as e:
            content = {
                'Not found key in request body: ': str(e),
                'proper request example' : {
                    "car_make" : "Honda",
                    "model_name": "civic"
                    }                
                }
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        URL = r'https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{0}?format=json'.format(wanted_car_make)

        try:
            # call external service
            response = requests.get(URL)
        except requests.exceptions.Timeout:
            error_detail = "Timeout exception raised during external service call"
            return Response(error_detail, status=status.HTTP_404_NOT_FOUND)
        except requests.exceptions.RequestException:
            error_detail = "Unknown exception raised during external service call"
            return Response(error_detail, status=status.HTTP_404_NOT_FOUND)
        
        if response.status_code == 200:
            print("response == 200")
            response_data = json.loads(response.content)

            response_data_results = response_data['Results']

            # search cars by car name (model)
            found_cars = [c for c in response_data_results if c['Model_Name'].upper() == wanted_car_name.upper()]

            if len(found_cars) > 0:
                found_car = found_cars[0]
            else:
                content = {'Eror': 'Car not found in external service.'}
                return Response(content, status=status.HTTP_404_NOT_FOUND)

            the_car = TheCar()
            the_car.make = found_car['Make_Name']
            the_car.model = found_car['Model_Name']

            # interaction with local db
            cars_db = CarsDbFacade()
            cars_db.add_car(the_car)
                        
            serializer = TheCarSerializer(the_car)
            return Response(serializer.data)
        else:
            error_detail = 'Error during call external service'
            return Response(error_detail, status=status.HTTP_404_NOT_FOUND)