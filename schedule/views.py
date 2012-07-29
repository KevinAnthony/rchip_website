from django.template import Context, loader, RequestContext
from django import template,forms
from schedule.models import episode_data,tv_shows,tv_shows_form,user_tv_shows
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from datetime import datetime,timedelta
from schedule.update import updateEpsList
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.exceptions import ValidationError
from django.utils import timezone
from pytz import timezone as pytimezone
import pytz
# Create your views here.
@csrf_exempt
def schedule_index(request):
    now = datetime.now(pytimezone('US/Eastern'))
    tda = now - timedelta(7)
    filterName = ""
    if request.user.is_authenticated():
        if request.method == 'POST':
            filterName = request.POST.get("show","")
            if filterName == "":
                eps_list = episode_data.objects.filter(show__user_tv_shows__user=request.user,air_date__gte=tda).order_by('air_date','eps_number')
            else:
                eps_list = episode_data.objects.filter(show__name=filterName,show__user_tv_shows__user=request.user).order_by('eps_number')
        else:
            eps_list = episode_data.objects.filter(show__user_tv_shows__user=request.user,air_date__gte=tda).order_by('air_date','eps_number')
        show_list = tv_shows.objects.filter(show_type = "tvshow",active=1,user_tv_shows__user=request.user).order_by('name')
    else:
        if request.method == 'POST':
            filterName = request.POST.get("show","")
            if filterName == "":
                eps_list = episode_data.objects.filter(air_date__gte=tda).order_by('air_date','eps_number')
            else:
                eps_list = episode_data.objects.filter(show = tv_shows.objects.get(name=filterName)).order_by('eps_number')
        else:
            eps_list = episode_data.objects.filter(air_date__gte=tda).order_by('air_date','eps_number')
        show_list = tv_shows.objects.filter(show_type = "tvshow",active=1).order_by('name')
    for e in eps_list:
        show = tv_shows.objects.get(id = e.show_id)
        e.air_date = e.air_date.replace(tzinfo=pytimezone('US/Eastern'))
        air_time = show.air_time
        offset = int(now.strftime("%z"))
        air_time += offset
        e.air_date = e.air_date + timedelta(hours = air_time/100, minutes = air_time%100) 
        if e.air_date < (now - timedelta(hours=1)):
            e.css_markup = "oldrow"
        elif e.air_date < now:
            e.css_markup = "playing"
        elif e.air_date < now + timedelta(1):
            e.css_markup = "today"
        elif e.air_date >= now + timedelta(7):
            e.css_markup = "futurerow"
        else:
            e.css_markup = "currentrow"
        if e.downloaded:
            e.uri = e.uri.replace("/mnt/raid/","ftp://192.168.1.3/")
    t = loader.get_template('templates/schedule_index.html')
    future = now + timedelta(7)
    c = Context({
        'eps_list': eps_list,
        'user':request.user,
        'show_list': show_list,
        'show_name': filterName,
    })
    return HttpResponse(t.render(c))

def schedule_update(request):
    updateEpsList().update()
    return schedule_index(request)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        new_user = form.save()
        return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    t = loader.get_template('templates/register.html')
    c = RequestContext(request,{'form': form ,'user':request.user,})
    return HttpResponse(t.render(c))

@login_required
@csrf_exempt
def schedule_config_tv_shows(request):
    tv_shows_list = tv_shows.objects.all()
    for show in tv_shows_list:
        if user_tv_shows.objects.filter(show=show, user=request.user):
            show.user_show=True
        else:
            show.user_show=False
    if request.method == 'POST':
        for show in tv_shows_list:
            if request.POST.get("active_%s"%(show.name)):
                active=True
            else:
                active=False
            if request.POST.get("download_%s"%(show.name)):
                download=True
            else:
                download=False
            if request.POST.get("show_%s"%(show.name)):
                user_show=True
            else:
                user_show=False
            if show.active != active or show.download != download:
                show.active=active
                show.download=download
                show.save()
            if show.user_show != user_show:
                if user_show:
                    user_tv_shows(show=show,user=request.user).save()
                else:
                    user_tv_shows.objects.filter(show=show).delete()
    t = loader.get_template('templates/schedule_tv_shows.html')
    c = RequestContext(request,{'tv_show_list': tv_shows_list ,'user':request.user,})
    return HttpResponse(t.render(c))

@login_required
def schedule_add_tv_show(request):
    if request.method == 'POST':
        form = tv_shows_form(request.POST)
        if form.is_valid():
            if not tv_shows.objects.filter(name=form.cleaned_data['name']):
                form.save()
            else:
                raise ValidationError("Show %s already in Database" % (form.cleaned_data['name']))
    else:
        form = tv_shows_form()
    t = loader.get_template('templates/schedule_add_tv_form.html')
    c = RequestContext(request,{"form":form})
    return HttpResponse(t.render(c))

