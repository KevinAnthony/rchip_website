from response import JSONResponse
from rchip.models import command_queue,daemon_register,message_register,music_info,remote_devices
from main.models import eps_data,tv_shows,user_tv_shows
from django.contrib.auth.models import User
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
import os,time
from datetime import datetime

@csrf_exempt
def json_get_daemons(request):
	id = get_id(request)
	if id is not None:        
		daemons = daemon_register.objects.all().filter(user=User.objects.get(id=id))
	        return JSONResponse(daemons.values('hostname'))
	else :
		return JSONResponse("Not Authorized")

@csrf_exempt
def json_get_video_path(request):
	id = get_id(request)
        if id is not None:
		host = request.GET['host']
		if host!=None:
			path = daemon_register.objects.all().filter(hostname=host,user=User.objects.get(id=id))
		else:
			path = daemon_register.objects.all()
	        return JSONResponse(path.values('path_to_root'))
	else :
		return JSONResponse("Not Authorized")

@csrf_exempt
def json_send_command(request):
	id = get_id(request)
        if id is not None:
		response = {}
		command_in = request.GET['command']
		command_text_in = request.GET['command_text']
		source_hostname_in = request.GET['source_hostname']
		destination_hostname_in = request.GET['destination_hostname']
		if (command_in != None):
			com_que = command_queue(command=command_in,command_text=command_text_in,source_hostname=source_hostname_in,destination_hostname=destination_hostname_in,user=User.objects.get(id=id))
			com_que.save()
			response['success']=True
		else:
			response['success']=False	
	        return JSONResponse(response)
	else :
		return JSONResponse("Not Authorized")


@csrf_exempt
def json_register_remote_device(request):
	id = get_id(request)
        if id is not None:
		response = {}
	        device_name_in = request.GET['device_name']
	        state_in = request.GET['state'] in ['true','TRUE','True','T','t','1']
		if (device_name_in!=None):
			try:
				rem_dev = remote_devices.objects.get(devices_name=device_name_in)
				rem_dev.active = state_in
				rem_dev.user = User.objects.get(id=id)
			except:
				rem_dev = remote_devices(devices_name=device_name_in,active=state_in,user=User.objects.get(id=id))
			rem_dev.save()
			response['success']=True
	        else:
	                response['success']=False
	        return JSONResponse(response)
	else :
		return JSONResponse("Not Authorized")

@csrf_exempt
def json_get_remote_device(request):
	id = get_id(request)
        if id is not None:
		try:
			return JSONResponse(remote_devices.objects.all().filter(active=True,user=User.objects.get(id=id)).values('devices_name'))
		except:
			return JSONResponse(None)

@csrf_exempt
def json_get_song_info(request):
	id = get_id(request)
        if id is not None:
	        host = request.GET['host']
		if host!=None:
			mus = music_info.objects.all().filter(destination_hostname=host,user=User.objects.get(id=id))
	        	return JSONResponse(mus.values('artist','album','song','elapsed_time','total_time','is_playing'))
		return JSONResponse(None)
	else :
		return JSONResponse("Not Authorized")

@csrf_exempt
def json_set_song_info(request):
	id = get_id(request)
        if id is not None:
		artist = request.GET['artist']
		album = request.GET['album']
		song = request.GET['song']
		e_time = request.GET['elapsed_time']
		t_time = request.GET['total_time']
		is_playing = request.GET['is_playing']
		d_hostname = request.GET['dest_hostname']
		obj, created = music_info.objects.get_or_create(destination_hostname=d_hostname, defaults={'artist':artist,'album':album,'song':song,'elapsed_time':e_time,'total_time':t_time,'is_playing':is_playing})
        	if not created:
			obj.artist = artist
			obj.album = artist
			obj.song = song
			obj.elapsed_time = e_time
			obj.total_time = t_time
			obj.is_playing = is_playing
		obj.user=User.objects.get(id=id)
        	obj.save()	
		return JSONResponse(None)
	else :
		return JSONResponse("Not Authorized")

