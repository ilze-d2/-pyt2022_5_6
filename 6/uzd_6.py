import sqlite3

fname = input('Enter the file name: ')                              # izsaukt faila nosaukuma ievadi, nosaukums mbox-short.txt
try:
    fhand = open(fname, 'r')                                        # atver failu, lai to lasītu
except:
    print('Wrong file name: ', fname)                               # izdrukā, ka ievadītais faila vārs nav pareizs
    quit()    

emailAddressSet = set()                                             # definēti list un set
emailAddressList = list()
domainSet = set()
domainList = list()
weekdaySet = set ()
weekdayList = list()
emailList = list ()

def getEmailAddressId (emailAddressName):                           # tiek meklēts epasta adreses ID numurs
    for item in emailAddressList:
        if item[1] == emailAddressName:
            return (item[0])

def getDomainId(domainName):                                        # tiek meklēts domēna adreses ID numurs
    for item in domainList:
        if item[1] == domainName:
            return (item[0])

def getWeekdayId(weekdayName):                                      # tiek meklēts dienas ID
    for item in weekdayList:
        if item[1] == weekdayName:
            return (item[0])

count = 0
for line in fhand:                      
    if line.startswith ('From '):                                   # tiek meklētas e-pasta adreses
        emailAddressName = line.split()[1]                          # rindas ar atlasītajām e-pastu datiem tiek sadalītas pēc atstarpēm un tiek atlassītas e-pastu adreses
        emailAddressSet.add (emailAddressName)                      # tiek veidots epasta adrešu set
        domainName = emailAddressName.split ("@") [1]               # e-pastu adreses tiek sadalītas pēc @ un tiek atlasīti domēnu nosaukumi            
        domainSet.add (domainName)                                  # tiek veidots domēnu set
        weekdayName = line.split()[2]                               # tiek atrasta nedēļas dienas
        weekdaySet.add (weekdayName)                                # tiek veidots nedēļas sienu set
        emailList.append ((emailAddressName, domainName, weekdayName))    # tiek apkopotas epastu adreses, domēnu nosaukumi un nedēļas dienu nosaukumi vienā list
        
    count = count + 1 

conn = sqlite3.connect('emailsFinal.sqlite')                        #tiek izveidots sql fails
cur = conn.cursor()           

cur.execute ('DROP TABLE IF EXISTS Weekdays')                       #tiek dzēsta esošā nedēļas dienu tabula
cur.execute ('CREATE TABLE Weekdays (Weekdays_Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, Weekdays TEXT)') #tiek izveidota jauna nedēļas dienu tabula
i=1
for j in weekdaySet:                                                # tiek iterēts cauri nedēļas dienu set
    cur.execute ('INSERT INTO Weekdays (Weekdays_Id, Weekdays) VALUES (?,?)', (i,j))    # iegūtās vērtības tiek saglabātas izveidotajā nedēļas dienu tabulā
    weekdayList.append ((i,j))                                      # tiek izveidots nedēļas dienu list
    i+=1

cur.execute ('DROP TABLE IF EXISTS Domain')
cur.execute ('CREATE TABLE Domain (Domain_Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, Domain TEXT)')      #tiek izveidota jauna domēnu tabula
i=1
for j in domainSet:
    cur.execute ('INSERT INTO Domain (Domain_Id, Domain) VALUES (?,?)', (i,j))
    domainList.append ((i,j))
    i+=1

cur.execute ('DROP TABLE IF EXISTS Email_Address')
cur.execute ('CREATE TABLE Email_Address (Email_Address_Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, Email_Address TEXT)')     #tiek izveidota jauna epasta adrešu tabula
i=1
for j in emailAddressSet:
    cur.execute ('INSERT INTO Email_Address (Email_Address_Id, Email_Address) VALUES (?,?)', (i,j))
    emailAddressList.append ((i,j))
    i+=1

cur.execute ('DROP TABLE IF EXISTS Recived_Emails')
# tiek izveidota saņemto epastu tabula
cur.execute ('CREATE TABLE Recived_Emails (Email_Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, Email_Address TEXT, Email_Address_Id INTEGER, Domain_Id INTEGER, Weekdays_Id INTEGER)') 
i=1
for j in emailList:
    e = getEmailAddressId(j[0])                                     # tiek izsaukta funkcija, lai atrastu atbilstošā epasta ID 
    d = getDomainId (j[1])                                          # tiek izsaukta funkcija, lai atrastu atbilstošā domēna ID 
    w = getWeekdayId(j[2])                                          # tiek izsaukta funkcija, lai atrastu atbilstošā nedēļas dienas ID
    cur.execute ('INSERT INTO Recived_Emails (Email_Id, Email_Address, Email_Address_Id, Domain_Id, Weekdays_Id) VALUES (?,?,?,?,?)', (i,j[0], e, d, w))
    i+=1

conn.commit()
domainNameInput = input ('Enter domain name: ')                     # tiek veikta domēna nosaukuma ievade

# tiek veikta tabulu datu apvienošana un izvadīti dati par domēnu nosaukumu, e-pasta adresēm un nedēļas dienu
cur.execute(''' SELECT Domain.Domain, Email_Address.Email_Address, Weekdays.Weekdays FROM Recived_Emails 
JOIN Domain JOIN Email_Address JOIN Weekdays ON Recived_Emails.Email_Address = Email_Address.Email_Address 
AND Recived_Emails.Email_Address_Id = Email_Address.Email_Address_Id AND Recived_Emails.Domain_Id = Domain.Domain_Id
AND Recived_Emails.Weekdays_Id = Weekdays.Weekdays_Id WHERE Domain.Domain = ? AND (Weekdays.Weekdays_Id = 2 
OR Weekdays.Weekdays_Id = 3)''', (domainNameInput,))

print ("On Fridays and Saturdays form" ,domainNameInput,"are these emails recived: ")

for c in cur:
    print (c)
   
cur.close()