import config
import urllib

IG_BASEURL = "https://api.instagram.com/v1/subscriptions/"

def subscribe_tag(tagname):
    return subscribe(
        'tag',
        'media',
        callback_url=config.base_url+"/ig_tags_cb",
        object_id = tagname
        )

def subscribe_georegion(lat,lng,radius):
    return subscribe(
        'geography',
        'media',
        config.base_url+"/ig_geo_cb",
        lat=lat,
        lng=lng,
        radius=radius
        )

def subscribe(obj, aspect, callback_url, **kwargs):
    params = {
        'client_id': config.instagram_client_id,
        'client_secret': config.instagram_client_secret,
        'object':obj,
        'aspect':aspect,
        'callback_url':callback_url}
    params.update(kwargs)
    params = urllib.urlencode(params)
    f = urllib.urlopen(IG_BASEURL, params)
    return f.read()                            

def list_subscriptions():
    f = urllib.urlopen(
        IG_BASEURL+"?client_secret=%s&client_id=%s"%(
            config.instagram_client_secret,
            config.instagram_client_id))
    return f.read()

