
from zipline.api import(    symbol,
                            order_target_percent,
                            schedule_function,
                            date_rules,
                            time_rules,
                            get_datetime
                         )
import talib as ta
import numpy as np

def initialize(context):

    context.stock = [ symbol('ASIANPAINT')]
    
    context.length_small_sma = 20
    # context.length_long_sma = 50

    for i in range (1,390,15):
        schedule_function(
                    run_strategy,
                    date_rules.every_day(),
                    time_rules.market_open(minutes=i))
    
    
def run_strategy(context,data):
    
    stock_data = data.history(context.stock, ['close'], 900,"1m" )
    for stock in context.stock:
        stock_data["close"][stock] = (stock_data["close"][stock]).resample("15T", label="right", closed="right").last()

    stock_data["close"].dropna(inplace=True)

    for stock in context.stock:
        stock_data["last_20_prices"] = stock_data["close"][stock].iloc[-context.length_small_sma:]
        # sma_20 = last_20_prices.mean()
        # last_50_prices = stock_data["close"][stock].iloc[-context.length_long_sma:]
        # sma_50 = last_50_prices.mean()
        stock_data["Handle_Start"] = np.where((stock_data["close"] < stock_data["last_20_prices"]) & (stock_data["close"].shift(-1) > stock_data["last_20_prices"].shift(-1)), stock_data["close"], np.NaN)
        stock_data["Cup_Bottom"] = stock_data["Handle_Start"].min()
        stock_data["Handle_End"] = stock_data["Handle_Start"].max()
        stock_data["Cup_Height"] = stock_data["Cup_Bottom"] - stock_data["Handle_End"]
        stock_data["Handle_Height"] = stock_data["Handle_End"] - stock_data["Handle_Start"]
        stock_data["Handle_Width"] = (stock_data["Handle_Start"] - stock_data["Handle_End"]).idxmax() - (stock_data["Handle_Start"] - stock_data["Handle_End"]).idxmin()
        stock_data["Buy_Signal"] = np.where((stock_data["Handle_Height"] / stock_data["Cup_Height"] < 0.15) & (stock_data["Handle_Width"] < 20), stock_data["Handle_End"], np.NaN)

        if(np.where(stock_data["Buy_Signal"].notna(), "Buy", np.NaN) == "Buy"):
            print("{} Going long on {}".format(get_datetime(), stock))
            order_target_percent(stock, 0.5)
        # if(stock_data["Signal"] = np.where((stock_data["close"] > stock_data["Buy_Signal"]) & (stock_data["Signal"] == "Buy"), "Sell", stock_data["Signal"]) == "Sell"):
        #     print("{} Exiting {}".format(get_datetime(), stock))
        #     order_target_percent(stock, 0)
        
