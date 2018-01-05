from frBaldwin import doBaldwin
from threading import Event, Thread, Timer
from time import strftime
from tkinter import StringVar, Text, Tk, Toplevel
from tkinter import ttk
import frlib

def runBaldwin():
    start = strftime('%m/%d/%Y %I:%M:%S %p')
    print('Starting at {}'.format(start), file=outFile)
    try:
        print('Checking if Flight Rising is up...', file=outFile)
        if frlib.frIsUp():
            print('Logging in...', file=outFile)
            session = frlib.frLogin(username, password)
            category = categoryCombo.get()
            allowed = allowedLists[category]
            status = doBaldwin(session, category, allowed, outFile)
            if status is False: #couldn't brew anything
                print('Stopping due to lack of ingredients.\n', file=outFile)
                baldwinTimer.idle.set()
                return
            else: #cauldron is brewing
                time = status + 5 #time remaining + 5 seconds
        else:
            print('Flight Rising appears to be down. Trying again in 1 minute.', file=outFile)
            time = 60 #1 minute
    except Exception as e:
        print('Something went wrong:', e, file=outFile)
        print('Trying again in 1 minute.', file=outFile)
        time = 60 #1 minute
    print(file=outFile)
    #schedule the next attempt
    baldwinTimer.start(time)

def buttonToggleWaiter():
    '''Waits for the Baldwin timer to become idle, then enables the start button
       and disables the stop button.'''
    
    baldwinTimer.idle.wait()
    startButton.state(['!disabled'])
    stopButton.state(['disabled'])

class BaldwinTimer():
    def __init__(self):
        self.timer = Timer(0, None) #just a dummy value
        self.idle = Event() #set = idle, clear = running
        
    def start(self, time=1):
        self.timer.cancel() #just in case
        self.idle.clear()
        self.timer = Timer(time, runBaldwin)
        self.timer.start()

    def stop(self):
        self.timer.cancel()
        self.idle.set()

def startButtonFunc():
    global toggleThread
    
    startButton.state(['disabled'])
    stopButton.state(['!disabled'])
    baldwinTimer.start()
    toggleThread = Thread(target=buttonToggleWaiter)
    toggleThread.start()

def stopButtonFunc():
    baldwinTimer.stop()

def exitHandler():
    baldwinTimer.stop()
    if toggleThread.is_alive():
        #I want to just join() the toggle thread, but this exit handler is holding the gui hostage...
        #I don't think I can do anything about that, so instead, we kick off a new thread and return.
        def foo():
            toggleThread.join()
            exitHandler()
        Thread(target=foo).start()
        return
    else:
        root.destroy()

class outWriter():
    def write(self, s):
        outText.configure(state='normal')
        outText.insert('end', s)
        outText.configure(state='disabled')
        outText.see('end')

