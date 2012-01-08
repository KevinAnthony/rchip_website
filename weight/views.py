from django.template import Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf

from weight.models import Weight
from forms import AddForm

# Create your views here.
@login_required
def index(request):
	Weights_list = Weight.objects.filter(user=request.user.id).order_by('-date')
	Weights_chart_list = Weight.objects.filter(user=request.user.id).order_by('date')
	Goal = 180
	try:
		Diff = Weights_chart_list[0].weight - Weights_list[0].weight
		ToGo = Weights_list[0].weight-Goal
	except:
		Diff = 0
		ToGo = 0
	if Diff > 0 :
		Str = 'Loss'
	else :
		Str = 'Gain'
	Diff = abs(Diff)
	Min = Weights_list[0].weight
	minDate = Weights_list[0].date
	Max = Weights_list[0].weight
	maxDate = Weights_list[0].date
	for w in Weights_list:	
		if w.weight < Min:
			Min = w.weight
			minDate = w.date
		elif w.weight > Max:
			Max = w.weight
			maxDate = w.date
	t = loader.get_template('weight/index.html')
	c = Context({
		'Weights_list': Weights_list,
		'Weights_chart_list': Weights_chart_list,
		'Goal': Goal,
		'Diff': Diff,
		'Str': Str,
		'user':request.user,
		'Max':Max,
		'minDate':minDate,
		'maxDate':maxDate,
		'Min':Min,
		'ToGo':ToGo,
	})
	return HttpResponse(t.render(c))

@login_required
@csrf_protect
def add(request):
	
	if request.method == 'POST':
        	form = AddForm(request.POST)
        	if form.is_valid():
		    newDate = form.cleaned_data['date']
    		    newWeight = form.cleaned_data['weight']
        	    w = Weight(weight=newWeight, date=newDate, username=request.user.username)
		    w.save()


                    return HttpResponseRedirect('/weight/')
   	else:
        	form = AddForm()
	t = loader.get_template('weight/add.html')
	c = RequestContext(request,{
		'form': form,
		'user':request.user,
	})
    	return HttpResponse(t.render(c))
