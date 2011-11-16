from django.db import models

# Create your models here.
class Weight(models.Model):
	weight = models.DecimalField(max_digits=4, decimal_places=1)
	date =models.DateField('Data of Weighting')
	username = models.CharField(max_length = 30)
	def __unicode__(self):
        	return self.weight
