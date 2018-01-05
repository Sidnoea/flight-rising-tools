from bs4 import BeautifulSoup
import requests

def frLogin(username, password):
    '''Logs into Flight Rising and returns a logged-in session.'''

    url = 'https://www1.flightrising.com/login'
    session = requests.session()
    r = session.get(url)
    page = BeautifulSoup(r.text, 'html.parser')
    token = page.find('input', attrs={'name':'_token'}).get('value')
    data = {'uname':username, 'pword':password, 'remember':'0', '_token':token}
    session.post(url, data)
    return session

def frIsUp():
    '''Returns False if Flight Rising seems to be down for maintenance, True otherwise.'''

    try:
        r = requests.get('https://www1.flightrising.com')
        page = BeautifulSoup(r.text, 'html.parser')
        status = page.find('a', attrs={'id':'statusboxcontext'})
        if (status is None) or (status.get('title').count('unavailable') > 0):
            return False
        return True
    except Exception: #no internet, site is completely offline, etc.
        return False
