from bs4 import BeautifulSoup
from time import strftime
import frlib
import sys

def doBaldwin(session, category, allowed, file=sys.stdout):
    '''Returns the number of seconds of brew time remaining if a brew is successfully started or
       still brewing, or returns False if a brew was not successfully started.'''
    
    #get cauldron status
    print('Checking cauldron...', file=file)
    r = session.get('https://www1.flightrising.com/trading/baldwin/transmute')
    page = BeautifulSoup(r.text, 'html.parser')
    if page.find('div', attrs={'id':'baldwin-timer-value'}): #cauldron is still brewing
        timeLeft = int(page.find('div', attrs={'id':'baldwin-timer-value'}).get('data-seconds-left'))
    else: #cauldron is either ready or empty
        if page.find('div', attrs={'class':'baldwin-cauldron-done'}): #cauldron is done brewing
            print('Collecting from cauldron...', file=file)
            token = page.find('input', attrs={'name':'_token'}).get('value')
            nexturl = page.find('input', attrs={'name':'nexturl'}).get('value')
            url = 'http://www1.flightrising.com/trading/baldwin/collect'
            data = {'_token':token, 'nexturl':nexturl}
            session.post(url, data)

        if category == 'create': #try to brew an allowed recipe
            print('Looking for a recipe to brew...', file=file)
            url = 'http://www1.flightrising.com/trading/baldwin/create/preview'
            for recipe in allowed:
                #load the recipe preview
                data = {'recipe': recipe}
                r = session.post(url, data)
                preview = BeautifulSoup(r.text, 'html.parser')
                if preview.find('input', attrs={'type':'submit'}): #we can brew this recipe
                    #get recipe name and brew time
                    name = preview.find('span', attrs={'class':'baldwin-redtext'}).string
                    cooldown = preview.find('div', attrs={'id':'baldwin-preview-icon-cooldown'})
                    if len(cooldown.find_all('b')) == 1: #brew time is in just minutes or just hours
                        timeTag = cooldown.find('b')
                        if timeTag.nextSibling.strip() == 'min': #brew time is in minutes
                            timeLeft = int(timeTag.string)*60
                        else: #brew time is in hours
                            timeLeft = int(timeTag.string)*60*60
                    else: #brew time is in hours and minutes (in that order)
                        times = [int(b.string) for b in cooldown.find_all('b')]
                        timeLeft = times[0]*60*60 + times[1]*60
                    break
            else: #we can't brew any of the recipes
                print('Cannot brew any allowed recipes.', file=file)
                return False

            #submit the recipe
            print('Brewing {}...'.format(name), file=file)
            r = session.get('http://www1.flightrising.com/trading/baldwin/create')
            page = BeautifulSoup(r.text, 'html.parser')
            token = page.find('input', attrs={'name':'_token'}).get('value')
            nexturl = page.find('div', attrs={'id':'baldwin-next-url'}).string
            url = 'http://www1.flightrising.com/trading/baldwin/create/commit'
            data = {'recipe':recipe, '_token':token, 'nexturl':nexturl}
            session.post(url, data)
            print('{} is brewing.'.format(name), file=file)
        else: #try to reduce an allowed ingredient
            longCategories = {'food':'food', 'mats':'material', 'app':'apparel', 'fam':'familiar', 'other':'trinket'}
            longCategory = longCategories[category]
            
            #get list of ingredients
            print('Looking for an allowed {}...'.format(longCategory), file=file)
            url = 'http://www1.flightrising.com/msgs/generic-item-page'
            data = {'tab':category, 'filter':'transmutable'}
            r = session.post(url, data)
            ingredients = BeautifulSoup(r.text, 'html.parser')
            
            #look for allowed ingredient
            for ingredient in ingredients.find_all('a'):
                itemID = ingredient.get('data-itemid')
                if itemID in allowed:
                    stackID = ingredient.get('data-stack')
                    timeLeft = 30*60 #reducing ingredients takes 30 minutes
                    break
            else: #no allowed ingredients found
                print('Could not find an allowed {}.'.format(longCategory), file=file)
                return False
            
            #submit ingredient to cauldron
            print('Adding {} to cauldron...'.format(longCategory), file=file)
            r = session.get('https://www1.flightrising.com/trading/baldwin/transmute')
            page = BeautifulSoup(r.text, 'html.parser')
            token = page.find('input', attrs={'name':'_token'}).get('value')
            url = 'https://www1.flightrising.com/trading/baldwin/transmute/begin'
            data = {'_token':token, 'item_in':itemID, 'stack':stackID}
            session.post(url, data)
            print('{} added to cauldron.'.format(longCategory.capitalize()), file=file)

    #show remaining time in pretty format and return it in seconds
    hours = timeLeft//3600
    minutes = (timeLeft%3600)//60
    seconds = timeLeft%60
    print('Cauldron has {:02}:{:02}:{:02} remaining.'.format(hours, minutes, seconds), file=file)
    return timeLeft