#allowed ingredient lists
allowedFood = ['21409'] #firecoiler
allowedMats = ['672'] #jar of slime
allowedApp = ['17893', '17903', '317', '323', '534', '548', '1155', '1156', '1552', '8314', '10741', '13854', '17281', '17894', '20583', '10362', '17264', '20580', '20604', '20605', '10736', '17884', '287', '20578', '818', '20552', '10364', '17250', '817', '1867', '1553', '17248', '17929', '17249', '12927', '13797', '17134', '17137', '271', '285', '946', '10724', '10734', '12907', '20554', '20568', '278', '281', '288', '348', '349', '367', '539', '947', '1151', '1159', '1254', '1547', '1548', '1549', '1708', '2463', '2975', '2976', '3115', '3116', '3117', '3118', '9813', '10365', '10394', '10716', '10737', '10744', '12905', '12906', '12928', '13792', '13795', '13843', '13848', '17135', '17142', '17242', '17252', '17267', '17877', '17885', '20550', '20579', '20584', '20612', '21268', '1153', '2757', '2974', '17139', '17280', '17140', '17136', '20611', '12904', '12929', '17913', '23028', '23036', '17902', '2971', '2981', '464', '542', '20556', '394', '17138', '9451', '370', '389', '1871', '5912', '10730', '386', '13856', '20570', '13829', '17232', '17918', '20610', '275', '816', '2468', '2984', '3285', '3288', '8318', '8594', '8595', '10372', '10380', '13806', '13808', '17235', '17239', '17246', '17256', '17272', '17276', '17284', '20569', '20582', '20600', '20601', '20609', '21276', '21806', '21830', '23033', '21829', '814', '13838', '17922', '268', '2565', '10727', '17274', '17920', '10399', '330', '363', '10720', '13790', '10397', '5694', '332', '391', '490', '10751', '17882', '286', '365', '369', '371', '428', '431', '434', '437', '656', '1865', '4006', '5157', '5688', '5692', '7279', '10390', '10400', '10738', '10748', '12903', '12908', '12926', '13809', '13839', '17141', '17886', '17911', '17927', '20553', '21817', '21831', '292', '17132', '492', '2978', '9222', '11517', '10379', '8810', '20555', '21805', '289', '739', '2561', '2980', '13822', '17900', '21853', '10393', '17930', '2759', '390', '13847', '2972', '21264', '21834', '21290', '276', '388', '426', '430', '1550', '5689', '8813', '9218', '9224', '10386', '10713', '13842', '17240', '21224', '21306', '21816', '23029', '364', '277', '2977', '436', '5693', '17921', '5403', '10361', '2985', '8316', '9219', '18822', '20602', '20606', '12924', '387', '9220', '20565', '21852', '8317', '21274', '433', '435', '477', '5166', '10369', '10721', '13810', '17263', '20603', '362', '21282', '17237', '7281', '13841']
allowedFam = ['21412', '21413', '21414', '21415', '21416', '21417', '21418', '21419', '21420', '21421', '21422', '21423', '21424', '21425', '21426', '21427', '21428', '21429', '21432', '21433', '21434', '21435', '21436', '21437'] #volcanic vents (excluding bosses)
allowedOther = ['5708'] #discarded ribbon
allowedCreate = ['146', '1'] #skink, glass beaker
allowedLists = {'food':allowedFood, 'mats':allowedMats, 'app':allowedApp, 'fam':allowedFam, 'other':allowedOther, 'create':allowedCreate}

baldwinTimer = BaldwinTimer()
toggleThread = Thread() #just a dummy value

#get username and password
creds = Tk()
creds.title('Log In')
ttk.Label(creds, text='Username:').grid(row=0, column=0)
usernameVar = StringVar()
ttk.Entry(creds, textvariable=usernameVar).grid(row=0, column=1)
ttk.Label(creds, text='Password:').grid(row=1, column=0)
passwordVar = StringVar()
ttk.Entry(creds, textvariable=passwordVar, show='*').grid(row=1, column=1)
ttk.Button(creds, text='Okay', command=creds.destroy).grid(row=2, column=0, columnspan=2)
creds.wait_window()
username, password = usernameVar.get(), passwordVar.get()

#set up main window
root = Tk()
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.title('Baldwin Manager')
root.protocol("WM_DELETE_WINDOW", exitHandler)

baseFrame = ttk.Frame(root)
baseFrame.rowconfigure(0, weight=1)
baseFrame.rowconfigure(1, weight=1)
baseFrame.rowconfigure(2, weight=1)
baseFrame.columnconfigure(0, weight=1)
baseFrame.columnconfigure(1, weight=1)
baseFrame.columnconfigure(2, weight=1)
baseFrame.grid(row=0, column=0)

startButton = ttk.Button(baseFrame, text='Start', command=startButtonFunc)
startButton.grid(row=0, column=0)

stopButton = ttk.Button(baseFrame, text='Stop', command=stopButtonFunc)
stopButton.grid(row=0, column=1)
stopButton.state(['disabled'])

blankButton = ttk.Button(baseFrame, text='Nothing')
blankButton.grid(row=0, column=2)

categories = ['food', 'mats', 'app', 'fam', 'other', 'create']
categoryCombo = ttk.Combobox(baseFrame, values=categories, state='readonly')
categoryCombo.set(categories[0])
categoryCombo.grid(row=1, column=0, columnspan=3)

outText = Text(baseFrame, height=20, width=80, state='disabled')
outText.grid(row=2, column=0, columnspan=3)
outScrollbar = ttk.Scrollbar(baseFrame, orient='vertical', command=outText.yview)
outScrollbar.grid(row=2, column=2, sticky='nse')
outText.configure(yscrollcommand=outScrollbar.set)

#redirect print statements to the text area
outFile = outWriter()

#start it up
root.mainloop()

print('I guess mainloop is over now.')
