# Stock-Screener (work in progress) 

demo video: https://youtu.be/HH-t3XpCbWs

<iframe width="560" height="315" src="https://www.youtube.com/embed/HH-t3XpCbWs" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

This is a web scraper that takes data from yahoo finance's top movers page and displays it in a gui.
Data displayed includes the stock symbol, current price, change in percentage,change in price, and the number of times a stock has crossed the +10% threshold.
This was made to track the volatility of stocks with the highest daily percentage gain, but I would like to make it more abstract.
The current getStocks library is recycled code from stocksfunction.py, which is also included. The original idea was to have a webscraper that keeps track of all the stocks that are at one point in the top 25 of stock gainers each day, and at the end of the day, save this data to a database file. This is why there is a save data function in the getStocks library which is currently unused. 

The main file to run is stocksUI.py, which imports getStocks.py and reads data from UserAgents.txt. 
Running stocksUI.py will display a stock table showing data from yahoo finance top movers, as well as a line editor where you can enter a symbol of a stock
to be added to the table of stocks being tracked.

For future iterations of this project, I will most likely just use a stock data API to get the data, rather than webscraping.
However webscraping from yahoo's top movers page allows me to get data for all of the 25 top moving stocks in one request, which 
for my initial intentions was very convienient. Another thing that is limiting this project is that you can only use the scroll bar and enter text
when the program is not pulling data. I do not know very much about threading so this was an oversight when the code was written.
