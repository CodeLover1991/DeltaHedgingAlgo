import pandas as pd
from GetVN30F1M import get_vn30f1m_data
from ReadVN30Data import vn30_f1m_data
import statistics as stat
import numpy as np

def update_vn30f1m_data(input_day, input_month, input_year):
    res = {}
    ticker = "VN30F1M"
    input_date = str(input_year)+'-'+str(input_month)+'-'+str(input_day)
    res['asset'] = ticker
    if get_vn30f1m_data(input_date, ticker).empty:
        return "Non-trading day is selected! Please check the date"
    else:
        res['price_opened'] = [get_vn30f1m_data(input_date, ticker)["price_opened"][0]]
        res['price_closed'] = [get_vn30f1m_data(input_date, ticker)["price_closed"][0]]
        res['transdate'] = [str(input_day)+'/'+str(input_month)+'/'+str(input_year)]
        res['Daily Rt %'] = [(res['price_closed'][0] / vn30_f1m_data.loc[0, 'price_closed'] - 1)*100]
        res['Daily STD %'] = [stat.stdev(vn30_f1m_data.loc[:23,'Daily Rt %'].to_list() + [res['Daily Rt %'][0]])]
        res['Annual STD %'] = [res['Daily STD %'][0] * np.sqrt(252)]
        df = pd.concat([pd.DataFrame(res).round(2), vn30_f1m_data], axis=0, ignore_index=True)
        #print(pd.DataFrame(res).round(2))
        df.to_csv('VN30F1M.csv', index = False)

#update_vn30f1m_data(30, 10, 2024)