def runBaldwin(scheduler, username, password, category, allowed):
    '''The event for the scheduler to run.'''
    
    start = strftime('%m/%d/%Y %I:%M:%S %p')
    print('Starting at {}'.format(start))
    try:
        print('Checking if Flight Rising is up...')
        if frlib.frIsUp():
            print('Logging in...')
            session = frlib.frLogin(username, password)
            status = doBaldwin(session, category, allowed)
            if status is False: #couldn't brew anything
                print('Exiting due to lack of ingredients.')
                return
            else: #cauldron is brewing
                time = status + 5 #time remaining + 5 seconds
        else:
            print('Flight Rising appears to be down. Trying again in 1 minute.')
            time = 60 #1 minute
    except Exception as e:
        print('Something went wrong:', e)
        print('Trying again in 1 minute.')
        time = 60 #1 minute
    print()
    #schedule the next attempt
    args = (scheduler, username, password, category, allowed)
    scheduler.enter(time, 1, runBaldwin, args)

if __name__ == '__main__':
    from getpass import getpass
    import sched
    import sys
    
    #allowed ingredient lists
    allowedFood = ['21409'] #firecoiler
    allowedMats = ['672'] #jar of slime
    allowedApp = ['17893', '17903', '317', '323', '534', '548', '1155', '1156', '1552', '8314', '10741', '13854', '17281', '17894', '20583', '10362', '17264', '20580', '20604', '20605', '10736', '17884', '287', '20578', '818', '20552', '10364', '17250', '817', '1867', '1553', '17248', '17929', '17249', '12927', '13797', '17134', '17137', '271', '285', '946', '10724', '10734', '12907', '20554', '20568', '278', '281', '288', '348', '349', '367', '539', '947', '1151', '1159', '1254', '1547', '1548', '1549', '1708', '2463', '2975', '2976', '3115', '3116', '3117', '3118', '9813', '10365', '10394', '10716', '10737', '10744', '12905', '12906', '12928', '13792', '13795', '13843', '13848', '17135', '17142', '17242', '17252', '17267', '17877', '17885', '20550', '20579', '20584', '20612', '21268', '1153', '2757', '2974', '17139', '17280', '17140', '17136', '20611', '12904', '12929', '17913', '23028', '23036', '17902', '2971', '2981', '464', '542', '20556', '394', '17138', '9451', '370', '389', '1871', '5912', '10730', '386', '13856', '20570', '13829', '17232', '17918', '20610', '275', '816', '2468', '2984', '3285', '3288', '8318', '8594', '8595', '10372', '10380', '13806', '13808', '17235', '17239', '17246', '17256', '17272', '17276', '17284', '20569', '20582', '20600', '20601', '20609', '21276', '21806', '21830', '23033', '21829', '814', '13838', '17922', '268', '2565', '10727', '17274', '17920', '10399', '330', '363', '10720', '13790', '10397', '5694', '332', '391', '490', '10751', '17882', '286', '365', '369', '371', '428', '431', '434', '437', '656', '1865', '4006', '5157', '5688', '5692', '7279', '10390', '10400', '10738', '10748', '12903', '12908', '12926', '13809', '13839', '17141', '17886', '17911', '17927', '20553', '21817', '21831', '292', '17132', '492', '2978', '9222', '11517', '10379', '8810', '20555', '21805', '289', '739', '2561', '2980', '13822', '17900', '21853', '10393', '17930', '2759', '390', '13847', '2972', '21264', '21834', '21290', '276', '388', '426', '430', '1550', '5689', '8813', '9218', '9224', '10386', '10713', '13842', '17240', '21224', '21306', '21816', '23029', '364', '277', '2977', '436', '5693', '17921', '5403', '10361', '2985', '8316', '9219', '18822', '20602', '20606', '12924', '387', '9220', '20565', '21852', '8317', '21274', '433', '435', '477', '5166', '10369', '10721', '13810', '17263', '20603', '362', '21282', '17237', '7281', '13841']
    allowedFam = []
    allowedOther = ['5708'] #discarded ribbon
    allowedCreate = ['146', '1'] #skink, glass beaker
    allowedLists = {'food':allowedFood, 'mats':allowedMats, 'app':allowedApp, 'fam':allowedFam, 'other':allowedOther, 'create':allowedCreate}
    
    #category of ingredient to melt
    category = 'create' #food, mats, app, fam, other, create
    allowed = allowedLists[category]

    #get credentials
    if len(sys.argv) == 3:
        username = sys.argv[1]
        password = sys.argv[2]
        print('Credentials supplied: {}'.format(username))
    else:
        username = input('Username: ')
        password = getpass()
    print()

    #start scheduler
    scheduler = sched.scheduler()
    args = (scheduler, username, password, category, allowed)
    scheduler.enter(1, 1, runBaldwin, args)
    scheduler.run()
