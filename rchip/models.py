from django.db import models

# Create your models here.
class command_queue(models.Model):
	date = models.DateTimeField(auto_now=True)
	command = models.CharField(max_length=255)
	command_text = models.CharField(max_length=4098)
	source_hostname = models.CharField(max_length=255)
	destination_hostname = models.CharField(max_length=255)

class daemon_register(models.Model):
	time_updated = models.DateTimeField(auto_now=True)
	hostname = models.CharField(max_length=32,unique=True)
	path_to_root = models.CharField(max_length=1024)

class message_register(models.Model):
	time_updated = models.DateTimeField(auto_now=True)
	source_hostname = models.CharField(max_length=255)
        destination_hostname = models.CharField(max_length=255)
	active = models.BooleanField()

class music_info(models.Model):
	time_updated = models.DateTimeField(auto_now=True)
	artist = models.CharField(max_length=255)
	album = models.CharField(max_length=255)
	song = models.CharField(max_length=255)
	elapsed_time =models.PositiveSmallIntegerField()
	total_time = models.PositiveSmallIntegerField()
	is_playing = models.BooleanField()
	destination_hostname = models.CharField(max_length=255,unique=True)

class remote_devices(models.Model):
        time_updated = models.DateTimeField(auto_now=True)
	devices_name = models.CharField(max_length=255,unique=True)
	active = models.BooleanField()
