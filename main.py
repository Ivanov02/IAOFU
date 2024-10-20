from get_match_details import *
import pandas as pd

# 100 = albastru/ 200 = rosu

dict_source = get_match_details()
dict_source_df = pd.DataFrame.from_dict(dict_source)
print(dict_source_df)

dict_source_df.to_csv("output.csv", sep=",", header=True, index=False, mode="a")
