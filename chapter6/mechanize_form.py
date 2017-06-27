import mechanize

LOGIN_URL = 'http://example.webscraping.com/places/default/user/login'
LOGIN_EMAIL = 'example@webscraping.com'
LOGIN_PASSWORD = 'example'
COUNTRY_EDIT_URL = "http://example.webscraping.com/places/default/edit/Afghanistan-1"



def test_mechanize_login():
    br = mechanize.Browser()
    br.open(LOGIN_URL)
    br.select_form(nr=0)
    br['email'] = LOGIN_EMAIL
    br['password'] = LOGIN_PASSWORD
    response = br.submit()
    br.open(COUNTRY_EDIT_URL)
    br.select_form(nr=0)
    print("Before: {}".format(br['population']))
    br['population'] = str(int(br['population']) + 1)
    br.submit()

    br.open(COUNTRY_EDIT_URL)
    br.select_form(nr=0)
    print("After: {}".format(br['population']))

if __name__ == "__main__":
    test_mechanize_login()
