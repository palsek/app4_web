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
from cars.setup import CARS_SERVICE_URL


class cars(APIView):

    def get(self, request, format=None):
        """"Get all cars from local db
        """

        cars_db = CarsDbFacade()
        all_cars = cars_db.get_all_cars()

        serializer = TheCarSerializer(all_cars, many=True)

        # prepare average rate for each car
        for car in serializer.data:
            car['average_rate'] = (car['rate1'] * 1 + car['rate2'] * 2 + car['rate3'] * 3 + car['rate4'] * 4 + car['rate5'] * 5) / car['rates']

        return Response(serializer.data)
        

    def post(self, request, format=None):
        """Search car in external service and adds it to local db
        """

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
        
        # prepare url to external car service
        car_service_url = CARS_SERVICE_URL + wanted_car_make + r'?format=json'

        try:
            # call external service
            response = requests.get(car_service_url)
        except requests.exceptions.Timeout:
            error_detail = "Timeout exception raised during external service call"
            return Response(error_detail, status=status.HTTP_404_NOT_FOUND)
        except requests.exceptions.RequestException:
            error_detail = "Unknown exception raised during external service call"
            return Response(error_detail, status=status.HTTP_404_NOT_FOUND)
        
        if response.status_code == 200:
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