import time
import async
import config
import urllib
import pprint
import json

LOCS = {'dolores_park':('37.7593835169', '-122.4271774291')}

IG_BASEURL = "https://api.instagram.com/v1/"

def objs_by_geography(geographies, count=10):
    return get_objs(geographies, 'geographies', count=count)

def get_objs_by_tag(tags, count=10):
    return get_objs(tags, 'tags', count=count)

def get_objs_by_location(locations, count=10):
    objs = get_objs(locations,'locations', count=count)
    for v in objs.values():
        for d in v.get('data',[]):
            d['created_time_str'] = time_ago_str(
                d['created_time'])
    return objs

def time_ago_str(raw_t):
    cur_ts = int(time.time())
    secs_ago = cur_ts - int(raw_t)
    mins_ago = secs_ago / 60
    secs_ago = secs_ago - 60*mins_ago
    hours_ago = mins_ago / 60
    mins_ago = mins_ago - 60*hours_ago
    days_ago = hours_ago / 24
    hours_ago = hours_ago - 24*days_ago
    weeks_ago = days_ago / 7
    days_ago = days_ago - 7*weeks_ago


    _s = ""
    if weeks_ago:
        _s += ("%s week" % weeks_ago) + (weeks_ago > 1 and "s " or " ")
    if days_ago:
        _s += ("%s day" % days_ago) + (days_ago > 1 and "s " or " ")
        if weeks_ago:
            return _s+" ago"
    if hours_ago:
        _s += ("%s hour" % hours_ago) + (hours_ago > 1 and "s " or " ")
        if days_ago or weeks_ago:
            return _s+" ago"
    if mins_ago:
        _s += ("%s minute" % mins_ago) + (mins_ago > 1 and "s " or " ")
        if hours_ago or days_ago or weeks_ago:
            return _s+" ago"
    if secs_ago:
        _s += ("%s second" % secs_ago) + (secs_ago > 1 and "s " or " ")
    _s = _s and _s+" ago" or "just now"
    return _s


def list_locations_by_geo(lat, lng, radius):
    path = IG_BASEURL+"locations/search"
    params = {
        'client_id': config.instagram_client_id,
        'lat': lat,
        'distance':radius,
        'lng': lng}
    params = urllib.urlencode(params)
    req_url = path+"?"+params
    loader = async.Dnld()
    to_ret = {}
    url, data = loader.download_urls(req_url)[0]
    return json.loads(data)

def get_objs(obj_ids, obj_type, count=10):
    if not isinstance(obj_ids, (list, tuple)):
        obj_ids = [obj_ids]

    req_urls = []
    for obj_id in obj_ids:
        path = IG_BASEURL+obj_type+"/"+obj_id+"/media/recent"
        params = {
            'client_id': config.instagram_client_id,
            'count': count }
        params = urllib.urlencode(params)
        req_urls.append(path+"?"+params)
        
    loader = async.Dnld()
    to_ret = {}
    for url, data in loader.download_urls(req_urls):
        key="uhoh"
        for obj_id in obj_ids:
            if obj_type+"/"+obj_id in url:
                key = obj_id
        try:
            to_ret[key] = json.loads(data) or {'data':[]}
        except ValueError:
            to_ret[key] = {'data':[]}
    return to_ret
