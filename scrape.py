from bs4 import BeautifulSoup
from datetime import date
import datetime
import requests
import sqlite3
import time
import csv


today = date.today()


class stock:
    def __init__(self, name, price, delta, percent, TenOver, Xten):
        self.name = name
        self.price = price
        self.delta = delta
        self.percent = percent
        self.TenOver = TenOver
        self.Xten = Xten


    def getPrice(self):
        return self.price

    def getName(self):
        return self.name

    def getDelta(self):
        return self.delta

    def getPercent(self):
        return self.percent

    def getTenOver(self):
        return self.TenOver

    def getXten(self):
        return self.Xten






# gives stocks default values

stock1 = stock('nil',0.0,'nil','nil',0,0)
stock2 = stock('nil',0.0,'nil','nil',0,0)
stock3 = stock('nil',0.0,'nil','nil',0,0)
stock4 = stock('nil',0.0,'nil','nil',0,0)
stock5 = stock('nil',0.0,'nil','nil',0,0)
stock6 = stock('nil',0.0,'nil','nil',0,0)
stock7 = stock('nil',0.0,'nil','nil',0,0)
stock8 = stock('nil',0.0,'nil','nil',0,0)
stock9 = stock('nil',0.0,'nil','nil',0,0)
stock10 = stock('nil',0.0,'nil','nil',0,0)
stock11 = stock('nil',0.0,'nil','nil',0,0)
stock12 = stock('nil',0.0,'nil','nil',0,0)
stock13 = stock('nil',0.0,'nil','nil',0,0)
stock14 = stock('nil',0.0,'nil','nil',0,0)
stock15 = stock('nil',0.0,'nil','nil',0,0)
stock16 = stock('nil',0.0,'nil','nil',0,0)
stock17 = stock('nil',0.0,'nil','nil',0,0)
stock18 = stock('nil',0.0,'nil','nil',0,0)
stock19 = stock('nil',0.0,'nil','nil',0,0)
stock20 = stock('nil',0.0,'nil','nil',0,0)
stock21 = stock('nil',0.0,'nil','nil',0,0)
stock22 = stock('nil',0.0,'nil','nil',0,0)
stock23 = stock('nil',0.0,'nil','nil',0,0)
stock24 = stock('nil',0.0,'nil','nil',0,0)
stock25 = stock('nil',0.0,'nil','nil',0,0)

wstock1 = stock('nil',0.0,'nil','nil',0,0)
wstock2 = stock('nil',0.0,'nil','nil',0,0)
wstock3 = stock('nil',0.0,'nil','nil',0,0)
wstock4 = stock('nil',0.0,'nil','nil',0,0)
wstock5 = stock('nil',0.0,'nil','nil',0,0)
wstock6 = stock('nil',0.0,'nil','nil',0,0)
wstock7 = stock('nil',0.0,'nil','nil',0,0)
wstock8 = stock('nil',0.0,'nil','nil',0,0)
wstock9 = stock('nil',0.0,'nil','nil',0,0)
wstock10 = stock('nil',0.0,'nil','nil',0,0)
wstock11 = stock('nil',0.0,'nil','nil',0,0)
wstock12 = stock('nil',0.0,'nil','nil',0,0)
wstock13 = stock('nil',0.0,'nil','nil',0,0)
wstock14 = stock('nil',0.0,'nil','nil',0,0)
wstock15 = stock('nil',0.0,'nil','nil',0,0)


stockpile = {
    "stock1": stock1,

    "stock2": stock2,

    "stock3": stock3,

    "stock4": stock4,

    "stock5": stock5,

    "stock6": stock6,

    "stock7": stock7,

    "stock8": stock8,

    "stock9": stock9,

    "stock10": stock10,

    "stock11": stock11,

    "stock12": stock12,

    "stock13": stock13,

    "stock14": stock14,

    "stock15": stock15,

    "stock16": stock16,

    "stock17": stock17,

    "stock18": stock18,

    "stock19": stock19,

    "stock20": stock20,

    "stock21": stock21,

    "stock22": stock22,

    "stock23": stock23,

    "stock24": stock24,

    "stock25": stock25,


}

