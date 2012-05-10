from utils import serialize_to_json
from django.http import HttpResponseForbidden, HttpResponse
import json
class JSONResponse(HttpResponse):
    """ JSON response class """
    def __init__(self,content='',json_opts={},Extra={},mimetype="application/json",*args,**kwargs):
        """
        This returns a object that we send as json content using
        utils.serialize_to_json, that is a wrapper to simplejson.dumps
        method using a custom class to handle models and querysets. Put your
        options to serialize_to_json in json_opts, other options are used by
        response.
        """
        if content:
            content = serialize_to_json(content,**json_opts)
        else:
            content = serialize_to_json([],**json_opts)
        content = self.insertExtras(content,Extra)
        super(JSONResponse,self).__init__(content,mimetype,*args,**kwargs)

    def insertExtras(self,content,extra):
        extra['data'] = json.loads(content)
        return json.dumps(extra)
