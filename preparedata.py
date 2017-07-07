
import pandas as pd
import matplotlib.pyplot as plt

import numpy as np
import csv


from matplotlib.ticker import FuncFormatter

def loadEvents():
    dictDf = dict()
    dfConcierge = pd.read_csv('./data/concierge.csv')
    dfDropbox = pd.read_csv('./data/dropbox.csv')
    dfMcAfee = pd.read_csv('./data/mcAfee.csv')
    dfRegister = pd.read_csv('./data/register.csv')
    dfApp = pd.read_csv('./data/app.csv')
    dictDf['/register'] = dfRegister
    dictDf['/Dropbox-Signup'] = dfDropbox
    dictDf['/mcafee'] = dfMcAfee
    dictDf['/Appselect1'] = dfApp
    dictDf['/OnlineConcierge'] = dfConcierge

    return dictDf


def getSkipByScreen(flowName, screenName,dict):
    #Posdf = pd.read_csv('./data/flownames.csv')
    try:
        skip = dict[screenName]
    except:
        print(screenName + 'not available')
        return 0

    if screenName == '/register':
        users= skip.loc[(skip['eventAction'] == 'LaterClicked') & (skip['dimension34']==flowName)]
    elif screenName == '/Dropbox-Signup':
        users= skip.loc[(skip['eventAction'] == 'SkipClicked') & (skip['dimension34']==flowName)]
    elif screenName == '/mcafee':
        users= skip.loc[(skip['eventAction'] == 'LaterClicked') & (skip['dimension34']==flowName)]
    elif screenName == '/Appselect1':
        users = skip.loc[(skip['eventAction'] == 'ContinueClicked') & (skip['dimension34'] == flowName)]
    #dict.at['/welcome', 'users']
    #elif screenName == '/OnlineConcierge':
    #    users = skip.loc[(skip['eventAction'] == 'ComeBackLater') & (skip['dimension34'] == flowName)]
    else:
        return 0

    a=None
    try:
        a =users['users'].iloc[0]
    except:
        print(flowName,screenName,'skip not found' )

    return a

def getPosByScreen(flowName, screenName,dict):
    #Posdf = pd.read_csv('./data/flownames.csv')
    try:
        skip = dict[screenName]
    except:
        print(screenName + 'not available')
        return 0

    if screenName == '/register':
        users= skip.loc[(skip['eventAction'] == 'HPAccountRegistered') & (skip['dimension34']==flowName)]
    elif screenName == '/Dropbox-Signup':
        users= skip.loc[(skip['eventAction'] == 'Dropbox-Signup') & (skip['dimension34']==flowName)& (skip['eventLabel']=='success')]
    elif screenName == '/mcafee':
        users= skip.loc[(skip['eventAction'] == 'McAfeeRegistered') & (skip['dimension34']==flowName)]
    elif screenName == '/Appselect1':
        users = skip.loc[(skip['eventAction'] == 'InstallAndContinueClicked') & (skip['dimension34'] == flowName)]
    #dict.at['/welcome', 'users']
    elif screenName == '/OnlineConcierge':
        users = skip.loc[(skip['eventAction'] == 'ContentClicked') & (skip['dimension34'] == flowName)]
    else:
        return 0
    a=None

    try:
        a =users['users'].iloc[0]
    except:
        print(flowName,screenName,'pos not found' )

    return a


def getErrByScreen(flowName, screenName,dict):
    #Posdf = pd.read_csv('./data/flownames.csv')
    try:
        skip = dict[screenName]
    except:
        print(screenName + 'not available')
        return 0

    if screenName == '/Dropbox-Signup':
        u1= skip.loc[(skip['eventAction'] == 'Dropbox-Signup') & (skip['dimension34']==flowName)& (skip['eventLabel']!='success')]
        users = u1.groupby("screenName").agg('sum')
        print(users)

    else:
        return 0
    a=None

    try:
        a =users['users'].iloc[0]
    except:
        print(flowName,screenName,'err not found' )

    return a

def currency(x, pos):
    'The two args are the value and tick position'
    if x >= 1000000:
        return '{:1.1f}M'.format(x*1e-6)
    return '{:1.0f}K'.format(x*1e-3)
def pct(x, pos):
    'The two args are the value and tick position'
    return '{:1.1f}%'.format(x*1e-2)

def getOrderedScreens(flowname):
    #Flow_AppInstall_Concierge
    #"11","Flow_Registration_Dropbox_McAfee_AppInstall_Concierge","JumpStart in field (UWP=>407)",13418
    dict = {
        'Flow':'/welcome',
        'Registration': '/register',
        'Dropbox': '/Dropbox-Signup',
        'McAfee': '/mcafee',
        'AppInstall': '/Appselect1',
        'Concierge': '/OnlineConcierge',
        'GetMoreApps' : 'x',
        'Mcafee' : '/mcafee',
        'Appinstall':'/Appselect1',
        'EMEA' : 'h',
        'MCD' : 'l'
    }
    str=list()
    screenlist = flowname.split('_')
    for screen in screenlist:
        if screen == 'Only': continue
        str.append(dict[screen])
    str.append('/concierge')
    str.append('/criticalerror')
    str.append('/exit')
    #print(flowname)
    #print(str)
    return str



