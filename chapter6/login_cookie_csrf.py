import urllib, urllib2

LOGIN_URL = 'http://example.webscraping.com/places/default/user/login'
LOGIN_EMAIL = 'example@webscraping.com'
LOGIN_PASSWORD = 'example'

def parse_form(html):
    import lxml.html
    tree = lxml.html.fromstring(html)
    data = {}
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')] = e.get('value')
    return data


def build_cookie():
    import cookielib
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    return opener


def test_parse_form():
    import pprint
    html = urllib2.urlopen(LOGIN_URL).read()
    form = parse_form(html)
    pprint.pprint(form)


def test_login_success():
    # html = urllib2.urlopen(LOGIN_URL).read()
    opener = build_cookie()
    html = opener.open(LOGIN_URL).read()
    data = parse_form(html)

    data['email'] = LOGIN_EMAIL
    data['password'] = LOGIN_PASSWORD
    encoded_data = urllib.urlencode(data)

    request = urllib2.Request(LOGIN_URL, encoded_data)
    response = opener.open(request)

    # print(response.geturl())
    if response.geturl() == LOGIN_URL:
        print "Login Failed"
    else:
        print "Login Success"


if __name__ == "__main__":
    test_login_success()
    # test_parse_form()
