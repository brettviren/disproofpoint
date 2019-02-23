#!/usr/bin/env python3

import re
import urllib.parse

re_mang = re.compile(r'https://urldefense.proofpoint.com/(v[0-9])/')
re_v1 = re.compile(r'u=(.+?)&k=')
re_v2 = re.compile(r'u=(.+?)&[dc]=')

def match_mangling(text):
    match = re_mang.search(text)
    if not match:
        return None
    ver = match.group(1)
    if ver in ["v1", "v2"]:
        return ver
    return None

def demangle_url_v1(url):
    return urllib.parse.unquote(url)

def demangle_url_v2(url):
    trans = str.maketrans('-_', '%/')
    return demangle_url_v1(url.translate(trans))

demangle_regsubs = [
    (re_v1, demangle_url_v1),
    (re_v2, demangle_url_v2),
]
def demangle_url(url):
    for reg, sub in demangle_regsubs:
        m = reg.search(url)
        if not m:
            continue
        return sub(m)
    return url

def resub(demangler):
    def doit(mo):
        url = mo.string[mo.start():mo.end()]
        ret = demangler(url)
        if ret:
            return ret
        return url
    return doit

mre_v1 = re.compile(r'https://urldefense.proofpoint.com/(v[0-9])/url\?u=(.+?)&k=')
mre_v2 = re.compile(r'https://urldefense.proofpoint.com/(v[0-9])/url\?u=(.+?)&([dcrms]=.*)&e=')
mdm_vers = dict(
    v1 = demangle_url_v1,
    v2 = demangle_url_v2,
)

def demangle_match(mo):
    v = mo.group(1)
    ret = mdm_vers[v](mo.group(2))
    #print (mo.groups(), ret)
    #spy = mo.group(3)
    #print (ret, spy.split('&'))
    return ret

def demangle_text(mangled_text):
    text,count = mre_v2.subn(demangle_match, mangled_text)
    if count > 0:
        return text
    return mangled_text

if '__main__' == __name__:
    import sys
    import email
    msg = email.message_from_file(open(sys.argv[1]))
    text = demangle_text(msg.get_payload(decode=True).decode('utf-8'))
    msg.set_payload(text)
    try:
        fname = sys.argv[2]
        open(fname,'w').write(msg.as_string())
    except IndexError:
        print (msg.as_string())
        
    
