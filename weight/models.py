from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Weight(models.Model):
	weight = models.DecimalField(max_digits=4, decimal_places=1)
	date =models.DateField('Data of Weighting')
	user = models.ForeignKey(User)	
	def __unicode__(self):
        	return self.weight
