import pprint
import translator
import ig_query
import json

class Controller(object):
    def handle(self):
        pass

class Index(Controller):
    @translator.translator()
    def handle(self):
        return "hiptownshowdown"

class LocationPics(Controller):
    @translator.translator(
        location=str,
        count=int,
        )
    def handle(self, location='', count=10):
        objs = ig_query.get_objs_by_location(
            location,
            count=count)
        img_urls = []
        for res in objs[location].get('data',[]):
            img_urls.append(
                res['images']['standard_resolution']['url'])
        img_html = str("".join(
            ["<img src='%s'/><br/>"%i for i in img_urls]))
        return "<html><head></head><body>"+img_html+"</body></html>"

class GetPicForLocation(Controller):
    @translator.translator(
        location=str,
        count=int,
        )
    def handle(self, location='', count=10):
        objs = ig_query.get_objs_by_location(
            location,
            count=count)
        return json.dumps({'data':objs[location].get('data',[])})


class GetLocations(Controller):
    @translator.translator(
        lat=str,
        lng=str,
        )
    def handle(self, lat='', lng=''):
        data = ig_query.list_locations_by_geo(
            lat, lng, 5000);
        return json.dumps(data)

class InstagramCallback(Controller):    
    @translator.translator(
        **{'hub.mode':str,
           'hub.challenge':str,
           'hub.verify':str}
          )
    def handle(
        self,
        *args,
        **kwargs):
        return kwargs.get('hub.challenge','')
