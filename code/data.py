import pandas as pd
all_stock_df = pd.read_csv("D:/Documents/College docs/Sem III/Mini project/data/NIFTY50_all_modified.csv")
all_stock_df["Date"] = pd.to_datetime(all_stock_df["Date"])