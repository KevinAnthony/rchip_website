from response import JSONResponse
from rchip.models import command_queue,daemon_register,message_register,music_info,remote_devices
from main.models import eps_data,tv_shows
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
import os

@csrf_exempt
def json_get_daemons(request):
        daemons = daemon_register.objects.all()
        return JSONResponse(daemons.values('hostname'))

@csrf_exempt
def json_get_video_path(request):
	host = request.GET['host']
	if host!=None:
		path = daemon_register.objects.all().filter(hostname=host)
	else:
		path = daemon_register.objects.all()
        return JSONResponse(path.values('path_to_root'))

@csrf_exempt
def json_send_command(request):
	response = {}
	command_in = request.GET['command']
	command_text_in = request.GET['command_text']
	source_hostname_in = request.GET['source_hostname']
	destination_hostname_in = request.GET['destination_hostname']
	if (command_in != None):
		com_que = command_queue(command=command_in,command_text=command_text_in,source_hostname=source_hostname_in,destination_hostname=destination_hostname_in)
		com_que.save()
		response['success']=True
	else:
		response['success']=False	
        return JSONResponse(response)

@csrf_exempt
def json_register_remote_device(request):
	response = {}
        device_name_in = request.GET['device_name']
        state_in = request.GET['state'] in ['true','TRUE','True','T','t','1']
	if (device_name_in!=None):
		try:
			rem_dev = remote_devices.objects.get(devices_name=device_name_in)
			rem_dev.active = state_in
		except:
			rem_dev = remote_devices(devices_name=device_name_in,active=state_in)
		rem_dev.save()
		response['success']=True
        else:
                response['success']=False
        return JSONResponse(response)

@csrf_exempt
def json_get_remote_device(request):
	return JSONResponse(remote_devices.objects.all().filter(active=True).values('devices_name'))

@csrf_exempt
def json_get_song_info(request):
        host = request.GET['host']
	if host!=None:
		mus = music_info.objects.all().filter(destination_hostname=host)
        	return JSONResponse(mus.values('artist','album','song','elapsed_time','total_time','is_playing'))
	return JSONResponse(None)

@csrf_exempt
def json_set_song_info(request):
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
        obj.save()	
	return JSONResponse(None)

@csrf_exempt
def json_get_command(request):
        host = request.GET['host']
	if host!=None:
                command = command_queue.objects.all().filter(destination_hostname=host)
		retval = JSONResponse(command.values('command','command_text'))
		command.delete()
		return retval
        return JSONResponse(None)

@csrf_exempt
def json_show_exists(request):
	show = request.GET['show_name']
	#check database if show exists, return true/false
	return JSONResponse(None)		

@csrf_exempt
def json_episode_name(request):
        show = request.GET['show_name']
	eps_name = request.GET['episode_number']
	return JSONResponse(None)

@csrf_exempt
def json_show_downloaded(request):
	file_path = request.GET['file_path']
	file_name = os.path.basename(file_path)
	showName = file_name.split('.')[0].replace('_',' ')
	epsNumber = file_name.split('.')[1]
	e = eps_data.objects.get(show=tv_shows.objects.get(name=showName),eps_number=epsNumber)
	e.downloaded = True
	e.uri = file_path
	e.save()
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
