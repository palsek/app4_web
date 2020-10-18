from .models import TheCar

# temporary virtual table which simulate data bases
list_of_cars = []

class CarsDbFacade:

    def add_car(self, car):
        """Add new car to db if already does not exists.
        """

        found_cars = [c for c in list_of_cars if c.make.upper() == car.make.upper() and c.model.upper() == car.model.upper()]
        
        if len(found_cars) == 0:
            list_of_cars.append(car)

    def get_all_cars(self):
        """Get all cars from db.
        """
        return list_of_cars

    def rate_car(self, make, model, rate):
        """Add new rate to specified car.
        """

        found_cars = [c for c in list_of_cars if c.make.upper() == make.upper() and c.model.upper() == model.upper()]
        
        if len(found_cars) > 0:
            found_car = found_cars[0]

            if rate == 1:
                found_car.rate1 = int(found_car.rate1) + 1 if found_car.rate1 is not None else 1
            elif rate == 2:
                found_car.rate2 = int(found_car.rate2) + 1 if found_car.rate1 is not None else 1
            elif rate == 3:
                found_car.rate3 = int(found_car.rate3) + 1 if found_car.rate1 is not None else 1
            elif rate == 4:
                found_car.rate4 = int(found_car.rate4) + 1 if found_car.rate1 is not None else 1
            elif rate == 5:
                found_car.rate5 = int(found_car.rate5) + 1 if found_car.rate1 is not None else 1
            
            found_car.rates += 1

            return True

        else:
            return False
        

    def get_most_popular_car(self, car_number):
        """Get the car which has the most rates.
        """
        
        most_popular_cars = sorted(list_of_cars, key=lambda c: c.rates, reverse=True)[:int(car_number)]        

        return most_popular_cars

