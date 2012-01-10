from django.template import Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect

from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf

from forms import HackForm

# Create your views here.
@csrf_protect
def index(request):
	word1error = ""
	word2error = ""
	word3error = ""
	word4error = ""
	correntWordCorrect = ""
	if request.method == 'POST':
        	form = HackForm(request.POST)
        	if form.is_valid():
		    	W1 = form.cleaned_data['word1']
		    	V1 = form.cleaned_data['val1']
		    	W2 = form.cleaned_data['word2']
                    	V2 = form.cleaned_data['val2']
		    	W3 = form.cleaned_data['word3']
                    	V3 = form.cleaned_data['val3']
			W4 = form.cleaned_data['word4']
			V4 = form.cleaned_data['val4']
			CW = form.cleaned_data['CurrentWord']
			if len(CW) != len(W1):
				word1error = "Word %s is the Wrong Length" % (W1)
			elif W2 != "" and len(CW) != len(W2):
                                word2error = "Word %s is the Wrong Length" % (W1)
                        elif W3 != "" and len(CW) != len(W3):
				word3error = "Word %s is the Wrong Length" % (W1)
			elif W4 != "" and len(CW) != len(W4):
				word4error = "Word %s is the Wrong Length" % (W1)
			else:
				for i in range(len(CW)):
					if CW[i] == W1[i]:
						V1 -= 1 
					if W2 != "" and CW[i] == W2[i]:
                        	                V2 -= 1
					if W3 != "" and CW[i] == W3[i]:
                        	                V3 -= 1
					if W4 != "" and CW[i] == W4[i]:
                        	                V4 -= 1
					if not V1 and not V2 and not V3 and not V4:
						correntWordCorrect = "%s is a valid word" %(CW)
   	else:
        	form = HackForm()
	t = loader.get_template('templates/hack_index.html')
	c = RequestContext(request,{
		'form': form ,
                'word1error': word1error,
                'word2error': word2error,
	        'word3error': word3error,
                'word4error': word4error,
                'correntWordCorrect':correntWordCorrect,
		'user':request.user,
	})
    	return HttpResponse(t.render(c))
