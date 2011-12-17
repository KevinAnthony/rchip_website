from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'nsh_website.views.home', name='home'),
     	url(r'^weight/$','weight.views.index'),
	url(r'^weight/add/$','weight.views.add'),

	url(r'^hack/$','hack.views.index'),
	url(r'^$','main.views.index'),
	url(r'^main/$','main.views.index'),
	url(r'^main/update/$','main.views.update'),

	url(r'^json/getdaemons/','rchip.views.json_get_daemons'),
	url(r'^json/getvideopath/','rchip.views.json_get_video_path'),
	url(r'^json/sendcommand/','rchip.views.json_send_command'),
	url(r'^json/registerremotedevice/','rchip.views.json_register_remote_device'),
	url(r'^json/getremotedevice/','rchip.views.json_get_remote_device'),
	url(r'^json/getsonginfo/','rchip.views.json_get_song_info'),
	url(r'^json/setsonginfo/','rchip.views.json_set_song_info'),
	url(r'^json/getcommand/','rchip.views.json_get_command'),
	url(r'^json/showdownloaded/','rchip.views.json_show_downloaded'),
	url(r'^json/isvalidshow/','rchip.views.json_is_valid_show'),
	url(r'^json/getepisodename/','rchip.views.json_get_episode_name'),
	url(r'^json/getactiveshows/','rchip.views.json_get_active_shows'),
	url(r'^json/updatelastcheck/','rchip.views.json_update_last_check'),
	url(r'^json/updatelastupdate/','rchip.views.json_update_last_update'),
	
	url(r'^accounts/login/$','django.contrib.auth.views.login', {'template_name': 'main/login.html', }),
	url(r'^accounts/logout/$', 'main.views.logout_view'),
	url(r'^accounts/register/$', 'main.views.register'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     	url(r'^admin/', include(admin.site.urls)),
)
