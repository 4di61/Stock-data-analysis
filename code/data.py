import pandas as pd
all_stock_df = pd.read_csv("D:/Documents/College docs/Sem III/Mini project/data/NIFTY50_all_modified.csv")
all_stock_df["Date"] = pd.to_datetime(all_stock_df["Date"])
industries = {}
for industry_name in list(all_stock_df.Industry.unique()):
    industries[industry_name] = list(
        all_stock_df.loc[all_stock_df.Industry == industry_name, "Symbol"].unique())
