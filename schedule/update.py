from datetime import datetime, timedelta
import zipfile,urllib,os
from xml.dom.minidom import parseString
from schedule.models import episode_data,tv_shows
from pytz import timezone
import logging
from django.conf import settings

class updateEpsList():
    def __init__(self):
        self.showList = tv_shows.objects.filter(active=True)
        self.apikey = '28CDD1E77B852D89'
        self.baseurl = 'http://www.thetvdb.com/api/%s/series'%(self.apikey)
    	self.logger = logging.getLogger(__name__)

    def update(self):
        tz = timezone('UTC')
        for list in self.showList:
            seriesID = list.thetvdb_id
            showName = list.name
            air_time = list.air_time
            if air_time == None:
                air_time = 0
            if not seriesID > 0:
                continue
            url = "%s/%s/all/en.zip" % (self.baseurl,seriesID)
            logging.debug("Processing files for show: %s" %(showName))
            logging.debug("With Url:%s" %(url))
            xmldom = self.processFile(url)
            print xmldom
            if xmldom == None:
                continue
            episode_data.objects.filter(show_id=tv_shows.objects.filter(name=showName),uri="").delete()
            for e in xmldom.getElementsByTagName("Episode"):
                try:
                    epsName = e.getElementsByTagName("EpisodeName")[0].childNodes[0].nodeValue
                except:
                    epsName = "Unknown"
                try:
                    epsNumber = e.getElementsByTagName("EpisodeNumber")[0].childNodes[0].nodeValue
                except:
                    epsNumber = "0"
                try:
                    seasonNumber =  e.getElementsByTagName("SeasonNumber")[0].childNodes[0].nodeValue
                except:
                    seasonNumber = "0"
                try:
                    date = datetime.strptime(e.getElementsByTagName("FirstAired")[0].childNodes[0].nodeValue, '%Y-%m-%d')
                except:
                    date = datetime.strptime("1970-01-01",'%Y-%m-%d')
                date = date.replace(tzinfo=tz,hour = 0)
                epsString = "S%02dE%02d"%(int(seasonNumber) if seasonNumber.isdigit() else 0,int(epsNumber) if epsNumber.isdigit() else 0)
                obj, created = episode_data.objects.get_or_create(show = tv_shows.objects.get(name=showName), eps_number = epsString, defaults={'air_date':date,'eps_name':epsName})
                if not created:
                    obj.show = tv_shows.objects.get(name=showName)
                    obj.eps_number = epsString
                    obj.air_date = date
                    obj.eps_name = epsName
                    obj.save()
                else:
                    obj.save()
        shows = tv_shows.objects.filter(active=1,show_type='tvshow')
        for show in shows:
            eps = episode_data.objects.filter(show=show,air_date__gte=datetime.now(tz)-timedelta(30))
            if len(eps) == 0:
                show.active=0
                show.save()
            shows = tv_shows.objects.filter(active=0,show_type='tvshow')
            for show in shows:
                eps = episode_data.objects.filter(show=show,air_date__gte=datetime.now(tz)-timedelta(30))
                if len(eps) <> 0:
                    show.active=1
                show.last_update=datetime.now(tz)
                show.save()

    def processFile(self,url):
        #try:
            file_uri = '/home/gigaroc/webapps/django/rchip_website/schedule/en.zip'
            urllib.urlretrieve(url,file_uri)
            file = zipfile.ZipFile(file_uri, "r")
            for name in file.namelist():
                if name == 'en.xml':
                    data = file.read(name)
                    xml = parseString(data)
                    break
                else:
                    logging.debug("No en.xml file")
            os.unlink(file_uri)
            return xml
        #except Exception as e:
        #    logging.warning("Problem with process file")
        #    logging.warning("{0} : {1}".format(e.errno,e.strerror))
        #    return None

if __name__ == "__main__":
    up = updateEpsList()
    up.update()
