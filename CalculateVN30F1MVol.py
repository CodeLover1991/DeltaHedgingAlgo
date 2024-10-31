from Config_Prod import user, password, host, port
from TrinoQuery import read_trino_query
import warnings
warnings.filterwarnings("ignore")

def get_vn30f1m_historical_vol(input_date, rolling_frame, input_ticker):
    query = f"""with ret as (select transdate, ticker, price_closed, price_closed / lead(price_closed) over(order by transdate desc) - 1 rt
            from iceberg.dwh_atomic.dwh_market_prices_and_transactions_securities_daily_prices
            where ticker = '{input_ticker}' ), 
            avg_ret as (select transdate, ticker,  
            stddev_samp(rt) over(partition by ticker order by transdate desc rows between current row and {rolling_frame-1} following) 
            std_daily from ret where ticker = '{input_ticker}')
            select * from avg_ret 
            where transdate = date('{input_date}')"""
    return read_trino_query(user, password, host, port, query)

#date = '2024-10-22'
#frame_size = 25
#ticker = "VN30F1M"
#print(get_vn30f1m_historical_vol(date, frame_size, ticker)["std_daily"].values[0])