from bs4 import BeautifulSoup
from getpass import getpass
import frlib

username = input('Username: ')
password = getpass()
session = frlib.frLogin(username, password)

url = 'http://www1.flightrising.com/msgs/generic-item-page'
data = {'tab':'app', 'filter':'transmutable'}
r = session.post(url, data)
apparelRaw = BeautifulSoup(r.text, 'html.parser')
##apparel = {app['data-itemid']:[app['data-name'], None] for app in apparelRaw('a')}

apparel = {}
for app in apparelRaw('a'):
    name = app['data-name']
    id = app['data-itemid']
    if id not in apparel:
        url = 'https://www1.flightrising.com/auction-house/buy/realm/app?itemname={}&currency=0'.format(name.replace(' ', '+'))
        r = session.get(url)
        page = BeautifulSoup(r.text, 'html.parser')
        listing = page.find(attrs={'class':'ah-listing-row'})
        if listing is None:
            print('{} ({}): no listings found'.format(name, id))
            apparel[id] = [name, id, 0]
        else:
            listingName = listing.find(attrs={'class':'ah-listing-itemname'}).string.strip()
            listingCost = int(listing.find(attrs={'class':'ah-listing-cost'}).string)
            apparel[id] = [listingName, id, listingCost]
            print('{} ({}): {}'.format(*apparel[id]))
apparel = sorted(apparel.values(), key=lambda x:x[2])
print()
for app in apparel:
    print('{} ({}): {}'.format(*app))
