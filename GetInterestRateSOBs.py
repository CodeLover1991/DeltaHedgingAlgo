from TrinoQuery import read_trino_query
from Config_Prod import user, password, host, port
import warnings
warnings.filterwarnings("ignore")

def get_sob_interest_rate(input_date, input_term, input_group):
    query = f"""SELECT interest_rate FROM iceberg.mart_macroeconomics.fact_money_market_term_deposit_rates_per_bank_group 
            where bank_group = '{input_group}' and term = '{input_term}' and report_date = date('{input_date}')"""
    return read_trino_query(user, password, host, port, query)

group = 'Nhóm NHTM nhà nước SOBs'
date = '2024-9-19'
term = '12m'
print(get_sob_interest_rate(date, term, group)["interest_rate"].values[0])