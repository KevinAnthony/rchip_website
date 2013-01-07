from response import JSONResponse
from rchip.models import command_queue,daemon_register,message_register,music_info,remote_devices
from schedule.models import episode_data,tv_shows,user_tv_shows
from django.contrib.auth.models import User
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseNotModified,HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
import os,time
from datetime import datetime,timedelta
import logging

@csrf_exempt
def json_get_daemons(request):
    id = get_id(request)
    if id is not None:
        daemons = daemon_register.objects.all().filter(user__id=id)
        return JSONResponse(daemons.values('hostname'),Extra={"success":True})
    else :
        return HttpResponseForbidden()

@csrf_exempt
def json_get_video_path(request):
    id = get_id(request)
    if id is not None:
        host = request.GET['host']
        if host!=None:
            path = daemon_register.objects.all().filter(hostname=host,user__id=id)
        else:
            path = daemon_register.objects.all()
        return JSONResponse(path.values('path_to_root'),Extra={"success":True})
    else :
        return HttpResponseForbidden()

@csrf_exempt
def json_register_daemon(request):
    id = get_id(request)
    if id is not None:
        response = {}
        hostname_in = request.GET['hostname']
        video_path = request.GET['video_path']
        if (hostname_in!=None):
            try:
                daemon = daemon_register.objects.get(hostname=hostname_in)
                daemon.path_to_root=video_path
                daemon.user = User.objects.get(id=id)
            except:
                new_user = User.objects.get(id=id)
                daemon = daemon_register(hostname=hostname_in,path_to_root=video_path,user__id=new_user)
            daemon.save()
            response['success']=True
        else:
            response['success']=False
        return JSONResponse(response,Extra={"success":True})
    else:
        return HttpResponseForbidden()

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
            new_user = User.objects.get(id=id)
            com_que = command_queue(command=command_in,command_text=command_text_in,source_hostname=source_hostname_in,destination_hostname=destination_hostname_in,user=new_user)
            com_que.save()
            response['success']=True
        else:
            response['success']=False
        return JSONResponse(response,Extra={"success":True})
    else:
        return HttpResponseForbidden()


@csrf_exempt
def json_register_remote_device(request):
    id = get_id(request)
    if id is not None:
        response = {}
        device_name_in = request.GET['device_name']
        state_in = request.GET['state'] in ['true','TRUE','True','T','t','1']
        if (device_name_in!=None):
            new_user = User.objects.get(id=id)
            try:
                rem_dev = remote_devices.objects.get(devices_name=device_name_in)
                rem_dev.active = state_in
                rem_dev.user = new_user
            except:
                rem_dev = remote_devices(devices_name=device_name_in,active=state_in,user=new_user)
            rem_dev.save()
            response['success']=True
        else:
            response['success']=False
        return JSONResponse(response,Extra={"success":True})
    else :
        return HttpResponseForbidden()

@csrf_exempt
def json_get_remote_device(request):
    id = get_id(request)
    if id is not None:
        try:
            return JSONResponse(remote_devices.objects.all().filter(active=True,user__id=id).values('devices_name'),Extra={"success":True})
        except:
            return JSONResponse(None)

@csrf_exempt
def json_get_song_info(request):
    id = get_id(request)
    if id is not None:
        host = request.GET['host']
        if host!=None:
            mus = music_info.objects.all().filter(destination_hostname=host,user__id=id)
            return JSONResponse(mus.values('artist','album','song','total_time','is_playing'),Extra={"success":True})
        return JSONResponse(Extra={"success":False})
    else :
        return HttpResponseForbidden()

@csrf_exempt
def json_set_song_info(request):
    id = get_id(request)
    if id is not None:
        artist = request.GET['artist']
        album = request.GET['album']
        song = request.GET['song']
        t_time = request.GET['total_time']
        is_playing = True if request.GET['is_playing'] == 1 else False
        d_hostname = request.GET['dest_hostname']
        new_user = User.objects.get(id=id)
        obj, created = music_info.objects.get_or_create(destination_hostname=d_hostname, defaults={'artist':artist,'album':album,'song':song,'total_time':t_time,'is_playing':is_playing},user=new_user)
        if not created:
            obj.artist = artist
            obj.album = artist
            obj.song = song
            obj.total_time = t_time
            obj.is_playing = is_playing
        obj.user=User.objects.get(id=id)
        obj.save()
        return JSONResponse(None,Extra={"success":True})
    else :
        return nHttpResponseForbidden()

@csrf_exempt
def json_get_command(request):
    id = get_id(request)
    if id is not None:
        host = request.GET['host']
        if host!=None:
            command = command_queue.objects.all().filter(destination_hostname=host,user__id=id)
            if not command.count():
                return HttpResponseNotModified()
            retval = JSONResponse(command.values('command','command_text'),Extra={"success":True})
            command.delete()
            return retval
        return JSONResponse(None,Extra={"success":True})
    else :
        return HttpResponseForbidden()

