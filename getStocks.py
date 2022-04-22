from bs4 import BeautifulSoup
from datetime import date
import datetime
import requests
import sqlite3
import random
import urllib3

urllib3.disable_warnings()




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

    def getAll(self):
        return [self.name,self.price,str(self.percent) + "%",self.delta,self.Xten]



def saveData(stocklist):

    connection = sqlite3.connect(str(date.today()) + ".db")
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS stocks (Symbol TEXT, Price TEXT, Delta TEXT, Percent TEXT, IsOverTen INTEGER, Xten INTEGER)")

    for a in stocklist:
        cursor.execute("INSERT INTO stocks VALUES (?, ?, ?, ?, ?, ?)",
                       (a.getName(), a.getPrice(), a.getDelta(), a.getPercent(), a.getTenOver(), a.getXten()))

        connection.commit()

    connection.close()

def getWebData(URL, *dataclass):
    listofdata = []

    file = open('UserAgents.txt')
    UserAgent = file.readlines()[random.randrange(0, 98, 1)]
    file.close()

    header = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7",
        "cache-control": "max-age=0",
        "dnt": "1",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": UserAgent[0].rstrip()}

    r = requests.get(URL,headers = header, verify=False)  # fixes ssl error, but not a permanent solution
    soup = BeautifulSoup(r.content, 'html.parser')

    for c in dataclass:
        for link in soup.find_all(
                class_=c):  # this is making a list of the data with the given class in string form
            listofdata.append(link.get_text())

    return listofdata


def getStockData(setofnames,stocks,listofnames):


    nameList = setofnames   #this will be a set of non repeated stock names that have been in the top 25 movers section
    stockpile = stocks   #list containing all stock objects
    stockpileNames = listofnames   #list containing names of stock pile in order


    currentMoversNameList = getWebData("https://finance.yahoo.com/gainers", "Fw(600) C($linkColor)")
    currentMoversDataList = getWebData("https://finance.yahoo.com/gainers",
                                       "Va(m) Ta(end) Pstart(20px) Fw(600) Fz(s)")

    # adds the name of any top mover stocks into nameList if they are not already in nameList
    for name in currentMoversNameList:
        nameList.add(name)

    # this loop updates stocks that are in namelist and on the yahoo movers page still

    for name in (nameList & set(currentMoversNameList)):

        j = currentMoversNameList.index(name)  # index of stock in current with the given name
        percentage = float(currentMoversDataList[(j * 3) + 2][1:(len(currentMoversDataList[(j * 3) + 2]) - 1)].replace(",", '',1))  # getting rid of parenthesis and commas

        if not any(x.getName() == name for x in stockpile):  # if there is not already a stock object for this particular stock, make one and add it to stockpile
            stockpile.append(stock(name, currentMoversDataList[j * 3], currentMoversDataList[(j * 3) + 1], percentage,True if percentage > 10 else False, 0))
            stockpileNames.append(name)

        else:
            i = stockpileNames.index(name)  # index of stock in stockpile with the given name

            stockpile[i].price = currentMoversDataList[j * 3]  # in currentDataList, data is formatted so that every three elements correspond with 1 name in current namelist, so the j*3 is the index for price, j*3 + 1for delta, and j*3 + 2  for percent
            stockpile[i].delta = currentMoversDataList[(j * 3) + 1]
            stockpile[i].percent = percentage

            #Xten only needs to change if the stock is being updated not created which is why this part is only here
            if stockpile[i].percent > 10 and stockpile[i].TenOver == False:
                stockpile[i].TenOver = True
                stockpile[i].Xten = stockpile[i].Xten + 1
            elif not stockpile[i].TenOver:
                stockpile[i].Tenover = False

    # this loop updates the stocks in namelist that are no longer on the yahoo movers page
    diff = (nameList ^ set(currentMoversNameList))

    if len(diff) > 0:
        for name in diff:
            i = stockpileNames.index(name)
            print(f'Pulling data for {name}')
            data = getWebData(f"https://finance.yahoo.com/quote/{name}", "Fw(b) Fz(36px) Mb(-4px) D(ib)",
                              "Fw(500) Pstart(8px) Fz(24px)",
                              "Fw(500) Pstart(8px) Fz(24px)")  # this makes a list of data for a particular stock, ex: ['83.00', '+0.31', '(+0.37%)', '+0.31', '(+0.37%)'], there are repitions hence the formatting going on in the next line

            print(data)
            # nameList and stockpile should always be in the same order and be the same length, therefore no sorting is needed to update the data for each stock in stockpile, as the current data variable will always match
            stockpile[i].price = data[0]
            stockpile[i].delta = data[1]
            stockpile[i].percent = float(data[2][2:(len(data[2]) - 2)].replace(",", '', 1))

            if stockpile[i].percent > 10 and stockpile[i].TenOver == False:
                stockpile[i].TenOver = True
                stockpile[i].Xten = stockpile[i].Xten + 1
            elif not stockpile[i].TenOver:
                stockpile[i].Tenover = False



    return [nameList,stockpile,stockpileNames]



