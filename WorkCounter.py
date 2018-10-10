#!/usr/local/bin/python
import smtplib
import datetime
import time
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import shelve

file = open('work.txt','a+')
shelveFile = shelve.open('hoursWorked')


currentStart = file.tell()

def getUnixTime ():
    timestamp = int(time.time())
    return timestamp

def get_sec(s):
    l = s.split(':')
    return int(l[0]) * 3600 + int(l[1]) * 60

def getGodzina ():
    now = datetime.datetime.now()

    hour = now.hour
    minute = now.minute
    if (len(str(hour)) == 1):
        hour = '0' + str(hour)

    if (len(str(minute)) == 1):
        minute = '0' + str(minute)

    time = '%s:%s' % (hour,minute)

    return time


def addZero (number):
    if (len(str(number)) == 1):
        number = '0' + str(number)
    return number

def getDate ():
    now = datetime.datetime.now()

    day = now.day
    month = now.month
    day = addZero(day)
    month = addZero(month)

    date = '%s-%s-%d' % (day, month, now.year)
    return date

def sendEmail(email):
    fromaddr = "email@gmail.com"
    toaddr = email
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = 'Imie Naziwsko - zestawienie pracy z dnia : ' + getDate()
    content = ''

    file.seek(currentStart)

    content += file.read(deltaEmailOffset)

    print content

    msg.attach(MIMEText(content, 'plain'))

    text = msg.as_string()

    server = smtplib.SMTP('smtp.gmail.com', 587)

    server.ehlo()
    server.starttls()
    server.ehlo()

    print 'Trying to send email to : ' + email

    try:
      server.login('email@gmail.com', 'password')
      server.sendmail('email@gmail.com', email, text)
      print 'Email sent ! '
    except:
      print 'Unable to send an email'


class produkt:
    idProduktu = 0
    uwagi = ''
    link = ''
    time = ''
    def __init__(self, idProduktu = None, uwagi = None,time = None):
        self.idProduktu = idProduktu
        self.uwagi = uwagi
        self.time = time
        self.link = "https://www.ergonauta.pl/panel/product-edit.php?idt="+str(idProduktu)

listaProduktow = []
jobStartTime = 0
jobEndTime = 0
jobTimeStr = ''
jobStartTimeUTC = 0
jobEndTimeUTC = 0
deltaEmailOffset = 0
emailOffsetEnd = 0

for i in listaProduktow:
    print i.idProduktu

isScriptRunning = True

print '''StartDay - create new day information
EndDay - finishing day by some new lines and send email
new | id | note |
pause
resume
special <command>
aktualnyCzasPracy
 '''

timeBeforePause = 0
timeAfterPause = 0

timePaused = 0

isPaused = False

while (isScriptRunning):
    command = raw_input()
    if (command == 'aktualnyCzasPracy'):
        jobEndTimeTMP = getUnixTime()

        delta = jobEndTimeTMP - jobStartTime - timePaused
        if (delta < 0):
            delta = 86400 - delta
        m, s = divmod(delta, 60)
        h, m = divmod(m, 60)

        print 'Aktualny czas pracy ' + str(addZero(h)) + ":" + str(addZero(m))
    elif (command == 'special'):
        input()
    elif (command == 'pause'):
        print 'Work PAUSED'
        timeBeforePause = getUnixTime()
        isPaused = True
    elif (command == 'resume'):
        print 'Work RESUMED'
        isPaused = False
        timeAfterPause = getUnixTime()
        timePaused = timePaused + timeAfterPause - timeBeforePause
    elif (command == 'StartDay'):

        print 'Dzisiaj jest : ' + getDate()
        jobStartTime = getUnixTime()
        jobStartTimeUTC = getGodzina()

    elif (command == 'EndDay'):
        if (len(listaProduktow) == 0):
            print 'Nic dzisiaj nie zrobiles leniu'
            print 'Podaj powod czemu nic dzisiaj nie zrobiles'
            powod = raw_input()
            file.write('\n')
            file.write(powod)
            file.close()
            isScriptRunning = False
            break;

        jobEndTime = getUnixTime()
        jobEndTimeUTC = getGodzina()

        delta = jobEndTime - jobStartTime - timePaused
        if (delta < 0):
            delta = 86400 - delta
        m, s = divmod(delta, 60)
        h, m = divmod(m, 60)

        try:
            shelveFile['products'] = shelveFile['products'] + len(listaProduktow)
        except:
            shelveFile['products'] = len(listaProduktow)


        try:
            seconds = get_sec(shelveFile['hours'])
            print "ILOSC SEKUND " + str(seconds)
            sum = delta + seconds
            mS, sS = divmod(sum, 60)
            hS, mS = divmod(mS, 60)
            print 'Aktualny czas pracy : ' + str(addZero(h)) + ":" + str(addZero(m))
            shelveFile['hours'] = str(addZero(hS)) + ":" +  str(addZero(mS))
            print str(addZero(hS))
            print str(addZero(mS))
            print shelveFile['hours']
            print 'Laczny czas pracy : ' + shelveFile['hours']
        except:
            shelveFile['hours'] = addZero(str(h)) + ":" + addZero(str(m))

        file.write(getDate())

        file.write('\n')

        file.write('\n')

        file.write('Podsumowanie :')

        file.write('\n')

        file.write('\n')

        file.write('Rozpoczecie pracy : ' + str(jobStartTimeUTC) + '\n')

        file.write('Zakonczenie pracy : ' + str(jobEndTimeUTC) + '\n')

        mP, sP = divmod(timePaused, 60)
        hP, mP = divmod(mP, 60)

        file.write('Laczny czas przerwy od pracy : ' + str(addZero(hP)) + ":" + str(addZero(mP)) + '\n')

        file.write('Czas pracy : ' + str(addZero(h))+':' + str(addZero(m)))

        file.write('\n')

        file.write('Laczny czas pracy : ' + shelveFile['hours'])

        file.write('\n')

        file.write('Ilosc produktow zaktualizowanych : ' + str(len(listaProduktow)) + '\n')

        file.write('Laczna ilosc produktow zaktualizowanych ' + str(shelveFile['products']) + '\n')

        file.write('\n')

        for i in listaProduktow:
            file.write('Id produktu %s \n Link : %s \n Godzina : %s \n Komentarz (opcjonalny) %s \n' % (i.idProduktu, i.link ,i.time, i.uwagi))

        file.write('\n')
        file.write('\n')
        file.write('-----------------------------------------------------\n')
        file.write('\n')
        emailOffsetEnd = file.tell()
        deltaEmailOffset = emailOffsetEnd - currentStart

        print 'Czy chcesz wyslac mail ? Napisz adres mail albo NIE'
        odp = raw_input()
        if (odp != 'NIE'):
            sendEmail(odp)

        file.close()
        isScriptRunning = False

    elif (command[:3] == 'new'):
        if (isPaused == False):
           if (len(listaProduktow) == 0):
                  productsSeek = file.tell()
           try:
            file.write('\n')
            parameters = command [4:]
            comment = ''
            id,comment = parameters.split('|')
            produktWpisanyObj = produkt(id,comment,getGodzina())
            listaProduktow.append(produktWpisanyObj)
           except:
            print 'Cos nie pyklo przy wpisywaniu produktu'
        else:
            print 'Nie dodawaj produktu jak masz przerwe'


