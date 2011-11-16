from django.utils import simplejson
from django.utils.encoding import force_unicode
from django.db.models.base import ModelBase
 
class LazyJSONEncoder(simplejson.JSONEncoder):
	def default(self,o):
		try:
            		iterable = iter(o)
        	except TypeError:
            		pass
        	else:
            		return list(iterable)
        	try:
            		isinstance(o.__class__,ModelBase)
        	except Exception:
            		pass
        	else:
            		return force_unicode(o)
        	return super(LazyJSONEncoder,self).default(obj)
 
def serialize_to_json(obj,*args,**kwargs):
    	kwargs['ensure_ascii'] = kwargs.get('ensure_ascii',False)
    	kwargs['cls'] = kwargs.get('cls',LazyJSONEncoder)
    	return simplejson.dumps(obj,*args,**kwargs)
