import pandas as pd
from datetime import datetime
import PandasConfig
from CalculateDelta import get_option_delta
from GetVN30F1M import get_vn30f1m_data

prev_day, prev_month, prev_year = 29, 10, 2024 # access deal book from previous day
file_name = "DealBook"+"_"+str(prev_year)+"_"+str(prev_month)+"_"+str(prev_day)+".csv"
deal_book = pd.read_csv(file_name, parse_dates = ['Open Date', 'Expiry Date'], thousands = ',', dtype = {'Strike':float})

curr_day, curr_month, curr_year = 30, 10, 2024
curr_date_str = str(curr_year)+"-"+str(curr_month)+"-"+str(curr_day)
call_list, put_list = [], []
spot = get_vn30f1m_data(curr_date_str, "VN30F1M")["price_closed"][0]
option_list = []

for idx, row in deal_book.iterrows():
    option_type = deal_book.iloc[idx]["Type"]
    open_date = deal_book.iloc[idx]["Open Date"]
    maturity_date = deal_book.iloc[idx]["Expiry Date"]
    strike = deal_book.iloc[idx]["Strike"]
    no_contracts = deal_book.iloc[idx]["No. Contracts"]
    iv = deal_book.iloc[idx]["Implied Vol"]
    rf = deal_book.iloc[idx]["Risk Free Rate"]
    new_delta = get_option_delta(strike, spot, maturity_date, curr_date_str, rf, iv, option_type)
    updated_option = {
        "Type": option_type,
        "Open Date": open_date,
        "Expiry Date": maturity_date,
        "Strike": strike,
        "No. Contracts": no_contracts,
        "Implied Vol": iv,
        "Risk Free Rate": rf,
        "Delta": round(-new_delta*no_contracts)
    }
    option_list.append(updated_option)
#print(pd.DataFrame(option_list))
updated_file_name = "DealBook"+"_"+str(curr_year)+"_"+str(curr_month)+"_"+str(curr_day)+".csv"
pd.DataFrame(option_list).to_csv(updated_file_name, index=False)
#deal_book = pd.read_csv(file_name, parse_dates = ['Open Date', 'Expiry Date'], thousands = ',', dtype = {'Strike':float})
#deal_data.to_csv('test.csv', date_format='%Y/%m/%d', index=False)