@csrf_exempt
def json_show_downloaded(request):
    file_path = request.GET['file_path']
    file_name = os.path.basename(file_path)
    is_anime = request.GET['anime'] == 'True'
    if not is_anime:
        showName = file_name.split('.')[0].replace('_',' ')
        epsNumber = file_name.split('.')[1]
        e = episode_data.objects.get(show=tv_shows.objects.get(name=showName),eps_number=epsNumber)
        e.downloaded = True
        e.uri = file_path
        e.save()
        ticker = "%s %s %s Downloaded|%s|%s" %(showName,epsNumber,e.eps_name,file_path,file_name)
    else:
        ticker = "%s Downloaded|%s|%s" %(file_name,file_path,file_name)
    #TODO: Here we need to only get remote devices in which show_view is checled
    for host in remote_devices.objects.all().filter(active=True):
        new_user = User.objects.get(id=host.user_id)
        cmd = command_queue(command='TMSG',command_text=ticker,source_hostname='FILE_SERVER',destination_hostname=host.devices_name,user=new_user)
        cmd.save()
    return JSONResponse(None,Extra={"success":True})

@csrf_exempt
def json_is_valid_show(request):
    show_name = request.GET['show_name']
    response = {}
    try:
        s = tv_shows.objects.get(name=show_name)
        response['valid']=True
    except:
        response['valid']=False
    return JSONResponse(response,Extra={"success":True})

@csrf_exempt
def json_get_nonstd_regex(request):
    show_name = request.GET['show_name']
    response = {}
    s = tv_shows.objects.get(name=show_name)
    response['regex']=s.nonstandard_name_regex
    return JSONResponse(response,Extra={"success":True})

@csrf_exempt
def json_get_episode_name(request):
    show_name = request.GET['show_name']
    episode = int(request.GET['episode'])
    season = int(request.GET['season'])
    retval = {}
    eps_number = 'S%02dE%02d' %(season,episode)
    try:
        e = episode_data.objects.get(show__name=show_name,eps_number=eps_number)
        retval['name']=e.eps_name
        retval['type']=e.show.show_type
        return JSONResponse(retval,Extra={"success":True})
    except:
        return JSONResponse(None)

@csrf_exempt
def json_get_active_shows(request):
    shows=tv_shows.objects.all().filter(active=1,download=True)
    return JSONResponse(shows.values('id','name','url','last_update','show_type'),Extra = {"success":True})

@csrf_exempt
def json_update_last_check(request):
    id = request.GET['id']
    date = time.strptime(request.GET['update_date'],"%Y-%m-%d %H:%M:%S",)
    tv = tv_shows.objects.get(id=id)
    tv.last_checked = date
    tv.save()
    return JSONResponse(None,Extra={"success":True})

@csrf_exempt
def json_update_last_update(request):
    id = request.GET['id']
    date = request.GET['update_date']
    tv = tv_shows.objects.get(id=id)
    tv.last_update = date
    tv.save()
    return JSONResponse(None,Extra={"success":True})

@csrf_exempt
def json_authenticate(request):
    response = {}
    if request.user.is_authenticated():
        response['success'] = True
        response['message'] = 'User Already Authenticated'
    else:
        username = request.GET['username']
        password = request.GET['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                response['success'] = True
                response['message'] = 'User Authenticated'
                request.session['member_id'] = user.id
            else:
                response['success'] = False
                response['message'] = 'User Account Disabled'
        else:
            response['success'] = False
            response['message'] = 'Invalid Credentials'
    return JSONResponse(None,Extra=response)

@csrf_exempt
def json_deauthenticate(request):
    response = {}
    logout(request)
    response['success'] = True
    return JSONResponse(None,Extra=response)

@csrf_exempt
def json_check_authentication(request):
    return JSONResponse({"authenticated":request.user.is_authenticated()},Extra={"success":True})

def json_get_upcoming_shows(request):
    now = datetime.now()
    id=get_id(request)
    if id != None:
        eps_list = episode_data.objects.filter(show__user_tv_shows__user__id=id,air_date__gte=now)
        return JSONResponse(eps_list.values('show__name','air_date','eps_name','eps_number','show__air_time'),Extra={"success":True})
    else:
        return HttpResponseForbidden()

@csrf_exempt
def json_delete_show(request):
    id = (get_id(request))
    if id != None:
        cmd_string = "%s|%s|%s" % (request.GET['show_name'],request.GET['episode_name'],request.GET['episode_number'])
        from_device = request.GET['device_name']
        devices = remote_devices.objects.all().filter(active=True,user__id=id)
        new_user = User.objects.get(id=id)
        for device in devices:
            if from_device != device.devices_name:
                com_que = command_queue(command="DELS",command_text=cmd_string,source_hostname=from_device,destination_hostname=device.devices_name,user=new_user)
                com_que.save()
        return JSONResponse(None,Extra={"success":True})
    else:
        return HttpResponseForbidden()

def get_id(request):
    try:
        return request.session['member_id']
    except:
        return None
