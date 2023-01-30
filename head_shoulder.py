
from zipline.api import(    symbol,
                            order_target_percent,
                            schedule_function,
                            date_rules,
                            time_rules,
                            get_datetime
                         )
#Technical Analysis library of Python
import talib as ta  

def initialize(context):

    #Stock which we want to buy ans sell acoording to Hand ans Shoulder Pattern
    context.stock = [ symbol('ASIANPAINT')]     

    #It will run at the 15min intervals after the markets open ie 9:15 to 3:15
    for i in range (1,390,15):
        schedule_function(
                    run_strategy,
                    date_rules.every_day(),
                    time_rules.market_open(minutes=i))
    
    
def run_strategy(context,data):
    
    #Collecting past history of the Stocks
    stock_data = data.history(context.stock, ["close"], 900,"1m" )
    for stock in context.stock:
        stock_data["close"][stock] = (stock_data["close"][stock]).resample("15T", label="right", closed="right").last()

    stock_data["close"].dropna(inplace=True)

    #Finding Head nd Shoulder
    for stock in context.stock:
        head_and_shoulders = ta.CDLHEADANDSHOULDERS(stock)
        
        # Generate signals when the pattern is observed
        if head_and_shoulders[-1] == 100:
            order_target_percent(stock, 0) # Sell
        elif head_and_shoulders[-1] == -100:
            order_target_percent(stock, 1.0/10) # Buy

        
