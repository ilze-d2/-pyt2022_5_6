import re
import sqlite3

fname = input('Enter the file name: ')                              # izsaukt faila nosaukuma ievadi, nosaukums mbox-short.txt
try:
    fhand = open(fname, 'r')                                        # atver failu, lai to lasītu
except:
    print('Wrong file name: ', fname)                               # izdrukā, ka ievadītais faila vārs nav pareizs
    quit()    

weekdaySet = set ()
emailAddressSet = set()
domainSet = set()

emailsList = list ()
weekdayList = list()
emailAddressList = list()
domainList = list()

def getWeekdayId(weekdayName):
    for item in weekdayList:
        if item[1] == weekdayName:
            return (item[0])

def getDomainId(domainName):
    for item in domainList:
        if item[1] == domainName:
            return (item[0])

def getEmailAddressId(emailAddressName):
    for item in emailAddressList:
        if item[1] == emailAddressName:
            return (item[0])

count = 0
for line in fhand:                      
    if line.startswith ('From:'):                                   # tiek meklētas e-pasta adreses
        emailAddressName = line.split()[1]                              # rindas ar atlasītajām e-pastu datiem tiek sadalītas pēc atstarpēm un tiek atlassītas e-pastu adreses
        emailAddressId = getEmailAddressId(emailAddressName)
        emailAddressSet.add (emailAddressName)
        emailAddressList.append (emailAddressName)
        domainName = emailAddressName.split ("@") [1]                       # e-pastu adreses tiek sadalītas pēc @ un tiek atlasīti domēnu nosaukumi            
        domainId = getDomainId (domainName)
        domainSet.add (domainName)
        domainList.append (domainName)

    if line.startswith ('Date:'):                                   # tiek meklēta rinda ar vēstules sūtīšanas datumu
        weekdayAll = re.findall ('Date: ([A-Za-z]*)' , line) [0]    # tiek atrasta nedēļas dienas
        if (weekdayAll != ""):                                      # tiek nodzēstas tukšās rindas
            weekdayName = weekdayAll
            weekdayId = getWeekdayId (weekdayName) 
            weekdaySet.add (weekdayName)
            weekdayList.append (weekdayName) 
    count = count + 1 

conn = sqlite3.connect('emailsFinal.sqlite')
cur = conn.cursor()           

cur.execute ('DROP TABLE IF EXISTS Weekdays')
cur.execute ('CREATE TABLE Weekdays (Weekdays_Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, Weekdays TEXT)')
i=1
for j in weekdaySet:
    cur.execute ('INSERT INTO Weekdays (Weekdays_Id, Weekdays) VALUES (?,?)', (i,j))
    i+=1

cur.execute ('DROP TABLE IF EXISTS Domain')
cur.execute ('CREATE TABLE Domain (Domain_Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, Domain TEXT)')
i=1
for j in domainSet:
    cur.execute ('INSERT INTO Domain (Domain_Id, Domain) VALUES (?,?)', (i,j))
    i+=1

cur.execute ('DROP TABLE IF EXISTS Email_Adress')
cur.execute ('CREATE TABLE Email_Adress (Email_Adress_Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, EmailAddress TEXT)')
i=1
for j in emailAddressSet:
    cur.execute ('INSERT INTO Email_Adress (Email_Adress_Id, EmailAddress) VALUES (?,?)', (i,j))
    i+=1

cur.execute ('DROP TABLE IF EXISTS Emails')
cur.execute ('CREATE TABLE Emails (Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, Email_Adress_Id INTEGER, Domain_Id INTEGER, Weekday_Id INTEGER)')
i=1
for j in emailsList:
    cur.execute ('INSERT INTO Emails (Id, Email_Adress_Id, Domain_Id, Weekday_Id) VALUES (?,?,?,?)', (i,j,j,j))
    i+=1

conn.commit()
cur.close()
