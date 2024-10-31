from datetime import datetime, timedelta
import numpy as np
from scipy.stats import norm

def get_option_delta(strike, spot, maturity_date, current_date, rf, vol, type):
    #maturity_date = datetime.strptime(maturity_date,'%Y-%m-%d')
    current_date = datetime.strptime(current_date, '%Y-%m-%d')
    if current_date<=maturity_date:
        time_to_expiry = (maturity_date-current_date)/timedelta(days=1)/365
        d1 = (np.log(spot/strike)+(rf+0.5*vol**2)*time_to_expiry)/(vol*np.sqrt(time_to_expiry))
        if type=='C':
            return norm.cdf(d1)
        elif type=='P':
            return norm.cdf(d1)-1
        else:
            raise ValueError("Invalid option type! Check infor at deal book")
    else:
        raise ValueError("Invalid current date! Current date must be before expiry date")