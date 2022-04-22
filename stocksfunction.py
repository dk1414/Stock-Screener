from bs4 import BeautifulSoup
from datetime import date
import datetime
import requests
import sqlite3
import time
import urllib3

urllib3.disable_warnings()






def TrackStockData(): #main loop used to update data over a period of time, returns stockpile





    def ifTime():  # checks if trading is open
        day_of_week = datetime.date.today().weekday()  # 0 is Monday, 6 is Sunday
        time = datetime.datetime.now().time()
        if day_of_week < 5 and (time > datetime.time(7, 30) and time < datetime.time(16)):
            return True

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

    def saveData(stocklist):

        connection = sqlite3.connect(str(date.today()) + ".db")
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS stocks (Symbol TEXT, Price TEXT, Delta TEXT, Percent TEXT, IsOverTen INTEGER, Xten INTEGER)")


        for a in stocklist:
            cursor.execute("INSERT INTO stocks VALUES (?, ?, ?, ?, ?, ?)", (a.getName(), a.getPrice(), a.getDelta(), a.getPercent(), a.getTenOver(), a.getXten()))

            connection.commit()

        connection.close()





    def getWebData(URL, *dataclass):
        listofdata = []
        header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"}
        r = requests.get(URL,headers = header) #fixes ssl error, but not a permanent solution
        soup = BeautifulSoup(r.content, 'html.parser')

        for c in dataclass:
            for link in soup.find_all(class_=c):  # this is making a list of the data with the given class in string form
                listofdata.append(link.get_text())

        return listofdata

    nameList = set() #this will be a set of non repeated stock names that have been in the top 25 movers section
    stockpile = [] #list containing all stock objects
    stockpileNames = [] #list containing names of stock pile in order

    while not ifTime():
        print("Waiting 5 min")
        time.sleep(500)


    #temp = 1
    while ifTime():
    #while temp < 3:
        #temp = temp + 1


        currentMoversNameList = getWebData("https://finance.yahoo.com/gainers", "Fw(600) C($linkColor)")
        currentMoversDataList = getWebData("https://finance.yahoo.com/gainers", "Va(m) Ta(end) Pstart(20px) Fw(600) Fz(s)")
        print(currentMoversNameList)
        print(currentMoversDataList)





        #adds the name of any top mover stocks into nameList if they are not already in nameList
        for name in currentMoversNameList:
            nameList.add(name)


        #this loop updates stocks that are in namelist and on the yahoo movers page still

        for name in (nameList & set(currentMoversNameList)):

            j = currentMoversNameList.index(name) #index of stock in current with the given name
            percentage = float(currentMoversDataList[(j * 3) + 2][1:(len(currentMoversDataList[(j * 3) + 2]) - 1)].replace(",",'',1)) #getting rid of parenthesis and commas

            if not any(x.getName() == name for x in stockpile): #if there is not already a stock object for this particular stock, make one and add it to stockpile
                stockpile.append(stock(name, currentMoversDataList[j * 3], currentMoversDataList[(j * 3) + 1], percentage, True if percentage > 10 else False, 0))
                stockpileNames.append(name)
            else:
                i = stockpileNames.index(name)  # index of stock in stockpile with the given name

                stockpile[i].price = currentMoversDataList[j * 3]   #in currentDataList, data is formatted so that every three elements correspond with 1 name in current namelist, so the j*3 is the index for price, j*3 + 1for delta, and j*3 + 2  for percent
                stockpile[i].delta = currentMoversDataList[(j * 3) + 1]
                stockpile[i].percent = percentage

                if stockpile[i].percent > 10 and stockpile[i].TenOver == False:
                    stockpile[i].TenOver = True
                    stockpile[i].Xten = stockpile[i].Xten + 1
                elif not stockpile[i].TenOver:
                    stockpile[i].Tenover = False






        #this loop updates the stocks in namelist that are no longer on the yahoo movers page
        diff = (nameList ^ set(currentMoversNameList))


        if len(diff) > 0:
            for name in diff:
                i = stockpileNames.index(name)
                print(f'Pulling data for {name}')
                data = getWebData(f"https://finance.yahoo.com/quote/{name}", "Fw(b) Fz(36px) Mb(-4px) D(ib)",
                                  "Fw(500) Pstart(8px) Fz(24px)",
                                  "Fw(500) Pstart(8px) Fz(24px)")  # this makes a list of data for a particular stock, ex: ['83.00', '+0.31', '(+0.37%)', '+0.31', '(+0.37%)'], there are repitions hence the formatting going on in the next line
                
                print(data)
                #nameList and stockpile should always be in the same order and be the same length, therefore no sorting is needed to update the data for each stock in stockpile, as the current data variable will always match
                stockpile[i].price = data[0]
                stockpile[i].delta = data[1]
                stockpile[i].percent = float(data[2][2:(len(data[2]) - 2)].replace(",",'',1))

                if stockpile[i].percent > 10 and stockpile[i].TenOver == False:
                    stockpile[i].TenOver = True
                    stockpile[i].Xten = stockpile[i].Xten + 1
                elif not stockpile[i].TenOver:
                    stockpile[i].Tenover = False



        #this bit only works assuming stockpile only has stocks in the current top 25, will probably just have to sort by percentage in the end,but its good notes
        #sortedStockpile = []

        #for s in currentMoversNameList:
            #t = list(filter(lambda i: i != None,(list(map(lambda x: x if x.getName() == s else None, stockpile)))))
            #sortedStockpile.append(t[0])



        for thing in stockpile:
            print(f'{thing.getName()}: {thing.getPrice()}, {thing.getDelta()}, {thing.getPercent()}')

        print(currentMoversNameList)
        print(nameList)
        print(list(map(lambda x: x.getName(),sorted(stockpile, key=lambda s: s.getPercent(), reverse=True))))
        time.sleep(3)



    sortedStockpile = sorted(stockpile, key= lambda s: s.getPercent(), reverse=True)
    saveData(sortedStockpile)


TrackStockData()











