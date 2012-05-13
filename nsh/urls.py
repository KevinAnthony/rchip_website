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

    url(r'^$','schedule.views.schedule_index'),
    url(r'^schedule/$','schedule.views.schedule_index'),
    url(r'^schedule/update/$','schedule.views.schedule_update'),
    url(r'^schedule/tvshows/$','schedule.views.schedule_config_tv_shows'),
    url(r'^schedule/addshow/$','schedule.views.schedule_add_tv_show'),

    url(r'^json/getdaemons/','rchip.views.json_get_daemons'),
    url(r'^json/registerdaemon/','rchip.views.json_register_daemon'),
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
    url(r'^json/authenticate/','rchip.views.json_authenticate'),
    url(r'^json/deauthenticate/','rchip.views.json_deauthenticate'),
    url(r'^json/getupcomingshows/','rchip.views.json_get_upcoming_shows'),

    url(r'^accounts/login/$','django.contrib.auth.views.login', {'template_name': 'templates/login.html', }),
    url(r'^accounts/logout/$', 'schedule.views.logout_view'),
    url(r'^accounts/register/$', 'schedule.views.register'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
         url(r'^admin/', include(admin.site.urls)),
)
