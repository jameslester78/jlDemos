def unescape(s):
    #the requests.get function will escape certain chars
    #so this will just reverse that
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    s = s.replace("&amp;", "&")
    return s