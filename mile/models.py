from django.db import models

# Create your models here.
class car(models.Model):
	make = models.CharField(max_length=16)
	model  = models.CharField(max_length=30)
	year   = models.IntegerField()
	string = models.CharField(max_length=64)

class mileage(models.Model):
	carString = models.CharField(max_length=64)
	date_of_fillup = models.DateField()
	num_of_gallons = models.DecimalField(max_digits=5,decimal_places=3)
	price_per_gallon = models.DecimalField(max_digits=5,decimal_places=3)
	price_of_fillup = models.DecimalField(max_digits=5,decimal_places=2)
	mpg = models.DecimalField(max_digits=4,decimal_places=2)
	octain = models.IntegerField()
	gas_station = models.CharField(max_length=64)
	userName = models.CharField(max_length=64)

class coinJar(models.Model):
	dollars = models.IntegerField()
	quarters = models.IntegerField()
	dimes = models.IntegerField()
	nickles = models.IntegerField()
	pennies = models.IntegerField()
	dateChanged = models.DateTimeField(auto_now=True)
	userName = models.CharField(max_length=64)
