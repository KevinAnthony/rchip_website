from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
# Create your models here.

class tv_shows(models.Model):
    name = models.CharField(max_length=64)
    url = models.CharField(max_length=512)
    show_type = models.CharField(max_length=16,default='tvshow')
    last_eps = models.CharField(max_length=10,default='S01E01')
    last_update = models.DateTimeField(default='1983-06-27 00:00:00')
    last_checked = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    download = models.BooleanField(default=False)
    thetvdb_id = models.IntegerField()
    air_time = models.IntegerField(default = 0)
    source_regex = models.CharField(max_length=32,default=None)
    destination_regex = models.CharField(max_length=32,default=None)
    def __unicode__(self):
            return self.name

class tv_shows_form(ModelForm):
    class Meta:
        model=tv_shows

class episode_data(models.Model):
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
