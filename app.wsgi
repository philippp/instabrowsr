#! /usr/bin/env python
import os
import re
import controller
import traceback

ROUTES = [
   ("^\/$",
    controller.Index),
   ("^\/ig_tags_cb[\/]?$",
    controller.InstagramCallback),
   ("^\/ig_geo_cb[\/]?$",
    controller.InstagramCallback),
   ("^\/ig_get_locations[\/]?$",
    controller.GetLocations),
   ("^\/ig_pictures_for_location[\/]?$",
    controller.GetPicForLocation),
   ("^\/location[\/]?$",
    controller.LocationPics),
   ]


def application(environ, start_response):
   # Since our routing catches most expressions, we check for
   # static files first

   for n, c in ROUTES:
      if re.match(n, environ['PATH_INFO']):
         try:
            resp = c().handle(environ)
            start_response(
               "200 OK",
               [('content-type',majick_filename(environ['PATH_INFO'])),
                ('content-length',str(len(resp)))])

         except Exception, e:
            traceback.print_exc()
            resp = "Oh snaps, I messed up. SOWEE."
            start_response("500 SERVER ERROR",
                           [('content-type','text/html'),
                            ('content-length',str(len(resp)))])
         return [resp]

   # If that fails, look for a file at this location
   fpath = '/var/www/hiptownshowdown/static' + environ['PATH_INFO']
   if os.path.isfile(fpath):
      mime = majick_filename(fpath)
      resp = file(fpath, 'r').read()
      start_response("200 OK",
                     [('content-type',mime),
                      ('content-length',str(len(resp)))])
      return [resp]


   e_msg = "nothing to see here"
   start_response("404 NOT FOUND",
                  [('content-type','text/html'),
                   ('content-length',str(len(e_msg)))])
   return [e_msg]


def majick_filename(filename):
   ext = filename.split(".")[-1]
   if ext == "css":
      return "text/css"
   if ext == "js":
      return "text/javascript"
   if ext == "html":
      return "text/html"
   return "text"
