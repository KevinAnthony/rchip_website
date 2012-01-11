from django.template import Context, loader, RequestContext
from django import template
from main.models import eps_data,tv_shows,user_tv_shows
from django.http import HttpResponse,HttpResponseRedirect
from datetime import datetime,timedelta
from main.update import updateEpsList 
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.context_processors import csrf

# Create your views here.
@csrf_exempt
def main_index(request):
	now = datetime.now()
	tda = now - timedelta(7)
	filterName = ""
	if request.user.is_authenticated():
		if request.method == 'POST':
			filterName = request.POST.get("show","")
			if filterName == "":
				eps_list = eps_data.objects.filter(show__user_tv_shows__user=request.user,air_date__gte=tda).order_by('air_date','eps_number')
			else:
				eps_list = eps_data.objects.filter(show__name=filterName,show__user_tv_shows__user=request.user).order_by('eps_number')
		else:
			eps_list = eps_data.objects.filter(show__user_tv_shows__user=request.user,air_date__gte=tda).order_by('air_date','eps_number')
		show_list = tv_shows.objects.filter(show_type = "tvshow",active=1,user_tv_shows__user=request.user).order_by('name')
	else:
		if request.method == 'POST':
			filterName = request.POST.get("show","")
			if filterName == "":
				eps_list = eps_data.objects.filter(air_date__gte=tda).order_by('air_date','eps_number')
			else:
				eps_list = eps_data.objects.filter(show = tv_shows.objects.get(name=filterName)).order_by('eps_number')
		else:
			eps_list = eps_data.objects.filter(air_date__gte=tda).order_by('air_date','eps_number')
		show_list = tv_shows.objects.filter(show_type = "tvshow",active=1).order_by('name')
	for e in eps_list:
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
	t = loader.get_template('templates/main_index.html')
	future = now + timedelta(7)
	c = Context({
		'eps_list': eps_list,
		'user':request.user,
		'show_list': show_list,
		'show_name': filterName,
	})
	return HttpResponse(t.render(c))

def main_update(request):
	updateEpsList().update()
	return index(request)

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

@csrf_exempt
def main_config_tv_shows(request):
	tv_shows_list = tv_shows.objects.all()
	for show in tv_shows_list:
		if user_tv_shows.objects.filter(show=show):
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
	t = loader.get_template('templates/main_tv_shows.html')
        c = RequestContext(request,{'tv_show_list': tv_shows_list ,'user':request.user,})
        return HttpResponse(t.render(c))	
	
def main_add_tv_show(request):
	return HttpResponse(None)