def plotBarhByFlow(flowname, df,users):
    df2 = df[df['dimension34'] == flowname][['screenName', 'users']]
    print(df2)


    plt.style.use('dark_background')

    df2.set_index('screenName', inplace=True)
    #print("df2|",df2)
    df3 = df2.reindex(getOrderedScreens(flowname)[::-1])

    deno = df3.at['/welcome','users']

    for i, trial in df3.iterrows():
        df3.loc[i, "pct"] = '{:.1%}'.format(trial["users"] / deno)

    #print("df3|",df3)

    ax = df3.plot.barh(stacked=True)
    #fig, ax = plt.subplots()

    for i, v in enumerate(df3['pct']):
        #print(i,v)
        ax.text(0, i + .25, str(v), color='white', fontweight='bold')
    plt.tight_layout()
    plt.title(flowname)
    formatter = FuncFormatter(currency)
    ax.xaxis.set_major_formatter(formatter)
    # plt.yticks(pos, ylabel)


    # df2.plot.bar(stacked=False)


    #plt.show()
    filename = './output/barh/' + str(users) + '_' + flowname + '.png'
    # plt.show()
    plt.savefig(filename, transparent=False, dpi=80, bbox_inches="tight")

def plotSbarhByFlow(flowname, df, users):

    df2 = df[df['dimension34'] == flowname][['screenName', 'users']]
    print(df2)
    #fig1 = plt.figure(figsize=(9, 5), dpi=100)

    plt.style.use('dark_background')

    df2.set_index('screenName', inplace=True)
    # #print("df2|",df2)
    df3 = df2.reindex(getOrderedScreens(flowname)[::-1])
    #
    # deno = df3.at['/welcome','users']
    #
    # for i, trial in df3.iterrows():
    #     df3.loc[i, "pct"] = '{:.1%}'.format(trial["users"] / deno)
    #
    # print("df3|",df3)
    #
    #
    # dftest=pd.datcolumns=['users', 'pct']

        # ax = df3.plot.barh(stacked=True)

    #add skip column
    for i, trial in df3.iterrows():
        #print(row['dimension34'], i)
        df3.loc[i, "skip"] = getSkipByScreen(row['dimension34'], i, dictEvents)
    # add pos column
    for i, trial in df3.iterrows():
        #print(row['dimension34'], i)
        df3.loc[i, "pos"] = getPosByScreen(row['dimension34'], i, dictEvents)

    # add err column
    for i, trial in df3.iterrows():
        #print(row['dimension34'], i)
        df3.loc[i, "error"] = getErrByScreen(row['dimension34'], i, dictEvents)

    # exit = users- pos - skip
    # for i, trial in df3.iterrows():
    #     #print(row['dimension34'], i)
    #     df3.loc[i, "pos"] = getPosByScreen(row['dimension34'], i, dictEvents)


    df4 = pd.DataFrame(df3, columns=['users', 'pos','skip','error'])
    print(df4)
    #df3.columns=['users', 'pct']
    #plt.figure(0)
    ax=df4.plot.barh(stacked=False)

    formatter = FuncFormatter(currency)
    ax.xaxis.set_major_formatter(formatter)
    # for i, v in enumerate(df3['pct']):
    #     #print(i,v)
    #     ax.text(0, i + .25, str(v), color='white', fontweight='bold')

    plt.title(flowname)
    # formatter = FuncFormatter(currency)
    # ax.xaxis.set_major_formatter(formatter)
    # plt.yticks(pos, ylabel)


    # df2.plot.bar(stacked=False)




    filename = './output/sbarh/' + str(users) + '_' + flowname + '.png'
    plt.tight_layout()
    plt.show()

    plt.title(flowname)
    plt.savefig(filename, transparent=False, dpi=80, bbox_inches="tight")


#main

reachscreen = pd.read_csv('./data/MyData.csv')

# get flow name, users
flownames = pd.read_csv('./data/flownames.csv')
# with open('./data/flownames.csv') as csvfile:
#     data = list(csv.DictReader(csvfile))

flows = flownames[['users','dimension34']]

slice=flows.query('users > 1350000 & users <1400000')
#slice=flows
for index, row in slice.iterrows():
    print(row['users'],row['dimension34'])

    plotBarhByFlow(row['dimension34'],reachscreen, row['users'])



# plot segmented barh
dictEvents = loadEvents()

for index, row in slice.iterrows():
    print(row['users'], row['dimension34'])
    plotSbarhByFlow(row['dimension34'], reachscreen, row['users'])



