from django.test import TestCase, SimpleTestCase

# Create your tests here.


class CarviewTest(SimpleTestCase):


    def test_get_cars_status_code(self):
        response = self.client.get('/cars/')
        self.assertEquals(response.status_code, 201)


