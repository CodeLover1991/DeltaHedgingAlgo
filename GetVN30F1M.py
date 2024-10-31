from TrinoQuery import read_trino_query
from Config_Prod import user, password, host, port
import warnings
warnings.filterwarnings("ignore")

def get_vn30f1m_data(input_date, input_ticker):
    query = f"""SELECT * FROM iceberg.dwh_atomic.dwh_market_prices_and_transactions_securities_daily_prices 
            WHERE  transdate = date('{input_date}') and ticker ='{input_ticker}'"""
    df = read_trino_query(user, password, host, port, query)
    if df.empty:
        print("Non-Trading day is selected! No prices available")
    return df

#print(get_vn30f1m_data('2024-10-07', 'VN30F1M'))