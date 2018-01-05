from bs4 import BeautifulSoup
import re

def doFamiliars(session, dragonID):
    print('Bonding with familiars...')
    #remove current familiar
    url = 'http://flightrising.com/includes/familiar_active.php'
    data = {'id':dragonID, 'itm':0}
    session.post(url, data)
    #get list of familiar ids
    url = 'http://flightrising.com/main.php?tab=familiar&did={}'.format(dragonID)
    r = session.get(url)
    page = BeautifulSoup(r.text, 'html.parser')
    familiars = page.find('div', attrs={'id':'invwindow'}).find_all('a')
    ids = [re.search('id=(\d+)', familiar.get('rel')[0])[1] for familiar in familiars]
    #bond with each familiar
    for i in range(len(ids)):
        id = ids[i]
        print('\b'*100 + 'Bonding with familiar {}/{}...'.format(i+1, len(ids)), end='', flush=True)
        #attach familiar
        url = 'http://flightrising.com/includes/familiar_active.php'
        data = {'id':dragonID, 'itm':id}
        session.post(url, data)
        #bond with familiar
        url = 'http://flightrising.com/includes/ol/fam_bonding.php'
        data = {'id':id}
        session.post(url, data)
    print('\nDone bonding with familiars.')

def doFeed(session):
    print('Feeding dragons...')
    url = 'http://flightrising.com/includes/ol/feed.php'
    data = {}
    session.post(url, data)
    print('Dragons fed.')

def doGather(session, action, location):
    print('Checking gathering turns...')
    r = session.get('http://flightrising.com/main.php?p=gather')
    page = BeautifulSoup(r.text, 'html.parser')
    turns = int(page.find(string=re.compile('Turns Left Today:')).next_sibling.string.strip())
    if turns > 0:
        action = action.lower()
        location = location.lower()
        participles = {'hunt':'hunting', 'fish':'fishing', 'catch':'catching',
                       'forage':'foraging', 'dig':'digging', 'scavenge':'scavenging'}
        locations = {'earth':1, 'plague':2, 'wind':3, 'water':4, 'lightning':5,
                     'ice':6, 'shadow':7, 'light':8, 'arcane':9, 'nature':10, 'fire':11}
        print('{} gathering turns left today. {} at {}...'.format(turns, participles[action].capitalize(), location.capitalize()))
        url = 'http://flightrising.com/main.php?p=gather&action={}'.format(action)
        data = {'gather':locations[location]}
        for i in range(turns):
            session.post(url, data)
        print('Done gathering.')
    else:
        print('No gathering turns left today.')

def doNests(session):
    print('Checking nests...')
    r = session.get('http://flightrising.com/main.php?tab=hatchery')
    page = BeautifulSoup(r.text, 'html.parser')
    nests = page('input', attrs={'name':'inc'})
    if nests:
        print('Found {} unincubated nests. Incubating...'.format(len(nests)))
        url = 'http://flightrising.com/main.php?tab=hatchery'
        for nest in nests:
            inc = nest.get('value')
            data = {'inc':inc}
            session.post(url, data)
        print('Nests incubated.')
    else:
        print('No unincubated nests found.')

def doPinkerton(session):
    print('Checking Pinkerton...')
    r = session.get('http://www1.flightrising.com/trading/pinkpile')
    page = BeautifulSoup(r.text, 'html.parser')
    disabled = page.find('input', attrs={'value':'Grab an Item'}).get('disabled')
    if disabled:
        print('You have already collected from Pinkerton today.')
    else:
        print('Collecting from Pinkerton...')
        token = page.find('input', attrs={'name':'_token'}).get('value')        
        url = 'http://www1.flightrising.com/trading/pinkpile'
        data = {'_token':token}
        session.post(url, data)
        print('Item collected.')

def doDailies(session, action, location, dragonID):
    doFeed(session)
    doGather(session, action, location)
    doNests(session)
    doPinkerton(session)
    doFamiliars(session, dragonID)

if __name__ == '__main__':
    from getpass import getpass
    from random import choice
    import frlib
    import sys

    action = 'scavenge'
    location = choice(['earth', 'plague', 'wind', 'water', 'lightning', 'ice', 'shadow', 'light', 'arcane', 'nature', 'fire'])
    dragonID = '23352198'
    print('Checking if Flight Rising is up...')
    if frlib.frIsUp():
        print('Logging in...')
        if len(sys.argv) == 3:
            username = sys.argv[1]
            password = sys.argv[2]
            print('Credentials supplied: {}'.format(username))
        else:
            username = input('Username: ')
            password = getpass()
        session = frlib.frLogin(username, password)
        doDailies(session, action, location, dragonID)
    else:
        print('Flight Rising appears to be down.')
