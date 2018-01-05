from bs4 import BeautifulSoup
from getpass import getpass
import frlib
import re

username = input('Username: ')
password = getpass()
session = frlib.frLogin(username, password)

r = session.get('http://www1.flightrising.com/auction-house/buy/realm/mats?currency=0')
page = BeautifulSoup(r.text, 'html.parser')
token = page.find('input', attrs={'name':'_token'}).get('value')
listing = page.find(attrs={'class':'ah-listing-row'})
name = listing.find(attrs={'class':'ah-listing-itemname'}).string
cost = listing.find(attrs={'class':'ah-listing-cost'}).string
id = listing.get('data-listing-id')

print('Token: {}'.format(token))
print('Name: {}'.format(re.sub(' +', ' ', name.strip())))
print('Cost: {} treasure'.format(cost))
print('id: {}'.format(id))

url = 'http://www1.flightrising.com/auction-house/ajax/buy'
data = {'_token':token, 'id':id}
##session.post(url, data)
