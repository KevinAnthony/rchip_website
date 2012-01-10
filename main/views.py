from django.template import Context, loader, RequestContext
from django import template
from main.models import eps_data,tv_shows
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
	if request.method == 'POST':
		filterName = request.POST.get("show","")
		if filterName == "":
			eps_list = eps_data.objects.filter(air_date__gte=tda).order_by('air_date','eps_number')
		else:
			eps_list = eps_data.objects.filter(show = tv_shows.objects.get(name=filterName),air_date__gte=now - timedelta(365)).order_by('air_date','eps_number')
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
	t = loader.get_template('templetes/register.html')
	c = RequestContext(request,{'form': form ,'user':request.user,})
	return HttpResponse(t.render(c))