@csrf_exempt
def json_get_command(request):
	id = get_id(request)
        if id is not None:
	        host = request.GET['host']
		if host!=None:
	                command = command_queue.objects.all().filter(destination_hostname=host,user=User.objects.get(id=id))
			retval = JSONResponse(command.values('command','command_text'))
			command.delete()
			return retval
	        return JSONResponse(None)
	else :
		return JSONResponse("Not Authorized")

@csrf_exempt
def json_show_downloaded(request):
	file_path = request.GET['file_path']
	file_name = os.path.basename(file_path)
	is_anime = request.GET['anime']
	if not is_anime:
		showName = file_name.split('.')[0].replace('_',' ')
		epsNumber = file_name.split('.')[1]
		e = eps_data.objects.get(show=tv_shows.objects.get(name=showName),eps_number=epsNumber)
		e.downloaded = True
		e.uri = file_path
		e.save()
	for host in remote_devices.objects.all().filter(active=True): 
		ticker = "%s %s %s Downloaded|%s|%s" %(showName,epsNumber,e.eps_name,file_path,file_name)
		command_queue(command='TMSEG',command_text=ticker,source_hostname='FILE_SERVER',destination_hostname=host.devices_name,user=User.objects.get(id=host.user_id))	
	return JSONResponse(None)
	
@csrf_exempt
def json_is_valid_show(request):
	show_name = request.GET['show_name']
	response = {}
	try:
		s = tv_shows.objects.get(name=show_name)
		response['valid']=True
	except:
		response['valid']=False
	return JSONResponse(response)	

@csrf_exempt
def json_get_episode_name(request):
	show_name = request.GET['show_name']
	episode = int(request.GET['episode'])
	season = int(request.GET['season'])
	retval = {}
	eps_number = 'S%02dE%02d' %(season,episode)
	try:
		e = eps_data.objects.get(show=tv_shows.objects.get(name=show_name),eps_number=eps_number)
		retval['name']=e.eps_name	
		return JSONResponse(retval)
	except:
		return JSONResponse(None)

@csrf_exempt
def json_get_active_shows(request):
        shows=tv_shows.objects.all().filter(active=1,download=True)
        return JSONResponse(shows.values('id','name','url','last_update','show_type'))

@csrf_exempt
def json_update_last_check(request):
	id = request.GET['id']
	date = time.strptime(request.GET['update_date'],"%Y-%m-%d %H:%M:%S",)
	tv = tv_shows.objects.get(id=id)
	tv.last_checked = date
	tv.save()	
	return JSONResponse(None)

@csrf_exempt
def json_update_last_update(request):
	id = request.GET['id']
	date = request.GET['update_date']
	tv = tv_shows.objects.get(id=id)
	tv.last_update = date
	tv.save()
	return JSONResponse(None)

@csrf_exempt
def json_authenticate(request):
	response = {}
	if request.user.is_authenticated():
		response['success'] = True
		response['Message'] = 'User Already Authenticated'
	else:
		username = request.GET['username']
    		password = request.GET['password']
    		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				response['success'] = True
				response['Message'] = 'User Authenticated'
				request.session['member_id'] = user.id
			else:
				response['success'] = False
                                response['Message'] = 'User Account Disabled'
		else:
			response['success'] = False
                        response['Message'] = 'Invalid Credentials'
	return JSONResponse(response)

@csrf_exempt
def json_deauthenticate(request):
	response = {}
	logout(request)
	response['success'] = True
	return JSONResponse(response)

def json_get_upcoming_shows(request):
	now = datetime.now()
	id=get_id(request)
	if id != None:
		eps_list = eps_data.objects.filter(show__user_tv_shows__user=User.objects.get(id=id),air_date__gte=now)
		return JSONResponse(eps_list.values('show__name','air_date','eps_name','eps_number'))
	else:
		return JSONResponse("Not Authorized")


def get_id(request):
	try:
		return request.session['member_id']
	except:
		return None
