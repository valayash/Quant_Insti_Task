
from zipline.api import(    symbol,
                            order_target_percent,
                            schedule_function,
                            date_rules,
                            time_rules,
                            get_datetime
                         )

def initialize(context):

    context.stock = [ symbol('AAPL'), symbol('GOOG')]
    
    context.length_small_sma = 20
    context.length_long_sma = 50

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
        last_20_prices = stock_data["close"][stock].iloc[-context.length_small_sma:]
        sma_20 = last_20_prices.mean()
        last_50_prices = stock_data["close"][stock].iloc[-context.length_long_sma:]
        sma_50 = last_50_prices.mean()

        if((sma_20 > sma_50) & (context.portfolio.positions[stock].amount == 0)):
            print("{} Going long on {}".format(get_datetime(), stock))
            order_target_percent(stock, 0.5)
        elif((sma_20 < sma_50) & (context.portfolio.positions[stock].amount != 0)):
            print("{} Exiting {}".format(get_datetime(), stock))
            order_target_percent(stock, 0)