watchlist = {
    "wstock1": wstock1,

    "wstock2": wstock2,

    "wstock3": wstock3,

    "wstock4": wstock4,

    "wstock5": wstock5,

    "wstock6": wstock6,

    "wstock7": wstock7,

    "wstock8": wstock8,

    "wstock9": wstock9,

    "wstock10": wstock10,

    "wstock11": wstock11,

    "wstock12": wstock12,

    "wstock13": wstock13,

    "wstock14": wstock14,

    "wstock15": wstock15,


}


dataList= []
nameList = []
wnameList = []



temp = 0
temp2 = 0
check = 0
dummy = 'hi'
s = 0
watchlen = 1

def ifTime(): #checks if trading is open
    day_of_week = datetime.date.today().weekday() # 0 is Monday, 6 is Sunday
    time = datetime.datetime.now().time()
    if day_of_week < 5 and (time > datetime.time(8,30) and time < datetime.time(15)):
        return True








#while stock trading is open

#while ifTime():
while check<2:

    URL = "https://finance.yahoo.com/gainers"
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html.parser')

    for link in soup.find_all( class_="Fw(600) C($linkColor)"): # this is making a list of the symbols
        nameList.append(link.string)
        temp = temp + 1
        stockpile["stock"+str(temp)].name = link.string





    for link in soup.find_all( class_="Va(m) Ta(end) Pstart(20px) Fw(600) Fz(s)"):# this is giving all three
        dataList.append(link.get_text())


    for i in dataList : #putting all the data in the right place

        index=dataList.index(i)

        temp1 = (index // 3) + 1

        tstock = stockpile["stock" + str(temp1)]


        if i.startswith('+') and not i.endswith("%"):
            tstock.delta = i


        elif not i.startswith('+') and not i.endswith("%"):
            tstock.price = i

        elif i.startswith('+') and i.endswith("%"):
            tstock.percent = i

            if float(i[1:(len(i) - 1)]) >= 10:
                tstock.TenOver = 1

                if tstock.getName() not in wnameList:
                    wnameList.append(tstock.getName())
            else:

                tstock.TenOver = 0


            if tstock.getName() in wnameList:
                changeMade = False

                for key in watchlist:

                    if watchlist[key].getName() == tstock.getName():
                        changeMade = True

                        watchlist[key].price = tstock.getPrice()
                        watchlist[key].percent = tstock.getPercent()
                        watchlist[key].delta = tstock.getDelta()

                        if watchlist[key].TenOver != tstock.getTenOver():
                            watchlist[key].Xten += 1

                        watchlist[key].TenOver = tstock.getTenOver()

                if not changeMade and watchlen < 15:

                    watchlist["wstock" + str(watchlen)].name = tstock.getName()
                    watchlist["wstock" + str(watchlen)].price = tstock.getPrice()
                    watchlist["wstock" + str(watchlen)].percent = tstock.getPercent()
                    watchlist["wstock" + str(watchlen)].delta = tstock.getDelta()
                    watchlist["wstock" + str(watchlen)].TenOver = tstock.getTenOver()
                    watchlen += 1


    temp2 = 0
    temp = 0
    check += 1
    nameList = []
    dataList = []
    time.sleep(1)









print(wnameList)
for a in watchlist:
        print(watchlist[a].getPrice())

#"CREATE TABLE IF NOT EXISTS stocks (Symbol TEXT, Price TEXT, Delta TEXT, Percent TEXT , IsOverTen INTEGER, Xten INTEGER)")

####### connection.close()




#this is the final part that should not be in the loop, it saves all the data. during handling this part might have to run, if thats the case then this would have to be an if, elif statement with an UPDATE counterpart

connection = sqlite3.connect(str(today) + ".db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS stocks (Symbol TEXT, Price TEXT, Delta TEXT, Percent TEXT, IsOverTen INTEGER, Xten INTEGER)")

while s < watchlen:
    s = s + 1
    cursor.execute("INSERT INTO stocks VALUES (?, ?, ?, ?, ?,?)", (watchlist["wstock" + str(s)].getXten(), watchlist["wstock" + str(s)].getPrice(), watchlist["wstock" + str(s)].getDelta(), watchlist["wstock" + str(s)].getPercent(), watchlist["wstock" + str(s)].getTenOver(), watchlist["wstock" + str(s)].getXten()))


connection.commit()
connection.close()




