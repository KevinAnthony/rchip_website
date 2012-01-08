from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class tv_shows(models.Model):
	name = models.CharField(max_length=64)
	url = models.CharField(max_length=512)
	show_type = models.CharField(max_length=16,default='tvshow')
	last_eps = models.CharField(max_length=10)
	last_update = models.DateTimeField(default='1983-06-27 00:00:00')
	last_checked = models.DateTimeField(auto_now=True)
	active = models.IntegerField()
	download = models.BooleanField()
	thetvdb_id = models.IntegerField()
	air_time = models.IntegerField(default = 0)
	def __unicode__(self):
        	return self.name

class eps_data(models.Model):
	show = models.ForeignKey('tv_shows')
	air_date = models.DateTimeField("Show Air Date")
	eps_name = models.CharField("Episode Name",max_length=256)
	eps_number = models.CharField("Episode Number",max_length=16)
	downloaded = models.BooleanField()
	uri = models.CharField(max_length=1024)
	css_markup = ""
	class Meta:
		unique_together = (("show","eps_number"))

class user_tv_shows(models.Model):
	show = models.ForeignKey('tv_shows')
	user = models.ForeignKey(User)
	class Meta:
                unique_together = (("show","user"))
