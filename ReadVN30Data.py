import matplotlib.pyplot as plt
import pandas as pd
import PandasConfig

file_name = 'VN30F1M.csv'
vn30_f1m_data = pd.read_csv(file_name)
reversed_data = vn30_f1m_data[::-1].reset_index(drop=True)
reversed_data.plot(x='transdate', y='price_closed', kind='line')
#print(vn30_f1m_data)
#plt.show()