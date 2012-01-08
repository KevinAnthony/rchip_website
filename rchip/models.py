from django.db import models
from main.models import tv_shows 
from django.contrib.auth.models import User

# Create your models here.
class command_queue(models.Model):
	date = models.DateTimeField(auto_now=True)
	command = models.CharField(max_length=255)
	command_text = models.CharField(max_length=4098)
	source_hostname = models.CharField(max_length=255)
	destination_hostname = models.CharField(max_length=255)
	user = models.ForeignKey(User)	

class daemon_register(models.Model):
	time_updated = models.DateTimeField(auto_now=True)
	hostname = models.CharField(max_length=32,unique=True)
	path_to_root = models.CharField(max_length=1024)
	user = models.ForeignKey(User)	

class message_register(models.Model):
	time_updated = models.DateTimeField(auto_now=True)
	source_hostname = models.CharField(max_length=255)
        destination_hostname = models.CharField(max_length=255)
	active = models.BooleanField()
	user = models.ForeignKey(User)

class music_info(models.Model):
	time_updated = models.DateTimeField(auto_now=True)
	artist = models.CharField(max_length=255)
	album = models.CharField(max_length=255)
	song = models.CharField(max_length=255)
	elapsed_time =models.PositiveSmallIntegerField()
	total_time = models.PositiveSmallIntegerField()
	is_playing = models.BooleanField()
	destination_hostname = models.CharField(max_length=255,unique=True)
	user = models.ForeignKey(User)

class remote_devices(models.Model):
        time_updated = models.DateTimeField(auto_now=True)
	devices_name = models.CharField(max_length=255,unique=True)
	active = models.BooleanField()
	user = models.ForeignKey(User)

