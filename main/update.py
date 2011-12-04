from datetime import datetime, timedelta
import zipfile,urllib,os
from xml.dom.minidom import parseString
from main.models import eps_data,tv_shows

class updateEpsList():
	def __init__(self):
		self.showList = tv_shows.objects.filter(show_type='tvshow')
		self.apikey = '28CDD1E77B852D89'
		self.baseurl = 'http://www.thetvdb.com/api/%s/series'%(self.apikey)
		self.init_logging()
		self.logger.warning("GOT HERE\n")

	def update(self):
		self.logger.error("Got Here\n")
		for list in self.showList:
			seriesID = list.thetvdb_id
			showName = list.name
			air_time = list.air_time
			self.logger.info("Uploading show: %s" %(showName))
			if air_time == None:
				air_time = 0
			url = "%s/%s/all/en.zip" % (self.baseurl,seriesID)
			self.logger.debug("URL: %s"%(url))
			xmldom = self.processFile(url)
			if xmldom == None:
				self.logger.warning("No File for show %s" %(showName))
				continue
			eps_data.objects.filter(show_id=tv_shows.objects.filter(name=showName),uri="").delete()
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
				date = date + timedelta(hours = air_time/100, minutes = air_time%100)
				epsString = "S%02dE%02d"%(int(seasonNumber) if seasonNumber.isdigit() else 0,int(epsNumber) if epsNumber.isdigit() else 0)
				obj, created = eps_data.objects.get_or_create(show = tv_shows.objects.get(name=showName), eps_number = epsString, defaults={'air_date':date,'eps_name':epsName})
				if not created:
					self.logger.debug("Created object %s"%(showName))
					obj.show = tv_shows.objects.get(name=showName)
					obj.eps_number = epsString
					obj.air_date = date
					obj.eps_name = epsName
					obj.save()
				else:
					obj.save()
		shows = tv_shows.objects.filter(active=1,show_type='tvshow')
		for show in shows:
			eps = eps_data.objects.filter(show=show,air_date__gte=datetime.now()-timedelta(30))
			if len(eps) == 0:
				show.active=0
				show.save()
		shows = tv_shows.objects.filter(active=0,show_type='tvshow')
                for show in shows:
                        eps = eps_data.objects.filter(show=show,air_date__gte=datetime.now()-timedelta(30))
                        if len(eps) <> 0:
                                show.active=1
				show.last_update=datetime.now()
                                show.save()


	def processFile(self,url):
		try
			urllib.urlretrieve(url,"/var/www/nsh/en.zip")
			file = zipfile.ZipFile("/var/www/nsh/en.zip", "r")
			for name in file.namelist():
				if name == 'en.xml':
					data = file.read(name)
					xml = parseString(data)
			os.unlink("/var/www/nsh/en.zip")	
			return xml
		except (Exception e):
			logging.error(e)	
			return None

	def init_logging(self):
		import logging
		self.logger = logging.getLogger('nsh_update')
		hdlr = logging.FileHandler('/var/www/upload.log')
		formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
		hdlr.setFormatter(formatter)
		self.logger.addHandler(hdlr) 
		self.logger.setLevel(logging.WARNING)

if __name__ == "__main__":
	up = updateEpsList()
	up.update()
