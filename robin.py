import io
import conf
import robin_stocks as r
import matplotlib.pyplot as plt
from flask import Flask, render_template

login = r.login(conf.username,conf.password)

#my_stocks = r.build_holdings()
#for key,value in my_stocks.items():
    #print(key,value)

#my_watchlist = r.get_all_watchlists()
#for key, value in my_watchlist.items():
    #print(key, value)
    

    

def getWatchListTickers(name):
    my_watchlist_by_name = r.get_watchlist_by_name(name)
    sym = []
    for key, value in my_watchlist_by_name.items():
        if(key == "results"):
            for name in value:
                for getId, getName in name.items():
                    if(getId == "symbol"):
                        sym.append(getName)
    return sym
    
    
def makeCordinates(tickerVal):
    get_data = r.get_stock_historicals(tickerVal, "day", "3month")
    x = []
    y = []
    data = "[{"
    name = ''
    date = 0
    for group in get_data:
        for key, value in group.items():
            if(key == "begins_at"):
                date += 1
                x.append(date)
                data += '"x": "' + str(date) + '",'
            if(key == "close_price"):
                y.append(float(value))
                data += '"y": "' + str(value) + '"}, {'
            if(key == "symbol"):
                name = value;
    data+= '}]'
    return name,x,y, data


def plotPoints(x, y, name):
    plt.plot(x, y) 
    plt.xlabel('Date') 
    plt.ylabel('Price') 
    plt.title(name) 
    plt.savefig('images/' + name + '.png')
    plt.clf()
    
def makeData(tickerList):
    allCharts = []
    for val in tickerList:
        cordinates = makeCordinates(val)
        allCharts.append(cordinates)
        #plotPoints(cordinates[0],cordinates[1], cordinates[2])
    return allCharts


#makeData(getWatchListTickers("Shoud I?"))




#makeData(getWatchListTickers("Shoud I?"))


app = Flask(__name__)

@app.route('/')
def index():
    ticker = getWatchListTickers("Shoud I?")
    charts = makeData(ticker)
    return render_template("my-robinhood.html", ticker = ticker, charts = charts)



