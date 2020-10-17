from rest_framework import serializers

from .models import TheCar
'''
class TheCarSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TheCar
        fields = ('make', 'model', 'year', 'vin')

        
        # make = models.TextField()
        # model = models.TextField()
        # year = models.IntegerField()
        # vin = models.TextField()
'''

class TheCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheCar
        #fields = ('make', 'model', 'year', 'vin', 'rate1', 'rate2', 'rate3', 'rate4', 'rate5', 'rates')
        fields = ('make', 'model', 'rate1', 'rate2', 'rate3', 'rate4', 'rate5', 'rates')



