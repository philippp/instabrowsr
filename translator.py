import cgi

def translator(*args, **kwargs):
    def reqHandler(fn):
        def reqStripper(self, env):
            import pprint; pprint.pprint(env)
            c_parms = {}
            if env.get('REQUEST_METHOD') == "GET":
                q_parms = cgi.parse_qs(env.get('QUERY_STRING'))
                print q_parms
                c_parms = translate_qs(q_parms, kwargs)
            elif env.get('REQUEST_METHOD') == "POST":
                try:
                    req_len = int(env.get('CONTENT_LENGTH', 0))
                except (ValueError):
                    req_len = 0
                req_body = env['wsgi.input'].read(req_len)
                q_parms = cgi.parse_qs(req_body)
                c_parms = translate_qs(q_parms, kwargs)
            return fn(self, **c_parms)

        reqStripper.func_name = fn.func_name
        return reqStripper
    return reqHandler


def translate_qs(qparms, qtypes):
    convparms = {}
    for pname, pvarr in qparms.iteritems():
        t_test = lambda t: qtypes.get(pname) == t
        if not qtypes.get(pname):
            continue
        if t_test(str):
            convparms[pname] = pvarr and str(pvarr[0]) or ""
        elif t_test(int):
            convparms[pname] = pvarr and int(pvarr[0]) or ""
        else:
            convparms[pname] = qtypes.get(pname)
        
    return convparms
